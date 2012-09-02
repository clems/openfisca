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
from numpy import  floor, arange, array, where 
from france.data import QUIMEN

ALL_MEN = [x[1] for x in QUIMEN]
PREF = QUIMEN['pref']
CREF = QUIMEN['cref']
ENFS = [QUIMEN['enf1'], QUIMEN['enf2'], QUIMEN['enf3'], QUIMEN['enf4'], QUIMEN['enf5'], QUIMEN['enf6'], QUIMEN['enf7'], QUIMEN['enf8'], QUIMEN['enf9'], ]

def _nbinde(agem, _option = {'agem' : ALL_MEN}):
    '''
    Number of household members
    'men'
    Values range between 1 and 6 for 6 members or more
    '''
    n1 = 0
    for ind in agem.iterkeys():
        n1 += 1*(floor(agem[ind]) >= 0) 
    
    n2 = where( n1 >=6, 6, n1)
    
    return n2


def _ageq(agem):
    '''
    Calcule la tranche d'âge quinquennal
    moins de 25 ans : 0
    25 à 29 ans     : 1
    30 à 34 ans     : 2
    35 à 39 ans     : 3
    40 à 44 ans     : 4
    45 à 49 ans     : 5
    50 à 54 ans     : 6
    55 à 59 ans     : 7
    60 à 64 ans     : 8
    65 à 69 ans     : 9
    70 à 74 ans     :10
    75 à 79 ans     :11
    80 ans et plus  :12
    'ind'
    '''
    age = floor(agem/12)
    tranche = array([ (age >= ag) for ag in arange(25,5,81) ]).sum(axis=0) 
    return tranche


def _nb_ageq0(agem, _option = {'agem': ALL_MEN}):
    '''
    Calcule le nombre d'individus dans chaque tranche d'âge quinquennal (voir ageq)
    'men'
    '''
    ag1 = 0
    nb  = 0
    for agm in agem.itervalues():   
        age = floor(agm/12) 
        nb   += (ag1 <= age) & (age <= (ag1+4))
    return nb

def _cohab(quimen, _option = {'quimen':[CREF]}):
    '''
    Indicatrice de vie en couple
    '''
    return 1 * (quimen[CREF] == 1)

def _act_cpl(activite, cohab, _option = {'activite':[PREF, CREF]}):
    '''
    Nombre d'actifs parmi la personne de référence et son conjoint
    '''
    return 1*(activite[PREF] <= 1) + 1*(activite[CREF] <= 1)*cohab

def _act_enf(activite, _option = {'activite': ENFS}):
    '''
    Nombre de membres actifs du ménage autre que la personne de référence ou son conjoint
    '''
    res = 0
    for act in activite.itervalues():
        res += 1*(act <= 1) 
    return res
    
    
#def _conf_fam(agem, activite, quimen, _option = {'quimen':[CREF], 'actvite': [PREF,CREF], 'agem': ALL_MEN}):
#    '''
#    Calcule le code de configuration du ménage 
#    Code à 4 chiffres
#        - premier chiffre   : 1 seul, 2 couple, 3 complexe
#        - deuxième chiffre  : 0 ou 1 selon activité de l'homme
#        - troisième chiffre : 0 ou 1 selon activité de la femme
#        - quatrième chiffre : nombre d'enfant 0,1,2,3 (3 et plus)
#    'men'
#    '''
#    # présence d'un couple  dans le ménage
#    code1 = 1000*(1 + 1 * (quimen[CREF] == 1))  # TODO gestion des ménages complexes 
#    code2 = activite
#    code3 = activite 
#    code4 = 0
    
    
def _typmen15(typmen15, nbindebis, cohab, act_cpl, cplx, act_enf):
    '''
    Type de ménage en 15 modalités
    1 Personne seule active
    2 Personne seule inactive
    3 Familles monoparentales, parent actif
    4 Familles monoparentales, parent inactif et au moins un enfant actif
    5 Familles monoparentales, tous inactifs
    6 Couples sans enfant, 1 actif
    7 Couples sans enfant, 2 actifs
    8 Couples sans enfant, tous inactifs
    9 Couples avec enfant, 1 membre du couple actif
    10 Couples avec enfant, 2 membres du couple actif
    11 Couples avec enfant, couple inactif et au moins un enfant actif
    12 Couples avec enfant, tous inactifs
    13 Autres ménages, 1 actif
    14 Autres ménages, 2 actifs ou plus
    15 Autres ménages, tous inactifs
    '''
    res = 0 + (
    1 * ( (nbindebis == 1) & (cohab == 0) & (act_cpl == 1)) + #  Personne seule active 
    2 * ( (nbindebis == 1) & (cohab == 0) & (act_cpl == 0)) + # Personne seule inactive
    3 * ( (nbindebis > 1)  & (cohab == 0) & (act_cpl == 1)) + # Familles monoparentales, parent actif
    4 * ( (nbindebis > 1)  & (cohab == 0) & (act_cpl == 0) & (act_enf >= 1) ) + # Familles monoparentales, parent inactif et au moins un enfant actif
    5 * ( (nbindebis > 1)  & (cohab == 0) & (act_cpl == 0) & (act_enf == 0) ) + # Familles monoparentales, tous inactifs
    6 * ( (nbindebis == 2) & (cohab == 1) & (act_cpl == 1) ) +   # Couples sans enfant, 1 actif
    7 * ( (nbindebis == 2) & (cohab == 1) & (act_cpl == 2) ) +   # Couples sans enfant, 2 actifs
    8 * ( (nbindebis == 2)  & (cohab == 1) & (act_cpl == 0) ) +   # Couples sans enfant, tous inactifs
    9 * ( (nbindebis > 2)  & (cohab == 1) & (act_cpl == 1) ) +   # Couples avec enfant, 1 membre du couple actif
    10 * ( (nbindebis > 2)  & (cohab == 1) & (act_cpl == 2) ) +  # Couples avec enfant, 2 membres du couple actif
    11 * ( (nbindebis > 2)  & (cohab == 1) & (act_cpl == 0) & (act_enf >= 1)) + # Couples avec enfant, couple inactif et au moins un enfant actif
    12 * ( (nbindebis > 2)  & (cohab == 1) & (act_cpl == 0) & (act_enf == 0)) + # Couples avec enfant, tous inactifs
    13 * ( (cplx == 1 ) & ( (act_cpl + act_enf) == 1) ) +      # Autres ménages, 1 actif
    14 * ( (cplx == 1 )  & ( (act_cpl + act_enf) >= 1) ) +     # Autres ménages, 2 actifs ou plus
    15 * ( (cplx == 1 )  & ( (act_cpl + act_enf) == 0) )  )     # Autres ménages, tous inactifs
    
    ratio = (( (typmen15!=res)*(typmen15<=12)).sum())/((typmen15<=12).sum())
    print ratio
    return res


#TYPMEN15
#Type de ménage (15 postes)
#1 Personne seule active
#2 Personne seule inactive
#3 Famille monoparentale, parent actif
#4 Famille monoparentale, parent inactif et au moins un enfant actif
#5 Famille monoparentale, tous inactifs
#6 Couple sans enfant, 1 actif
#7 Couple sans enfant, 2 actifs
#8 Couple sans enfant, tous inactifs
#9 Couple avec enfant, 1 membre du couple actif
#10 Couple avec enfant, 2 membres du couple actif
#11 Couple avec enfant, couple inactif et au moins un enfant actif
#12 Couple avec enfant, tous inactif
#13 Autres ménages, 1 actif
#14 Autres ménages, 2 actifs ou plus
#15 Autres ménages, tous inactifs
