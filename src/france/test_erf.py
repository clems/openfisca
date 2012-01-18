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
import os
import numpy as np
from scipy import stats
from pylab import hist, setp, figure, show

from parametres.paramData import XmlReader, Tree2Object
from france.model import Model
from france.data import InputTable



if __name__ == '__main__':
    import datetime
    date = datetime.date(2006,01,01)
    reader = XmlReader('../data/param.xml', date)
    P = Tree2Object(reader.tree)
    P.datesim = date
    print P.datesim.year
    
    #print os.listdir('../../../cas/')
    
    # cas MBJ 
    filename = 'C:/Users/Utilisateur/Desktop/calmar/final.csv'
    # maison MBJ 
    #filename = '../../../cas/final.csv'
    
    inputs = InputTable()
    inputs.populate_from_external_data(filename)
    inputs.noi.get_value().shape

    inputs.ident.set_value(inputs.idmen.get_value()*100+inputs.noi.get_value(), inputs.index['ind'])

#    marge=dict(sali=np.array(497498908810.0), 
#               choi=np.array(24346459438.0), 
#               rsti=np.array(193174835599.0))


    marge = {'sali': 500000000000,
             'choi':  25000000000, 
             'rsti': 200000000000}

    param = {'method': 'logit', 'up':3, 'lo':.33}
    
    model = Model(P)
    model.set_inputs(inputs)
    
    inputs.gen_index(['men', 'fam', 'foy'])
    inputs.calibrate(marge,param=param)

    print 'sali weigthed sum', sum(inputs.sali.get_value()*inputs.wprm.get_value())
    print 'sali w. s. after calib', sum(inputs.sali.get_value()*inputs.pondfin.get_value())
    
    print 'choi weigthed sum', sum(inputs.choi.get_value()*inputs.wprm.get_value())
    print 'choi w. s. after calib', sum(inputs.choi.get_value()*inputs.pondfin.get_value())
    
    print 'rsti weigthed sum', sum(inputs.rsti.get_value()*inputs.wprm.get_value())
    print 'rsti w. s. after calib', sum(inputs.rsti.get_value()*inputs.pondfin.get_value())
    
    weight_ratio = inputs.pondfin.get_value()/inputs.wprm.get_value()
    
    print 'low ratios: ',  np.sort(weight_ratio)[1:5]
    print 'large ratios : ' ,  np.sort(weight_ratio)[-5:]

    n, bins, patches = hist(weight_ratio, 100, normed=1, histtype='stepfilled')
    setp(patches, 'facecolor', 'g', 'alpha', 0.75)
    show()

#    model.calculate('nbptr')
    model.calculate('irpp')
#            model.calculate('af')
#    model.calculate('cf')
#    print stats.itemfreq(inputs.statmarit.get_value())
#    print stats.itemfreq(model.nbptr.get_value())
#    print sum(model.af.get_value()*inputs.wprm.get_value())/1e9
#    print sum(model.cf.get_value()*inputs.wprm.get_value())/1e9
    print sum(model.irpp.get_value()*inputs.wprm.get_value())/1e9
    print sum(model.irpp.get_value()*inputs.pondfin.get_value())/1e9
#    model.as_csv('out.csv')