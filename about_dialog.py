import os

from qgis.PyQt.QtCore import QSettings, QLocale
from qgis.PyQt.QtWidgets import QDialog
from qgis.PyQt import uic
from qgis.utils import pluginMetadata

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "about_dialog_base.ui")
)


class AboutDialog(QDialog, FORM_CLASS):
    def __init__(self, package_name):
        super().__init__()
        self.locale_short_name = "en"
        self.setupUi(self)
        self.package_name = package_name
        replacemens = self.__replacemens()
        self.pluginName.setText(self.pluginName.text().replace(
            "{plugin_name}", replacemens["{plugin_name}"])
        )
        self.setWindowTitle(
            self.windowTitle().format(
                plugin_name=replacemens["{plugin_name}"]
            )
        )
        html = self.textBrowser.toHtml()
        for key, value in replacemens.items():
            html = html.replace(key, value)
        self.textBrowser.setHtml(html)

    def __locale(self):
        override_locale = QSettings().value(
            "locale/overrideFlag", False, type=bool
        )
        if not override_locale:
            locale_full_name = QLocale.system().name()
        else:
            locale_full_name = QSettings().value("locale/userLocale", "")

        return locale_full_name[0:2]

    def __replacemens(self):
        is_ru = self.__locale() in ["ru", "uk"]
        main_url = (
            "https://nextgis.ru"
            if is_ru in ["ru", "uk"]
            else "http://nextgis.com"
        )
        description = pluginMetadata(
            self.package_name, "description_ru" if is_ru else "description"
        )
        about = pluginMetadata(
            self.package_name, "about_ru" if is_ru else "about"
        )
        about_stop_phrase = "Разработан компанией" if is_ru else "Developed by"
        about = about[:about.find(about_stop_phrase)]
        video_url = pluginMetadata(
            self.package_name, "video_ru" if is_ru else "video"
        )
        author = pluginMetadata(self.package_name, "author")
        homepage_url = pluginMetadata(self.package_name, "repository")
        tracker = pluginMetadata(self.package_name, "tracker")
        plugin_name = pluginMetadata(self.package_name, "name")
        replacemens = {
            "{plugin_name}": plugin_name,
            "{description}": description,
            "{about}": about,
            "{authors}": author,
            "{video_url}": video_url,
            "{homepage_url}": homepage_url,
            "{tracker_url}": tracker,
            "{main_url}": main_url,
        }
        return replacemens
