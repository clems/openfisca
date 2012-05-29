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


def _nbinde2(agem, _option = {'agem' : ALL_MEN}):
    '''
    Number of household members
    'men'
    '''
    print ALL_MEN
    n1 = 0
    for ind in agem.iterkeys():
        n1 += 1*(floor(agem[ind]/12) >= 0) 
    
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


def _conf_fam(agem, activite, _option = {'agem': ALL_MEN}):
    '''
    Calcule le code de configuration du ménage 
    Code à 5 chiffres
        - premier chiffre   : 1 seul, 2 couple, 3 complexe
        - deuxième chiffre  : 0 ou 1 selon activité de l'homme
        - troisième chiffre : 0 ou 1 selon activité de la femme
        - quatrième chiffre : nombre d'enfant 0,1,2,3 (3 et plus)
    'men'
    '''
    
    pass
    
def _typmen15(agem, activite, _option = {'agem': ALL_MEN}):    
    pass
#TYPMEN15
#Type de ménage (15 postes)
#10 Personne seule active
#11 Personne seule inactive
#21 Famille monoparentale, parent actif
#22 Famille monoparentale, parent inactif et au moins un enfant actif
#23 Famille monoparentale, tous inactifs
#31 Couple sans enfant, 1 actif
#32 Couple sans enfant, 2 actifs
#33 Couple sans enfant, tous inactifs
#41 Couple avec enfant, 1 membre du couple actif
#42 Couple avec enfant, 2 membres du couple actif
#43 Couple avec enfant, couple inactif et au moins un enfant actif
#44 Couple avec enfant, tous inactif
#51 Autres ménages, 1 actif
#52 Autres ménages, 2 actifs ou plus
#53 Autres ménages, tous inactifs

# ddipl
#1 Diplôme supérieur
#3 Baccalauréat + 2 ans
#4 Baccalauréat ou brevet professionnel ou autre diplôme de ce niveau
#5 CAP, BEP ou autre diplôme de ce niveau
#6 Brevet des collèges
#7 Aucun diplôme ou CEP


# O non renseigné
# 1 Agriculture, sylviculture et pêche      
# 2 Industries agricoles
# 3 Industries des biens de consommation
# 4 Industrie automobile
# 5 Industries des biens d'équipement
# 6 Industries des biens intermédiaires
# 7 Energie
# 8 Construction
# 9 Commerce et réparations
# 10 Transports
# 11 Activités financières
# 12 Activités immobilières
# 13 Services aux entreprises
# 14 Services aux particuliers
# 15 Education, santé, action sociale
# 16 Administrations

  