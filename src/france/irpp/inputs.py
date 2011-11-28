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

from core.datatable import DataTable, IntCol, EnumCol, BoolCol, FloatCol, AgesCol
from france.data import QUIMEN, QUIFOY, QUIFAM

class InputTable(DataTable):
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
    
    sal = IntCol()
    cho = IntCol()
    rst = IntCol()
    fra = IntCol()
    alr = IntCol()
    
    hsup = IntCol()
    inv = BoolCol()
    alt = BoolCol()
    choCheckBox = BoolCol()
    ppeCheckBox = BoolCol()
    ppeHeure = IntCol()
    age = AgesCol()
    agem = AgesCol()
    zone_apl = IntCol()
    loyer = IntCol()
    so = IntCol(default = 3)
    activite = IntCol()
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
    # RVCM
    f2ch = IntCol()
    f2dc = IntCol()
    f2ts = IntCol()
    f2ca = IntCol()
    f2fu = IntCol()
    f2go = IntCol()
    f2tr = IntCol()
    
    f2aa = IntCol()
    f2al = IntCol()
    f2am = IntCol()
    f2an = IntCol()
    
    
    f3vc = IntCol()
    f3vd = IntCol()
    f3ve = IntCol()
    f3vf = IntCol()
    f3vg = IntCol()
    f3vh = IntCol()
    f3vl = IntCol()
    f3vi = IntCol()
    f3vm = IntCol()
    
    # Revenu foncier
    f4ba = IntCol()
    f4bb = IntCol()
    f4bc = IntCol()
    f4bd = IntCol()
    f4be = IntCol()
    
    f4bl = IntCol()
    
    f5qm = IntCol()
    f5rm = IntCol()
    
    # Deficit Antérieur
    f6fa = IntCol()
    f6fb = IntCol()
    f6fc = IntCol()
    f6fd = IntCol()
    f6fe = IntCol()
    f6fl = IntCol()
    
    f6gh = IntCol()
    f6de = IntCol()

    # from elsewhere
    af = FloatCol()

    # to remove
    charges_deduc = IntCol()
    reductions = IntCol()
    rpns_pvce = IntCol()
    