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
from numpy import minimum as min_, maximum as max_, logical_not as not_, zeros
from france.data import year

taille = 0

def niches(creimp, accult, percvm, direpa, mecena, prlire, aidper,
           quaenv, drbail, garext, preetu, saldom, inthab, assloy, 
           autent, acqgpl, divide, aidmob, jeunes):
    niches = []
    if year == 2002:
        niches = [creimp + accult + prlire + aidper + acqgpl + drbail]
    elif year == 2003:
        niches = [creimp + accult + mecena + prlire + aidper + acqgpl + drbail]
    elif year == 2004:
        niches = [creimp + accult + mecena + prlire + aidper + acqgpl + drbail]
    elif year == 2005:
        niches = [creimp + divide + direpa + accult + mecena + prlire + aidper +
                  quaenv + acqgpl + drbail + garext + preetu + assloy + aidmob + jeunes]
    elif year == 2006:
        niches = [creimp + divide + direpa + accult + mecena + prlire + aidper +
                  quaenv + acqgpl + drbail + garext + preetu + assloy + aidmob + jeunes]
    elif year == 2007:
        niches = [creimp + divide + direpa + accult + mecena + prlire + aidper +
                  quaenv + acqgpl + drbail + garext + preetu + saldom + inthab + assloy + 
                  aidmob + jeunes]
    elif year == 2008:
        niches = [creimp + divide + direpa + accult + mecena + prlire + aidper +
                  quaenv + drbail + garext + preetu + saldom + inthab + assloy + aidmob + 
                  jeunes]
    elif year == 2009:
        niches = [creimp + divide + direpa + accult + mecena + prlire + aidper +
                  quaenv + drbail + garext + preetu + saldom + inthab + assloy + autent]
    elif year == 2010:
        niches = [creimp + accult + percvm + direpa + mecena + prlire + aidper +
                  quaenv + drbail + garext + preetu + saldom + inthab + assloy + 
                  autent]
    return niches

def _nb_pac2(nbF, nbJ, nbR, nbH):
    return nbF + nbJ + nbR + nbH/2

def _creimp(f2ab, f8ta, f8tb, f8tf, f8tg, f8th, f8tc, f8td, f8te, f8to, f8tp, f8uz, f8tz, f8wa, f8wb, f8wc, f8wd, f8we, f8wr, f8ws, f8wt, f8wu, f8wv, f8wx, f8wy, P, table):
    '''
    Avoir fiscaux et crédits d'impôt
    '''
    
    if year == 2002:        
        return (f2ab + f8ta + f8tb + f8tc + f8td + f8te - f8tf + f8tg + f8th)

    elif year == 2003:
        return (f2ab + f8ta + f8tb + f8tc + f8td + f8te - f8tf + f8tg + f8th + f8to - f8tp)

    elif year == 2004:
        return (f2ab + f8ta + f8tb + f8tc + f8td + f8te - f8tf + f8tg + f8th + f8to - f8tp + f8uz + f8tz)
        
    elif year == 2005:
        return (f2ab + f8ta + f8tb + f8tc + f8td + f8te - f8tf + f8tg + f8th + f8to - f8tp + f8uz + f8tz + f8wa + f8wb + f8wc + f8we)

    elif year == 2006:
        return (f2ab + f8ta + f8tb + f8tc + f8te - f8tf + f8tg + f8th
                   + f8to - f8tp + f8uz + f8tz + f8wa + f8wb + f8wc + f8wd + f8we + f8wr + f8ws + f8wt + f8wu)

    elif year == 2007:
        return (f2ab + f8ta + f8tb + f8tc + f8te - f8tf + f8tg + f8th
                   + f8to - f8tp + f8uz + f8tz + f8wa + f8wb + f8wc + f8wd + f8wr + f8ws + f8wt + f8wu + f8wv + f8wx)
        
    elif year == 2008:
        return (f2ab + f8ta + f8tb + f8tc + f8te - f8tf + f8tg + f8th
                   + f8to - f8tp + f8uz + f8tz + f8wa + f8wb + f8wc + f8wd + f8we + f8wr + f8ws + f8wt + f8wu + f8wv + f8wx)

    elif year == 2009:
        return (f2ab + f8ta + f8tb - f8tf + f8tg + f8th + f8to - f8tp 
                   + f8uz + f8tz + f8wa + f8wb + f8wd + f8we + f8wr + f8ws + f8wt + f8wu + f8wv + f8wx + f8wy)

    elif year == 2010:
        return (f2ab + f8ta + f8tb + f8tc - f8tf + f8tg + f8th + f8to - f8tp + f8uz + f8tz + f8wa + f8wb + f8wd + f8we + f8wr + f8wt + f8wu + f8wv)

def _divide(marpac, f2dc, f2gr, _P):
    '''
    Crédit d'impôt dividendes
    '''    
    P = _P.ir.credits_impots.divide
    
    max1 = P.divide.max*(marpac+1)
    return min_(P.divide.taux*(f2dc + f2gr), max1)

def _percvm():
    '''
    Crédit d’impôt pertes sur cessions de valeurs mobilières (3W)
    '''
    return zeros(taille)

