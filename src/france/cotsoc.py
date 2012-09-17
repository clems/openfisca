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
from france.data import CAT
from numpy import maximum as max_, minimum as min_, logical_not as not_, zeros
from core.utils import Bareme, scaleBaremes, combineBaremes


                
# TODO: CHECK la csg déductible en 2006 est case GH
# TODO:  la revenus soumis aux csg déductible et imposable sont en CG et BH en 2010 

#        # Heures supplémentaires exonérées
#        if not self.bareme.ir.autre.hsup_exo:
#            self.sal += self.hsup
#            self.hsup = 0*self.hsup
                        
# Exonération de CSG et de CRDS sur les revenus du chômage 
# et des préretraites si cela abaisse ces revenus sous le smic brut        
# TODO mettre un trigger pour l'éxonération des revenus du chômage sous un smic

# TODO RAFP assiette = prime
# TODO pension assiette = salaire hors prime
# autres salaires + primes
# TODO personnels non titulaires IRCANTEC etc

# TODO contribution patronale de prévoyance complémentaire
# Formation professionnelle (entreprise de 10 à moins de 20 salariés) salaire total 1,05%
# Formation professionnelle (entreprise de moins de 10 salariés)      salaire total 0,55%
# Taxe sur les salaries (pour ceux non-assujettis à la TVA)           salaire total 4,25% 
# TODO accident du travail ?
    
#temp = 0
#if hasattr(P, "prelsoc"):
#    for val in P.prelsoc.__dict__.itervalues(): temp += val
#    P.prelsoc.total = temp         
#else : 
#    P.__dict__.update({"prelsoc": {"total": 0} })
#
#a = {'sal':sal, 'pat':pat, 'csg':csg, 'crds':crds, 'exo_fillon': P.cotsoc.exo_fillon, 'lps': P.lps, 'ir': P.ir, 'prelsoc': P.prelsoc}
#return Dicts2Object(**a)

def _mhsup(hsup):
    return -hsup

############################################################################
## Revenus du capital
############################################################################

# revenus du capital soumis au barème
def _csg_cap_bar(rev_cap_bar, _P):
    '''
    Calcule la CSG sur les revenus du captial soumis au barème
    '''
    return - rev_cap_bar*_P.csg.capital.glob

def _crds_cap_bar(rev_cap_bar, _P):
    '''
    Calcule la CRDS sur les revenus du capital soumis au barème
    '''
    return - rev_cap_bar*_P.crds.capital

def _prelsoc_cap_bar(rev_cap_bar, _P):
    '''
    Calcule le prélèvement social sur les revenus du capital soumis au barème
    '''
    P = _P.prelsoc
    if _P.datesim.year < 2006:
        total = P.base 
    elif _P.datesim.year < 2009:    
        total = P.base + P.add
    else:    
        total = P.base + P.add + P.rsa
    return - rev_cap_bar*total

# revenus du capital soumis au prélèvement libératoire
def _csg_cap_lib(rev_cap_lib, _P):
    '''
    Calcule la CSG sur les revenus du capital soumis au prélèvement libératoire
    '''
    return - rev_cap_lib*_P.csg.capital.glob

def _crds_cap_lib(rev_cap_lib, _P):
    '''
    Calcule la CRDS sur les revenus du capital soumis au prélèvement libératoire
    '''
    return - rev_cap_lib*_P.crds.capital

def _prelsoc_cap_lib(rev_cap_lib, _P):
    '''
    Calcule le prélèvement social sur les revenus du capital soumis au prélèvement libératoire
    '''
    P = _P.prelsoc
    if _P.datesim.year < 2006:
        total = P.base 
    elif _P.datesim.year < 2009:    
        total = P.base + P.add
    else:    
        total = P.base + P.add + P.rsa
    return - rev_cap_lib*total


# TODO: non_imposabilité pour les revenus au barème
#        verse = (-csgcap_bar - crdscap_bar - prelsoccap_bar) > bareme.csg.capital.nonimp
##        verse=1
#        # CSG sur les revenus du patrimoine non imposés au barême (contributions sociales déjà prélevées)
#                
#        table.setIndiv('csgcap_bar', csgcap_bar*verse)
#        table.setIndiv('prelsoccap_bar', prelsoccap_bar*verse)
#        table.setIndiv('crdscap_bar', crdscap_bar*verse)


############################################################################
## Salaires
############################################################################

