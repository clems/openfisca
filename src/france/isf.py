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
    return (1-P.taux)*ab

def _forets(bc, _P):
    P= _P.isf.nonbat
    return bc*P.taux_f
 
def _ruraux(be, _P): 
    ''' bien ruraux loués à long terme'''
    P = _P.isf.nonbat
    return min_(be, P.seuil)*P.taux_r1 + max_(be-P.seuil,0)*P.taux_r2 
 
def _grp_agr(bh, _P):
    '''part de groupements forestiers- agricoles fonciers'''
    P = _P.isf.nonbat
    return min_(bh, P.seuil)*P.taux_r1 + max_(bh-P.seuil,0)*P.taux_r2

## droits sociaux- valeurs mobilières- liquidités- autres meubles ##

def _actions_sal(cl2, _P): ## non présent en 2005##
    P= _P.isf.droits_soc
    ''' parts ou actions détenues par les salariés et mandataires sociaux'''
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


def _patrimoine(res_princ, ac, forets, ruraux, grp_agr, bk, actions_sal, actions_conserv, cd, cf2, ce, autres_biens_meubles):
    # res_princ résidence principale
    # ac autres immeubles
    # bk autres biens  
    # cd droits sociaux de sociétés dans lesquelles vous avez exercez une fonction ou activité
    # ce autres valeurs mobilières
    # cf2  liquidités
    return autres_biens_meubles + cf2 + ce + res_princ + ac + forets + ruraux + grp_agr + bk + actions_sal + actions_conserv + cd

def _forf_mob(ef, patrimoine, _P):
    P=_P.isf.forf_mob
    return (ef != 0)*ef + (ef==0)*patrimoine*P.taux 
  
def _ass_isf(patrimoine, forf_mob, gh):
    return forf_mob + patrimoine - gh 
    
## calcul de l'impôt par application du barème ##

def _isf_iai(ass_isf, _P):
    bar = _P.isf.bareme
    bar.t_x()
    print "isf_iai"
    print bar.calc(ass_isf)
    return bar.calc(ass_isf)

## réductions pour personnes à charges ##
def _reduc_pac(nb_pac, nbH, _P):
    P= _P.isf.reduc_pac
    return nb_pac*P.reduc_1*(nb_pac-nbH)+ nb_pac*P.reduc_2*nbH  

## réductions pour investissements dans les PME ##
def _inv_pme(mt, ne, mv, nf, mx, na, _P):
    P= _P.isf.pme
    inv_dir_soc = mt*P.taux2 + ne*P.taux1
    holdings = mv*P.taux2+ nf*P.taux1
    fip = mx*P.taux1
    fcpi= na*P.taux1
    return holdings + fip + fcpi + inv_dir_soc

def _org_int_gen(nc, _P):
    P= _P.isf.pme
    return nc*P.taux2

def _mai(isf_iai, inv_pme, org_int_gen, reduc_pac, _P ) :
    '''
    montant de l'impôt avant imputation
    '''
    borne_max = _P.isf.pme.max
    return isf_iai - min_(inv_pme + org_int_gen, borne_max) - reduc_pac

  
## calcul du plafonnement ##
  
def _tot_impot(irpp, mai ):
    return -irpp + mai



def _revetproduits(sal_net, pen_net, rto_net, rfr_rvcm, fon, ric, rag, rpns_exon, rpns_pvct, rev_cap_lib, imp_lib, _P) :   # TODO: ric? benef indu et comm
    pt = sal_net + pen_net + rto_net + rfr_rvcm + ric + rag + rpns_exon + rpns_pvct + rev_cap_lib + imp_lib 
    # rev_cap et imp_lib pour produits soumis à prel libératoire- check ##
    ## def rev_exon et rev_etranger dans data? ##
    P= _P.isf.bouclier
    return pt*P.taux

def _plafonnement(tot_impot, revetproduits): 
    return tot_impot - revetproduits

def _limitationplaf (mai, plafonnement, _P):
    '''
    limitation du plafonnement
    '''
    P = _P.isf.plaf
    return (mai<= P.seuil1)*plafonnement + (P.seuil1 <= mai)*(mai <= P.seuil2)*min_(plafonnement, P.seuil1) + (mai >= P.seuil2)*min_(mai*P.taux, plafonnement)  
    
     
    
def _isfapresplafonnement(mai, limitationplaf):
    print 'isfapresplaf'
    print (mai - limitationplaf)
    return (mai - limitationplaf)
    
## rs est le montant des impôts acquittés hors de France ## 
## montant net à payer ##
def _isf(rs, mai, isfapresplafonnement, irpp):
    print 'irpp'
    print irpp
    print 'isf'
    print -(isfapresplafonnement - rs)*((-irpp)>0) + (mai-rs)*((-irpp)<=0)
    return -(isfapresplafonnement - rs)*((-irpp)>0) + (mai-rs)*((-irpp)<=0)
## avec indicatrice ## 




