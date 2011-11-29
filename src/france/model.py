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

from core.systemsf import SystemSf, Prestation
import irpp as ir
import france.pfam.funcs as pf
import france.cotsoc as cs

class Model(SystemSf):
    # variables pour les cotisations sociales
    salbrut = Prestation(cs._salbrut)
    sal_h_b = Prestation(cs._sal_h_b)
    cotpat  = Prestation(cs._cotpat)
    alleg_fillon = Prestation(cs._alleg_fillon)
    cotsal  = Prestation(cs._cotsal)
    csgsald = Prestation(cs._csgsald)
    csgsali = Prestation(cs._csgsali)
    sal = Prestation(cs._sal)
    
    salsuperbrut = Prestation(cs._salsuperbrut)
    
    chobrut = Prestation(cs._chobrut)
    csgchod = Prestation(cs._csgchod)
    csgchoi = Prestation(cs._csgchoi)
    cho = Prestation(cs._cho)

    rstbrut = Prestation(cs._rstbrut)
    csgrstd = Prestation(cs._csgrstd)
    csgrsti = Prestation(cs._csgrsti)
    rst = Prestation(cs._rst)
    # variables pour l'ir
    marpac = Prestation(ir._marpac, 'foy')
    celdiv = Prestation(ir._celdiv, 'foy')
    veuf = Prestation(ir._veuf, 'foy')
    jveuf = Prestation(ir._jveuf, 'foy')

    rbg = Prestation(ir._rbg, 'foy', label = u"Revenu brut global")
    rng = Prestation(ir._rng, 'foy', label = u"Revenu net global")
    rni = Prestation(ir._rni, 'foy', label = u"Revenu net imposable")
    
    abat_spe = Prestation(ir._abat_spe, 'foy', label = u"Abattements spéciaux")
    alloc = Prestation(ir._alloc, 'foy', label = u"Allocation familiale pour l'ir")
    deficit_ante = Prestation(ir._deficit_ante, 'foy', label = u"Déficit global antérieur")
    rev_cat = Prestation(ir._rev_cat, 'foy', label = u"Revenus catégoriels")
    nbptr = Prestation(ir._nbptr, 'foy', label = u"Nombre de parts")
    rev_sal = Prestation(ir._rev_sal)
    sal_net = Prestation(ir._sal_net)
    rev_pen = Prestation(ir._rev_pen)
    pen_net = Prestation(ir._pen_net)
    tspr = Prestation(ir._tspr)
    rev_cat_tspr = Prestation(ir._rev_cat_tspr, 'foy', label = u"Revenu catégoriel - Salaires, pensions et rentes")
    rev_cat_rvcm = Prestation(ir._rev_cat_rvcm, 'foy', label = u'Revenu catégoriel - Capitaux')
    rev_cat_rpns = Prestation(ir._rev_cat_rpns, 'foy', label = u'Revenu catégoriel - Rpns')
    rev_cat_rfon = Prestation(ir._rev_cat_rfon, 'foy', label = u'Revenu catégoriel - Foncier')
    rto = Prestation(ir._rto, 'foy', label = u'Rentes viagères (rentes à titre onéreux)')
    rto_net = Prestation(ir._rto_net, 'foy', label = u'Rentes viagères après abattements')
    deficit_rcm = Prestation(ir._deficit_rcm, 'foy', u'Deficit capitaux mobiliers')
    csg_deduc = Prestation(ir._csg_deduc, 'foy', u'Csg déductible')
    
    plus_values = Prestation(ir._plus_values, 'foy')
    ir_brut = Prestation(ir._ir_brut, 'foy')
    nb_pac = Prestation(ir._nb_pac, 'foy')
    nb_adult = Prestation(ir._nb_adult, 'foy')
    ir_plaf_qf = Prestation(ir._ir_plaf_qf, 'foy')
    nat_imp = Prestation(ir._nat_imp, 'foy')
    decote = Prestation(ir._decote, 'foy')
    ip_net = Prestation(ir._ip_net, 'foy')
    iaidrdi = Prestation(ir._iaidrdi, 'foy')
    teicaa = Prestation(ir._teicaa, 'foy')
    cont_rev_loc = Prestation(ir._cont_rev_loc, 'foy')
    iai = Prestation(ir._iai, 'foy')
    tehr = Prestation(ir._tehr, 'foy')

    ppe_coef = Prestation(ir._ppe_coef)
    ppe_base = Prestation(ir._ppe_base)
    ppe_coef_tp = Prestation(ir._ppe_coef_tp)
    ppe_elig = Prestation(ir._ppe_elig)
    ppe_elig_i = Prestation(ir._ppe_elig_i)
    ppe_rev = Prestation(ir._ppe_rev)
    ppe = Prestation(ir._ppe, 'foy')
    irpp = Prestation(ir._irpp, 'foy')

    rfr = Prestation(ir._rfr, 'foy')

    div_rmi  = Prestation(ir._div_rmi, 'foy')
    rev_coll = Prestation(ir._rev_coll, 'foy')
