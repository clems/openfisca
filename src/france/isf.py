# -*- coding:utf-8 -*-
# Copyright © 2012 Sarah Dijols

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
from numpy import ( maximum as max_, minimum as min_) 


## immeubles bâtis- non bâtis, parts de groupements ##

def _res_princ (ab, _P):
    P= _P.isf.res_princ
    print 'residence'
    print ab
    print (1-P.taux)*ab
    return (1-P.taux)*ab

def _forets(bc, _P):
    P= _P.isf.nonbat
    return bc*P.taux_f
 
def _ruraux(be, _P): 
    ''' bien ruraux loués à long terme'''
    P = _P.isf.nonbat
    return min_(be, P.seuil)*P.taux_r1 + max_(be-P.seuil,0)*P.taux_r2 
 
def _grp_agr(bh, _P):
    '''
    part de groupements forestiers- agricoles fonciers
    '''
    P = _P.isf.nonbat
    return min_(bh, P.seuil)*P.taux_r1 + max_(bh-P.seuil,0)*P.taux_r2

## droits sociaux- valeurs mobilières- liquidités- autres meubles ##

def _isf_actions_sal(cl2, _P): ## non présent en 2005##
    '''
    parts ou actions détenues par les salariés et mandataires sociaux
    '''
    P = _P.isf.droits_soc
    return  cl2*P.taux1  

def _actions_conserv(cb, _P):
    P= _P.isf.droits_soc
    ''' parts ou actions de sociétés avec engagement de 6 ans conservation minimum'''
    return cb*P.taux2 
def _autres_biens_meubles(cg, co):
    '''
    autres bien meubles dont contrat d'assurance vie
    '''
    return cg 


def _patrimoine(res_princ, ac, forets, ruraux, grp_agr, bk, isf_actions_sal, actions_conserv, cd, cf2, ce, autres_biens_meubles):
    # res_princ résidence principale
    # ac autres immeubles
    # bk autres biens  
    # cd droits sociaux de sociétés dans lesquelles vous avez exercez une fonction ou activité
    # ce autres valeurs mobilières
    # cf2  liquidités
    return autres_biens_meubles + cf2 + ce + res_princ + ac + forets + ruraux + grp_agr + bk + isf_actions_sal + actions_conserv + cd

def _forf_mob(ef, patrimoine, _P):
    P=_P.isf.forf_mob
    return (ef != 0)*ef + (ef==0)*patrimoine*P.taux 
  
def _ass_isf(patrimoine, forf_mob, gh):
  
    return forf_mob + patrimoine - gh 
    
## calcul de l'impôt par application du barème ##

def _isf_iai(ass_isf, _P):
    bar = _P.isf.bareme
    bar.t_x()
    return bar.calc(ass_isf)

def _isf_reduc_pac(nb_pac, nbH, _P):
    '''
    réductions pour personnes à charges
    '''
    P= _P.isf.reduc_pac
   
    return P.reduc_1*(nb_pac)+ P.reduc_2*nbH  


def _isf_inv_pme(mt, ne, mv, nf, mx, na, _P):
    '''
    réductions pour investissements dans les PME
    à partir de 2008!
    '''
    
    P= _P.isf.pme
    inv_dir_soc = mt*P.taux2 + ne*P.taux1
    holdings = mv*P.taux2+ nf*P.taux1
    fip = mx*P.taux1
    fcpi= na*P.taux1
    return holdings + fip + fcpi + inv_dir_soc

    
def _isf_org_int_gen(nc, _P):
    P = _P.isf.pme
    return nc*P.taux2

def _isf_avant_plaf(isf_iai, isf_inv_pme, isf_org_int_gen, isf_reduc_pac, _P ) :
    '''
    montant de l'impôt avant plafonnement
    '''
    borne_max = _P.isf.pme.max
    print "isf_avant_plaf"
    print isf_iai - min_(isf_inv_pme + isf_org_int_gen, borne_max) - isf_reduc_pac
    return isf_iai - min_(isf_inv_pme + isf_org_int_gen, borne_max) - isf_reduc_pac

  
## calcul du plafonnement ##
  
def _tot_impot(irpp, isf_avant_plaf ):
    print 'tot impot'
    print -irpp + isf_avant_plaf 
    return -irpp + isf_avant_plaf
# irpp n'est pas suffisant : ajouter ir soumis à taux propor + impôt acquitté à l'étranger
# + prélèvement libé de l'année passée + montant de la csg TODO


