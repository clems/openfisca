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
import funcs as fc

class Model(SystemSf):
    etu      = Prestation(fc._etu, label = u"Indicatrice individuelle étudiant")
    biact    = Prestation(fc._biact, 'fam', label = u"Indicatrice de biactivité")
    concub   = Prestation(fc._concub, 'fam', label = u"Indicatrice de vie en couple") 
    nb_par   = Prestation(fc._nb_par, 'fam', label = u"Nombre de parents")
    
    rpns_fam = Prestation(fc._tspr_fam, 'fam', label = u"Traitements, salaires, pensions et rentes de la famille")
    tspr_fam = Prestation(fc._rpns_fam, 'fam', label = u"Revenus des personnes non salariés de la famille")
    rst_fam  = Prestation(fc._rst_fam, 'fam', label = u"Retraites au sens strict de la famille")
    
    af_nbenf = Prestation(fc._af_nbenf, 'fam', u"Nombre d'enfant au sens des AF")
    af_base  = Prestation(fc._af_base, 'fam', label ='Allocations familiales - Base')
    af_majo  = Prestation(fc._af_majo, 'fam', label ='Allocations familiales - Majoration pour age')
    af_forf  = Prestation(fc._af_forf, 'fam', label ='Allocations familiales - Forfait 20 ans')
    af       = Prestation(fc._af, 'fam', label = u"Allocations familiales")
    
    
    rev_pf   = Prestation(fc._rev_pf, 'fam', label ='Base ressource individuele des prestations familiales')
    br_pf    = Prestation(fc._br_pf, 'fam', label ='Base ressource des prestations familiales')
    cf_temp  = Prestation(fc._cf, 'fam', label = u"Complément familial avant d'éventuels cumuls")
    asf      = Prestation(fc._asf, 'fam', label = u"Allocation de soutien familial")
# TODO mensualisation âge    ars     = Prestation(ARS, 'fam', label = u"Allocation de rentrée scolaire")
    paje_base_temp = Prestation(fc._paje_base, 'fam', label = u"Allocation de base de la PAJE sans tenir compte d'éventuels cumuls")
    paje_base      = Prestation(fc._paje_cumul_cf, 'fam', label = u"Allocation de base de la PAJE")
    cf             = Prestation(fc._cf_cumul_paje, 'fam', label = u"Complément familial avant d'éventuels cumuls")
    paje_nais      = Prestation(fc._paje_nais, 'fam', label = u"Allocation de naissance de la PAJE")
    paje_clca      = Prestation(fc._paje_clca, 'fam', label = u"PAJE - Complément de libre choix d'activité")
    paje_clca_taux_plein      = Prestation(fc._paje_clca_taux_plein, 'fam', label = u"Indicatrice Clca taux plein")
    paje_clca_taux_partiel      = Prestation(fc._paje_clca_taux_partiel, 'fam', label = u"Indicatrice Clca taux partiel ")
    #paje_clmg        = Prestation(Paje_Clmg, 'fam', label = u"PAJE - Complément de libre choix du mode de garde")
    aeeh           = Prestation(fc._aeeh, 'fam', label = u"Allocation d'éducation de l'enfant handicapé")