#    alv = Prestation(ir._alv)
    glo = Prestation(ir._glo, 'foy')
    rag  = Prestation(ir._rag)
    ric  = Prestation(ir._ric)
    rac  = Prestation(ir._rac)
    rnc  = Prestation(ir._rnc)
    rpns = Prestation(ir._rpns)
    div  = Prestation(ir._div, 'foy')
    fon  = Prestation(ir._fon, 'foy')
    rfon_rmi = Prestation(ir._rfon_rmi, 'foy')
    
    rpns_mvct = Prestation(ir._rpns_mvct)
    rpns_pvct = Prestation(ir._rpns_pvct)
    rpns_mvlt = Prestation(ir._rpns_mvlt)
    rpns_pvce = Prestation(ir._rpns_pvce)
    rpns_exon = Prestation(ir._rpns_exon)
    
    rev_cap_bar = Prestation(ir._rev_cap_bar, 'foy')
    rev_cap_lib = Prestation(ir._rev_cap_lib, 'foy')
    avf = Prestation(ir._avf, 'foy')
    
# variables pour les prestations familiales
    etu      = Prestation(pf._etu, label = u"Indicatrice individuelle étudiant")
    biact    = Prestation(pf._biact, 'fam', label = u"Indicatrice de biactivité")
    concub   = Prestation(pf._concub, 'fam', label = u"Indicatrice de vie en couple") 
    maries   = Prestation(pf._maries, 'fam') 
    nb_par   = Prestation(pf._nb_par, 'fam', label = u"Nombre de parents")
    smic55   = Prestation(pf._smic55, 'fam', label = u"Indicatrice d'un salaire supérieur à 55% du smic")
    
    af_nbenf = Prestation(pf._af_nbenf, 'fam', u"Nombre d'enfant au sens des AF")
    af_base  = Prestation(pf._af_base, 'fam', label ='Allocations familiales - Base')
    af_majo  = Prestation(pf._af_majo, 'fam', label ='Allocations familiales - Majoration pour age')
    af_forf  = Prestation(pf._af_forf, 'fam', label ='Allocations familiales - Forfait 20 ans')
    af       = Prestation(pf._af, 'fam', label = u"Allocations familiales")
    
    rev_pf   = Prestation(pf._rev_pf, 'fam', label ='Base ressource individuele des prestations familiales')
    br_pf    = Prestation(pf._br_pf, 'fam', label ='Base ressource des prestations familiales')
    cf_temp  = Prestation(pf._cf, 'fam', label = u"Complément familial avant d'éventuels cumuls")
    asf      = Prestation(pf._asf, 'fam', label = u"Allocation de soutien familial")

