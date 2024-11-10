import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QLineEdit, QPushButton, QWidget, QHBoxLayout, QToolBar, QLabel, QDialog, QDialogButtonBox
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest


class BrowserTab(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.setUrl(QUrl("https://www.yahoo.com"))


class ThemeSelectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("selection themeing")

        layout = QVBoxLayout()
        self.green_theme_btn = QPushButton("BUTIFEL THEIME (Current Theme)")
        self.green_theme_btn.setStyleSheet("background-color: #00FF00; color: hotpink; font-family: Papyrus; font-size: 14px;")
        layout.addWidget(self.green_theme_btn)

        self.inverted_theme_btn = QPushButton("ALSO BUTIFEL THEIME")
        self.inverted_theme_btn.setStyleSheet("background-color: black; color: white; font-family: Papyrus; font-size: 14px;")
        layout.addWidget(self.inverted_theme_btn)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(self.button_box)

        self.green_theme_btn.clicked.connect(self.apply_green_theme)
        self.inverted_theme_btn.clicked.connect(self.apply_inverted_theme)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.setLayout(layout)

    def apply_green_theme(self):
        self.parent().change_theme("green")

    def apply_inverted_theme(self):
        self.parent().change_theme("inverted")


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("shitscape browser")
        self.setGeometry(200, 200, 1200, 800)

        self.current_theme = "green"

        self.main_layout = QVBoxLayout()

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.add_new_tab(QUrl("https://www.yahoo.com"), "nEW TAB")

        self.toolbar = QToolBar()
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)

        # Create navigation buttons
        back_btn = QPushButton("NOT TELLING U")
        forward_btn = QPushButton("THIS TOO")
        reload_btn = QPushButton("😃")
        back_btn.clicked.connect(lambda: self.tabs.currentWidget().back())
        forward_btn.clicked.connect(lambda: self.tabs.currentWidget().forward())
        reload_btn.clicked.connect(lambda: self.tabs.currentWidget().reload())
        self.toolbar.addWidget(back_btn)
        self.toolbar.addWidget(forward_btn)
        self.toolbar.addWidget(reload_btn)

        # Create URL bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.url_bar.setStyleSheet("background-color: yellow; font-family: Papyrus; font-size: 16px;")
        self.toolbar.addWidget(self.url_bar)

        # Create "Change Theme" button
        theme_btn = QPushButton("CHEGNE THEIME")
        theme_btn.clicked.connect(self.open_theme_dialog)
        self.toolbar.addWidget(theme_btn)

        # Create "New Tab" button
        new_tab_btn = QPushButton("ADD A TAB LOL")
        new_tab_btn.clicked.connect(self.add_new_tab_button_clicked)
        self.toolbar.addWidget(new_tab_btn)

        # Sidebar setup (image and text)
        self.image_sidebar = QLabel()
        self.image_sidebar.setVisible(False)  # Initially hidden
        self.load_image_from_url("https://camo.githubusercontent.com/2dac725347f0b07fba8535a78d16a08f1bb1dfe1f75c27173cd80ab4c530c3ca/68747470733a2f2f73746f726167652e70726f626f617264732e636f6d2f363531333538312f696d616765732f704a4562776f796a5946665a4a47445075546f562e706e67")  # Replace with correct URL if needed

        self.sidebar_text = QLabel("shitscape browser")
        self.sidebar_text.setFont(QFont("Papyrus", 28, QFont.StyleItalic))
        self.sidebar_text.setStyleSheet("color: blue; font-family: Papyrus; font-size: 28px;")
        self.sidebar_text.setAlignment(Qt.AlignCenter)

        main_content_layout = QVBoxLayout()
        main_content_layout.addWidget(self.toolbar)
        main_content_layout.addWidget(self.tabs)

        main_content_container = QWidget()
        main_content_container.setLayout(main_content_layout)

        sidebar_layout = QVBoxLayout()
        sidebar_layout.addWidget(self.sidebar_text)
        sidebar_layout.addWidget(self.image_sidebar)

        sidebar_container = QWidget()
        sidebar_container.setLayout(sidebar_layout)

        top_layout = QHBoxLayout()
        top_layout.addWidget(main_content_container)
        top_layout.addWidget(sidebar_container)

        top_container = QWidget()
        top_container.setLayout(top_layout)

        self.main_layout.addWidget(top_container)

        self.bottom_image_label = QLabel()
        self.load_bottom_image("https://cdn.discordapp.com/attachments/978783217492582430/1305068391840743444/S-11-9-20241.png?ex=6731af27&is=67305da7&hm=4d94e07fa7a29d8a87ec21af64c8f7b9b7b876fc72ac82edd7223b20d00102a5")
        self.main_layout.addWidget(self.bottom_image_label)

        container = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)

        self.change_theme("green")

    def load_image_from_url(self, url):
        network_manager = QNetworkAccessManager(self)
        request = QNetworkRequest(QUrl(url))
        network_reply = network_manager.get(request)
        network_reply.finished.connect(lambda: self.handle_image_loaded(network_reply))

    def handle_image_loaded(self, network_reply):
        image_data = network_reply.readAll()
        pixmap = QPixmap()
        pixmap.loadFromData(image_data)

        if not pixmap.isNull():
            # Adjust size of the sidebar image (making it smaller)
            self.image_sidebar.setPixmap(pixmap.scaled(200, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation))  # Smaller size
            self.image_sidebar.setVisible(True)  # Make the image visible after loading

    def load_bottom_image(self, url):
        network_manager = QNetworkAccessManager(self)
        request = QNetworkRequest(QUrl(url))
        network_reply = network_manager.get(request)
        network_reply.finished.connect(lambda: self.handle_bottom_image_loaded(network_reply))

    def handle_bottom_image_loaded(self, network_reply):
        image_data = network_reply.readAll()
        pixmap = QPixmap()
        pixmap.loadFromData(image_data)

        if not pixmap.isNull():
            # Adjust size of the bottom image (making it smaller)
            self.bottom_image_label.setPixmap(pixmap.scaled(self.width(), 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))  # Smaller size

    def open_theme_dialog(self):
        dialog = ThemeSelectionDialog(self)
        dialog.exec_()

    def change_theme(self, theme):
        if theme == "green":
            self.setStyleSheet("background-color: green; font-family: Papyrus; font-size: 16px;")
            self.toolbar.setStyleSheet("background-color: hotpink; font-family: Papyrus; font-size: 16px;")
            self.url_bar.setStyleSheet("background-color: yellow; color: black; font-family: Papyrus; font-size: 16px;")
            self.image_sidebar.setStyleSheet("background-color: hotpink; font-family: Papyrus; font-size: 16px;")
        elif theme == "inverted":
            self.setStyleSheet("background-color: black; color: white; font-family: Papyrus; font-size: 16px;")
            self.toolbar.setStyleSheet("background-color: white; color: black; font-family: Papyrus; font-size: 16px;")
            self.url_bar.setStyleSheet("background-color: yellow; color: white; font-family: Papyrus; font-size: 16px;")
            self.image_sidebar.setStyleSheet("background-color: white; color: black; font-family: Papyrus; font-size: 16px;")

    def add_new_tab(self, qurl, label="nEW TAB"):
        browser_tab = BrowserTab()
        browser_tab.setUrl(qurl)
        i = self.tabs.addTab(browser_tab, label)
        self.tabs.setCurrentIndex(i)
        browser_tab.urlChanged.connect(lambda qurl, browser_tab=browser_tab: self.update_url_bar(qurl, browser_tab))

    def add_new_tab_button_clicked(self):
        self.add_new_tab(QUrl("https://www.yahoo.com"), "nEW TAB")

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("https"):
            url = "https://" + url
        self.tabs.currentWidget().setUrl(QUrl(url))

    def update_url_bar(self, qurl, browser_tab):
        if qurl != self.tabs.currentWidget().url():
            self.url_bar.setText(qurl.toString())

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = Browser()
    browser.show()
    sys.exit(app.exec_())
