# -*- coding: utf-8 -*-
# ******************************************************************************
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
# ******************************************************************************

from PyQt5.QtGui import *
from qgis.core import *
from PyQt5.QtWidgets import QMessageBox, QAction

from .copy_coordstool import CopyCoordstool
from . import aboutdialog

# initialize resources (icons) from resources.py
from . import resources


class Copy_Coords:

    def __init__(self, iface):
        """Initialize class"""
        # save reference to QGIS interface
        self.iface = iface
        self.qgsVersion = unicode(Qgis.versionInt())
        self.helpIsActive = False

    def initGui(self):
        """Initialize graphic user interface"""

        # create action that will be run by the plugin
        self.action = QAction("Copy coordinates", self.iface.mainWindow())
        self.action.setIcon(QIcon(":/icons/cursor.png"))
        self.action.setWhatsThis("Copy coordinates")
        self.action.setStatusTip("Copy coordinates for pasting somewhere else")
        self.actionAbout = QAction('About', self.iface.mainWindow())
        self.actionAbout.setWhatsThis('About Copy Coords')

        # add plugin menu to Vector toolbar
        self.iface.addPluginToMenu("Copy_Coords", self.action)
        self.iface.addPluginToMenu("Copy_Coords", self.actionAbout)

        # add icon to new menu item in Vector toolbar
        self.iface.addToolBarIcon(self.action)

        # connect action to the run method
        self.action.triggered.connect(self.run)
        self.actionAbout.triggered.connect(self.about)

        # prepare map tool
        self.mapTool = CopyCoordstool(self.iface)
        # self.iface.mapCanvas().mapToolSet.connect(self.mapToolChanged)

    def unload(self):
        """Actions to run when the plugin is unloaded"""
        # remove menu and icon from the menu
        self.iface.removeToolBarIcon(self.action)
        self.iface.removePluginMenu("Copy_Coords", self.action)

        if self.iface.mapCanvas().mapTool() == self.mapTool:
            self.iface.mapCanvas().unsetMapTool(self.mapTool)

        del self.mapTool

    def run(self):
        """Action to run"""
        # create a string and show it

        self.iface.mapCanvas().setMapTool(self.mapTool)

    def about(self):
        dlg = aboutdialog.AboutDialog('copy_coords')
        dlg.exec_()