def _salbrut(sali, hsup, type_sal, _defaultP):
    '''
    Calcule le salaire brut à partir du salaire net
    '''
    plaf_ss = 12*_defaultP.cotsoc.gen.plaf_ss

    sal = scaleBaremes(_defaultP.cotsoc.sal, plaf_ss)
    csg = scaleBaremes(_defaultP.csg       , plaf_ss)
    
    sal.noncadre.__dict__.update(sal.commun.__dict__)
    sal.cadre.__dict__.update(sal.commun.__dict__)

    noncadre = combineBaremes(sal.noncadre)
    cadre    = combineBaremes(sal.cadre)
    fonc     = combineBaremes(sal.fonc)

    # On ajoute la CSG deductible
    noncadre.addBareme(csg.act.deduc)
    cadre.addBareme(csg.act.deduc)
    fonc.addBareme(csg.act.deduc)
    
    nca = noncadre.inverse()
    cad = cadre.inverse()
    fon = fonc.inverse()

    brut_nca = nca.calc(sali)
    brut_cad = cad.calc(sali)
    brut_fon = fon.calc(sali)

    salbrut = (brut_nca*(type_sal == CAT['noncadre']) + 
               brut_cad*(type_sal == CAT['cadre']) + 
               brut_fon*(type_sal == CAT['fonc']) )
    
    return salbrut + hsup

def _cotpat_contrib(salbrut, hsup, type_sal, _P):
    '''
    Cotisation sociales patronales contributives
    '''
    plaf_ss = 12*_P.cotsoc.gen.plaf_ss
    pat = scaleBaremes(_P.cotsoc.pat, plaf_ss)
    pat.noncadre.__dict__.update(pat.commun.__dict__)
    pat.cadre.__dict__.update(pat.commun.__dict__)
    pat.fonc.__dict__.update(pat.commun.__dict__)
    for var in ["apprentissage", "apprentissage2", "vieillesseplaf", "vieillessedeplaf", "formprof", "chomfg", "construction","assedic"]:
        del pat.fonc.__dict__[var]
    del pat.commun

    n = len(salbrut)
    cotpat = zeros(n)
    for categ in CAT:
        iscat = (type_sal == categ[1])
        for bar in getattr(pat,categ[0]).__dict__.itervalues():
            is_contrib = (bar.option == "contrib")
            temp = - (iscat*bar.calc(salbrut))*is_contrib
            cotpat += temp
    return cotpat


def _cotpat_noncontrib(salbrut, hsup, type_sal, _P):
    '''
    Cotisation sociales patronales non contributives
    '''
    plaf_ss = 12*_P.cotsoc.gen.plaf_ss
    pat = scaleBaremes(_P.cotsoc.pat, plaf_ss)
    pat.noncadre.__dict__.update(pat.commun.__dict__)
    pat.cadre.__dict__.update(pat.commun.__dict__)
    pat.fonc.__dict__.update(pat.commun.__dict__)
    for var in ["apprentissage", "apprentissage2", "vieillesseplaf", "vieillessedeplaf", "formprof", "chomfg", "construction","assedic"]:
        del pat.fonc.__dict__[var]
    del pat.commun

    n = len(salbrut)
    cotpat = zeros(n)
    for categ in CAT:
        iscat = (type_sal == categ[1])
        for bar in getattr(pat,categ[0]).__dict__.itervalues():
            is_noncontrib = (bar.option == "noncontrib")
            temp = - (iscat*bar.calc(salbrut))*is_noncontrib
            cotpat += temp
    return cotpat


def _cotpat(cotpat_contrib, cotpat_noncontrib):
    '''
    Cotisations sociales patronales
    '''
    return cotpat_contrib + cotpat_noncontrib


def _cotsal_contrib(salbrut, hsup, type_sal, _P):
    '''
    Cotisations sociales salariales contributives
    '''
    plaf_ss = 12*_P.cotsoc.gen.plaf_ss
    sal = scaleBaremes(_P.cotsoc.sal, plaf_ss)
    sal.noncadre.__dict__.update(sal.commun.__dict__)
    sal.cadre.__dict__.update(sal.commun.__dict__)
    del sal.commun
    
    n = len(salbrut)
    cotsal = zeros(n)
    for categ in CAT:
        iscat = (type_sal == categ[1])
        for bar in getattr(sal,categ[0]).__dict__.itervalues():
            is_contrib = (bar.option == "contrib")
            temp = - (iscat*bar.calc(salbrut-hsup))*is_contrib
            cotsal += temp
    return cotsal

