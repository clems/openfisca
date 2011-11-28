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
    marpac = Prestation(fc._marpac, 'foy')
    celdiv = Prestation(fc._celdiv, 'foy')
    veuf = Prestation(fc._veuf, 'foy')
    jveuf = Prestation(fc._jveuf, 'foy')

    rbg = Prestation(fc._rbg, 'foy', label = u"Revenu brut global")
    rng = Prestation(fc._rng, 'foy', label = u"Revenu net global")
    rni = Prestation(fc._rni, 'foy', label = u"Revenu net imposable")
    
    abat_spe = Prestation(fc._abat_spe, 'foy', label = u"Abattements spéciaux")
    alloc = Prestation(fc._alloc, 'foy', label = u"Allocation familiale pour l'ir")
    deficit_ante = Prestation(fc._deficit_ante, 'foy', label = u"Déficit global antérieur")
    rev_cat = Prestation(fc._rev_cat, 'foy', label = u"Revenus catégoriels")
    nbptr = Prestation(fc._nbptr, 'foy', label = u"Nombre de parts")
    rev_sal = Prestation(fc._rev_sal)
    sal_net = Prestation(fc._sal_net)
    rev_pen = Prestation(fc._rev_pen)
    pen_net = Prestation(fc._pen_net)
    tspr = Prestation(fc._tspr)
    rev_cat_tspr = Prestation(fc._rev_cat_tspr, 'foy', label = u"Revenu catégoriel - Salaires, pensions et rentes")
    rev_cat_rvcm = Prestation(fc._rev_cat_rvcm, 'foy', label = u'Revenu catégoriel - Capitaux')
    rev_cat_rpns = Prestation(fc._rev_cat_rpns, 'foy', label = u'Revenu catégoriel - Rpns')
    rev_cat_rfon = Prestation(fc._rev_cat_rfon, 'foy', label = u'Revenu catégoriel - Foncier')
    rto_net = Prestation(fc._rto_net, 'foy', label = u'Rentes viagère après abattements')
    deficit_rcm = Prestation(fc._deficit_rcm, 'foy', u'Deficit capitaux mobiliers')
    csg_deduc = Prestation(fc._csg_deduc, 'foy', u'Csg déductible')
    
    plus_values = Prestation(fc._plus_values, 'foy')
    ir_brut = Prestation(fc._ir_brut, 'foy')
    nb_pac = Prestation(fc._nb_pac, 'foy')
    nb_adult = Prestation(fc._nb_adult, 'foy')
    ir_plaf_qf = Prestation(fc._ir_plaf_qf, 'foy')
    nat_imp = Prestation(fc._nat_imp, 'foy')
    decote = Prestation(fc._decote, 'foy')
    ip_net = Prestation(fc._ip_net, 'foy')
    iaidrdi = Prestation(fc._iaidrdi, 'foy')
    teicaa = Prestation(fc._teicaa, 'foy')
    cont_rev_loc = Prestation(fc._cont_rev_loc, 'foy')
    iai = Prestation(fc._iai,'foy')
