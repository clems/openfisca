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
    marpac = Prestation(fc.marpac, 'foy')
    celdiv = Prestation(fc.celdiv, 'foy')
    veuf = Prestation(fc.veuf, 'foy')
    jveuf = Prestation(fc.jveuf, 'foy')

    rbg = Prestation(fc.rbg, 'foy', label = u"Revenu brut global")
    rng = Prestation(fc.rng, 'foy', label = u"Revenu net global")
    rni = Prestation(fc.rni, 'foy', label = u"Revenu net imposable")
    
    abat_spe = Prestation(fc.abat_spe, 'foy', label = u"Abattements spéciaux")
    alloc = Prestation(fc.alloc, 'foy', label = u"Allocation familiale pour l'ir")
    deficit_ante = Prestation(fc.deficit_ante, 'foy', label = u"Déficit global antérieur")
    rev_cat = Prestation(fc.rev_cat, 'foy', label = u"Revenus catégoriels")
    nbptr = Prestation(fc.nbptr, 'foy', label = u"Nombre de parts")
    rev_sal = Prestation(fc.rev_sal)
    sal_net = Prestation(fc.sal_net)
    rev_pen = Prestation(fc.rev_pen)
    pen_net = Prestation(fc.pen_net)
    tspr = Prestation(fc.tspr)
    rev_cat_tspr = Prestation(fc.rev_cat_tspr, 'foy', label = u"Revenu catégoriel - Salaires, pensions et rentes")
    rev_cat_rvcm = Prestation(fc.rev_cat_rvcm, 'foy', label = u'Revenu catégoriel - Capitaux')
    rev_cat_rpns = Prestation(fc.rev_cat_rpns, 'foy', label = u'Revenu catégoriel - Rpns')
    rev_cat_rfon = Prestation(fc.rev_cat_rfon, 'foy', label = u'Revenu catégoriel - Foncier')
    rto_net = Prestation(fc.rto_net, 'foy', label = u'Rentes viagère après abattements')
    deficit_rcm = Prestation(fc.deficit_rcm, 'foy', u'Deficit capitaux mobiliers')
    csg_deduc = Prestation(fc.csg_deduc, 'foy', u'Csg déductible')
