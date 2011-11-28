# -*- coding:utf-8 -*-
# Copyright © 2011 Clément Schaff, Mahdi Ben Jelloul

"""
openFisca, Logiciel libre de simulation du système socio-fiscal français
Copyright © 2011 Clément Schaff, Mahdi Ben Jelloul

This file is part of openFisca.

    openFisca is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    openFisca is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with openFisca.  If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import division
from numpy import ( maximum as max_, minimum as min_, logical_xor as xor_, 
                    logical_not as not_, round)
from Utils import BarmMar

from france.data import QUIFOY, year

VOUS = QUIFOY['vous']
CONJ = QUIFOY['conj']
PAC1 = QUIFOY['pac1']
PAC2 = QUIFOY['pac2']
PAC3 = QUIFOY['pac3']
ALL = []
for qui in QUIFOY:
    ALL.append(qui[1])
        

# zglof = Glo(table)
# zetrf = zeros(taille)
# jveuf = zeros(taille, dtype = bool)
# jourXYZ = 360*ones(taille)
# Reprise du crédit d'impôt en faveur des jeunes, des accomptes et des versements mensues de prime pour l'emploi
# reprise = zeros(taille) # TODO : reprise=J80;
# Pcredit = P.credits_impots
# if hasattr(P.reductions_impots,'saldom'): Pcredit.saldom =  P.reductions_impots.saldom
# credits_impot = Credits(Pcredit, table)
# Réduction d'impôt
# reductions = Reductions(IPnet, P.reductions_impots)

#def mcirra():
#    # impôt sur le revenu
#    mcirra = -((IMP<=-8)*IMP)
#    mciria = max_(0,(IMP>=0)*IMP)
##        mciria = max_(0,(IMP>=0)*IMP - credimp_etranger - cont_rev_loc - ( f8to + f8tb + f8tc ))
#    
#    # Dans l'ERFS, les prelevement libératoire sur les montants non déclarés
#    # sont intégrés. Pas possible de le recalculer.
#    
#    # impot sur le revenu du foyer (hors prélèvement libératoire, revenus au quotient)
#    irpp   = -(mciria + ppetot - mcirra )
    

###############################################################################
## Initialisation de quelques variables utiles pour la suite
###############################################################################

def _nb_adult(marpac, celdiv, veuf):
    return 2*marpac + 1*(celdiv | veuf)

def _nb_pac(nbF, nbJ, nbR):
    return nbF + nbJ + nbR
        
def _marpac(statmarit):
    '''
    Marié ou Pacsé
    'foy'
    '''
    return (statmarit == 1) | (statmarit == 5)

def _celdiv(statmarit):
    '''
    Célibataire ou divorcé
    'foy'
    '''
    return (statmarit == 2) | (statmarit == 3)

def _veuf(statmarit):
    '''
    Veuf
    'foy'
    '''
    return statmarit == 4

def _jveuf(statmarit):
    '''
    Jeune Veuf
    'foy'
    '''
    return statmarit == 6

###############################################################################
## Revenus catégoriels
###############################################################################

def _alloc(af, _P):
    '''
    ALLOCATION FAMILLIALE IMPOSABLE
    '''
    P = _P.ir.autre
    return af*P.alloc_imp

def _rev_sal(sal):
    '''
    Revenu imposé comme des salaires (salaires, mais aussi 3vj, 3vk)
    '''
    return sal

def _sal_net(rev_sal, choCheckBox, fra, _P):
    '''
    Salaires après abattements
    '''
    P = _P.ir.tspr.abatpro
    amin = P.min*not_(choCheckBox) + P.min2*choCheckBox
    abatfor = round(min_(max_(P.taux*rev_sal, amin),P.max))
    return (fra > abatfor)*(rev_sal - fra) \
         + (fra <= abatfor)*max_(0,rev_sal - abatfor)

def _rev_pen(alr, rst):
    '''
    Revenu imposé comme des pensions (retraites, pensions alimentaires, etc.)
    '''
    return alr + rst

def _pen_net(rev_pen, _P):
    '''
    Pensions après abattements
    '''
    P = _P.ir.tspr.abatpen
#    #problème car les pensions sont majorées au niveau du foyer
#    d11 = ( AS + BS + CS + DS + ES + 
#            AO + BO + CO + DO + EO ) 
#    penv2 = (d11-f11> P.abatpen.max)*(penv + (d11-f11-P.abatpen.max)) + (d11-f11<= P.abatpen.max)*penv   
#    # Plus d'abatement de 20% en 2006

    return max_(0, rev_pen - round(max_(P.taux*rev_pen , P.min)))

def _rto_net(f1aw, f1bw, f1cw, f1dw, _P):
    '''
    Rentes viagères après abatements
    '''
    P = _P.ir.tspr.abatviag
    return round(P.taux1*f1aw + 
                 P.taux2*f1bw + 
                 P.taux3*f1cw + 
                 P.taux4*f1dw )

def _tspr(sal_net, pen_net):
    '''
    Traitemens salaires pensions et rentes individuelles
    '''
    return sal_net + pen_net

def _rev_cat_tspr(tspr, rto_net, _option = {'tspr': ALL}):
    '''
    TRAITEMENTS SALAIRES PENSIONS ET RENTES
    '''
    out = 0
    for qui in tspr.itervalues():
        out += qui

    out += rto_net
    
    return out

def _rev_cat_rvcm(marpac, deficit_rcm, f2ch, f2dc, f2ts, f2ca, f2fu, f2go, f2tr, _P):
    '''
    REVENUS DES VALEURS ET CAPITAUX MOBILIERS
    '''
    P = _P.ir.rvcm
    if year > 2004: f2gr = 0

    ## Calcul du revenu catégoriel
    #1.2 Revenus des valeurs et capitaux mobiliers
    b12 = min_(f2ch, P.abat_assvie*(1 + marpac))
    TOT1 = f2ch-b12
    # Part des frais s'imputant sur les revenus déclarés case DC
    den = ((f2dc + f2ts)!=0)*(f2dc + f2ts) + ((f2dc + f2ts)==0)
    F1 =  f2ca/den*f2dc
    
    # Revenus de capitaux mobiliers nets de frais, ouvrant droit à abattement
    # partie négative (à déduire des autres revenus nets de frais d'abattements
    g12a = - min_(f2dc*P.abatmob_taux - F1,0)
    # partie positive
    g12b = max_(f2dc*P.abatmob_taux - F1,0)
    
    rev = g12b + f2gr + f2fu*P.abatmob_taux

    # Abattements, limité au revenu
    h12 = P.abatmob*(1 + marpac)
    TOT2 = max_(0,rev - h12)
    i121= -min_(0,rev - h12)
    
    # Pars des frais s'imputant sur les revenus déclarés ligne TS
    F2 = f2ca - F1
    TOT3 = (f2ts - F2) + f2go*P.majGO + f2tr - g12a

    DEF = deficit_rcm

    ## TODO: pour le calcul du revenu fiscal de référence
    rfr_rvcm = max_((1-P.abatmob_taux)*(f2dc + f2fu) - i121, 0)

    return max_(TOT1 + TOT2 + TOT3 - DEF, 0)

def _rev_cat_rfon(f4ba, f4bb, f4bc, f4bd, f4be, _P):
    '''
    REVENUS FONCIERS
    '''    
    P = _P.ir.microfoncier
    ## Calcul du revenu catégoriel
    a13 = f4ba + f4be - P.taux*f4be*(f4be <= P.max)
    b13 = f4bb
    c13 = a13-b13
    d13 = f4bc
    e13 = c13- d13*(c13>=0)
    f13 = f4bd*(e13>=0)
    g13 = max_(0, e13- f13)
    out  = (c13>=0)*(g13 + e13*(e13<0)) - (c13<0)*d13
    return out

def _rev_cat_rpns(sal):
    return 0*sal

def _rev_cat(rev_cat_tspr, rev_cat_rvcm, rev_cat_rfon, rev_cat_rpns):
    '''
    Revenus Categoriels
    '''
#    AUTRE = TSPR + RVCM + RFON
    return rev_cat_tspr + rev_cat_rvcm + rev_cat_rfon + rev_cat_rpns

###############################################################################
## Déroulé du calcul de l'irpp
###############################################################################

def _rbg(alloc, rev_cat, deficit_ante, f6gh, _P):
    '''
    Revenu brut global (Total 17)
    '''
    # sans les revenus au quotient
    return max_(0, alloc + rev_cat + f6gh - deficit_ante)

def _csg_deduc(rbg, f6de):
    '''
    CSG déductible
    '''
    return min_(f6de, max_(rbg, 0))

def _rng(rbg, csg_deduc, charges_deduc):
    '''
    Revenu net global (total 20)
    '''
    return max_(0, rbg - csg_deduc - charges_deduc)

def _rni(rng, abat_spe):
    return rng - abat_spe

def _ir_brut(nbptr, rni, _P):
    '''
    Impot sur le revenu avant non imposabilité et plafonnement du quotien
    'foy'
    '''
    P = _P.ir.bareme
    return nbptr*BarmMar(rni/nbptr, P) # TODO : partir d'ici, petite différence avec Matlab

def _ir_plaf_qf(ir_brut, rni, nb_adult, nb_pac, nbptr, marpac, veuf, jveuf, celdiv, caseE, caseF, caseG, caseH, caseK, caseN, caseP, caseS, caseT, caseW, nbF, nbG, nbH, nbI, nbR, _P):
    '''
    Impôt après plafonnement du quotient familial et réduction complémentaire
    '''
    P = _P.ir
    I = ir_brut
    A = BarmMar(rni/nb_adult,P.bareme)
    A = nb_adult*A    

    aa0 = (nbptr-nb_adult)*2           #nombre de demi part excédant nbadult
    # on dirait que les impôts font une erreur sur aa1 (je suis obligé de
    # diviser par 2)
    aa1 = min_((nbptr-1)*2,2)/2  # deux première demi part excédants une part
    aa2 = max_((nbptr-2)*2,0)    # nombre de demi part restantes
    # celdiv parents isolés
    condition61 = (celdiv==1) & caseT
    B1 = P.plafond_qf.celib_enf*aa1 + P.plafond_qf.marpac*aa2
    # tous les autres
    B2 = P.plafond_qf.marpac*aa0                 #si autre
    # celdiv, veufs (non jveuf) vivants seuls et autres conditions TODO année codéee en dur
    # TODO: année en dur... pour caseH
    condition63 = ((celdiv==1) | ((veuf==1) & not_(jveuf))) & not_(caseN) & (nb_pac==0) & (caseK | caseE) & (caseH<1981)
    B3 = P.plafond_qf.celib

    B = B1*condition61 + \
        B2*(not_(condition61 | condition63)) + \
        B3*(condition63 & not_(condition61))
    C = max_(0,A-B);
    # Impôt après plafonnement
    IP0 = max_(I, C) #I*(I>=C) + C*(I<C);

    # 6.2 réduction d'impôt pratiquée sur l'impot après plafonnement et le cas particulier des DOM
    # pas de réduction complémentaire
    condition62a = (I>=C);
    # réduction complémentaire
    condition62b = (I<C);
    # celdiv veuf
    condition62caa0 = (celdiv | (veuf & not_(jveuf)))
    condition62caa1 = (nb_pac==0)&(caseP | caseG | caseF | caseW)
    condition62caa2 = caseP & ((nbF-nbG>0)|(nbH - nbI>0))
    condition62caa3 = not_(caseN) & (caseE | caseK )  & (caseH>=1981)
    condition62caa  = condition62caa0 & (condition62caa1 | condition62caa2 | condition62caa3)
    # marié pacs
    condition62cab = (marpac | jveuf) & caseS & not_(caseP | caseF)
    condition62ca =    (condition62caa | condition62cab);

    # plus de 590 euros si on a des plus de
    condition62cb = ((nbG+nbR+nbI)>0) | caseP | caseF
    D = P.plafond_qf.reduc_postplafond*(condition62ca + ~condition62ca*condition62cb*( 1*caseP + 1*caseF + nbG + nbR + nbI/2 ))

    E = max_(0,A-I-B)
    Fo = D*(D<=E) + E*(E<D)
    out = IP0-Fo

    return out
    # TODO :6.3 Cas particulier: Contribuables domiciliés dans les DOM.    
    # conditionGuadMarReu =
    # conditionGuyane=
    # conitionDOM = conditionGuadMarReu | conditionGuyane;
    # postplafGuadMarReu = 5100;
    # postplafGuyane = 6700;
    # IP2 = IP1 - conditionGuadMarReu*min( postplafGuadMarReu,.3*IP1)  - conditionGuyane*min(postplafGuyane,.4*IP1);
#
#
#    # Récapitulatif
#    return condition62a*IP0 + condition62b*IP1 # IP2 si DOM

def _decote(ir_plaf_qf, _P):
    '''
    Décote
    '''
    P = _P.ir.decote
    return (ir_plaf_qf < P.seuil)*(P.seuil - ir_plaf_qf)*0.5

def _nat_imp(rni, nbptr, _P):
    '''
    Renvoie 1 si le foyer est imposable, 0 sinon
    '''
    P = _P.ir.non_imposable
    seuil = P.seuil + (nbptr - 1)*P.supp
    return rni >= seuil

def _ip_net(ir_plaf_qf, nat_imp, decote):
    '''
    irpp après décote et prise en compte de la non imposabilité
    '''
    return nat_imp*max_(0, ir_plaf_qf - decote)

def _iaidrdi(ip_net, reductions):
    '''
    impot après imputation des réductions d'impôt
    '''
    return   ip_net - reductions

def _cont_rev_loc(f4bl):
    '''
    Contribution sur les revenus locatifs
    '''
    loyf_taux = 0.025
    loyf_seuil = 0
    return round(loyf_taux *(f4bl >= loyf_seuil)*f4bl)

def _teicaa(f5qm, f5rm):
    '''
    Taxe exceptionelle sur l'indemnité compensatrice des agents d'assurance
    '''
    #     H90_a1 = 0*max_(0,min_(f5qm,23000));
    H90_a2 = .04*max_(0,min_(f5qm - 23000,107000));
    H90_a3 = .026*max_(0,f5qm - 107000);
    #     H90_b1 = 0*max_(0,min_(f5rm,23000));
    H90_b2 = .04*max_(0,min_(f5qm-23000,107000));
    H90_b3 = .026*max_(0,f5qm - 107000);
    
    return H90_a2 + H90_a3 + H90_b2 + H90_b3;

def _iai(iaidrdi, plus_values, cont_rev_loc, teicaa):
    '''
    impôt avant imputation
    '''
    return iaidrdi + plus_values + cont_rev_loc + teicaa

def _tehr(rfr, nb_adult, P):
    '''
    Taxe exceptionnelle sur les hauts revenus
    'foy'
    '''
    return BarmMar(rfr/nb_adult, P)*nb_adult
    
def _irpp(iai, credits_impot, tehr, ppe):
    '''
    Montant avant seuil de recouvrement (hors ppe)
    '''
    return  iai - credits_impot + ppe + tehr


###############################################################################
## Autres totaux utiles pour la suite
###############################################################################

def _rfr(rni, alloc, f3va, f3vg, f3vi, rfr_cd, rfr_rvcm, rpns_exo, rpns_pvce, rev_cap_lib):
    '''
    Revenu fiscal de reference
    '''
    return max_(0, rni - alloc) + rfr_cd + rfr_rvcm + rev_cap_lib + f3vi + rpns_exo + rpns_pvce + f3va + f3vg
 
def _glo(f1tv, f1tw, f1tx, f1uv, f1uw, f1ux, f3vf, f3vi, f3vj, f3vk):
    '''
    Gains de levée d'option
    'foy'
    '''
    return f1tv + f1tw + f1tx + f1uv + f1uw + f1ux + f3vf + f3vi + f3vj + f3vk                   

def _rto(f1aw, f1bw, f1cw, f1dw):
    '''
    Rentes viagères à titre onéreux
    '''
    return f1aw + f1bw + f1cw + f1dw

def _deficit_rcm(f2aa, f2al, f2am, f2an):
    return f2aa + f2al + f2am + f2an
    
def _rev_cap_bar(f2dc, f2gr, f2ch, f2ts, f2go, f2tr, f2fu, avf):
    '''
    revenus du capital imposés au barème
    '''
    return f2dc + f2gr + f2ch + f2ts + f2go + f2tr + f2fu - avf

def _rev_cap_lib(f2da, f2dh, f2ee):
    '''
    Revenu du capital imposé au prélèvement libératoire
    '''
    if year <=2007: out = f2dh + f2ee
    else: out = f2da + f2dh + f2ee
    return out

def _avf(f2ab):
    # a.(ii) Avoir fiscal et crédits d'impôt (zavff)
    return f2ab
    # a.(iii) Les revenus de valeurs mobilières soumis au prélèvement
    # libératoire (zvalf)

    
def _imp_lib(f2da, f2dh, f2ee, _P):
    '''
    Prelèvement libératoire sur les revenus du capital
    '''
    P = _P.ir.prelevement_liberatoire
    if year <=2007: 
        out = - (P.assvie*f2dh + P.autre*f2ee )
    else:
        out = - (P.action*f2da + P.assvie*f2dh + P.autre*f2ee )
    return out

def _rfon_rmi(f4ba, f4be):
    '''
    Revenus fonciers pour la base ressource du rmi/rsa
    '''
    return f4ba + f4be


def _fon(f4ba, f4bb, f4bc, f4bd, f4be, _P):
    ## Calcul des totaux        
    P = _P.ir.microfoncier
    fon = f4ba - f4bb - f4bc + round(f4be*(1-P.taux))  
    return fon


#def _rpns_full(self, P, table):
#    '''
#    REVENUS DES PROFESSIONS NON SALARIEES
#    partie 5 de la déclaration complémentaire
#    '''
#
#    def abatv(rev, P):
#        return max_(0,rev - min_(rev, max_(P.microentreprise.vente_taux*min_(P.microentreprise.vente_max, rev), P.microentreprise.vente_min)))
#    
#    def abats(rev, P):
#        return max_(0,rev - min_(rev, max_(P.microentreprise.servi_taux*min_(P.microentreprise.servi_max, rev), P.microentreprise.servi_min)))
#    
#    def abatnc(rev, P):
#        return max_(0,rev - min_(rev, max_(P.nc_abat_taux*min_(P.nc_abat_max, rev), P.nc_abat_min)))
#
#
#def _rpns_pvce(self):
#    ''' 
#    Plus values de cession
#    '''
#    fragf = f5hx + f5ix + f5jx
#    aragf = f5he + f5ie + f5je
#    nragf = f5hk + f5ik + f5jk
#    mbicf = f5kq + f5lq + f5mq
#    abicf = f5ke + f5le + f5me
#    nbicf = f5kk + f5lk + f5mk
#    maccf = f5nq + f5oq + f5pq
#    aaccf = f5ne + f5oe + f5pe
#    naccf = f5nk + f5ok + f5pk
#    mncnp = f5kv + f5lv + f5mv
#    cncnp = f5so + f5nt + f5ot
#    mbncf = f5hr + f5ir + f5jr
#    abncf = f5qd + f5rd + f5sd
#    nbncf = f5qj + f5rj + f5sj
#
#    return ( fragf + aragf + nragf + mbicf + abicf + 
#             nbicf + maccf + aaccf + naccf + mbncf + 
#             abncf + nbncf + mncnp + cncnp )
#
#def _rpns_exon(self):
#    ''' 
#    Plus values de cession
#    '''
#    fragf = f5hn + f5in + f5jn
#    aragf = f5hb + f5ib + f5jb
#    nragf = f5hh + f5ih + f5jh
#    mbicf = f5kn + f5ln + f5mn
#    abicf = f5kb + f5lb + f5mb
#    nbicf = f5kh + f5lh + f5mh 
#    maccf = f5nn + f5on + f5pn
#    aaccf = f5nb + f5ob + f5pb
#    naccf = f5nh + f5oh + f5ph
#    mbncf = f5hp + f5ip + f5jp
#    abncf = f5qb + f5rb + f5sb
#    nbncf = f5qh + f5rh + f5sh
#    
#    return (fragf + aragf + nragf + mbicf + abicf + 
#            nbicf + maccf + aaccf + naccf + mbncf + 
#            abncf + nbncf )
#        # TODO: Prendre en compte les déficits?
##            return fragf_exon + aragf_exon + nragf_exon + mbicf_exon + max_(abicf_exon-abicf_defe,0) + max_(nbicf_exon-nbicf_defe,0) + maccf_exon + aaccf_exon + naccf_exon + mbncf_exon + abncf_exon + nbncf_exon 
#
#
#    # plus values de cession
#    rpns_pvce = Pvce(self)
#    # revenus exonérés
#    rpns_exo =  Exon(self)
#
#    ## A revenus agricoles 
#    table.openWriteMode()
#    
#    #regime du forfait
#    frag_impo = f5ho + f5io + f5jo
#    frag_pvct = f5hw + f5iw + f5jw
#    frag_timp = frag_impo + frag_pvct  # majoration de 25% mais les pvct ne sont pas majorées de 25%
#    
#    #Régime du bénéfice réel ou transitoire bénéficiant de l'abattement CGA
#    arag_impg = f5hc + f5ic + f5jc
#    arag_defi = f5hf + f5if + f5jf
#    arag_timp = arag_impg                  # + aragf_impx/5 pas de majoration;
#    
#    #Régime du bénéfice réel ou transitoire ne bénéficiant pas de l'abattement CGA
#    nrag_impg = f5hi + f5ii + f5ji
#    nrag_defi = f5hl + f5il + f5jl
#    nrag_timp = nrag_impg # + nragf_impx/5 ; # majoration de 25% mais les pvct ne sont pas majorées de 25%
#    
#    #Jeunes agriculteurs montant de l'abattement de 50% ou 100% ;
#    nrag_ajag = f5hm + f5im + f5jm 
#    # TODO: à integrer qqpart
#    
#    # déficits agricole des années antérieurs (imputables uniquement
#    # sur des revenus agricoles)
#    rag_timp = frag_timp + arag_timp + nrag_timp 
#    cond = (AUTRE <= P.def_agri_seuil)
#    def_agri = cond*(arag_defi + nrag_defi) + not_(cond)*min_(rag_timp, arag_defi + nrag_defi)
#    # TODO : check 2006 cf art 156 du CGI pour 2006
#    # sur base 2003:
#    # cf menage 3020938 pour le déficit agricole qui peut déduire et ménage
#    # 3001872 qui ne peut pas déduire.
#    def_agri_ant    = min_(max_(0,rag_timp - def_agri), f5sq)
#
#def _rag(frag_exon, frag_impo, arag_exon, arag_impg, arag_defi, nrag_exon, nrag_impg, nrag_defi, nrag_ajag):
#    '''
#    frag_exon (f5hn, f5in, f5jn)
#    frag_impo (f5ho, f5io, f5jo)    
#    arag_exon (f5hb, f5ib, f5jb)
#    arag_impg (f5hc, f5ic, f5jc)
#    arag_defi (f5hf, f5if, f5jf)
#    nrag_exon (f5hh, f5ih, f5jh)
#    nrag_impg (f5hi, f5ii, f5ji)
#    nrag_defi (f5hl, f5il, f5jl)
#    nrag_ajag (f5hm, f5im, f5jm)
#    '''    
#    rag = (frag_exon + frag_impo + 
#           arag_exon + arag_impg - arag_defi + 
#           nrag_exon + nrag_impg - nrag_defi + 
#           nrag_ajag)
#
##    zragf = ragv + ragc + ragp
#    
#    ## B revenus industriels et commerciaux professionnels 
#    
#    #regime micro entreprise
#    mbicf_impv = abatv(f5ko,P) + abatv(f5lo,P) + abatv(f5mo,P)
#    mbicf_imps = abats(f5kp,P) + abats(f5lp,P) + abats(f5mp,P)
#    mbicf_pvct = f5kx + f5lx + f5mx
#    mbicf_mvlt = f5kr + f5lr + f5mr
#    mbicf_mvct = f5hu
#    mbicf_timp = mbicf_impv + mbicf_imps - mbicf_mvlt
#    
#    #Régime du bénéfice réel bénéficiant de l'abattement CGA
#    abicf_impn = f5kc + f5lc + f5mc
#    abicf_imps = f5kd + f5ld + f5md
#    abicf_defn = f5kf + f5lf + f5mf
#    abicf_defs = f5kg + f5lg + f5mg
#    abicf_timp = abicf_impn + abicf_imps - (abicf_defn + abicf_defs)
#    abicf_defe = -min_(abicf_timp,0) 
#    # base 2003: cf ménage 3021218 pour l'imputation illimitée de ces déficits.
#    
#    #Régime du bénéfice réel ne bénéficiant pas de l'abattement CGA
#    nbicf_impn = f5ki + f5li + f5mi
#    nbicf_imps = f5kj + f5lj + f5mj
#    nbicf_defn = f5kl + f5ll + f5ml
#    nbicf_defs = f5km + f5lm + f5mm
#    nbicf_timp = (nbicf_impn + nbicf_imps) - (nbicf_defn + nbicf_defs)
#    nbicf_defe = -min_(nbicf_timp,0) ;
#    # base 2003 cf ménage 3015286 pour l'imputation illimitée de ces déficits.
#    
#    #Abatemment artisant pécheur
#    nbicf_apch = f5ks + f5ls + f5ms # TODO : à intégrer qqpart
#    
#    zbicv = f5kn + f5ko + f5kp + f5kb + f5kh + f5kc + f5ki + f5kd + f5kj - f5kf - f5kl - f5kg - f5km + f5ks
#    zbicc = f5ln + f5lo + f5lp + f5lb + f5lh + f5lc + f5li + f5ld + f5lj - f5lf - f5ll - f5lg - f5lm + f5ls     
#    zbicp = f5mn + f5mo + f5mp + f5mb + f5mh + f5mc + f5mi + f5md + f5mj - f5mf - f5ml - f5mg - f5mm + f5ms
#    
#    condv = (f5ko>0) & (f5kp==0)
#    condc = (f5lo>0) & (f5lp==0)
#    condp = (f5mo>0) & (f5mp==0)
#    tauxv = P.microentreprise.vente_taux*condv + P.microentreprise.servi_taux*not_(condv)
#    tauxc = P.microentreprise.vente_taux*condc + P.microentreprise.servi_taux*not_(condc)
#    tauxp = P.microentreprise.vente_taux*condp + P.microentreprise.servi_taux*not_(condp)
#    
#    P.cbicf_min = 305
#    
#    cbicv = min_(f5ko+f5kp+f5kn, max_(P.cbicf_min,round(f5ko*P.microentreprise.vente_taux + f5kp*P.microentreprise.servi_taux + f5kn*tauxv)))
#    cbicc = min_(f5lo+f5lp+f5ln, max_(P.cbicf_min,round(f5lo*P.microentreprise.vente_taux + f5lp*P.microentreprise.servi_taux + f5ln*tauxc)));
#    cbicp = min_(f5mo+f5mp+f5mn, max_(P.cbicf_min,round(f5mo*P.microentreprise.vente_taux + f5mp*P.microentreprise.servi_taux + f5mn*tauxp)));
#    
#    ricv = zbicv - cbicv
#    ricc = zbicc - cbicc
#    ricp = zbicp - cbicp
#    
#    table.set('ric', ricv, 'foy', 'vous')
#    table.set('ric', ricc, 'foy', 'conj')
#    table.set('ric', ricp, 'foy', 'pac1')
#    
#    zricf = ricv + ricc + ricp
#    
#    ## C revenus industriels et commerciaux non professionnels 
#    # (revenus accesoires du foyers en nomenclature INSEE)
#    #regime micro entreprise
#    maccf_impv = abatv(f5no,P) + abatv(f5oo,P) + abatv(f5po,P);
#    maccf_imps = abats(f5np,P) + abats(f5op,P) + abats(f5pp,P);
#    maccf_pvct = f5nx + f5ox + f5px
#    maccf_mvlt = f5nr + f5or + f5pr
#    maccf_mvct = f5iu
#    maccf_timp = maccf_impv + maccf_imps - maccf_mvlt
#    
#    #Régime du bénéfice réel bénéficiant de l'abattement CGA
#    aaccf_impn = f5nc + f5oc + f5pc
#    aaccf_imps = f5nd + f5od + f5pd
#    aaccf_defn = f5nf + f5of + f5pf
#    aaccf_defs = f5ng + f5og + f5pg
#    aaccf_timp = max_(0,aaccf_impn + aaccf_imps - (aaccf_defn + aaccf_defs))
#    
#    #Régime du bénéfice réel ne bénéficiant pas de l'abattement CGA
#    naccf_impn = f5ni + f5oi + f5pi
#    naccf_imps = f5nj + f5oj + f5pj
#    naccf_defn = f5nl + f5ol + f5pl
#    naccf_defs = f5nm + f5om + f5pm
#    naccf_timp = max_(0,naccf_impn + naccf_imps - (naccf_defn + naccf_defs))
#    # TODO : base 2003 comprendre pourquoi le ménage 3018590 n'est pas imposé sur 5nj.
#    
#    ## E revenus non commerciaux non professionnels 
#    #regime déclaratif special ou micro-bnc
#    mncnp_impo = abatnc(f5ku,P) + abatnc(f5lu,P) + abatnc(f5mu,P);
#    mncnp_pvct = f5ky + f5ly + f5my
#    mncnp_mvlt = f5kw + f5lw + f5mw
#    mncnp_mvct = f5ju;
#    mncnp_timp = mncnp_impo - mncnp_mvlt;
#    
#    # TODO : 2006 
#    # régime de la déclaration controlée 
#    cncnp_bene = f5sn + f5ns + f5os
#    cncnp_defi = f5sp + f5nu + f5ou + f5sr
#    #total 11
#    cncnp_timp = max_(0,cncnp_bene - cncnp_defi); 
#    # TODO : abatement jeunes créateurs 
#    
#    zaccv = f5nn + f5no + f5np + f5nb + f5nc + f5nd - f5nf - f5ng + f5nh + f5ni + f5nj - f5nl - f5nm + f5ku + f5sn - f5sp + f5sv ;
#
#    zaccc = f5on + f5oo + f5op + f5ob + f5oc + f5od - f5of - f5og + f5oh + f5oi + f5oj - f5ol - f5om + f5lu + f5ns - f5nu + f5sw ;
#    
#    zaccp = f5pn + f5po + f5pp + f5pb + f5pc + f5pd - f5pf - f5pg + f5ph + f5pi + f5pj - f5pl - f5pm + f5mu + f5os - f5ou + f5sx ;
#    
#    condv = (f5no >0) & (f5np ==0) ;
#    condc = (f5oo >0) & (f5op ==0) ;
#    condp = (f5po >0) & (f5pp ==0) ;
#    tauxv = P.microentreprise.vente_taux*condv + P.microentreprise.servi_taux*not_(condv) ;
#    tauxc = P.microentreprise.vente_taux*condc + P.microentreprise.servi_taux*not_(condc) ;
#    tauxp = P.microentreprise.vente_taux*condp + P.microentreprise.servi_taux*not_(condp) ;
#    
#    caccv = min_(f5no + f5np + f5nn + f5ku, max_(P.nc_abat_min, 
#            round(f5no*P.microentreprise.vente_taux + f5np*P.microentreprise.servi_taux 
#            + f5nn*tauxv + f5ku*P.nc_abat_taux )));
#    caccc = min_(f5oo + f5op + f5on + f5lu, max_(P.nc_abat_min, 
#            round(f5oo*P.microentreprise.vente_taux + f5op*P.microentreprise.servi_taux 
#            + f5on*tauxc + f5lu*P.nc_abat_taux )));
#    caccp = min_(f5po + f5pp + f5pn + f5mu, max_(P.nc_abat_min, 
#            round(f5po*P.microentreprise.vente_taux + f5pp*P.microentreprise.servi_taux 
#            + f5pn*tauxp + f5mu*P.nc_abat_taux )));
#    
#    racv = zaccv - caccv
#    racc = zaccc - caccc
#    racp = zaccp - caccp
#
#    table.set('rac', racv, 'foy', 'vous')
#    table.set('rac', racc, 'foy', 'conj')
#    table.set('rac', racp, 'foy', 'pac1')
#    
#    
#    zracf = racv + racc + racp
#    
#    ## D revenus non commerciaux professionnels
#    
#    #regime déclaratif special ou micro-bnc
#    mbncf_impo = abatnc(f5hq,P) + abatnc(f5iq,P) + abatnc(f5jq,P)
#    mbncf_pvct = f5hv + f5iv + f5jv
#    mbncf_mvlt = f5hs + f5is + f5js
#    mbncf_mvct = f5kz
#    mbncf_timp = mbncf_impo - mbncf_mvlt
#    
#    #regime de la déclaration contrôlée bénéficiant de l'abattement association agréée
#    abncf_impo = f5qc + f5rc + f5sc
#    abncf_defi = f5qe + f5re + f5se
#    abncf_timp = abncf_impo - abncf_defi;
#    
#    #regime de la déclaration contrôlée ne bénéficiant pas de l'abattement association agréée
#    nbncf_impo = f5qi + f5ri + f5si ;
#    nbncf_defi = f5qk + f5rk + f5sk ;
#    nbncf_timp = nbncf_impo - nbncf_defi;
#    # cf base 2003 menage 3021505 pour les deficits
#    
#    zbncv = f5hp + f5hq + f5qb + f5qh + f5qc + f5qi - f5qe - f5qk + f5ql + f5qm;
#    zbncc = f5ip + f5iq + f5rb + f5rh + f5rc + f5ri - f5re - f5rk + f5rl + f5rm;
#    zbncp = f5jp + f5jq + f5sb + f5sh + f5sc + f5si - f5se - f5sk + f5sl ;
#    
#    cbncv = min_(f5hp + f5hq, max_(P.nc_abat_min, round((f5hp + f5hq)*P.nc_abat_taux)))
#    cbncc = min_(f5ip + f5iq, max_(P.nc_abat_min, round((f5ip + f5iq)*P.nc_abat_taux)))
#    cbncp = min_(f5jp + f5jq, max_(P.nc_abat_min, round((f5jp + f5jq)*P.nc_abat_taux)))
#    
#    rncv = zbncv - cbncv
#    rncc = zbncc - cbncc
#    rncp = zbncp - cbncp
#
#    table.set('rnc', rncv, 'foy', 'vous')
#    table.set('rnc', rncc, 'foy', 'conj')
#    table.set('rnc', rncp, 'foy', 'pac1')
#            
#    zrncf =  rncv +  rncv +  rncp
#    
#    ## Totaux
#    atimp = aragf_timp + abicf_timp +  aaccf_timp + abncf_timp;
#    ntimp = nragf_timp + nbicf_timp +  naccf_timp + nbncf_timp;
#    
#    majo_cga = max_(0,P.cga_taux2*(ntimp+fragf_impo)); # pour ne pas avoir à
#                                            # majorer les déficits
#    #total 6
#    rev_NS = fragf_impo + fragf_pvct + atimp + ntimp + majo_cga - def_agri - def_agri_ant 
#    
#    #revenu net après abatement
#    # total 7
#    rev_NS_mi = mbicf_timp + maccf_timp + mbncf_timp + mncnp_timp 
#    
#    
#    #plus value ou moins value à court terme
#    #activité exercée à titre professionnel 
#    # total 8
#    pvct_pro = mbicf_pvct - mbicf_mvct + mbncf_pvct - mbncf_mvct
#    #activité exercée à titre non professionnel
#    #revenus industriels et commerciaux non professionnels 
#    # total 9
#    pvct_icnpro = min_(maccf_pvct - maccf_mvct, maccf_timp) 
#    #revenus non commerciaux non professionnels 
#    # total 10
#    pvct_ncnpro = min_(mncnp_pvct - mncnp_mvct, mncnp_timp)
#    
#    #total 11 cncnp_timp déja calculé        
#    
#    rpns_pvct = fragf_pvct + mbicf_pvct + maccf_pvct + mbncf_pvct + mncnp_pvct;
#    rpns_mvct = mbicf_mvct + maccf_mvct + mbncf_mvct + mncnp_mvct;
#    rpns_mvlt = mbicf_mvlt + maccf_mvlt + mbncf_mvlt + mncnp_mvlt;
#    
#    # imp_plusval_ces = plusval_ces*plusvalces_taux;
#    RPNS = rev_NS + rev_NS_mi + pvct_pro + pvct_icnpro + pvct_ncnpro + cncnp_timp
#    
#    # Calcul des revenus individuels
#    rpnsv = ragv + ricv + racv + rncv
#    rpnsc = ragc + ricc + racc + rncc
#    rpnsp = ragp + ricp + racp + rncp
#    
#    table.set('rpns', rpnsv, 'foy', 'vous')
#    table.set('rpns', rpnsc, 'foy', 'conj')
#    table.set('rpns', rpnsp, 'foy', 'pac1')   
#    
#    table.close_()
#
#    return RPNS

def _deficit_ante(f6fa, f6fb, f6fc, f6fd, f6fe, f6fl):
    '''
    Déficits antérieurs
    '''
    return f6fa + f6fb + f6fc + f6fd + f6fe + f6fl


#def Charges_deductibles(self, P):
#    '''
#    Charges déductibles
#    '''
#    table = population
#
#    table.openReadMode()
#    niches1, niches2, ind_rfr = charges_deductibles.niches(year)
#    charges_deductibles.charges_calc(self, P, table, niches1, niches2, ind_rfr)
#
#    ## stockage des pensions dans les individus
#    zalvf = charges_deductibles.penali(self, P, table)
#    table.close_()
#
#    table.openWriteMode()
#    table.setColl('alv', -zalvf, table = 'output')
#    table.close_()

def _abat_spe(age, caseP, caseF, rng, nbN, _P, _option = {'age': [VOUS, CONJ]}):
    '''
    Abattements spéciaux 
    - pour personnes âges ou invalides : Si vous êtes âgé(e) de plus de 65 ans
      ou invalide (titulaire d’une pension d’invalidité militaire ou d’accident 
      du travail d’au moins 40 % ou titulaire de la carte d’invalidité), vous 
      bénéficiez d’un abattement de 2 172 € si le revenu net global de votre 
      foyer fiscal n’excède pas 13 370 € ; il est de 1 086 € si ce revenu est 
      compris entre 13 370 € et 21 570 €. Cet abattement est doublé si votre 
      conjoint ou votre partenaire de PACS remplit également ces conditions 
      d’âge ou d’invalidité. Cet abattement sera déduit automatiquement lors 
      du calcul de l’impôt.
    - pour enfants à charge ayant fondé un foyer distinct : Si vous avez accepté
      le rattachement de vos enfants mariés ou pacsés ou de vos enfants 
      célibataires, veufs, divorcés, séparés, chargés de famille, vous bénéficiez 
      d’un abattement sur le revenu imposable de 5 495 € par personne ainsi 
      rattachée. Si l’enfant de la personne rattachée est réputé à charge de 
      l’un et l’autre de ses parents (garde alternée), cet abattement est divisé 
      par deux soit 2 748€. Exemple : 10 990 € pour un jeune ménage et 8 243 €
      pour un célibataire avec un jeune enfant en résidence alternée.
    '''
    ageV, ageC = age[VOUS], age[CONJ]
    invV, invC = caseP, caseF
    P = _P.ir.abattements_speciaux
    as_inv = P.inv_montant*((rng <= P.inv_max1) + 
                            ((rng > P.inv_max1)&(rng <= P.inv_max2))*0.5*(1*(((ageV>=65)&(ageV>0))| invV) + 
                                                                        1*(((ageC>=65)&(ageC>0))| invC) )  )
    as_enf = nbN*P.enf_montant 

    return min_(rng, as_inv + as_enf)

def _nbptr(nb_pac, marpac, celdiv, veuf, jveuf, nbF, nbG, nbH, nbI, nbR, nbJ, caseP, caseW, caseG, caseE, caseK, caseN, caseF, caseS, caseL, caseT, _P):
    '''
    nombre de parts du foyer
    note 1 enfants et résidence alternée (formulaire 2041 GV page 10)
    
    P.enf1 : nb part 2 premiers enfants
    P.enf2 : nb part enfants de rang 3 ou plus
    P.inv1 : nb part supp enfants invalides (I, G)
    P.inv2 : nb part supp adultes invalides (R)
    P.not31 : nb part supp note 3 : cases W ou G pour veuf, celib ou div
    P.not32 : nb part supp note 3 : personne seule ayant élevé des enfants
    P.not41 : nb part supp adultes invalides (vous et/ou conjoint) note 4
    P.not42 : nb part supp adultes anciens combattants (vous et/ou conjoint) note 4
    P.not6 : nb part supp note 6
    P.isol : demi-part parent isolé (T)
    P.edcd : enfant issu du mariage avec conjoint décédé;
    '''
    P = _P.ir.quotient_familial
    no_pac  = nb_pac == 0 # Aucune personne à charge en garde exclusive
    has_pac = not_(no_pac)
    no_alt  = nbH == 0 # Aucun enfant à charge en garde alternée
    has_alt = not_(no_alt)
    
    ## nombre de parts liées aux enfants à charge
    # que des enfants en résidence alternée
    enf1 = (no_pac & has_alt)*(P.enf1*min_(nbH,2)*0.5 + P.enf2*max_(nbH-2,0)*0.5)
    # pas que des enfants en résidence alternée
    enf2 = (has_pac & has_alt)*((nb_pac==1)*(P.enf1*min_(nbH,1)*0.5 + P.enf2*max_(nbH-1,0)*0.5) + (nb_pac>1)*(P.enf2*nbH*0.5))
    # pas d'enfant en résidence alternée    
    enf3 = P.enf1*min_(nb_pac,2) + P.enf2*max_((nb_pac-2),0)
    
    enf = enf1 + enf2 + enf3 
    ## note 2 : nombre de parts liées aux invalides (enfant + adulte)
    n2 = P.inv1*(nbG + nbI/2) + P.inv2*nbR 
    
    ## note 3 : Pas de personne à charge
    # - invalide ;

    n31a = P.not31a*( no_pac & no_alt & caseP )
    # - ancien combatant ;
    n31b = P.not31b*( no_pac & no_alt & ( caseW | caseG ) ) 
    n31 = max_(n31a,n31b)
    # - personne seule ayant élevé des enfants
    n32 = P.not32*( no_pac & no_alt &(( caseE | caseK) & not_(caseN)))
    n3 = max_(n31,n32)
    ## note 4 Invalidité de la personne ou du conjoint pour les mariés ou
    ## jeunes veuf(ve)s
    n4 = max_(P.not41*(1*caseP + 1*caseF), P.not42*(caseW | caseS))
    
    ## note 5
    #  - enfant du conjoint décédé
    n51 =  P.cdcd*(caseL & ((nbF + nbJ)>0))
    #  - enfant autre et parent isolé
    n52 =  P.isol*caseT*( ((no_pac & has_alt)*((nbH==1)*0.5 + (nbH>=2))) + 1*has_pac)
    n5 = max_(n51,n52)
    
    ## note 6 invalide avec personne à charge
    n6 = P.not6*(caseP & (has_pac | has_alt))
    
    ## note 7 Parent isolé
    n7 = P.isol*caseT*((no_pac & has_alt)*((nbH==1)*0.5 + (nbH>=2)) + 1*has_pac)
    
    ## Régime des mariés ou pacsés
    m = 2 + enf + n2 + n4
    
    ## veufs  hors jveuf
    v = 1 + enf + n2 + n3 + n5 + n6
    
    ## celib div
    c = 1 + enf + n2 + n3 + n6 + n7
    return (marpac | jveuf)*m + (veuf & not_(jveuf))*v + celdiv*c
    

#def Reductions(self, IPnet, P, table):
#    ''' 
#    Réductions d'impôts
#    '''
#    table.openReadMode()
#    niches = reductions_impots.niches(year)
#    reducs = zeros(taille)
#    for niche in niches:
#        reducs += niche(self, P, table)
#         
#    table.close_()
#    return min_(reducs, IPnet)

def _plus_values(f3vg, f3vh, f3vl, f3vm, f3vi, f3vf, f3vd, rpns_pvce, _P):
    P = _P.ir.plus_values
        # revenus taxés à un taux proportionnel
    rdp = max_(0,f3vg - f3vh) + f3vl + rpns_pvce + f3vm + f3vi + f3vf
    out = (P.pvce*rpns_pvce +
           P.taux1*max_(0,f3vg - f3vh) +
           P.caprisque*f3vl +
           P.pea*f3vm +
           P.taux3*f3vi +
           P.taux4*f3vf )
    if year >= 2008:
        # revenus taxés à un taux proportionnel
        rdp += f3vd
        out += P.taux1*f3vd
        
    return round(out)

def _div(rpns_pvce, rpns_pvct, rpns_mvct, rpns_mvlt, f3vc, f3ve, f3vg, f3vh, f3vl, f3vm):
    return f3vc + f3ve + f3vg - f3vh + f3vl+ f3vm + rpns_pvce + rpns_pvct - rpns_mvct - rpns_mvlt
    

def _div_rmi(f3vc, f3ve, f3vg, f3vl, f3vm):
    return f3vc + f3ve + f3vg + f3vl+ f3vm
    
def _rev_coll(rto_net, rev_cap_lib, rev_cap_bar, div, abat_spe, alv, glo, fon, f7ga, f7gb, f7gc):
    '''
    revenus collectif
    'foy'
    '''
    # TODO: ajouter les revenus de l'étranger etr*0.9
    return rto_net + rev_cap_lib + rev_cap_bar  + fon + glo - alv - f7ga - f7gb - f7gc - abat_spe
    
    # pour le calcul de l'allocation de soutien familial     
def _asf_elig(caseT, caseL):
    return caseT | caseL

def al_nbinv(nbR):
    return nbR

#def Credits(self, P, table):
#    '''
#    Imputations (crédits d'impôts)
#    '''
#    table.openReadMode()
#    niches = credits_impots.niches(year)
#    reducs = zeros(taille)
#    for niche in niches:
#        reducs += niche(self, P, table)
#    table.close_()
#
#    ppe = Ppe(P.ppe)
#
#    return reducs + ppe

###############################################################################
## Calcul de la prime pour l'emploi
###############################################################################

def _ppe_coef(jour_xyz):
    '''
    ppe: coefficient de conversion en cas de changement en cours d'année
    'foy'
    '''    
    nbJour = (jour_xyz==0) + jour_xyz
    return 360/nbJour

def _ppe_elig(rfr, ppe_coef, marpac, veuf, celdiv, nbptr, _P):
    '''
    eligibilité à la ppe, returns a bool
    'foy'
    '''
    P = _P.ir.ppe
    seuil = (veuf|celdiv)*(P.eligi1 + 2*max_(nbptr-1,0)*P.eligi3) \
            + marpac*(P.eligi2 + 2*max_(nbptr-2,0)*P.eligi3)
    out = (rfr*ppe_coef) <= seuil
    return out

def _ppe_rev(sal, hsup, rpns, _P):
    '''
    base ressource de la ppe
    'ind'
    '''
    P = _P.ir.ppe
    # Revenu d'activité salarié
    rev_sa = sal + hsup #+ TV + TW + TX + AQ + LZ + VJ
    # Revenu d'activité non salarié
    rev_ns = min_(0,rpns)/P.abatns + max_(0,rpns)*P.abatns
    return rev_sa + rev_ns

def _ppe_coeff_tp(ppeHeure, ppeJours, ppeCheckBox, ppe_tp_ns, _P):
    P = _P.ir.ppe
    frac_sa = ppeHeure/P.TP_nbh
    frac_ns = ppeJours/P.TP_nbj
    # TODO: changer ppeCheckBox en ppe_tp_sa
    tp = (ppeCheckBox == 1)|(ppe_tp_ns == 1)|(frac_sa + frac_ns >= 1)
    return tp + not_(tp)*(frac_sa + frac_ns) 
    
def _ppe_base(ppe_rev, ppe_coeff_tp, ppe_coef):
    out = ppe_rev/(ppe_coeff_tp + (ppe_coeff_tp==0))*ppe_coef
    return out

def _ppe_elig_i(ppe_rev, ppe_coef_tp, _P):
    '''
    eligibilité individuelle à la ppe
    '''
    P = _P.ir.ppe
    return (ppe_rev >= P.seuil1)&(_ppe_coeff_tp!=0)

def _ppe(ppe_elig, ppe_elig_i, ppe_rev, ppe_base, ppe_coef, ppe_coef_tp, nb_pac, marpac, celdiv, veuf, caseT, caseL, nbH, _P, _option = {'ppe_elig_i': ALL, 'ppe_base': ALL, 'ppe_rev': ALL, 'ppe_coef_tp': ALL}):
    '''
    Prime pour l'emploi
    '''
    P = _P.ir.ppe

    eliv, elic, eli1, eli2, eli3 = ppe_elig_i[VOUS], ppe_elig_i[CONJ], ppe_elig_i[PAC1], ppe_elig_i[PAC2], ppe_elig_i[PAC3], 
    basevi, baseci = ppe_rev[VOUS], ppe_rev[CONJ]
    basev, basec, base1, base2, base3  = ppe_base[VOUS], ppe_base[CONJ], ppe_base[PAC1], ppe_base[PAC2], ppe_base[PAC1]
    coef_tpv, coef_tpc, coef_tp1, coef_tp2, coef_tp3  = ppe_coef_tp[VOUS], ppe_coef_tp[CONJ], ppe_coef_tp[PAC1], ppe_coef_tp[PAC2], ppe_coef_tp[PAC1]
    
    nb_pac_ppe = max_(0, nb_pac - eli1 - eli2 -eli3 )
        
    ligne2 = marpac & xor_(basevi >= P.seuil1, baseci >= P.seuil1)
    ligne3 = (celdiv | veuf) & caseT & not_(veuf & caseT & caseL)
    ligne1 = not_(ligne2) & not_(ligne3)
    
    base_monact = ligne2*(eliv*basev + elic*basec)
    base_monacti = ligne2*(eliv*basevi + elic*baseci)

    def ppe_bar1(base):
        cond1 = ligne1 | ligne3
        cond2 = ligne2
        return 1/ppe_coef*((cond1 & (base <= P.seuil2))*(base)*P.taux1 +
                           (cond1 & (base> P.seuil2) & (base <= P.seuil3))*(P.seuil3 - base)*P.taux2 +
                           (cond2 & (base <= P.seuil2))*(base*P.taux1 ) +
                           (cond2 & (base >  P.seuil2) & (base <= P.seuil3))*((P.seuil3 - base)*P.taux2) +
                           (cond2 & (base >  P.seuil4) & (base <= P.seuil5))*(P.seuil5 - base)*P.taux3)

    def ppe_bar2(base):
        return 1/ppe_coef*((base <= P.seuil2)*(base)*P.taux1 +
                           ((base> P.seuil2) & (base <= P.seuil3))*(P.seuil3 - base1)*P.taux2 )

    # calcul des primes individuelles.
    ppev = eliv*ppe_bar1(basev)
    ppec = elic*ppe_bar1(basec)
    ppe1 = eli1*ppe_bar2(base1)
    ppe2 = eli2*ppe_bar2(base2)
    ppe3 = eli3*ppe_bar2(base3)
    
    ppe_monact_vous = (eliv & ligne2 & (basevi>=P.seuil1) & (basev <= P.seuil4))*P.monact
    ppe_monact_conj = (elic & ligne2 & (baseci>=P.seuil1) & (basec <= P.seuil4))*P.monact
    
    maj_pac = ppe_elig*(eliv|elic)*(
        (ligne1 & marpac & ((ppev+ppec)!=0) & (min_(basev,basec)<= P.seuil3))*P.pac*(nb_pac_ppe + nbH*0.5) +
        (ligne1 & (celdiv | veuf) & eliv & (basev<=P.seuil3))*P.pac*(nb_pac_ppe + nbH*0.5) +
        (ligne2 & (base_monacti >= P.seuil1) & (base_monact <= P.seuil3))*P.pac*(nb_pac_ppe + nbH*0.5) +
        (ligne2 & (base_monact > P.seuil3) & (base_monact <= P.seuil5))*P.pac*((nb_pac_ppe!=0) + 0.5*((nb_pac_ppe==0) & (nbH!=0))) +
        (ligne3 & (basevi >=P.seuil1) & (basev <= P.seuil3))*((min_(nb_pac_ppe,1)*2*P.pac + max_(nb_pac_ppe-1,0)*P.pac) + (nb_pac_ppe==0)*(min_(nbH,2)*P.pac + max_(nbH-2,0)*P.pac*0.5)) +
        (ligne3 & (basev  > P.seuil3) & (basev <= P.seuil5))*P.pac*((nb_pac_ppe!=0)*2 +((nb_pac_ppe==0) & (nbH!=0))))

    def coef(coef_tp):
        return (coef_tp <=0.5)*coef_tp*1.45 + (coef_tp > 0.5)*(0.55*coef_tp + 0.45)
    
    ppe_vous = ppe_elig*(ppev*coef(coef_tpv) + ppe_monact_vous)
    ppe_conj = ppe_elig*(ppec*coef(coef_tpc) + ppe_monact_conj)
    ppe_pac1 = ppe_elig*(ppe1*coef(coef_tp1))
    ppe_pac2 = ppe_elig*(ppe2*coef(coef_tp2))
    ppe_pac3 = ppe_elig*(ppe3*coef(coef_tp3))
    
    ppe_tot = ppe_vous + ppe_conj + ppe_pac1 + ppe_pac2 + ppe_pac3 +  maj_pac
    
    ppe_tot = (ppe_tot!=0)*max_(P.versmin,ppe_vous + ppe_conj + ppe_pac1 + ppe_pac2 + ppe_pac3 + maj_pac)
            
    return ppe_tot