def _direpa(f2bg):
    '''
    Crédit d’impôt directive « épargne » (case 2BG)
    '''
    return f2bg

def _accult(f7uo, _P):
    '''
    Acquisition de biens culturels (case 7UO)
    '''
    P = _P.ir.credits_impots.accult
    return P.taux*f7uo

def _mecena(f7us):
    '''
    Mécénat d'entreprise (case 7US)
    '''
    return f7us

def _prlire():
    '''
    Prélèvement libératoire à restituer (case 2DH)
    '''
    return zeros(taille)

def _quaenv(marpac, nb_pac2, f7wf, f7wh, f7wk, f7wq, f7sb, f7sd, f7se, f7sh, f7wg, f7sc, _P):
    '''
    Crédits d’impôt pour dépenses en faveur de la qualité environnementale 
    (cases 7WF, 7WH, 7WK, 7WQ, 7SB, 7SD, 7SE et 7SH)
    '''
    P = _P.ir.credits_impots.quaenv
     
    n = nb_pac2
    if year == 2005:
        max0 = P.max*(1+marpac) + P.pac1*(n>=1) + P.pac2*(n>=2) + P.pac2*(max_(n-2,0))
                
    elif year >= 2006:
        max0 = P.max*(1+marpac) + P.pac1*n
    
    if year == 2005:
        max1 = max_(0, max0 - f7wf)
        max2 = max_(0, max1 - f7wg)
        return (P.taux_wf*min_(f7wf, max0) +
                P.taux_wg*min_(f7wg, max1) +
                P.taux_wh*min_(f7wh, max2) )

    elif year in (2006, 2007, 2008):
        max1 = max_(0, max0 - f7wf)
        max2 = max_(0, max1 - f7wg)
        max3 = max_(0, max2 - f7wh)
        return (P.taux_wf*min_(f7wf, max0) +
                P.taux_wg*min_(f7wg, max1) +
                P.taux_wh*min_(f7wh, max2) +
                P.taux_wq*min_(f7wq, max3) )

    elif year == 2009:
        max1 = max_(0, max0 - f7wf)
        max2 = max_(0, max1 - f7se)
        max3 = max_(0, max2 - f7wk)
        max4 = max_(0, max3 - f7sd)
        max5 = max_(0, max4 - f7wg)
        max6 = max_(0, max5 - f7sc)
        max7 = max_(0, max6 - f7wh)
        return (P.taux_wf*min_(f7wf, max0) +
                P.taux_se*min_(f7se, max1) +
                P.taux_wk*min_(f7wk, max2) +
                P.taux_sd*min_(f7sd, max3) +
                P.taux_wg*min_(f7wg, max4) +
                P.taux_sc*min_(f7sc, max5) +
                P.taux_wh*min_(f7wh, max6) +
                P.taux_sb*min_(f7sb, max7) )

    elif year == 2010:
        max1 = max_(0, max0 - f7wf)
        max2 = max_(0, max1 - f7se)
        max3 = max_(0, max2 - f7wk)
        max4 = max_(0, max3 - f7sd)
        max5 = max_(0, max4 - f7wh)
        max6 = max_(0, max5 - f7sb)
        max7 = max_(0, max6 - f7wq)
        return (P.taux_wf*min_(f7wf, max0) +
                P.taux_se*min_(f7se, max1) +
                P.taux_wk*min_(f7wk, max2) +
                P.taux_sd*min_(f7sd, max3) +
                P.taux_wh*min_(f7wh, max4)+
                P.taux_sb*min_(f7sb, max5) +
                P.taux_wq*min_(f7wq, max6) +
                P.taux_sh*min_(f7sh, max7) )

def _aidper(marpac, nb_pac2, f7wf, f7wi, f7wj, f7wl, f7sf, f7si, nb_pac2, _P):
    '''
    Crédits d’impôt pour dépenses en faveur de l’aide aux personnes 
    (cases 7WI, 7WJ, 7WL et 7SF).
    '''
    P = _P.ir.credits_impots.aidper

    n = nb_pac2
    if year <= 2005:
        max0 = P.max*(1+marpac) + P.pac1*(n>=1) + P.pac2*(n>=2) + P.pac2*(max_(n-2,0))
               
    elif year >= 2006:
        max0 = P.max*(1+marpac) + P.pac1*n

    if year in (2002,2003):
        return P.taux_wi*min_(f7wi, max0) # TODO enfant en résidence altérnée
    elif year <= 2009:
        max1 = max_(0, max0 - f7wj)
        return (P.taux_wj*min_(f7wj, max0) +
                P.taux_wi*min_(f7wi, max1) )
    elif year == 2010:
        max1 = max_(0, max0 - f7wl)
        max2 = max_(0, max1 - f7sf)
        max3 = max_(0, max2 - f7wj)
        return (P.taux_wl*min_(f7wl, max0) +
                P.taux_sf*min_(f7sf, max1) +
                P.taux_wj*min_(f7wj, max2) +
                P.taux_wi*min_(f7si, max3) )

