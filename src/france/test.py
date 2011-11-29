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
from france.model import Model
from france.data import InputTable

    
if __name__ == '__main__':
    import datetime
    date = datetime.date(2010,01,01)
    reader = XmlReader('../data/param.xml', date)
    P = Tree2Object(reader.tree)

    f = '../castypes/2010 - Couple 3 enfants.ofct'
    scenario = Scenario()
    scenario.openFile(f)
        
    inputs = InputTable(6)
    inputs.populate_from_scenario(scenario)
    inputs.gen_index(['men', 'foy', 'fam'])

    model = Model(P)
    model.set_inputs(inputs)

#    model.calculate('irpp')

    model.calculate('irpp')
    model.calculate('aspa_elig')
    model.calculate('salsuperbrut')
    #model.calculate('paje') 
    model.calculate('af_nbenf')
    print inputs.sali.get_value()
    print model.salbrut.get_value()
    print model.csgsald.get_value()
#    print model.cho.get_value()
    print model.ars.get_value()
    # print model.paje.get_value()
    print model.af_nbenf.get_value()
    print model.aspa_elig.get_value()