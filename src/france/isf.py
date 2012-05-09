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


## immeubles non bâtis, part de groupement ##
def _forets(bc):
    return bc*0.25
 
# def fractsup ##
def _ruraux(be, _P): 
    ''' bien ruraux loués à long terme'''
    seuil = _P.isf.nonbat.seuil
    return min_(be, seuil)*0.25 + max_(be-seuil,0)*0.5  
 
def _grp_agr(bh, _P):
    '''part de groupements forestiers- agricoles fonciers'''
    seuil = _P.isf.nonbat.seuil
    return min_(bh, seuil)*0.25 + max_(bh-seuil,0)*0.5  

## droits sociaux- valeurs mobilières- liquidités- autres meubles ##

def _actions_sal(cl2): ## non présent en 2005##
    ''' parts ou actions détenues par les salariés et mandataires sociaux'''
    return  cl2*0.25  # TODO: inclure dans param
## 0,25 en 2011, 0,5 en 2005##

def _actions_conserv(cb):
    ''' parts ou actions de sociétés avec engagement de 6 ans conservation minimum'''
    return cb*0.25 # TODO: inclure dans param

def _autres_bien_meubles(cg, co):
    '''
    autres bien meubles dont contrat d'assurance vie
    '''
    return cg 

## pas besoin d'ajouter le montant des exonérations ##

def _patrimoine(ab, ac, forets, ruraux, grp_agr, bk, actions_sal, actions_conserv, droits_soc, autres_val_mob, liquidites, autres_biens_meubles):
    # ab résidence principale
    # ac autres immeubles
    # cd droits sociaux de sociétés dans lesquelles vous avez exercez une fonction ou activité
    # ce autres valeurs mobilières
    # cf  liquidités
    return autres_biens_meubles + liquidites + autres_val_mob + ab + ac + forets + ruraux + grp_agr + bk + actions_sal + actions_conserv + droits_soc

def _forf_mob(ef, patrimoine):
    return (ef != 0)*ef + (ef==0)*patrimoine*0.05 # TODO: inclure dans param
  
def _ass_isf(patrimoine, forf_mob, gh):
    return forf_mob + patrimoine - gh 
    
## calcul de l'impôt par application du barème ##

def _isf_iai(ass_isf, _P):
    bar = _P.isf.bareme
    bar.t_x()
    return bar.calc(ass_isf)

## réductions pour personnes à charges ##
def _reduc_pac(nb_pac, nbH):
    return nb_pac*150*(nb_pac-nbH)+ nb_pac*75*nbH  # TODO: inclure dans param

## réductions pour investissements dans les PME ##
def _inv_pme(mt, ne, mv, nf, mx, na):
    inv_dir_soc = mt*0.75 + ne*0.5
    holdings = mv*0.75 + nf*0.5
    fip = mx*0.5
    fcpi= na*0.5
    return holdings + fip + fcpi + inv_dir_soc

def _org_int_gen(nc):
    return nc*0.75

def _mai(isf_iai, inv_pme, org_int_gen, reduc_pac, _P ) :
    '''
    montant de l'impôt avant imputation
    '''
    borne_max = _P.isf.pme.max
    return isf_iai - min_(inv_pme + org_int_gen, borne_max) - reduc_pac
  
## calcul du plafonnement ##
  
def _tot_impot(irpp, mai ):
    return irpp + mai

def _revetproduits(sal_net, pen_net, rto_net, rfr_rvcm, fon) :   # TODO:  à vérifier !
    pt = sal_net + pen_net + rto_net + rfr_rvcm # TODO: à finir
    return pt*0.85 

def _plafonnement(totaldesimpots, revetproduits): 
    return totaldesimpots - revetproduits

def _limitationplaf (mai, plafonnement, _P):
    '''
    limitation du plafonnement
    '''
    P = _P.isf.plaf
    return (mai<= P.seuil1)*plafonnement + (P.seuil1 <= mai <= P.seuil2)*min_(_plafonnement, P.seuil1) + (mai >= P.seuil2)*min_(mai*0.5, _plafonnement)  
    
     
    
def _isfapresplafonnement(_mai, _limitationplaf):
        return _mai - _limitationplaf
    

## montant net à payer ##
def _isf(rs, mai, isfapresplafonnement):
    return _isfapresplafonnement - rs 
    
## 



