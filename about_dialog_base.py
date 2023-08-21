import os

from PyQt5.QtCore import QTranslator, QFileInfo, QCoreApplication
from qgis.PyQt.QtCore import QSettings, QUrl, QLocale
from qgis.PyQt.QtGui import QDesktopServices, QTextDocument, QPixmap, QFont
from qgis.PyQt.QtWidgets import QDialogButtonBox, QDialog
from qgis.PyQt import uic
import qgis

FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'about_dialog_base.ui'))


class AboutDialog(QDialog, FORM_CLASS):
    def __init__(self, package_name):
        super().__init__()
        self.setupUi(self)
        self.__init_locale()
        self.package_name = package_name
        self.pluginName.setText(f'<p>{qgis.utils.pluginMetadata(f"{self.package_name}", "name")}</p>')
        font = QFont("MS Shell Dlg 2", 16)
        font.setBold(True)
        self.pluginName.setFont(font)
        self.setWindowTitle(
            self.windowTitle().format(plugin_name=qgis.utils.pluginMetadata(f"{self.package_name}", "name")))
        replacemens = self.replacemens()
        html = self.textBrowser.toHtml()
        for key, value in replacemens.items():
            html = self.tr(html.replace(key, value))
        self.textBrowser.setHtml(html)
        self.textBrowser.setOpenLinks(True)
        self.textBrowser.setOpenExternalLinks(True)

        _current_path = os.path.abspath(os.path.dirname(__file__))
        locale_full_name = QSettings().value('locale/userLocale', '')
        translation_path = os.path.join(_current_path, 'i18n', 'about_base_' + locale_full_name + '.qm')

        self.locale_path = translation_path
        self.translator = QTranslator()
        self.translator.load(self.locale_path)
        print(self.locale_path)
        QCoreApplication.installTranslator(self.translator)

    def __init_locale(self):
        override_locale = QSettings().value('locale/overrideFlag', False, type=bool)
        if not override_locale:
            locale_full_name = QLocale.system().name()
        else:
            locale_full_name = QSettings().value('locale/userLocale', '')

        locale_short_name = locale_full_name[0:2]
        self.main_url = 'https://nextgis.ru' if locale_short_name in ['ru', 'uk'] else 'http://nextgis.com'

    def replacemens(self):
        description = qgis.utils.pluginMetadata(f"{self.package_name}", "description")
        about = ". ".join(qgis.utils.pluginMetadata(f"{self.package_name}", "about").split("Developed")[0:-1])
        author = qgis.utils.pluginMetadata(f"{self.package_name}", "author")
        link_video = qgis.utils.pluginMetadata(f"{self.package_name}",
                                               'video_ru' if self.main_url.endswith('.ru') else 'video_en')
        homepage = qgis.utils.pluginMetadata(f"{self.package_name}", "repository")
        tracker = qgis.utils.pluginMetadata(f"{self.package_name}", "tracker")
        replacemens = {
            '{description}': f'{description}',
            '{about}': f'{about}',
            # '{main_url}': f'<p>{main_url}</p>',
            '{author}': f'<a href="{self.main_url}">{author}</a>',
            '{link_video}': f'<a href="{link_video}">{link_video}</a>',
            '{homepage}': f'<a href="{homepage}">{homepage}</a>',
            '{tracker}': f'<a href="{tracker}">bugtracker</a>',
            '{other}': self.tr('Other helpful services by NextGIS:'
                               f'<ul><li><b>Convenient up-to-date data extracts for any place in the world: '
                               f'<a href="{self.main_url}">{self.main_url}</a></b></li>'
                               f'<li><b>Fully featured Web GIS service: '
                               f'<a href="https://nextgis.com/nextgis-com/plans">'
                               f'https://nextgis.com/nextgis-com/plans</a></b></li></ul>'),
        }
        return replacemens
