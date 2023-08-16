import os

from PyQt5.QtGui import QFont
from qgis.PyQt.QtCore import QSettings, QUrl, QLocale
from qgis.PyQt.QtGui import QDesktopServices, QTextDocument, QPixmap
from qgis.PyQt.QtWidgets import QDialogButtonBox, QDialog
from qgis.PyQt import uic
import qgis

FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'about_base.ui'))


class AboutDialog(QDialog, FORM_CLASS):
    def __init__(self, metadata_name):
        super().__init__()
        self.setupUi(self)
        self.__init__locale()
        self.metadata_name = metadata_name
        self.pluginName.setText(f'<p>{qgis.utils.pluginMetadata(f"{self.metadata_name}", "name")}</p>')
        font = QFont("MS Shell Dlg 2", 16)
        font.setBold(True)
        self.pluginName.setFont(font)
        self.setWindowTitle(
            self.windowTitle().format(plugin_name=qgis.utils.pluginMetadata(f"{self.metadata_name}", "name")))
        replacemens = self.getReplacemens()
        html = self.textBrowser.toHtml()
        for key, value in replacemens.items():
            html = html.replace(key, value)
        self.textBrowser.setHtml(html)
        self.textBrowser.setOpenLinks(True)
        self.textBrowser.setOpenExternalLinks(True)

    def __init__locale(self):
        overrideLocale = QSettings().value('locale/overrideFlag', False, type=bool)
        if not overrideLocale:
            localeFullName = QLocale.system().name()
        else:
            localeFullName = QSettings().value('locale/userLocale', '')

        localeShortName = localeFullName[0:2]
        self.main_url = 'https://nextgis.ru' if localeShortName in ['ru', 'uk'] else 'http://nextgis.com'

    def getReplacemens(self):
        description = qgis.utils.pluginMetadata(f"{self.metadata_name}", "description")
        about = ". ".join(qgis.utils.pluginMetadata(f"{self.metadata_name}", "about").split("Developed")[0:-1])
        author = qgis.utils.pluginMetadata(f"{self.metadata_name}", "author")
        link_video = qgis.utils.pluginMetadata(f"{self.metadata_name}",
                                               'video_ru' if self.main_url.split('.')[-1] == 'ru' else 'video_en')
        homepage = qgis.utils.pluginMetadata(f"{self.metadata_name}", "repository")
        tracker = qgis.utils.pluginMetadata(f"{self.metadata_name}", "tracker")
        replacemens = {
            '{description}': f'{description}',
            '{about}': f'{about}',
            # '{main_url}': f'<p>{main_url}</p>',
            '{author}': f'<a href="{self.main_url}">{author}</a>',
            '{link_video}': f'<a href="{link_video}">{link_video}</a>',
            '{homepage}': f'<a href="{homepage}">{homepage}</a>',
            '{tracker}': f'<a href="{tracker}">bugtracker</a>',
            '{other}': 'Other helpful services by NextGIS:'
                       f'<ul><li><b>Convenient up-to-date data extracts for any place in the world: <a href="{self.main_url}">{self.main_url}</a></b></li>'
                       f'<li><b>Fully featured Web GIS service: <a href="https://nextgis.com/nextgis-com/plans">https://nextgis.com/nextgis-com/plans</a></b></li></ul>',
        }
        return replacemens