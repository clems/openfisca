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

from parametres.paramData import XmlReader, Tree2Object
from Utils import Scenario
from model import Model
from france.data import InputTable

    
if __name__ == '__main__':
    import datetime
    date = datetime.date(2010,01,01)
    reader = XmlReader('../../data/param.xml', date)
    P = Tree2Object(reader.tree)

    f = '../../castypes/2010 - Couple 3 enfants.ofct'
    scenario = Scenario()
    scenario.openFile(f)
    
    
    inputs = InputTable(6)
    inputs.populate_from_scenario(scenario, date)
    inputs.gen_index(['men', 'foy', 'fam'])    

    pfam = Model(P)
    pfam.set_inputs(inputs)
    pfam.calculate('af')
    pfam.calculate('cf_temp')
    pfam.calculate('asf')
    #pfam.calculate('ars')
    pfam.calculate('paje_base_temp')
    pfam.calculate('cf')
    pfam.calculate('paje_base')
    pfam.calculate('paje_nais')
    pfam.calculate('paje_clca')
    pfam.calculate('paje_clca_taux_plein')
    pfam.calculate('paje_clca_taux_partiel')
    #pfam.calculate('paje_clmg')
    pfam.calculate('aeeh')
    
    print inputs.age.get_value()
    print pfam.af.get_value()
    print pfam.af_nbenf.get_value()
    print pfam.af_base.get_value()
    print pfam.cf_temp.get_value()
    print pfam.cf.get_value()
    print pfam.asf.get_value()
    #print pfam.ars.get_value()
    print pfam.paje_base.get_value()
    print pfam.paje_nais.get_value()
    print pfam.paje_clca.get_value()
    print pfam.paje_clca_taux_plein.get_value()
    print pfam.paje_clca_taux_partiel.get_value()
    #print pfam.paje_clmg.get_value()
    print pfam.aeeh.get_value()