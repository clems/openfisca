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
from numpy import (round, ceil, floor, maximum as max_, minimum as min_, 
                   logical_not as not_)
from france.data import QUIFAM, QUIMEN
from france.pfam import nb_enf

CHEF = QUIFAM['chef']
PART = QUIFAM['part']
ENFS = [QUIFAM['enf1'], QUIFAM['enf2'], QUIFAM['enf3'], QUIFAM['enf4'], QUIFAM['enf5'], QUIFAM['enf6'], QUIFAM['enf7'], QUIFAM['enf8'], QUIFAM['enf9'], ]

ALL = [x[1] for x in QUIMEN]

def _uc(agem, _option = {'agem': ALL}):
    '''
    Calcule le nombre d'unités de consommation du ménage avec l'échelle de l'insee
    'men'
    '''
    uc_adt = 0.5
    uc_enf = 0.3
    uc = 0.5
    for agm in agem.itervalues():
        age = floor(agm/12)
        adt = (15 <= age) & (age <= 150)
        enf = (0  <= age) & (age <= 14)
        uc += adt*uc_adt + enf*uc_enf
    return uc

def _typ_men(isol, af_nbenf):
    '''
    type de menage
    'men'
    TODO: prendre les enfants du ménages et non ceux de la famille
    '''
    _0_kid = af_nbenf == 0
    _1_kid = af_nbenf == 1
    _2_kid = af_nbenf == 2
    _3_kid = af_nbenf >= 3
    
    return (0*(isol & _0_kid) + # Célibataire
            1*(not_(isol) & _0_kid) + # Couple sans enfants
            2*(not_(isol) & _1_kid) + # Couple un enfant
            3*(not_(isol) & _2_kid) + # Couple deux enfants
            4*(not_(isol) & _3_kid) + # Couple trois enfants et plus
            5*(isol & _1_kid) + # Famille monoparentale un enfant
            6*(isol & _2_kid) + # Famille monoparentale deux enfants
            7*(isol & _3_kid) ) # Famille monoparentale trois enfants et plus
            
    
def _revdisp(rev_trav, pen, rev_cap, ir_lps, psoc, ppe_cumul_rsa_act, impo):
    '''Revenu disponible'''
    return rev_trav + pen + rev_cap + ir_lps + psoc + ppe_cumul_rsa_act + impo

def _rev_trav(sal_net, rag, ric, rnc):
    '''Revenu du travail'''
    return sal_net + rag + ric + rnc

def _pen(chonet, rstnet, alr, alv, rto):
    '''Pensions'''
    return chonet + rstnet + alr + alv + rto

def _chonet(cho, csgchoi, crdscho):
    '''Chômage net'''
    return cho + csgchoi + crdscho

def _rstnet(rst, csgrsti, crdsrst):
    '''Retraites nettes'''
    return rst + csgrsti + crdsrst

def _cotsoc_bar(csg_cap_bar, prelsoc_cap_bar, crds_cap_bar):
    '''Cotisations sociales sur les revenus du capital imposés au barème'''
    return csg_cap_bar + prelsoc_cap_bar + crds_cap_bar

def _cotsoc_lib(csg_cap_lib, prelsoc_cap_lib, crds_cap_lib):
    '''Cotisations sociales sur les revenus du capital soumis au prélèvement libératoire'''
    return csg_cap_lib + prelsoc_cap_lib + crds_cap_lib

def _rev_cap(fon, rev_cap_bar, cotsoc_bar, rev_cap_lib, cotsoc_lib, imp_lib, rac):
    '''Revenus du patrimoine'''
    return fon + rev_cap_bar + cotsoc_bar + rev_cap_lib + cotsoc_lib + imp_lib + rac

def _psoc(pfam, mini, logt):
    '''Prestations sociales'''
    return pfam + mini + logt

def _pfam(af, cf, ars, aeeh, paje, asf, crds_pfam):
    ''' Prestations familiales '''
    return af + cf + ars + aeeh + paje + asf + crds_pfam

def _paje(paje_base, paje_nais, paje_clca, paje_colca, paje_clmg):
    ''' Prestation d'accueil du jeune enfant '''
    return paje_base + paje_nais + paje_clca + paje_colca + paje_clmg

def _mini(mv, aah, caah, asi, rsa, aefa, api):
    ''' Minima sociaux '''
    return mv + aah + caah + asi + rsa + aefa + api

def _logt(apl, als, alf, alset, crds_lgtm):
    ''' Prestations logement '''
    return apl + als + alf + alset + crds_lgtm

def _impo(irpp):
    '''Impôts directs'''
    return irpp
