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

from core.description import ModelDescription
from core.columns import IntCol, EnumCol, BoolCol, AgesCol, FloatCol
from core.utils import Enum

QUIFOY = Enum(['vous', 'conj', 'pac1','pac2','pac3','pac4','pac5','pac6','pac7','pac8','pac9'])
QUIFAM = Enum(['chef', 'part', 'enf1','enf2','enf3','enf4','enf5','enf6','enf7','enf8','enf9'])
QUIMEN = Enum(['pref', 'cref', 'enf1','enf2','enf3','enf4','enf5','enf6','enf7','enf8','enf9'])
CAT    = Enum(['noncadre', 'cadre', 'fonc'])


class InputTable(ModelDescription):
    '''
    Socio-economic data
    Donnée d'entrée de la simulation à fournir à partir d'une enquète ou 
    à générer avec un générateur de cas type
    '''
    noi = IntCol()

    idmen   = IntCol() # 600001, 600002,
    idfoy   = IntCol() # idmen + noi du déclarant
    idfam   = IntCol() # idmen + noi du chef de famille

    quimen  = EnumCol(QUIMEN)
    quifoy  = EnumCol(QUIFOY)
    quifam  = EnumCol(QUIFAM)
    
    type_sal = EnumCol(CAT)
    
    sali = IntCol() #(f1aj, f1bj, f1cj, f1dj, f1ej)
    choi = IntCol() # (f1ap, f1bp, f1cp, f1dp, f1ep)
    rsti = IntCol() # (f1as, f1bs, f1cs, f1ds, f1es)
    fra = IntCol() # (f1ak, f1bk, f1ck, f1dk, f1ek)

    alr = IntCol() # (f1ao, f1bo, f1co, f1do, f1eo)
    
    hsup = IntCol()  # f1au
    inv = BoolCol(label = u'invalide')
    alt = BoolCol(label = u'garde alternée')
    cho_ld = BoolCol(label = 'chômeur de longue durée') # (f1ai, f1bi, f1ci, f1di, f1ei)
    ppe_tp_sa = BoolCol() # (f1ax, f1bx, f1cx, f1dx, f1qx)
    ppe_tp_ns = BoolCol() # (f5nw, f5ow, f5pw)
    ppe_du_sa = IntCol() # (f1av, f1bv, f1cv, f1dv, f1qv)
    ppe_du_ns = IntCol() # (f5nv, f5ov, f5pv)
    jour_xyz = IntCol(default = 360)
    age = AgesCol(label = u"âge")
    agem = AgesCol(label = u"âge (en mois)")
    
    zone_apl = EnumCol(label = u"zone apl", default = 2, unit= 'menage')
    loyer = IntCol(unit='menage') # Loyer mensuel
    so = EnumCol(label = u"statut d'occupation",
                  enum = Enum([u"Non renseigné",
                               u"Accédant à la propriété",
                               u"Propriétaire (non accédant) du logement",
                               u"Locataire d'un logement HLM",
                               u"Locataire ou sous-locataire d'un logement loué vide non-HLM",
                               u"Locataire ou sous-locataire d'un logement loué meublé ou d'une chambre d'hôtel",
                               u"Logé gratuitement par des parents, des amis ou l'employeur"]), unit='menage')
    activite = IntCol()
    boursier = BoolCol()
    code_postal = IntCol(unit='menage')
    
    statmarit = IntCol(default = 2)
    
    nbR = IntCol(unit= 'foyer')
    nbJ = IntCol(unit= 'foyer')
    nbI = IntCol(unit= 'foyer')
    nbH = IntCol(unit= 'foyer')
    nbG = IntCol(unit= 'foyer')
    nbF = IntCol(unit= 'foyer')
    nbN = IntCol(unit= 'foyer')
    
    caseE = BoolCol(unit= 'foyer')
    caseF = BoolCol(unit= 'foyer')
    caseG = BoolCol(unit= 'foyer')
    caseH = IntCol(unit= 'foyer')
    caseK = BoolCol(unit= 'foyer')
    caseL = BoolCol(unit= 'foyer')
    caseN = BoolCol(unit= 'foyer')
    caseP = BoolCol(unit= 'foyer')
    caseS = BoolCol(unit= 'foyer')
    caseT = BoolCol(unit= 'foyer')
    caseW = BoolCol(unit= 'foyer')
    
    # Rentes viagères
    f1aw = IntCol(unit= 'foyer')
    f1bw = IntCol(unit= 'foyer')
    f1cw = IntCol(unit= 'foyer')
    f1dw = IntCol(unit= 'foyer')
    
    f1tv = IntCol(unit= 'foyer')
    f1uv = IntCol(unit= 'foyer')
    f1tw = IntCol(unit= 'foyer')
    f1uw = IntCol(unit= 'foyer')
    f1tx = IntCol(unit= 'foyer')
    f1ux = IntCol(unit= 'foyer')
    
    # RVCM
    # revenus au prélèvement libératoire
    f2da = IntCol(unit= 'foyer')
    f2dh = IntCol(unit= 'foyer')
    f2ee = IntCol(unit= 'foyer')

    # revenus ouvrant droit à abattement
    f2dc = IntCol(unit= 'foyer')
    f2fu = IntCol(unit= 'foyer')
    f2ch = IntCol(unit= 'foyer')
    
    # Revenus n'ouvrant pas droit à abattement
    f2ts = IntCol(unit= 'foyer')
    f2go = IntCol(unit= 'foyer')
    f2tr = IntCol(unit= 'foyer')
    
    # Autres
    f2cg = IntCol(unit= 'foyer')
    f2bh = IntCol(unit= 'foyer')
    f2ca = IntCol(unit= 'foyer')
    f2aa = IntCol(unit='foyer')
    f2ab = IntCol(unit= 'foyer')
    f2al = IntCol(unit= 'foyer')
    f2am = IntCol(unit= 'foyer')
    f2an = IntCol(unit= 'foyer')
    # non accessible (from previous years)
    f2gr = IntCol(unit= 'foyer') 
        
    f3vc = IntCol(unit= 'foyer')
    f3vd = IntCol(unit= 'foyer')
    f3ve = IntCol(unit= 'foyer')
    f3vf = IntCol(unit= 'foyer')    
    
    f3vl = IntCol(unit= 'foyer')
    f3vi = IntCol(unit= 'foyer')
    f3vm = IntCol(unit= 'foyer')
    
    f3vj = IntCol(unit= 'foyer')
    f3vk = IntCol(unit= 'foyer')
    f3va = IntCol(unit= 'foyer')
    
    # Plus values et gains taxables à 18%
    f3vg = IntCol(unit= 'foyer')
    f3vh = IntCol(unit= 'foyer')
    f3vt = IntCol(unit= 'foyer')
    f3vu = IntCol(unit= 'foyer')
    f3vv = IntCol(unit= 'foyer')

    # Revenu foncier
    f4ba = IntCol(unit= 'foyer')
    f4bb = IntCol(unit= 'foyer')
    f4bc = IntCol(unit= 'foyer')
    f4bd = IntCol(unit= 'foyer')
    f4be = IntCol(unit= 'foyer')
    
    # Prime d'assurance loyers impayés
    f4bf = IntCol(unit= 'foyer')
    
    f4bl = IntCol(unit= 'foyer')
    
    f5qm = IntCol(unit= 'foyer')
    f5rm = IntCol(unit= 'foyer')
    
    # Csg déductible
    f6de = IntCol(unit= 'foyer')

    # Pensions alimentaires
    f6gi = IntCol(unit= 'foyer')
    f6gj = IntCol(unit= 'foyer')
    f6el = IntCol(unit= 'foyer')
    f6em = IntCol(unit= 'foyer')
    f6gp = IntCol(unit= 'foyer')
    f6gu = IntCol(unit= 'foyer')
    
    # Frais d'accueil d'une personne de plus de 75 ans dans le besoin
    f6eu = IntCol(unit= 'foyer')
    f6ev = IntCol(unit= 'foyer')
    
    # Déductions diverses
    f6dd = IntCol(unit= 'foyer')
    
    # Épargne retraite - PERP, PRÉFON, COREM et CGOS
    f6ps = IntCol(unit= 'foyer')
    f6rs = IntCol(unit= 'foyer')
    f6ss = IntCol(unit= 'foyer')
    f6pt = IntCol(unit= 'foyer')
    f6rt = IntCol(unit= 'foyer')
    f6st = IntCol(unit= 'foyer')
    f6pu = IntCol(unit= 'foyer')
    f6ru = IntCol(unit= 'foyer')
    f6su = IntCol(unit= 'foyer')
    
    # Souscriptions en faveur du cinéma ou de l’audiovisuel
    f6aa = IntCol(unit= 'foyer')
    
    # Souscriptions au capital des SOFIPÊCHE
    f6cc = IntCol(unit= 'foyer')
    
    # Investissements DOM-TOM dans le cadre d’une entreprise <= 2005
    # ou Versements sur un compte épargne codéveloppement 
    f6eh = IntCol(unit= 'foyer')
    
    # Pertes en capital consécutives à la souscription au capital de sociétés 
    # nouvelles ou de sociétés en difficulté
    f6da = IntCol(unit= 'foyer')
    
    
    # Dépenses de grosses réparations effectuées par les nus propriétaires
    f6cb = IntCol(unit= 'foyer')
    f6hj = IntCol(unit= 'foyer')
    
    # Sommes à rajouter au revenu imposable
    f6gh = IntCol(unit= 'foyer')    
    
    # Deficit Antérieur
    f6fa = IntCol(unit= 'foyer')
    f6fb = IntCol(unit= 'foyer')
    f6fc = IntCol(unit= 'foyer')
    f6fd = IntCol(unit= 'foyer')
    f6fe = IntCol(unit= 'foyer')
    f6fl = IntCol(unit= 'foyer')
    
    # Dons
    f7ud = IntCol(unit= 'foyer')
    f7uf = IntCol(unit= 'foyer')
    f7xs = IntCol(unit= 'foyer')
    f7xt = IntCol(unit= 'foyer')
    f7xu = IntCol(unit= 'foyer')
    f7xw = IntCol(unit= 'foyer')
    f7xy = IntCol(unit= 'foyer')
    
    # Cotisations syndicales des salariées et pensionnés
    f7ac = IntCol(unit= 'foyer')
    f7ae = IntCol(unit= 'foyer')
    f7ag = IntCol(unit= 'foyer')

    # Salarié à domicile
    f7db = IntCol(unit= 'foyer')
    f7df = IntCol(unit= 'foyer')
    f7dq = IntCol(unit= 'foyer')
    f7dg = BoolCol(unit= 'foyer')
    f7dl = IntCol(unit= 'foyer')
    
    # Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale
    f7vy = IntCol(unit= 'foyer')
    f7vz = IntCol(unit= 'foyer')
    f7vx = IntCol(unit= 'foyer')
    f7vw = IntCol(unit= 'foyer')

    # Dépenses d'accueil dans un établissement pour personnes âgées dépendantes
    f7cd = IntCol(unit= 'foyer')
    f7ce = IntCol(unit= 'foyer')

    # Frais de garde des enfants de moins de 6 ans
    f7ga = IntCol(unit= 'foyer')
    f7gb = IntCol(unit= 'foyer')
    f7gc = IntCol(unit= 'foyer')
    f7ge = IntCol(unit= 'foyer')
    f7gf = IntCol(unit= 'foyer')
    f7gg = IntCol(unit= 'foyer')

    # Enfants à charge poursuivant leurs études
    f7ea = IntCol(unit= 'foyer')
    f7eb = IntCol(unit= 'foyer')
    f7ec = IntCol(unit= 'foyer')
    f7ed = IntCol(unit= 'foyer')
    f7ef = IntCol(unit= 'foyer')
    f7eg = IntCol(unit= 'foyer')

    # Intérêts des prêts étudiants
    f7td = IntCol(unit= 'foyer')
    f7vo = IntCol(unit= 'foyer')
    f7uk = IntCol(unit= 'foyer')
    
    # Primes de survies, contrat d'épargne handicap
    f7gz = IntCol(unit= 'foyer')
    
    # Prestations compensatoires
    f7wm = IntCol(unit= 'foyer')
    f7wn = IntCol(unit= 'foyer')
    f7wo = IntCol(unit= 'foyer')
    f7wp = IntCol(unit= 'foyer')
    
    # Dépenses en faveur de la qualité environnementale
    f7we = IntCol(unit= 'foyer')
    f7wq = IntCol(unit= 'foyer')
    f7wh = IntCol(unit= 'foyer')
    f7wk = IntCol(unit= 'foyer')
    f7wf = IntCol(unit= 'foyer')
    
    # Dépenses en faveur de l'aide aux personnes
    f7wi = IntCol(unit= 'foyer')
    f7wj = IntCol(unit= 'foyer')
    f7wl = IntCol(unit= 'foyer')
    
    # Investissements dans les DOM-TOM dans le cadre d'une entrepise
    f7ur = IntCol(unit= 'foyer')
    f7oz = IntCol(unit= 'foyer')
    f7pz = IntCol(unit= 'foyer')
    f7qz = IntCol(unit= 'foyer')
    f7rz = IntCol(unit= 'foyer')
    f7sz = IntCol(unit= 'foyer')
    
    # Aide aux créateurs et repreneurs d'entreprises
    f7fy = IntCol(unit= 'foyer')
    f7gy = IntCol(unit= 'foyer')
    f7jy = IntCol(unit= 'foyer')
    f7hy = IntCol(unit= 'foyer')
    f7ky = IntCol(unit= 'foyer')
    f7iy = IntCol(unit= 'foyer')
    f7ly = IntCol(unit= 'foyer')
    f7my = IntCol(unit= 'foyer')

    # Travaux de restauration immobilière
    f7ra = IntCol(unit= 'foyer')
    f7rb = IntCol(unit= 'foyer')
    
    # Assurance-vie
    f7gw = IntCol(unit= 'foyer')
    f7gx = IntCol(unit= 'foyer')
    # f7gy = IntCol() existe ailleurs

    # Investissements locatifs dans le secteur de touristique            
    f7xc = IntCol(unit= 'foyer')
    f7xd = IntCol(unit= 'foyer')
    f7xe = IntCol(unit= 'foyer')
    f7xf = IntCol(unit= 'foyer')
    f7xh = IntCol(unit= 'foyer')
    f7xi = IntCol(unit= 'foyer')
    f7xj = IntCol(unit= 'foyer')
    f7xk = IntCol(unit= 'foyer')
    f7xl = IntCol(unit= 'foyer')
    f7xm = IntCol(unit= 'foyer')
    f7xn = IntCol(unit= 'foyer')
    f7xo = IntCol(unit= 'foyer')
    
    # Souscriptions au capital des PME
    f7cf = IntCol(unit= 'foyer')
    f7cl = IntCol(unit= 'foyer')
    f7cm = IntCol(unit= 'foyer')
    f7cn = IntCol(unit= 'foyer')
    f7cu = IntCol(unit= 'foyer')

    # Souscription au capital d’une SOFIPECHE 
    f7gs = IntCol(unit= 'foyer')

    # Investissements OUTRE-MER dans le secteur du logement et autres secteurs d’activité    
    f7ua = IntCol(unit= 'foyer')
    f7ub = IntCol(unit= 'foyer')
    f7uc = IntCol(unit= 'foyer')
    f7ui = IntCol(unit= 'foyer')
    f7uj = IntCol(unit= 'foyer')
    f7qb = IntCol(unit= 'foyer')
    f7qc = IntCol(unit= 'foyer')
    f7qd = IntCol(unit= 'foyer')
    f7ql = IntCol(unit= 'foyer')
    f7qt = IntCol(unit= 'foyer')
    f7qm = IntCol(unit= 'foyer')
    
    # Souscription de parts de fonds communs de placement dans l'innovation, 
    # de fonds d'investissement de proximité    
    f7gq = IntCol(unit= 'foyer')
    f7fq = IntCol(unit= 'foyer')
    f7fm = IntCol(unit= 'foyer')
    
    # Souscriptions au capital de SOFICA
    f7gn = IntCol(unit= 'foyer')
    f7fn = IntCol(unit= 'foyer')

    # Intérèts d'emprunts pour reprises de société
    f7fh = IntCol(unit= 'foyer')         

    # Frais de comptabilité et d'adhésion à un CGA ou AA         
    f7ff = IntCol(unit= 'foyer')
    f7fg = IntCol(unit= 'foyer')
    
    # Travaux de conservation et de restauration d’objets classés monuments historiques
    f7nz = IntCol(unit= 'foyer')
    
    # Dépenses de protections du patrimoine naturel
    f7ka = IntCol(unit= 'foyer')

    # Intérêts d'emprunts
    f7wg = IntCol(unit= 'foyer')
    
    # Intérêts des prêts à la consommation (case UH)
    f7uh = IntCol(unit= 'foyer')
    
    # Investissements forestiers
    f7un = IntCol(unit= 'foyer')
    
    # Intérêts pour paiement différé accordé aux agriculteurs
    f7um = IntCol(unit= 'foyer')

    # Investissements locatif neufs : Dispositif Scellier
    f7hj = IntCol(unit= 'foyer')
    f7hk = IntCol(unit= 'foyer')
    f7hn = IntCol(unit= 'foyer')
    f7ho = IntCol(unit= 'foyer')
    f7hl = IntCol(unit= 'foyer')
    f7hm = IntCol(unit= 'foyer')
    f7hr = IntCol(unit= 'foyer')
    f7hs = IntCol(unit= 'foyer')
    f7la = IntCol(unit= 'foyer')

    # Investissement en vue de la location meublée non professionnelle dans certains établissements ou résidences
    f7ij = IntCol(unit= 'foyer')
    f7il = IntCol(unit= 'foyer')
    f7im = IntCol(unit= 'foyer')
    f7ik = IntCol(unit= 'foyer')
    f7is = IntCol(unit= 'foyer')
    
    # Investissements locatifs dans les résidences de tourisme situées dans une zone de 
    # revitalisation rurale
    f7gt = IntCol(unit= 'foyer')
    f7xg = IntCol(unit= 'foyer')
    f7gu = IntCol(unit= 'foyer')
    f7gv = IntCol(unit= 'foyer')
    
    # Avoir fiscaux et crédits d'impôt     
    # f2ab déjà disponible
    f8ta = IntCol(unit= 'foyer')
    f8tb = IntCol(unit= 'foyer')
    f8tf = IntCol(unit= 'foyer')
    f8tg = IntCol(unit= 'foyer')
    f8th = IntCol(unit= 'foyer')
    f8tc = IntCol(unit= 'foyer')
    f8td = IntCol(unit= 'foyer')
    f8te = IntCol(unit= 'foyer')
    f8to = IntCol(unit= 'foyer')
    f8tp = IntCol(unit= 'foyer')
    f8uz = IntCol(unit= 'foyer')
    f8tz = IntCol(unit= 'foyer')
    f8wa = IntCol(unit= 'foyer')
    f8wb = IntCol(unit= 'foyer')
    f8wc = IntCol(unit= 'foyer')
    f8wd = IntCol(unit= 'foyer')
    f8we = IntCol(unit= 'foyer')
    f8wr = IntCol(unit= 'foyer')
    f8ws = IntCol(unit= 'foyer')
    f8wt = IntCol(unit= 'foyer')
    f8wu = IntCol(unit= 'foyer')
    f8wv = IntCol(unit= 'foyer')
    f8wx = IntCol(unit= 'foyer')
    f8wy = IntCol(unit= 'foyer')
    
    # Acquisition de biens culturels
    f7uo = IntCol(unit= 'foyer')

    
    # Mécénat d'entreprise    
    f7us = IntCol(unit= 'foyer')

    # Crédits d’impôt pour dépenses en faveur de la qualité environnementale
    # f7wf = IntCol() déjà disponible
    # f7wh = IntCol() déjà disponible
    # f7wk = IntCol() déjà disponible
    # f7wq = IntCol() déjà disponible
    f7sb = IntCol(unit= 'foyer')
    f7sd = IntCol(unit= 'foyer')
    f7se = IntCol(unit= 'foyer')
    f7sh = IntCol(unit= 'foyer')
    # f7wg = IntCol() déjà disponible
    f7sc = IntCol(unit= 'foyer')
    
    # Crédit d'impôt pour dépense d'acquisition ou de transformation d'un véhicule GPL ou mixte
    f7up = IntCol(unit= 'foyer')
    f7uq = IntCol(unit= 'foyer')

    # Crédit d'impôt aide à la mobilité
    f1ar = IntCol(unit= 'foyer')
    f1br = IntCol(unit= 'foyer')
    f1cr = IntCol(unit= 'foyer')
    f1dr = IntCol(unit= 'foyer')
    f1er = IntCol(unit= 'foyer')

    # Crédit d’impôt directive « épargne » (case 2BG)
    f2bg = IntCol(unit= 'foyer')
    
    # Crédit d’impôt représentatif de la taxe additionnelle au droit de bail
    f4tq = IntCol(unit= 'foyer')
    

    # Crédits d’impôt pour dépenses en faveur de l’aide aux personnes
    # f7wf
    # f7wi
    # f7wj
    # f7wl
    f7sf = IntCol(unit= 'foyer')
    f7si = IntCol(unit= 'foyer')
    
    # Frais de garde des enfants à l’extérieur du domicile 
    f4ga = IntCol(unit= 'foyer')
    f4gb = IntCol(unit= 'foyer')
    f4gc = IntCol(unit= 'foyer')
    f4ge = IntCol(unit= 'foyer')
    f4gf = IntCol(unit= 'foyer')
    f4gg = IntCol(unit= 'foyer')

    # Auto-entrepreneur : versements d’impôt sur le revenu 
    f8uy = IntCol(unit= 'foyer')

    # Revenus des professions non salariées
    frag_exon = IntCol(unit= 'foyer') # (f5hn, f5in, f5jn)
    frag_impo = IntCol(unit= 'foyer') # (f5ho, f5io, f5jo)    
    arag_exon = IntCol(unit= 'foyer') # (f5hb, f5ib, f5jb)
    arag_impg = IntCol(unit= 'foyer') # (f5hc, f5ic, f5jc)
    arag_defi = IntCol(unit= 'foyer') # (f5hf, f5if, f5jf)
    nrag_exon = IntCol(unit= 'foyer') # (f5hh, f5ih, f5jh)
    nrag_impg = IntCol(unit= 'foyer') # (f5hi, f5ii, f5ji)
    nrag_defi = IntCol(unit= 'foyer') # (f5hl, f5il, f5jl)
    nrag_ajag = IntCol(unit= 'foyer') # (f5hm, f5im, f5jm)

    mbic_exon = IntCol(unit= 'foyer') # (f5kn, f5ln, f5mn)
    abic_exon = IntCol(unit= 'foyer') # (f5kb, f5lb, f5mb)
    nbic_exon = IntCol(unit= 'foyer') # (f5kh, f5lh, f5mh)
    mbic_impv = IntCol(unit= 'foyer') # (f5ko, f5lo, f5mo)
    mbic_imps = IntCol(unit= 'foyer') # (f5kp, f5lp, f5mp)
    abic_impn = IntCol(unit= 'foyer') # (f5kc, f5lc, f5mc)
    abic_imps = IntCol(unit= 'foyer') # (f5kd, f5ld, f5md)
    nbic_impn = IntCol(unit= 'foyer') # (f5ki, f5li, f5mi)
    nbic_imps = IntCol(unit= 'foyer') # (f5kj, f5lj, f5mj)
    abic_defn = IntCol(unit= 'foyer') # (f5kf, f5lf, f5mf)
    abic_defs = IntCol(unit= 'foyer') # (f5kg, f5lg, f5mg)
    nbic_defn = IntCol(unit= 'foyer') # (f5kl, f5ll, f5ml)
    nbic_defs = IntCol(unit= 'foyer') # (f5km, f5lm, f5mm)
    nbic_apch = IntCol(unit= 'foyer') # (f5ks, f5ls, f5ms)

    macc_exon = IntCol(unit= 'foyer') # (f5nn, f5on, f5pn)
    aacc_exon = IntCol(unit= 'foyer') # (f5nb, f5ob, f5pb)
    nacc_exon = IntCol(unit= 'foyer') # (f5nh, f5oh, f5ph)
    macc_impv = IntCol(unit= 'foyer') # (f5no, f5oo, f5po)
    macc_imps = IntCol(unit= 'foyer') # (f5np, f5op, f5pp)
    aacc_impn = IntCol(unit= 'foyer') # (f5nc, f5oc, f5pc)
    aacc_imps = IntCol(unit= 'foyer') # (f5nd, f5od, f5pd)
    aacc_defn = IntCol(unit= 'foyer') # (f5nf, f5of, f5pf)
    aacc_defs = IntCol(unit= 'foyer') # (f5ng, f5og, f5pg)
    nacc_impn = IntCol(unit= 'foyer') # (f5ni, f5oi, f5pi)
    nacc_imps = IntCol(unit= 'foyer') # (f5nj, f5oj, f5pj)
    nacc_defn = IntCol(unit= 'foyer') # (f5nl, f5ol, f5pl)
    nacc_defs = IntCol(unit= 'foyer') # (f5nm, f5om, f5pm)
    mncn_impo = IntCol(unit= 'foyer') # (f5ku, f5lu, f5mu)
    cncn_bene = IntCol(unit= 'foyer') # (f5sn, f5ns, f5os)
    cncn_defi = IntCol(unit= 'foyer') # (f5sp, f5nu, f5ou, f5sr)

    mbnc_exon = IntCol(unit= 'foyer') # (f5hp, f5ip, f5jp)
    abnc_exon = IntCol(unit= 'foyer') # (f5qb, f5rb, f5sb)
    nbnc_exon = IntCol(unit= 'foyer') # (f5qh, f5rh, f5sh)
    mbnc_impo = IntCol(unit= 'foyer') # (f5hq, f5iq, f5jq)
    abnc_impo = IntCol(unit= 'foyer') # (f5qc, f5rc, f5sc)
    abnc_defi = IntCol(unit= 'foyer') # (f5qe, f5re, f5se)
    nbnc_impo = IntCol(unit= 'foyer') # (f5qi, f5ri, f5si)
    nbnc_defi = IntCol(unit= 'foyer') # (f5qk, f5rk, f5sk)

    mbic_mvct = IntCol(unit= 'foyer') # (f5hu)
    macc_mvct = IntCol(unit= 'foyer') # (f5iu)
    mncn_mvct = IntCol(unit= 'foyer') # (f5ju)
    mbnc_mvct = IntCol(unit= 'foyer') # (f5kz)

    frag_pvct = IntCol(unit= 'foyer') # (f5hw, f5iw, f5jw)
    mbic_pvct = IntCol(unit= 'foyer') # (f5kx, f5lx, f5mx)
    macc_pvct = IntCol(unit= 'foyer') # (f5nx, f5ox, f5px)
    mbnc_pvct = IntCol(unit= 'foyer') # (f5hv, f5iv, f5jv)
    mncn_pvct = IntCol(unit= 'foyer') # (f5ky, f5ly, f5my)

    mbic_mvlt = IntCol(unit= 'foyer') # (f5kr, f5lr, f5mr)
    macc_mvlt = IntCol(unit= 'foyer') # (f5nr, f5or, f5pr)
    mncn_mvlt = IntCol(unit= 'foyer') # (f5kw, f5lw, f5mw)
    mbnc_mvlt = IntCol(unit= 'foyer') # (f5hs, f5is, f5js)

    frag_pvce = IntCol(unit= 'foyer') # (f5hx, f5ix, f5jx)
    arag_pvce = IntCol(unit= 'foyer') # (f5he, f5ie, f5je)
    nrag_pvce = IntCol(unit= 'foyer') # (f5hk, f5ik, f5jk)
    mbic_pvce = IntCol(unit= 'foyer') # (f5kq, f5lq, f5mq)
    abic_pvce = IntCol(unit= 'foyer') # (f5ke, f5le, f5me)
    nbic_pvce = IntCol(unit= 'foyer') # (f5kk, f5lk, f5mk)
    macc_pvce = IntCol(unit= 'foyer') # (f5nq, f5oq, f5pq)
    aacc_pvce = IntCol(unit= 'foyer') # (f5ne, f5oe, f5pe)
    nacc_pvce = IntCol(unit= 'foyer') # (f5nk, f5ok, f5pk)
    mncn_pvce = IntCol(unit= 'foyer') # (f5kv, f5lv, f5mv)
    cncn_pvce = IntCol(unit= 'foyer') # (f5so, f5nt, f5ot)
    mbnc_pvce = IntCol(unit= 'foyer') # (f5hr, f5ir, f5jr)
    abnc_pvce = IntCol(unit= 'foyer') # (f5qd, f5rd, f5sd)
    nbnc_pvce = IntCol(unit= 'foyer') # (f5qj, f5rj, f5sj)