def _cotsal_noncontrib(salbrut, hsup, type_sal, _P):
    '''
    Cotisations sociales salariales non-contributives
    '''
    plaf_ss = 12*_P.cotsoc.gen.plaf_ss
    sal = scaleBaremes(_P.cotsoc.sal, plaf_ss)
    sal.noncadre.__dict__.update(sal.commun.__dict__)
    sal.cadre.__dict__.update(sal.commun.__dict__)
    del sal.commun
    
    n = len(salbrut)
    cotsal = zeros(n)
    for categ in CAT:
        iscat = (type_sal == categ[1])
        for bar in getattr(sal,categ[0]).__dict__.itervalues():
            is_noncontrib = (bar.option == "noncontrib")
            temp = - (iscat*bar.calc(salbrut-hsup))*is_noncontrib
            cotsal += temp
    return cotsal

def _cotsal(cotsal_contrib, cotsal_noncontrib):
    '''
    Cotisations sociales salariales
    '''
    return cotsal_contrib + cotsal_noncontrib



def _csgsald(salbrut, hsup, _P):
    '''
    CSG deductible sur les salaires
    '''
    plaf_ss = 12*_P.cotsoc.gen.plaf_ss
    csg = scaleBaremes(_P.csg.act.deduc, plaf_ss)
    return - csg.calc(salbrut - hsup) 

def _csgsali(salbrut, hsup, _P):
    '''
    CSG imposable sur les salaires
    '''
    plaf_ss = 12*_P.cotsoc.gen.plaf_ss
    csg = scaleBaremes(_P.csg.act.impos, plaf_ss)
    return  - csg.calc(salbrut - hsup)

def _crdssal(salbrut, hsup, _P):
    '''
    CRDS sur les salaires
    '''
    plaf_ss = 12*_P.cotsoc.gen.plaf_ss
    crds = scaleBaremes(_P.crds.act, plaf_ss)
    return - crds.calc(salbrut - hsup)


def _sal_h_b(salbrut):
    '''
    Salaire horaire brut
    '''
    nbh_travaillees = 151.67*12
    return salbrut/nbh_travaillees


def _alleg_fillon(salbrut, sal_h_b, type_sal, _P):
    P = _P.cotsoc
    # TODO: utiliser type sal: uniquement pour les non cadres
    taux_fillon = taux_exo_fillon(sal_h_b, P) # * type_sal== 'noncadre'
    alleg_fillon = taux_fillon*salbrut
    return alleg_fillon

def _sal(salbrut, csgsald, cotsal, hsup):
    '''
    Calcul du salaire imposable
    '''
    return salbrut + csgsald + cotsal - hsup

def _salsuperbrut(salbrut, cotpat, alleg_fillon):
    return salbrut - cotpat - alleg_fillon
############################################################################
## Allocations chômage
############################################################################

def _chobrut(choi, csg_taux_plein, _P):
    '''
    Calcule les allocations chômage brute à partir des allocations nettes
    '''
    P = _P.csg.chom
    chom_plein = P.plein.deduc.inverse()
    chom_reduit = P.reduit.deduc.inverse()
    chobrut = not_(csg_taux_plein)*chom_reduit.calc(choi) +  csg_taux_plein*chom_plein.calc(choi)
    return chobrut

def _csgchod(chobrut, csg_taux_plein, _P):
    '''
    CSG déductible sur les allocations chômage
    '''
    plaf_ss = 12*_P.cotsoc.gen.plaf_ss
    csg = scaleBaremes(_P.csg.chom, plaf_ss)
    taux_plein = csg.plein.deduc.calc(chobrut)
    taux_reduit = csg.reduit.deduc.calc(chobrut)
    csgchod = csg_taux_plein*taux_plein + not_(csg_taux_plein)*taux_reduit
    return - csgchod

def _csgchoi(chobrut, csg_taux_plein, _P):
    '''
    CSG imposable sur les allocations chômage
    '''
    plaf_ss = 12*_P.cotsoc.gen.plaf_ss
    csg = scaleBaremes(_P.csg.chom, plaf_ss)
    taux_plein = csg.plein.impos.calc(chobrut)
    taux_reduit = csg.reduit.impos.calc(chobrut)
    csgchoi = csg_taux_plein*taux_plein + not_(csg_taux_plein)*taux_reduit
    return - csgchoi

def _crdscho(chobrut, _P):
    '''
    CRDS sur les allocations chômage
    '''
    plaf_ss = 12*_P.cotsoc.gen.plaf_ss
    crds = scaleBaremes(_P.crds.act, plaf_ss)
    return - crds.calc(chobrut)

def _cho(chobrut, csgchod):
    return chobrut + csgchod

# TODO: exonération de csg si la csg porte le montant de l'allocation chômage en dessous du SMIC
# cho_seuil_exo = P.csg.chom.min_exo*nbh_travaillees*smic_h_b
#isnotexo = cho > cho_seuil_exo                 
#
#csgchod = isnotexo*csgchod
#csgchoi = isnotexo*csgchoi
#crdscho = isnotexo*crdscho
#
#chobrut = isnotexo*chobrut + not_(isnotexo)*cho
#table.setIndiv('chobrut', chobrut)
#table.setIndiv('cho', chobrut + isnotexo*csgchod)

