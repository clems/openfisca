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
from datetime import date


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
    
    hsup = IntCol()
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
    
    zone_apl = EnumCol(label = u"zone apl", default = 2)
    loyer = IntCol() # Loyer mensuel
    so = EnumCol(label = u"statut d'occupation",
                  enum = Enum([u"Non renseigné",
                               u"Accédant à la propriété",
                               u"Propriétaire (non accédant) du logement",
                               u"Locataire d'un logement HLM",
                               u"Locataire ou sous-locataire d'un logement loué vide non-HLM",
                               u"Locataire ou sous-locataire d'un logement loué meublé ou d'une chambre d'hôtel",
                               u"Logé gratuitement par des parents, des amis ou l'employeur"]))
    activite = IntCol()
    boursier = BoolCol()
    code_postal = IntCol()
    
    statmarit = IntCol(default = 2)
    
    nbR = IntCol()
    nbJ = IntCol()
    nbI = IntCol()
    nbH = IntCol()
    nbG = IntCol()
    nbF = IntCol()
    nbN = IntCol()
    
    caseE = BoolCol()
    caseF = BoolCol()
    caseG = BoolCol()
    caseH = IntCol()
    caseK = BoolCol()
    caseL = BoolCol()
    caseN = BoolCol()
    caseP = BoolCol()
    caseS = BoolCol()
    caseT = BoolCol()
    caseW = BoolCol()
    
    # Rentes viagères
    f1aw = IntCol()
    f1bw = IntCol()
    f1cw = IntCol()
    f1dw = IntCol()
    
    f1tv = IntCol()
    f1uv = IntCol()
    f1tw = IntCol()
    f1uw = IntCol()
    f1tx = IntCol()
    f1ux = IntCol()
    
    # RVCM
    # revenus au prélèvement libératoire
    f2da = IntCol()
    f2dh = IntCol()
    f2ee = IntCol()

    # revenus ouvrant droit à abattement
    f2dc = IntCol()
    f2fu = IntCol()
    f2ch = IntCol()
    
    # Revenus n'ouvrant pas droit à abattement
    f2ts = IntCol()
    f2go = IntCol()
    f2tr = IntCol()
    
    # Autres
    f2cg = IntCol()
    f2bh = IntCol()
    f2ca = IntCol()
    f2ab = IntCol()    
    f2aa = IntCol()
    f2al = IntCol()
    f2am = IntCol()
    f2an = IntCol()

    # non accessible (from previous years)
    f2gr = IntCol() 
        
    f3vc = IntCol()
    f3vd = IntCol()
    f3ve = IntCol()
    f3vf = IntCol()    
    
    f3vl = IntCol()
    f3vi = IntCol()
    f3vm = IntCol()
    
    f3vj = IntCol()
    f3vk = IntCol()
    f3va = IntCol()
    
    # Plus values et gains taxables à 18%
    f3vg = IntCol()
    f3vh = IntCol()
    f3vt = IntCol()
    f3vu = IntCol()
    f3vv = IntCol()

    # Revenu foncier
    f4ba = IntCol()
    f4bb = IntCol()
    f4bc = IntCol()
    f4bd = IntCol()
    f4be = IntCol()
    
    # Prime d'assurance loyers impayés
    f4bf = IntCol()
    
    f4bl = IntCol()
    
    f5qm = IntCol()
    f5rm = IntCol()
    
    # Csg déductible
    f6de = IntCol()

    # Pensions alimentaires
    f6gi = IntCol()
    f6gj = IntCol()
    f6el = IntCol()
    f6em = IntCol()
    f6gp = IntCol()
    f6gu = IntCol()
    
    # Frais d'accueil d'une personne de plus de 75 ans dans le besoin
    f6eu = IntCol()
    f6ev = IntCol()
    
    # Déductions diverses
    f6dd = IntCol()
    
    # Épargne retraite - PERP, PRÉFON, COREM et CGOS
    f6ps = IntCol()
    f6rs = IntCol()
    f6ss = IntCol()
    f6pt = IntCol()
    f6rt = IntCol()
    f6st = IntCol()
    f6pu = IntCol()
    f6ru = IntCol()
    f6su = IntCol()
    
    # Souscriptions en faveur du cinéma ou de l’audiovisuel
    f6aa = IntCol()
    
    # Souscriptions au capital des SOFIPÊCHE
    f6cc = IntCol()
    
    # Investissements DOM-TOM dans le cadre d’une entreprise <= 2005
    # ou Versements sur un compte épargne codéveloppement 
    f6eh = IntCol()
    
    # Pertes en capital consécutives à la souscription au capital de sociétés 
    # nouvelles ou de sociétés en difficulté
    f6da = IntCol()
    
    
    # Dépenses de grosses réparations effectuées par les nus propriétaires
    f6cb = IntCol()
    f6hj = IntCol()
    f6hk = IntCol(start = date(2011,1,1))
    
    # Sommes à rajouter au revenu imposable
    f6gh = IntCol()    
    
    # Deficit Antérieur
    f6fa = IntCol()
    f6fb = IntCol()
    f6fc = IntCol()
    f6fd = IntCol()
    f6fe = IntCol()
    f6fl = IntCol()
    
    # Dons
    f7ud = IntCol()
    f7uf = IntCol()
    f7xs = IntCol()
    f7xt = IntCol()
    f7xu = IntCol()
    f7xw = IntCol()
    f7xy = IntCol()
    
    # Cotisations syndicales des salariées et pensionnés
    f7ac = IntCol()
    f7ae = IntCol()
    f7ag = IntCol()

    # Salarié à domicile
    f7db = IntCol()
    f7df = IntCol()
    f7dq = IntCol()
    f7dg = BoolCol()
    f7dl = IntCol()
    
    # Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale
    f7vy = IntCol()
    f7vz = IntCol()
    f7vx = IntCol()
    f7vw = IntCol()

    # Dépenses d'accueil dans un établissement pour personnes âgées dépendantes
    f7cd = IntCol()
    f7ce = IntCol()

    # Frais de garde des enfants de moins de 6 ans
    f7ga = IntCol()
    f7gb = IntCol()
    f7gc = IntCol()
    f7ge = IntCol()
    f7gf = IntCol()
    f7gg = IntCol()

    # Enfants à charge poursuivant leurs études
    f7ea = IntCol()
    f7eb = IntCol()
    f7ec = IntCol()
    f7ed = IntCol()
    f7ef = IntCol()
    f7eg = IntCol()

    # Intérêts des prêts étudiants
    f7td = IntCol()
    f7vo = IntCol()
    f7uk = IntCol()
    
    # Primes de survies, contrat d'épargne handicap
    f7gz = IntCol()
    
    # Prestations compensatoires
    f7wm = IntCol()
    f7wn = IntCol()
    f7wo = IntCol()
    f7wp = IntCol()
    
    # Dépenses en faveur de la qualité environnementale
    f7we = IntCol()
    f7wq = IntCol()
    f7wh = IntCol()
    f7wk = IntCol()
    f7wf = IntCol()
    
    # Dépenses en faveur de l'aide aux personnes
    f7wi = IntCol()
    f7wj = IntCol()
    f7wl = IntCol()
    
    # Investissements dans les DOM-TOM dans le cadre d'une entrepise
    f7ur = IntCol()
    f7oz = IntCol()
    f7pz = IntCol()
    f7qz = IntCol()
    f7rz = IntCol()
    f7sz = IntCol()
    
    # Aide aux créateurs et repreneurs d'entreprises
    f7fy = IntCol()
    f7gy = IntCol()
    f7jy = IntCol()
    f7hy = IntCol()
    f7ky = IntCol()
    f7iy = IntCol()
    f7ly = IntCol()
    f7my = IntCol()

    # Travaux de restauration immobilière
    f7ra = IntCol()
    f7rb = IntCol()
    
    # Assurance-vie
    f7gw = IntCol()
    f7gx = IntCol()
    # f7gy = IntCol() existe ailleurs

    # Investissements locatifs dans le secteur de touristique            
    f7xc = IntCol()
    f7xd = IntCol()
    f7xe = IntCol()
    f7xf = IntCol()
    f7xh = IntCol()
    f7xi = IntCol()
    f7xj = IntCol()
    f7xk = IntCol()
    f7xl = IntCol()
    f7xm = IntCol()
    f7xn = IntCol()
    f7xo = IntCol()
    
    # Souscriptions au capital des PME
    f7cf = IntCol()
    f7cl = IntCol()
    f7cm = IntCol()
    f7cn = IntCol()
    f7cu = IntCol()

    # Souscription au capital d’une SOFIPECHE 
    f7gs = IntCol()

    # Investissements OUTRE-MER dans le secteur du logement et autres secteurs d’activité    
    f7ua = IntCol()
    f7ub = IntCol()
    f7uc = IntCol()
    f7ui = IntCol()
    f7uj = IntCol()
    f7qb = IntCol()
    f7qc = IntCol()
    f7qd = IntCol()
    f7ql = IntCol()
    f7qt = IntCol()
    f7qm = IntCol()
    
    # Souscription de parts de fonds communs de placement dans l'innovation, 
    # de fonds d'investissement de proximité    
    f7gq = IntCol()
    f7fq = IntCol()
    f7fm = IntCol()
    
    # Souscriptions au capital de SOFICA
    f7gn = IntCol()
    f7fn = IntCol()

    # Intérèts d'emprunts pour reprises de société
    f7fh = IntCol()         

    # Frais de comptabilité et d'adhésion à un CGA ou AA         
    f7ff = IntCol()
    f7fg = IntCol()
    
    # Travaux de conservation et de restauration d’objets classés monuments historiques
    f7nz = IntCol()
    
    # Dépenses de protections du patrimoine naturel
    f7ka = IntCol()

    # Intérêts d'emprunts
    f7wg = IntCol()
    
    # Intérêts des prêts à la consommation (case UH)
    f7uh = IntCol()
    
    # Investissements forestiers
    f7un = IntCol()
    
    # Intérêts pour paiement différé accordé aux agriculteurs
    f7um = IntCol()

    # Investissements locatif neufs : Dispositif Scellier
    f7hj = IntCol()
    f7hk = IntCol()
    f7hn = IntCol()
    f7ho = IntCol()
    f7hl = IntCol()
    f7hm = IntCol()
    f7hr = IntCol()
    f7hs = IntCol()
    f7la = IntCol()

    # Investissement en vue de la location meublée non professionnelle dans certains établissements ou résidences
    f7ij = IntCol()
    f7il = IntCol()
    f7im = IntCol()
    f7ik = IntCol()
    f7is = IntCol()
    
    # Investissements locatifs dans les résidences de tourisme situées dans une zone de 
    # revitalisation rurale
    f7gt = IntCol()
    f7xg = IntCol()
    f7gu = IntCol()
    f7gv = IntCol()
    
    # Avoir fiscaux et crédits d'impôt     
    # f2ab déjà disponible
    f8ta = IntCol()
    f8tb = IntCol()
    f8tf = IntCol()
    f8tg = IntCol()
    f8th = IntCol()
    f8tc = IntCol()
    f8td = IntCol()
    f8te = IntCol()
    f8to = IntCol()
    f8tp = IntCol()
    f8uz = IntCol()
    f8tz = IntCol()
    f8wa = IntCol()
    f8wb = IntCol()
    f8wc = IntCol()
    f8wd = IntCol()
    f8we = IntCol()
    f8wr = IntCol()
    f8ws = IntCol()
    f8wt = IntCol()
    f8wu = IntCol()
    f8wv = IntCol()
    f8wx = IntCol()
    f8wy = IntCol()
    
    # Acquisition de biens culturels
    f7uo = IntCol()

    
    # Mécénat d'entreprise    
    f7us = IntCol()

    # Crédits d’impôt pour dépenses en faveur de la qualité environnementale
    # f7wf = IntCol() déjà disponible
    # f7wh = IntCol() déjà disponible
    # f7wk = IntCol() déjà disponible
    # f7wq = IntCol() déjà disponible
    f7sb = IntCol()
    f7sd = IntCol()
    f7se = IntCol()
    f7sh = IntCol()
    # f7wg = IntCol() déjà disponible
    f7sc = IntCol()
    
    # Crédit d'impôt pour dépense d'acquisition ou de transformation d'un véhicule GPL ou mixte
    f7up = IntCol()
    f7uq = IntCol()

    # Crédit d'impôt aide à la mobilité
    f1ar = IntCol()
    f1br = IntCol()
    f1cr = IntCol()
    f1dr = IntCol()
    f1er = IntCol()

    # Crédit d’impôt directive « épargne » (case 2BG)
    f2bg = IntCol()
    
    # Crédit d’impôt représentatif de la taxe additionnelle au droit de bail
    f4tq = IntCol()
    

    # Crédits d’impôt pour dépenses en faveur de l’aide aux personnes
    # f7wf
    # f7wi
    # f7wj
    # f7wl
    f7sf = IntCol()
    f7si = IntCol()
    
    # Frais de garde des enfants à l’extérieur du domicile 
    f4ga = IntCol()
    f4gb = IntCol()
    f4gc = IntCol()
    f4ge = IntCol()
    f4gf = IntCol()
    f4gg = IntCol()

    # Auto-entrepreneur : versements d’impôt sur le revenu 
    f8uy = IntCol()

    # Revenus des professions non salariées
    frag_exon = IntCol() # (f5hn, f5in, f5jn)
    frag_impo = IntCol() # (f5ho, f5io, f5jo)    
    arag_exon = IntCol() # (f5hb, f5ib, f5jb)
    arag_impg = IntCol() # (f5hc, f5ic, f5jc)
    arag_defi = IntCol() # (f5hf, f5if, f5jf)
    nrag_exon = IntCol() # (f5hh, f5ih, f5jh)
    nrag_impg = IntCol() # (f5hi, f5ii, f5ji)
    nrag_defi = IntCol() # (f5hl, f5il, f5jl)
    nrag_ajag = IntCol() # (f5hm, f5im, f5jm)

    mbic_exon = IntCol() # (f5kn, f5ln, f5mn)
    abic_exon = IntCol() # (f5kb, f5lb, f5mb)
    nbic_exon = IntCol() # (f5kh, f5lh, f5mh)
    mbic_impv = IntCol() # (f5ko, f5lo, f5mo)
    mbic_imps = IntCol() # (f5kp, f5lp, f5mp)
    abic_impn = IntCol() # (f5kc, f5lc, f5mc)
    abic_imps = IntCol() # (f5kd, f5ld, f5md)
    nbic_impn = IntCol() # (f5ki, f5li, f5mi)
    nbic_imps = IntCol() # (f5kj, f5lj, f5mj)
    abic_defn = IntCol() # (f5kf, f5lf, f5mf)
    abic_defs = IntCol() # (f5kg, f5lg, f5mg)
    nbic_defn = IntCol() # (f5kl, f5ll, f5ml)
    nbic_defs = IntCol() # (f5km, f5lm, f5mm)
    nbic_apch = IntCol() # (f5ks, f5ls, f5ms)

    macc_exon = IntCol() # (f5nn, f5on, f5pn)
    aacc_exon = IntCol() # (f5nb, f5ob, f5pb)
    nacc_exon = IntCol() # (f5nh, f5oh, f5ph)
    macc_impv = IntCol() # (f5no, f5oo, f5po)
    macc_imps = IntCol() # (f5np, f5op, f5pp)
    aacc_impn = IntCol() # (f5nc, f5oc, f5pc)
    aacc_imps = IntCol() # (f5nd, f5od, f5pd)
    aacc_defn = IntCol() # (f5nf, f5of, f5pf)
    aacc_defs = IntCol() # (f5ng, f5og, f5pg)
    nacc_impn = IntCol() # (f5ni, f5oi, f5pi)
    nacc_imps = IntCol() # (f5nj, f5oj, f5pj)
    nacc_defn = IntCol() # (f5nl, f5ol, f5pl)
    nacc_defs = IntCol() # (f5nm, f5om, f5pm)
    mncn_impo = IntCol() # (f5ku, f5lu, f5mu)
    cncn_bene = IntCol() # (f5sn, f5ns, f5os)
    cncn_defi = IntCol() # (f5sp, f5nu, f5ou, f5sr)

    mbnc_exon = IntCol() # (f5hp, f5ip, f5jp)
    abnc_exon = IntCol() # (f5qb, f5rb, f5sb)
    nbnc_exon = IntCol() # (f5qh, f5rh, f5sh)
    mbnc_impo = IntCol() # (f5hq, f5iq, f5jq)
    abnc_impo = IntCol() # (f5qc, f5rc, f5sc)
    abnc_defi = IntCol() # (f5qe, f5re, f5se)
    nbnc_impo = IntCol() # (f5qi, f5ri, f5si)
    nbnc_defi = IntCol() # (f5qk, f5rk, f5sk)

    mbic_mvct = IntCol() # (f5hu)
    macc_mvct = IntCol() # (f5iu)
    mncn_mvct = IntCol() # (f5ju)
    mbnc_mvct = IntCol() # (f5kz)

    frag_pvct = IntCol() # (f5hw, f5iw, f5jw)
    mbic_pvct = IntCol() # (f5kx, f5lx, f5mx)
    macc_pvct = IntCol() # (f5nx, f5ox, f5px)
    mbnc_pvct = IntCol() # (f5hv, f5iv, f5jv)
    mncn_pvct = IntCol() # (f5ky, f5ly, f5my)

    mbic_mvlt = IntCol() # (f5kr, f5lr, f5mr)
    macc_mvlt = IntCol() # (f5nr, f5or, f5pr)
    mncn_mvlt = IntCol() # (f5kw, f5lw, f5mw)
    mbnc_mvlt = IntCol() # (f5hs, f5is, f5js)

    frag_pvce = IntCol() # (f5hx, f5ix, f5jx)
    arag_pvce = IntCol() # (f5he, f5ie, f5je)
    nrag_pvce = IntCol() # (f5hk, f5ik, f5jk)
    mbic_pvce = IntCol() # (f5kq, f5lq, f5mq)
    abic_pvce = IntCol() # (f5ke, f5le, f5me)
    nbic_pvce = IntCol() # (f5kk, f5lk, f5mk)
    macc_pvce = IntCol() # (f5nq, f5oq, f5pq)
    aacc_pvce = IntCol() # (f5ne, f5oe, f5pe)
    nacc_pvce = IntCol() # (f5nk, f5ok, f5pk)
    mncn_pvce = IntCol() # (f5kv, f5lv, f5mv)
    cncn_pvce = IntCol() # (f5so, f5nt, f5ot)
    mbnc_pvce = IntCol() # (f5hr, f5ir, f5jr)
    abnc_pvce = IntCol() # (f5qd, f5rd, f5sd)
    nbnc_pvce = IntCol() # (f5qj, f5rj, f5sj)