# TODO mensualisation âge    ars     = Prestation(ARS, 'fam', label = u"Allocation de rentrée scolaire")
    paje_base_temp = Prestation(pf._paje_base, 'fam', label = u"Allocation de base de la PAJE sans tenir compte d'éventuels cumuls")
    paje_base      = Prestation(pf._paje_cumul_cf, 'fam', label = u"Allocation de base de la PAJE")
    cf             = Prestation(pf._cf_cumul_paje, 'fam', label = u"Complément familial avant d'éventuels cumuls")
    paje_nais      = Prestation(pf._paje_nais, 'fam', label = u"Allocation de naissance de la PAJE")
    paje_clca      = Prestation(pf._paje_clca, 'fam', label = u"PAJE - Complément de libre choix d'activité")
    paje_clca_taux_plein   = Prestation(pf._paje_clca_taux_plein, 'fam', label = u"Indicatrice Clca taux plein")
    paje_clca_taux_partiel = Prestation(pf._paje_clca_taux_partiel, 'fam', label = u"Indicatrice Clca taux partiel ")
    paje_colca     = Prestation(pf._paje_colca, 'fam', label = u"PAJE - Complément optionnel de libre choix d'activité")
    paje_clmg        = Prestation(pf._paje_clmg, 'fam', label = u"PAJE - Complément de libre choix du mode de garde")
    aeeh           = Prestation(pf._aeeh, 'fam', label = u"Allocation d'éducation de l'enfant handicapé")
    
    ape            = Prestation(pf._ape, 'fam', label = u"Allocation parentale d'éducation")
    apje           = Prestation(pf._apje, 'fam', label = u"Allocation pour le jeune enfant") 
    
    asf_elig = Prestation(ir._asf_elig, 'foy')

    # Allocations logement
    br_al  = Prestation(pf._br_al, 'fam', label = u"Base ressource des allocations logement")
    al_pac = Prestation(pf._al_pac, 'fam', label = u"Nombre de personnes à charge au sens des allocations logement")  
    al     = Prestation(pf._al, 'fam', label = u"Allocation logement (indifferrenciée)")
    alf    = Prestation(pf._alf, 'fam', label = u"Allocation logement familiale")
    als    = Prestation(pf._als, 'fam', label = u"Allocation logement sociale")
    alset  = Prestation(pf._alset, 'fam', label = u"Allocation logement sociale étudiante")
    
    # RSA/RMI
    rmi_nbp = Prestation(pf._rmi_nbp, 'fam', label = u"Nombre de personne à charge au sens du Rmi/Rsa")
    br_rmi  = Prestation(pf._br_rmi, 'fam', label = u"Base ressources du Rmi/Rsa")
    ra_rsa  = Prestation(pf._ra_rsa, 'fam', label = u"Revenus d'activité du Rsa")
    rsa  = Prestation(pf._ra_rsa, 'fam')
    
    
    # ASPA/ASI
    br_mv   = Prestation(pf._br_mv, 'fam', label = u"Base ressources du minimum vieillesse/ASPA")
    
    asi_aspa_nb_alloc = Prestation(pf._asi_aspa_nb_alloc, 'fam')
    asi_aspa_elig = Prestation(pf._asi_elig, 'fam')
    asi_elig = Prestation(pf._asi_elig, label = u"Indicatrice individuelle d'éligibilité à l'allocation supplémentaire d'invalidité")           
    asi_coexist_aspa = Prestation(pf._asi_coexist_aspa, 'fam', label = u"Allocation supplémentaire d'invalidité quand un adulte de la famille perçoit l'ASPA")
    asi_pure         = Prestation(pf._asi_pure, 'fam', label = u"Allocation supplémentaire d'invalidité quand aucun adulte de la famille ne perçoit l'ASPA") 
    asi     = Prestation(pf._asi, 'fam', label = u"Allocation supplémentaire d'invalidité")
    
    aspa_elig = Prestation(pf._asi_elig, label = u"Indicatrice individuelle d'éligibilité à l'allocation de solidarité aux personnes agées")
    aspa_coexist_asi  = Prestation(pf._aspa_coexist_asi, 'fam', label = u"Allocation de solidarité aux personnes agées quand un adulte de la famille perçoit l'ASI")
    aspa_pure         = Prestation(pf._aspa_pure, 'fam', label = u"Allocation de solidarité aux personnes agées quand aucun adulte de la famille ne perçoit l'ASI") 
    mv     = Prestation(pf._aspa, 'fam', label = u"Allocation de solidarité aux personnes agées")
    
    # AAH
    br_aah  = Prestation(pf._br_aah, 'fam', label = u"Base ressources de l'allocation adulte handicapé")
    aah     = Prestation(pf._aah, 'fam', label = u"Allocation adulte handicapé")
    caah    = Prestation(pf._caah, 'fam', label = u"Complément de l'allocation adulte handicapé")
