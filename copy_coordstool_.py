# -*- coding: utf-8 -*-


from __future__ import absolute_import
from builtins import str
from qgis.PyQt.QtCore import *

from qgis.PyQt.QtGui import *
from PyQt5.QtWidgets import QMainWindow, QAction, QMenu, QApplication


from qgis.core import *

from qgis.gui import *



from . import resources

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

  

    crsSrc = self.canvas.mapSettings().destinationCrs()

    crsWGS = QgsCoordinateReferenceSystem(4326)



    QApplication.setOverrideCursor(Qt.WaitCursor)

    x = event.pos().x()

    y = event.pos().y()

    point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)

    #If Shift is pressed, convert coords to EPSG:4326

    if event.modifiers() == Qt.ShiftModifier:

        xform = QgsCoordinateTransform(crsSrc, crsWGS)

        point = xform.transform(QgsPoint(point.x(),point.y()))

    QApplication.restoreOverrideCursor()



    xx = str(point.x()) 

    yy = str(point.y())



    #QMessageBox.warning(self.iface.mainWindow(),xx,yy)

    clipboard = QApplication.clipboard()

    clipboard.setText(str(xx)+"\t"+str(yy))

