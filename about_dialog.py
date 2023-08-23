import os

from qgis.PyQt.QtCore import QSettings, QUrl, QLocale, QTranslator, QFileInfo, QCoreApplication
from qgis.PyQt.QtGui import QDesktopServices, QTextDocument, QPixmap, QFont
from qgis.PyQt.QtWidgets import QDialogButtonBox, QDialog
from qgis.PyQt import uic
import qgis

FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'about_dialog_base.ui'))


class AboutDialog(QDialog, FORM_CLASS):
    def __init__(self, package_name):
        super().__init__()
        self.locale_short_name = 'en'
        self.setupUi(self)
        self.__init_locale()
        self.package_name = package_name
        font = QFont("MS Shell Dlg 2", 16)
        font.setBold(True)
        self.pluginName.setFont(font)
        replacemens = self.__replacemens()
        self.pluginName.setText(f'<p>{replacemens["{plugin_name}"]}</p>')
        self.setWindowTitle(
            self.windowTitle().format(plugin_name=replacemens['{plugin_name}']))
        html = self.textBrowser.toHtml()
        for key, value in replacemens.items():
            html = self.tr(html.replace(key, value))
        self.textBrowser.setHtml(html)
        self.textBrowser.setOpenLinks(True)
        self.textBrowser.setOpenExternalLinks(True)

    def locale(self):
        return self.locale_short_name

    def __init_locale(self):
        override_locale = QSettings().value('locale/overrideFlag', False, type=bool)
        if not override_locale:
            locale_full_name = QLocale.system().name()
        else:
            locale_full_name = QSettings().value('locale/userLocale', '')

        self.locale_short_name = locale_full_name[0:2]
        self.main_url = 'https://nextgis.ru' if self.locale_short_name in ['ru', 'uk'] else 'http://nextgis.com'

    def __replacemens(self):
        if self.locale() in ['ru', 'uk']:
            description = qgis.utils.pluginMetadata(f"{self.package_name}", "description_ru")
            about = ". ".join(qgis.utils.pluginMetadata(f"{self.package_name}", "about_ru").split("Разработан")[0:-1])
            link_video = qgis.utils.pluginMetadata(f"{self.package_name}", 'video_ru')
        else:
            description = qgis.utils.pluginMetadata(f"{self.package_name}", "description")
            about = ". ".join(qgis.utils.pluginMetadata(f"{self.package_name}", "about").split("Developed")[0:-1])
            link_video = qgis.utils.pluginMetadata(f"{self.package_name}", 'video')
        author = qgis.utils.pluginMetadata(f"{self.package_name}", "author")
        homepage = qgis.utils.pluginMetadata(f"{self.package_name}", "repository")
        tracker = qgis.utils.pluginMetadata(f"{self.package_name}", "tracker")
        plugin_name = qgis.utils.pluginMetadata(f"{self.package_name}", "name")
        replacemens = {
            '{developers_text}': self.tr("Developers:"),
            '{homepage_text}': self.tr('Homepage:'),
            '{video_text}': self.tr('Video with an overview of the plugin:'),
            '{bugs_text}': self.tr('Please report bugs at'),
            '{plugin_name}': plugin_name,
            '{description}': f'{description}',
            '{about}': f'{about}',
            # '{main_url}': f'<p>{main_url}</p>',
            '{author}': f'<a href="{self.main_url}">{author}</a>',
            '{link_video}': f'<a href="{link_video}">{link_video}</a>',
            '{homepage}': f'<a href="{homepage}">{homepage}</a>',
            '{tracker}': f'<a href="{tracker}">' + self.tr(f'bugtracker</a>'),
            '{other}': self.tr(f'Other helpful services by NextGIS:') +
                       self.tr(f'<ul><li><b>Convenient up-to-date data extracts for any place in the world: ') +
                       f'<a href="{self.main_url}">{self.main_url}</a></b></li>' +
                       self.tr(f'<li><b>Fully featured Web GIS service: ') +
                       f'<a href="https://nextgis.com/nextgis-com/plans">' +
                       f'https://nextgis.com/nextgis-com/plans</a></b></li></ul>',
        }
        return replacemens