############################################################################
## Pensions
############################################################################
def _rstbrut(rsti, csg_taux_plein, _P):
    '''
    Calcule les pensions de retraites brutes à partir des pensions nettes
    '''
    P = _P.csg.retraite
    rst_plein = P.plein.deduc.inverse()  # TODO rajouter la non  déductible dans param
    rst_reduit = P.reduit.deduc.inverse()  #
    rstbrut = not_(csg_taux_plein)*rst_reduit.calc(rsti) + csg_taux_plein*rst_plein.calc(rsti, )    
    return rstbrut

def _csgrstd(rstbrut, csg_taux_plein, _P):
    '''
    CSG déductible sur les allocations chômage
    '''
    plaf_ss = 12*_P.cotsoc.gen.plaf_ss
    csg = scaleBaremes(_P.csg.retraite, plaf_ss)
    taux_plein = csg.plein.deduc.calc(rstbrut)
    taux_reduit = csg.reduit.deduc.calc(rstbrut)
    csgrstd = csg_taux_plein*taux_plein + not_(csg_taux_plein)*taux_reduit
    return - csgrstd

def _csgrsti(rstbrut, csg_taux_plein, _P):
    '''
    CSG imposable sur les allocations chômage
    '''
    plaf_ss = 12*_P.cotsoc.gen.plaf_ss
    csg = scaleBaremes(_P.csg.retraite, plaf_ss)
    taux_plein = csg.plein.impos.calc(rstbrut)
    taux_reduit = csg.reduit.impos.calc(rstbrut)
    csgrsti = csg_taux_plein*taux_plein + not_(csg_taux_plein)*taux_reduit
    return - csgrsti

def _crdsrst(rstbrut, _P):
    '''
    CRDS sur les pensions
    '''
    plaf_ss = 12*_P.cotsoc.gen.plaf_ss
    crds = scaleBaremes(_P.crds.rst, plaf_ss)
    return - crds.calc(rstbrut)

def _rst(rstbrut, csgrstd):
    '''
    Calcule les pensions nettes
    '''
    return rstbrut + csgrstd

############################################################################
## Impôt Landais, Piketty, Saez
############################################################################

def _base_csg(salbrut, chobrut, rstbrut, rev_cap_bar, rev_cap_lib):
    '''
    Assiette de la csg
    '''
    return salbrut + chobrut + rstbrut + rev_cap_bar + rev_cap_lib

def _ir_lps(base_csg, nbF, nbH, statmarit, _P):
    '''
    Impôt individuel sur l'ensemble de l'assiette de la csg, comme proposé par
    Landais, Piketty, Saez (2011)
    '''
    P = _P.lps
    nbEnf = (nbF + nbH/2)
    ae = nbEnf*P.abatt_enfant
    re = nbEnf*P.reduc_enfant
    ce = nbEnf*P.credit_enfant

    couple = (statmarit == 1) | (statmarit == 5)
    ac = couple*P.abatt_conj
    rc = couple*P.reduc_conj

    return - max_(0, P.bareme.calc(max_(base_csg - ae - ac, 0) )-re-rc) + ce


############################################################################
## Helper functions
############################################################################

def taux_exo_fillon(sal_h_b, P):
    '''
    Exonération Fillon
    http://www.securite-sociale.fr/comprendre/dossiers/exocotisations/exoenvigueur/fillon.htm
    '''
    # TODO Ainsi, à compter du 1er juillet 2007, le taux d’exonération des employeurs de 19 salariés au plus
    # passera pour une rémunération horaire égale au SMIC de 26 % à 28,1 %.
    
    # TODO la divison par zéro engendre un warning
    # Le montant maximum de l’allègement dépend de l’effectif de l’entreprise. 
    # Le montant est calculé chaque année civile, pour chaque salarié ; 
    # il est égal au produit de la totalité de la rémunération annuelle telle que visée à l’article L. 242-1 du code de la Sécurité sociale par un coefficient. 
    # Ce montant est majoré de 10 % pour les entreprises de travail temporaire au titre des salariés temporaires pour lesquels elle est tenue à l’obligation 
    # d’indemnisation compensatrice de congés payés.
    smic_h_b = P.gen.smic_h_b
    seuil = P.exo_fillon.seuil
    tx_max = P.exo_fillon.tx_max
    if seuil <= 1:
        return 0 
    return tx_max*min_(1,max_(seuil*smic_h_b/(sal_h_b + 1e-10)-1,0)/(seuil-1))

