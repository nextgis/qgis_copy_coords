# -*- coding: utf-8 -*-
#******************************************************************************
#
# Copy_Coords
# ---------------------------------------------------------
# This plugin takes coordinates of a mouse click and copies them to the table
#
# Copyright (C) 2013 Maxim Dubinin (sim@gis-lab.info), NextGIS (info@nextgis.org)
#
# This source is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# This code is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# A copy of the GNU General Public License is available on the World Wide Web
# at <http://www.gnu.org/licenses/>. You can also obtain it by writing
# to the Free Software Foundation, 51 Franklin Street, Suite 500 Boston,
# MA 02110-1335 USA.
#
#******************************************************************************

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *
from qgis.gui import *

import resources
import os
import tempfile
import platform

class CopyCoordstool(QgsMapTool):
  def __init__(self, iface):
    QgsMapTool.__init__(self, iface.mapCanvas())

    self.canvas = iface.mapCanvas()
    #self.emitPoint = QgsMapToolEmitPoint(self.canvas)
    self.iface = iface

    self.cursor = QCursor(QPixmap(":/icons/cursor.png"), 1, 1)

  def activate(self):
    self.canvas.setCursor(self.cursor)

  def canvasReleaseEvent(self, event):

    QApplication.setOverrideCursor(Qt.WaitCursor)
    x = event.pos().x()
    y = event.pos().y()
    point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
    QApplication.restoreOverrideCursor()

    xx = str(point.x()) 
    yy = str(point.y())

    #QMessageBox.warning(self.iface.mainWindow(),xx,yy)
    clipboard = QApplication.clipboard()
    clipboard.setText(str(xx)+"\t"+str(yy))
