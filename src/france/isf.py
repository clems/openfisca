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

def _isf(assiette_isf, _P):
    bar = _P.isf.bareme
    return bar.calc(assiette_isf)



def _assiette_isf(patrimoine, abat,):
    pass

## situation de famille ##
def _nb_adult(marpac, celdiv, veuf):
    return 2*marpac + 1*(celdiv | veuf)

def _nb_pac(nbF, nbJ, nbR):
    return nbF + nbJ + nbR
        
def _marpac(statmarit):
    '''
    Marié (1) ou Pacsé (5)
    'foy'
    '''
    return (statmarit == 1) | (statmarit == 5)

def _celdiv(statmarit):
    '''
    Célibataire (2) ou divorcé (3)
    'foy'
    '''
    return (statmarit == 2) | (statmarit == 3)

def _veuf(statmarit):
    '''
    Veuf (4)
    'foy'
    '''
    return statmarit == 4

def _jveuf(statmarit):
    '''
    Jeune Veuf
    'foy'
    '''
    return statmarit == 6

def 

## qualification de biens professionnels exonérés ##



## immeubles bâtis- Annexe 1 ##
 def résidenceprincipale= ab
 def autresimmeubles= ac

## immeubles non bâtis, part de groupement ##
 def boisforêts= bc
 return bc*0.25= bd
 
 def bienrurauxllt= be 
 ''' bien ruraux loués à long terme'''
 return be-fractsup ## aller chercher fractsup- en fonction de la date, dans les parzm? ##
 if be-fractsup<=0 
 return bf= 0.25*be
 else 
 return bf+bg= (be-fractsup)*0.50+ fractsup*0.25
 
 def pgfagaf= bh
 '''part de groupements forestiers- agricoles fonciers'''
 return be-fractsup
 if bh-fractsup<=0 
 return bi= 0.25*bh
 else 
 return bi+bj=(bh-fractsup)*0.50+ fractsup*0.25


def autresbiens= bk
''' autres biens '''
    
## droits sociaux- valeurs mobilières- liquidités- autres meubles ##

def padsms= cl2
''' parts ou actions détenues par les salariés et mandataires sociaux'''
    return cm= cl*0.25

def pasec= cb 
''' parts ou actions de sociétés avec engagement de 6 ans conservation minimum'''
    return cc= cb*0.25

def dssfa= cd 
''' droits sociaux de sociétés dans lesquelles vous avez exercez une fonction ou activité'''
    return cd

def autresvaleursmob= ce
'''autres valeurs mobilières'''
    return ce

def liquidités= cf
''' liquidités'''
    return cf

def autresbienmeubles= cg
''' autres bien meubles dont contrat d'assurance vie'''
    return co 
    return cg ## comment s'intercale les deux, voir annexe##

## pas besoin d'ajouter le montant des exonérations ##

def patrimoine = ab+ ac+ bd+ bf+ bg + bi + bj + bk + cm + cc + cd+ ce + cf+ cg 
 def forfaitmobilier= ef
 def totpatrimoine = de+ ef 
 
 ## passifs et autres réductions ## 
  def gh
  ''' passifs et autres réductions'''
      
 def assiette-isf
 return totpatrimoine- gh 
    

## calcul de l'impôt par application du barème ##

## réductions pour personnes à charges ##
 def reduc (nb_pac):
 return nb_pac * 150
 def reduc2 (nb? )= ## garde alternée##
 return nb*75
 
 def impareduc
  calc.bar(assiette-isf)
  
  
  ## calcul du plafonnement ##
  
 






## imputation de l'impôt sur la fortune acquitté hors de France) ##



## inclure les exonérations##
## bouclier fiscal##