# pfam only
    inactif   = BoolCol(unit='fam')
    partiel1  = BoolCol(unit='fam')
    partiel2  = BoolCol(unit='fam') 
    categ_inv = IntCol(unit='fam')
    opt_colca = BoolCol(unit='fam')
    empl_dir  = BoolCol(unit='fam') 
    ass_mat   = BoolCol(unit='fam')
    gar_dom   = BoolCol(unit='fam')

# zones apl and calibration 
    tu99 = EnumCol(label = u"tranche d'unité urbaine",
                   enum=Enum([u'Communes rurales',
                         u'moins de 5 000 habitants',
                         u'5 000 à 9 999 habitants',
                         u'10 000 à 19 999 habitants',
                         u'20 000 à 49 999 habitants',
                         u'50 000 à 99 999 habitants',
                         u'100 000 à 199 999 habitants',
                         u'200 000 habitants ou plus (sauf agglomération parisienne)',
                         u'agglomération parisienne']), unit='menage')
    
    tau99 = EnumCol(label = u"tranche d'aire urbaine", unit='menage')
    reg   = EnumCol(unit='menage')
    pol99 = EnumCol(unit='menage')
    cstotpragr = EnumCol(label = u"catégorie socio_professionelle agrégée de la personne de référence",
                         enum = Enum([u"Non renseignée",
                                      u"Agriculteurs exploitants",
                                      u"Artisans, commerçants, chefs d'entreprise",
                                      u"Cadres supérieurs",
                                      u"Professions intermédiaires",
                                      u"Employés",
                                      u"Ouvriers",
                                      u"Retraités",
                                      u"Autres inactifs"]))
    
    naf16pr = EnumCol(label = u"activité économique de l'établissement de l'emploi principal actuel de la personne de référence",
                      enum = Enum([u"Sans objet",
                                   u"Non renseigné",
                                   u"Agriculture, sylviculture et pêche",
                                   u"Industries agricoles",
                                   u"Industries des biens de consommation",
                                   u"Industrie automobile",
                                   u"Industries des biens d'équipement",
                                   u"Industries des biens intermédiaires",
                                   u"Energie",
                                   u"Construction",
                                   u"Commerce et réparations",
                                   u"Transports",
                                   u"Activités financières",
                                   u"Activités immobilières",
                                   u"Services aux entreprises",
                                   u"Services aux particuliers",
                                   u"Education, santé, action sociale",
                                   u"Administrations"],start=-1)) # 17 postes + 1 (-1: sans objet, 0: nonrenseigné) 
    
    typmen15 = EnumCol(label = u"type de ménage",
                       enum = Enum([u"Personne seule active",
                                    u"Personne seule inactive",
                                    u"Familles monoparentales, parent actif",
                                    u"Familles monoparentales, parent inactif et au moins un enfant actif",
                                    u"Familles monoparentales, tous inactifs",
                                    u"Couples sans enfant, 1 actif",
                                    u"Couples sans enfant, 2 actifs",
                                    u"Couples sans enfant, tous inactifs",
                                    u"Couples avec enfant, 1 membre du couple actif",
                                    u"Couples avec enfant, 2 membres du couple actif",
                                    u"Couples avec enfant, couple inactif et au moins un enfant actif",
                                    u"Couples avec enfant, tous inactifs",
                                    u"Autres ménages, 1 actif",
                                    u"Autres ménages, 2 actifs ou plus",
                                    u"Autres ménages, tous inactifs"],start=1))
    
    ageq  = EnumCol(label = u"âge quinquennal de la personne de référence",
                    enum = Enum([u"moins de 25 ans",
                                 u"25 à 29 ans",
                                 u"30 à 34 ans",
                                 u"35 à 39 ans",
                                 u"40 à 44 ans",
                                 u"45 à 49 ans",
                                 u"50 à 54 ans",
                                 u"55 à 59 ans",
                                 u"60 à 64 ans",
                                 u"65 à 69 ans",
                                 u"70 à 74 ans",
                                 u"75 à 79 ans",
                                 u"80 ans et plus"]))

                                 
    nbinde = EnumCol(label = u"taille du ménage",
                     enum = Enum([u"Une personne",
                                  u"Deux personnes",
                                  u"Trois personnes",
                                  u"Quatre personnes",
                                  u"Cinq personnes",
                                  u"Six personnes et plus"], start=1))

    ddipl = EnumCol(label = u"diplôme de la personne de référence",
                    enum = Enum([u"Diplôme supérieur",
                                 u"Baccalauréat + 2 ans",
                                 u"Baccalauréat ou brevet professionnel ou autre diplôme de ce niveau",
                                 u"CAP, BEP ou autre diplôme de ce niveau",
                                 u"Brevet des collèges",
                                 u"Aucun diplôme ou CEP"],start=1)) 
    
    act5 = EnumCol(label = u"activité",
                     enum = Enum([u"Salarié",
                                  u"Indépendant",
                                  u"Chômeur",
                                  u"Retraité",
                                  u"Inactif"],start=1)) # 5 postes normalement TODO; check=0
    wprm_init = FloatCol()