# pfam only
    inactif   = BoolCol()
    partiel1  = BoolCol()
    partiel2  = BoolCol() 
    categ_inv = IntCol()
    opt_colca = BoolCol()
    empl_dir  = BoolCol() 
    ass_mat   = BoolCol()
    gar_dom   = BoolCol()

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
                         u'agglomération parisienne']))
    
    tau99 = EnumCol(label = u"tranche d'aire urbaine")
    reg   = EnumCol()
    pol99 = EnumCol()
    cstotpragr = EnumCol(label = u"catégorie socio_professionelle agrégée de la personne de référence",
                         enum = Enum([u"Sans objet",
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
                                   u"Administrations"])) # 16 postes + 1 (17 sans objet) 
    
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
                     enum = Enum(['Bizarre' 
                                  u"Salarié",
                                  u"Indépendant",
                                  u"Chômeur",
                                  u"Retraité",
                                  u"Inactif"])) # 5 postes normalement TODO; check=0
    wprm_init = FloatCol()

## ISF ##
    
## Immeubles bâtis ##
    b1ab = IntCol() ##  valeur résidence principale avant abattement ##
    b1ac = IntCol()
## non bâtis ##
    b1bc = IntCol()
    b1be = IntCol()
    b1bh = IntCol()
    b1bk = IntCol() 
## droits sociaux- valeurs mobilières-liquidités- autres meubles ##

    b1cl = IntCol()
    b1cb = IntCol()
    b1cd = IntCol()
    b1ce = IntCol()
    b1cf = IntCol()
    b1cg = IntCol()

    b1co = IntCol()

#    b1ch
#    b1ci
#    b1cj
#    b1ck


## passifs et autres réduc ##
    b2gh= IntCol()
    
## réductions ##
    b2mt = IntCol()
    b2ne = IntCol()
    b2mv = IntCol()
    b2nf = IntCol()
    b2mx = IntCol()
    b2na = IntCol()
    b2nc = IntCol()

##  montant impôt acquitté hors de France ##
    b4rs = IntCol()

## BOUCLIER FISCAL ##

    rev_or= IntCol()
    rev_exo= IntCol()
    tax_hab= IntCol()
    tax_fonc= IntCol()
    restit_imp= IntCol()
        
    # to remove
    wprm = FloatCol()
    etr = IntCol()     
    coloc = BoolCol()
    csg_taux_plein = BoolCol(default = True)
    aer = IntCol()
    ass = IntCol()
    f5sq = IntCol()
