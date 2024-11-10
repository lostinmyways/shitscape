import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        def inject_papyrus_font(self):
        
            script = """
            var style = document.createElement('style');
            style.innerHTML = 'body { font-family: "Papyrus", sans-serif !important; }';
            document.head.appendChild(style);
            """
            self.sender().page().runJavaScript(script)

        self.tabs = []  
        self.current_tab = None  

        
        self.resize(800, 600)

        
        self.setStyleSheet("QMainWindow { background-color: #ff00e8; }")

        
        self.navbar = QToolBar()
        self.navbar.setStyleSheet("QToolBar { background-color: #9c4dcc; border: none; }")
        self.addToolBar(self.navbar)

    
        self.address_bar = QLineEdit(self)
        self.address_bar.setPlaceholderText("FUCK YOU!!!!")
        self.address_bar.setStyleSheet("QLineEdit { background-color: white; border-radius: 5px; padding-left: 10px; }")
        self.address_bar.returnPressed.connect(self.load_url_from_address_bar)
        self.navbar.addWidget(self.address_bar)

        
        self.tab_bar = QTabWidget()
        self.navbar.addWidget(self.tab_bar)

        
        self.new_tab_button = QAction("neW TAB LOL", self)
        self.new_tab_button.triggered.connect(self.add_new_tab)
        self.navbar.addAction(self.new_tab_button)

        
        self.tab_bar.currentChanged.connect(self.on_tab_changed)

        
        self.add_new_tab(homepage=True)

        

    def add_new_tab(self, homepage=False):
        
        tab = QWidget()
        tab_layout = QVBoxLayout()

        
        browser = QWebEngineView()
        if homepage:
            
            browser.setUrl(QUrl("https://nobodyhere.com/bugs/on.here?something=matches"))
        else:
            browser.setUrl(QUrl("https://nobodyhere.com/bugs/on.here?something=matches"))  

        
        browser.urlChanged.connect(self.update_address_bar)

        
        browser.loadFinished.connect(self.inject_custom_text)

        tab_layout.addWidget(browser)

        
        tab_content = QWidget()
        tab_content.setLayout(tab_layout)

        
        tab_index = self.tab_bar.addTab(tab_content, "New Tab")
        self.tab_bar.setCurrentIndex(tab_index)

        
        self.tabs.append(browser)

        
        close_button = QPushButton("X", self)
        close_button.clicked.connect(lambda: self.close_tab(self.tab_bar.indexOf(tab_content)))
        close_button.setFixedSize(20, 20)
        tab_layout.addWidget(close_button, alignment=Qt.AlignRight)

    def inject_custom_text(self):
        
        script = """
            var div = document.createElement('div');
            div.style.position = 'absolute';
            div.style.top = '0';
            div.style.left = '0';
            div.style.width = '100%';
            div.style.textAlign = 'center';
            div.style.fontSize = '48px';
            div.style.fontFamily = 'Papyrus, sans-serif';
            div.style.color = '#c4f697';
            div.style.zIndex = '1000';
            div.innerText = 'Shitscape Web Browser';
            document.body.appendChild(div);
        """
       
        self.sender().page().runJavaScript(script)

    def load_url_from_address_bar(self):
        
        url = self.address_bar.text().strip()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url  
        if self.tabs:
            self.tabs[self.tab_bar.currentIndex()].setUrl(QUrl(url))
        self.address_bar.setText(url)

    def update_address_bar(self, url):
        
        self.address_bar.setText(url.toString())

    def close_tab(self, index):
        
        if index >= 0:
            self.tab_bar.removeTab(index)
            self.tabs.pop(index)

    def on_tab_changed(self, index):
        
        if index < len(self.tabs):
            self.current_tab = self.tabs[index]
            
            self.address_bar.setText(self.tabs[index].url().toString())

    def closeEvent(self, event):
        
        reply = QMessageBox.question(self, 'LOSER', 'are YUO SURE U WANT TO QUITING???',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


app = QApplication(sys.argv)
QApplication.setApplicationName("shitscape web 0.1")


app.setStyleSheet("""
    QMainWindow { background-color: #ff00f3; }
    QToolBar { background-color: #64f974; }
    QTabWidget { background-color: #9c4dcc; }
    QPushButton { background-color: #6a1b9a; color: white; border: none; padding: 5px; border-radius: 5px; }
    QLineEdit { background-color: white; border-radius: 5px; padding-left: 10px; }
    QTabBar::tab { background-color: #9c4dcc; color: white; border: 1px solid #6a1b9a; padding: 10px; }
    QTabBar::tab:selected { background-color: #6a1b9a; }
""")
#helo guys it me i writing de code and it lol and very good browser web lol and yes

window = Browser()
window.show()


app.exec_()
