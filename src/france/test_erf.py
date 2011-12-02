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
from france.model import Model
from france.data import InputTable
import numpy as np
from scipy import stats

if __name__ == '__main__':
    import datetime
    date = datetime.date(2006,01,01)
    reader = XmlReader('../data/param.xml', date)
    P = Tree2Object(reader.tree)

    filename = '../../../../Documents/Data/R/erf/2006/final.csv'
        
    inputs = InputTable()
    inputs.populate_from_external_data(filename)

    print inputs.sali.get_value().shape
    print inputs.sali.get_value().sum()

    model = Model(P)
    model.set_inputs(inputs)

    model.calculate('nbptr')
    model.calculate('irpp')
    model.calculate('af')
    model.calculate('cf')
    print stats.itemfreq(model.nbptr.get_value())
    print sum(model.af.get_value()*inputs.wprm.get_value())/1e9
    print sum(model.cf.get_value()*inputs.wprm.get_value())/1e9
    print sum(model.irpp.get_value()*inputs.wprm.get_value())/1e9