def _acqgpl(f7up, f7uq, _P):
    '''
    Crédit d'impôt pour dépense d'acquisition ou de transformation d'un véhicule GPL ou mixte
    '''
    P = _P.ir.credits_impots.acqgpl

    if 2002 <= year <= 2007:
        return f7up*P.mont_up + f7uq*P.acqgpl.mont_uq

def _drbail(f4tq, _P):
    '''
    Crédit d’impôt représentatif de la taxe additionnelle au droit de bail (case 4TQ)
    '''
    P = _P.ir.credits_impots.drbail
    return P.taux*f4tq

def _garext(f4ga, f4gb, f4gc, f4ge, f4gf, f4gg, _P, table):
    '''
    Frais de garde des enfants à l’extérieur du domicile (cases 7GA à 7GC et 7GE à 7GG)
    '''
    P = _P.ir.credits_impots.garext
    max1 = P.max
    
    
    return P.garext.taux*(min_(f4ga, max1) + 
                          min_(f4gb, max1) +
                          min_(f4gc, max1) +
                          min_(f4ge, max1/2) +
                          min_(f4gf, max1/2) +
                          min_(f4gg, max1/2))

def _preetu(f7uk, f7vo, f7td, _P):
    '''
    Crédit d’impôt pour souscription de prêts étudiants (cases 7UK, 7VO et 7TD)
    '''
    P = _P.ir.credits_impots.preetu
    
    
    if   year == 2005:  max1 = P.max
    elif year >= 2006:  max1 = P.max*(1+f7vo)
    if year in (2005,2006,2007):
        return P.taux*min_(f7uk, max1)
    elif year >=2008:
        return P.taux*min_(f7uk, P.max) + P.taux*min_(f7td, max1)

def _saldom(nb_pac2, f7db, f7dg, f7dl, f7dq, _P, table):
    '''
    Crédit d’impôt emploi d’un salarié à domicile (cases 7DB, 7DG)
    '''
    P = _P.ir.credits_impots.saldom
    
    isinvalid = f7dg
    
    if year in (2007,2008):
        nbpacmin = nb_pac2 + f7dl
        maxBase = P.max1
        maxDuMaxNonInv = P.max2
        maxNonInv = min_(maxBase + P.pac*nbpacmin, maxDuMaxNonInv)
        maxEffectif = maxNonInv*not_(isinvalid) + P.max3*isinvalid
        
    elif year in (2009, 2010):
        annee1 = f7dq
        nbpacmin = nb_pac2 + f7dl
        maxBase = P.max1*not_(annee1) + P.max1_1ereAnnee*annee1
        maxDuMaxNonInv = P.max2*not_(annee1) + P.max2_1ereAnnee*annee1
        maxNonInv = min_(maxBase + P.pac*nbpacmin, maxDuMaxNonInv)
        maxEffectif = maxNonInv*not_(isinvalid) + P.max3*isinvalid
            
    return P.taux*min_(f7db, maxEffectif)

def _inthab(marpac, nb_pac2, caseP, caseF, nbG, nbR, f7vw, f7vx, f7vy, f7vz, _P):
    '''
    Crédit d’impôt intérêts des emprunts pour l’habitation principale (cases 7VW, 7VX, 7VY et 7VZ)
    '''
    P = _P.ir.credits_impots.inthab
        
    invalide = caseP |caseF | (nbG!=0) | (nbR!=0)
    nb = nb_pac2
    max0 = P.max*(marpac+1)*(1+invalide) + nb*P.add

    if year == 2007:
        return zeros(taille)
    if year == 2008:  
        max1 = min_(max0 - f7vy, 0)
        return (P.taux1*min_(f7vy, max0) + 
                P.taux3*min_(f7vz, max1) )
    if year == 2009:
        max1 = min_(max0 - f7vx, 0)
        max2 = min_(max1 - f7vy, 0)
        return (P.taux1*min_(f7vx, max0) + 
                P.taux1*min_(f7vy, max1) + 
                P.taux3*min_(f7vz, max2) )
    if year == 2010:
        max1 = min_(max0 - f7vx, 0)
        max2 = min_(max1 - f7vy, 0)
        max3 = min_(max2 - f7vw, 0)
        return (P.inthab.taux1*min_(f7vx, max0) + 
                P.inthab.taux1*min_(f7vy, max1) + 
                P.inthab.taux2*min_(f7vw, max2) + 
                P.inthab.taux3*min_(f7vz, max3) )

def _assloy(f4bf, P):
    '''
    Crédit d’impôt primes d’assurance pour loyers impayés (case 4BF)
    '''
    return P.assloy.taux*f4bf

def _autent( P):
    '''
    Auto-entrepreneur : versements d’impôt sur le revenu (case 8UY)
    '''
    return zeros(taille)

def _aidmob(f1ar, f1br, f1cr, f1dr, f1er, P):
    '''
    Crédit d'impôt aide à la mobilité
    '''
    
    return (f1ar + f1br + f1cr + f1dr + f1er)*P.aidmob.montant

def _jeunes( P, table):
    '''
    Crédit d'impôt en faveur des jeunes
    '''
    return  zeros(taille) # D'après  le document num. 2041 GY
                                # somme calculée sur formulaire 2041