def _revetproduits(sal_net, pen_net, rto_net, rfr_rvcm, fon, ric, rag, rpns_exon, rpns_pvct, rev_cap_lib, imp_lib, _P) :   # TODO: ric? benef indu et comm 
    pt = max_(sal_net + pen_net + rto_net + rfr_rvcm + ric + rag + rpns_exon + rpns_pvct + rev_cap_lib + imp_lib, 0)
    # rev_cap et imp_lib pour produits soumis à prel libératoire- check TODO
    ## def rev_exon et rev_etranger dans data? ##
    P= _P.isf.plafonnement
    return pt*P.taux

def _isf_apres_plaf(tot_impot, revetproduits, isf_avant_plaf, _P): 
    plafonnement = max_(tot_impot- revetproduits, 0)
    P = _P.isf.plaf
    limitationplaf = (isf_avant_plaf<= P.seuil1)*plafonnement + (P.seuil1 <= isf_avant_plaf)*(isf_avant_plaf <= P.seuil2)*min_(plafonnement, P.seuil1) + (isf_avant_plaf >= P.seuil2)*min_(isf_avant_plaf*P.taux, plafonnement)  
    return (isf_avant_plaf - limitationplaf)
## si ISF avant plafonnement n'excède pas seuil 1= la limitation du plafonnement ne joue pas ##
## si entre les deux seuils; l'allègement est limité au 1er seuil ##
## si ISF avant plafonnement est supérieur au 2nd seuil, l'allègement qui résulte du plafonnement est limité à 50% de l'ISF ##


## rs est le montant des impôts acquittés hors de France ## 
## montant net à payer ##
def _isf(rs, isf_avant_plaf, isf_apres_plaf, irpp):
   
    return -((isf_apres_plaf - rs)*((-irpp)>0) + (isf_avant_plaf-rs)*((-irpp)<=0))
## avec indicatrice ## 


## BOUCLIER FISCAL ##

## calcul de l'ensemble des revenus du contribuable ##
def _bouclier_rev(rbg, rpns_maj, csg_deduc, deficit_globaux, rcvm_rfr, deficit_ante, rev_cap_lib, imp_lib, rev_exo, rev_or, pen_alim, eparet, ric):
    ''' total des revenus sur l'année 'n' net de charges
    '''
    null = 0*rbg
    ## Revenus 
    # Revenus soumis au barème
    frac_deficit_globaux = deficit_globaux 
    ## def _deficit_rcm(f2aa, f2al, f2am, f2an):
    ## return f2aa + f2al + f2am + f2an ??
    frac_rcvm_rfr = 0.7*rcvm_rfr
    ## revenus distribués? 
    ## A majorer de l'abatt de 40% - montant brut en cas de PFL
    ## pour le calcul de droit à restitution : prendre 0.7*montant_brut_rev_dist_soumis_au_barème
    
    rev_bar = rbg - rpns_maj - csg_deduc - deficit_ante

## AJOUTER : indemnités de fonction percus par les élus- revenus soumis à régimes spéciaux

    # Revenu soumis à l'impôt sur le revenu forfaitaire
    rev_lib = rev_cap_lib + imp_lib+ ric 
    ## AJOUTER plus-values immo et moins values? 
    
    ##Revenus exonérés d'IR réalisés en France et à l'étranger##
    rev_exo= primes_pel + primes_cel + rente_pea + int_livrets + plus_values_per

    ## proposer à l'utilisateur des taux de réference- PER, PEA, PEL,...TODO
    ## sommes investis- calculer les plus_values annuelles et prendre en compte pour rev_exo?
    # revenus soumis à la taxe forfaitaire sur les métaux précieux : rev_or 
  
    revenus = rev_bar + rev_lib + rev_exo + rev_or
    
    ## CHARGES 
    # Pension alimentaires
    # Cotisations ou primes versées au titre de l'épargne retraite
   
    charges = pen_alim + eparet
    
    return revenus - charges
    
    
def bouclier_imp_gen (irpp, tax_hab, tax_fonc, isf, ): ## ajouter CSG- CRDS
    ## ajouter Prelèvements sources/ libé 
    ## impôt sur les plus-values immo et cession de fonds de commerce
    imp1= 0
    ''' 
    impôts payés en l'année 'n' au titre des revenus réalisés sur l'année 'n' 
    '''
    imp2= irpp + isf + tax_hab + tax_fonc
    '''
    impôts payés en l'année 'n' au titre des revenus réalisés en 'n-1'
    '''
    return imp1+ imp2

def _restitutions(ppe, restit_imp ):
    '''
    restitutions d'impôt sur le revenu et degrèvements percus en l'année 'n'
    '''
    return ppe+ restit_imp

def bouclier_sumimp(imp_gen, restitutions):
    '''
    somme totale des impôts moins restitutions et degrèvements 
    '''
    return imp_gen - restitutions

def _bouclier_fis(sumimp,revenus, _P):
    P= _P.isf.bouclier
    return sumimp - (revenus*P.taux)