## ISF ##
    
## Immeubles bâtis ##
    b1ab = IntCol(unit= 'foyer') ##  valeur résidence principale avant abattement ##
    b1ac = IntCol(unit= 'foyer')
## non bâtis ##
    b1bc = IntCol(unit= 'foyer')
    b1be = IntCol(unit= 'foyer')
    b1bh = IntCol(unit= 'foyer')
    b1bk = IntCol(unit= 'foyer') 
## droits sociaux- valeurs mobilières-liquidités- autres meubles ##

    b1cl = IntCol(unit= 'foyer')
    b1cb = IntCol(unit= 'foyer')
    b1cd = IntCol(unit= 'foyer')
    b1ce = IntCol(unit= 'foyer')
    b1cf = IntCol(unit= 'foyer')
    b1cg = IntCol(unit= 'foyer')

    b1co = IntCol(unit= 'foyer')

#    b1ch
#    b1ci
#    b1cj
#    b1ck


## passifs et autres réduc ##
    b2gh= IntCol(unit= 'foyer')
    
## réductions ##
    b2mt = IntCol(unit= 'foyer')
    b2ne = IntCol(unit= 'foyer')
    b2mv = IntCol(unit= 'foyer')
    b2nf = IntCol(unit= 'foyer')
    b2mx = IntCol(unit= 'foyer')
    b2na = IntCol(unit= 'foyer')
    b2nc = IntCol(unit= 'foyer')

##  montant impôt acquitté hors de France ##
    b4rs = IntCol(unit= 'foyer')

## BOUCLIER FISCAL ##

    rev_or= IntCol()
    rev_exo= IntCol()
    tax_hab= IntCol()
    tax_fonc= IntCol()
    restit_imp= IntCol()
        
    # to remove
    champm = BoolCol()
    wprm = FloatCol()
    etr = IntCol()     
    coloc = BoolCol()
    csg_taux_plein = BoolCol(default = True)
    aer = IntCol()
    ass = IntCol()
    f5sq = IntCol()
