import os

from PyQt5.QtGui import QFont
from qgis.PyQt.QtCore import QSettings, QUrl, QLocale
from qgis.PyQt.QtGui import QDesktopServices, QTextDocument, QPixmap
from qgis.PyQt.QtWidgets import QDialogButtonBox, QDialog
from qgis.PyQt import uic
import qgis

FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'about_base.ui'))


class AboutDialog(QDialog, FORM_CLASS):
    def __init__(self, metadata_name='digitizr'):
        super().__init__()
        self.setupUi(self)
        self.metadata_name = metadata_name
        # self.btnHelp = self.buttonBox.button(QDialogButtonBox.Help)
        self.plugin_name.setText(f'<p>{qgis.utils.pluginMetadata(f"{self.metadata_name}", "name")}</p>')
        font = QFont("MS Shell Dlg 2", 16)
        font.setBold(True)
        self.plugin_name.setFont(font)
        doc = QTextDocument()
        self.setWindowTitle(self.windowTitle().format(plugin_name=qgis.utils.pluginMetadata(f"{self.metadata_name}", "name")))
        doc.setHtml(self.getAboutText())
        self.textBrowser.setDocument(doc)
        self.textBrowser.setOpenExternalLinks(True)
        # self.setWindowTitle(f'About {qgis.utils.pluginMetadata(f"{self.metadata_name}", "name")}')

        # self.buttonBox.helpRequested.connect(self.openHelp)


    def reject(self):
        QDialog.reject(self)

    def openHelp(self):
        overrideLocale = QSettings().value('locale/overrideFlag', False, type=bool)
        if not overrideLocale:
            localeFullName = QLocale.system().name()
        else:
            localeFullName = QSettings().value('locale/userLocale', '')

        localeShortName = localeFullName[0:2]
        if localeShortName in ['ru', 'uk']:
            QDesktopServices.openUrl(QUrl('https://nextgis.ru'))
        else:
            QDesktopServices.openUrl(QUrl('http://nextgis.com'))

    def getAboutText(self):
        return self.tr(f'<p>{qgis.utils.pluginMetadata(f"{self.metadata_name}", "description")}</p>'
                       f'<p>{qgis.utils.pluginMetadata(f"{self.metadata_name}", "about")}</p>'
                       '<p><strong>Developers</strong>: '
                       f'<a href="http://nextgis.org">{qgis.utils.pluginMetadata(f"{self.metadata_name}", "author")}</a></p>'
                       '<p><strong>Homepage</strong>: '
                       f'<a href="{qgis.utils.pluginMetadata(f"{self.metadata_name}", "repository")}">'
                       f'{qgis.utils.pluginMetadata(f"{self.metadata_name}", "repository")}</a></p>'
                       '<p>Please report bugs at '
                       f'<a href="{qgis.utils.pluginMetadata(f"{self.metadata_name}", "tracker")}">'
                       'bugtracker</a></p>'
                       '<p>Links on youtube: '
                       '<p>RU: '
                       f'<a href="{qgis.utils.pluginMetadata(f"{self.metadata_name}", "youtube_ru")}">' 
                       f'{qgis.utils.pluginMetadata(f"{self.metadata_name}", "youtube_ru")}</a></p>'
                       '<p>EN: '
                       f'<a href="{qgis.utils.pluginMetadata(f"{self.metadata_name}", "youtube_en")}">' 
                       f'{qgis.utils.pluginMetadata(f"{self.metadata_name}", "youtube_en")}</a></p>'
                       '<p>Other helpful services by NextGIS:</p>'
                       '<ul><li><b>Convenient up-to-date data extracts for any place in the world: <a href="https://data.nextgis.com">https://data.nextgis.com</a></b></li>'
                       '<li><b>Fully featured Web GIS service: <a href="https://nextgis.com/nextgis-com/plans">https://nextgis.com/nextgis-com/plans</a></b></li></ul>'
                       )
