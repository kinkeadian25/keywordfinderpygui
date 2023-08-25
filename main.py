import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTabWidget, QTextEdit, QFileDialog, QLabel, QMessageBox, QInputDialog, QLineEdit, QComboBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import csv
import qdarkstyle
from file_processor import update_keywords, search_files, update_keyword_in_db

class KeywordSearchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Keyword Search in Text Files')
        layout = QVBoxLayout()

        self.label = QLabel('Choose a folder and run the report.')
        self.label.setFont(QFont("Verdana", 14))
        layout.addWidget(self.label)

        self.folder_path = ""
        self.chooseDirButton = QPushButton("Choose Directory")
        self.chooseDirButton.setFont(QFont("Verdana", 12))
        self.chooseDirButton.clicked.connect(self.choose_dir)
        layout.addWidget(self.chooseDirButton)

        self.runButton = QPushButton("Run Report")
        self.runButton.setFont(QFont("Verdana", 12))
        self.runButton.clicked.connect(self.run_report)
        layout.addWidget(self.runButton)

        self.exportButton = QPushButton("Export to CSV")
        self.exportButton.setFont(QFont("Verdana", 12))
        self.exportButton.clicked.connect(self.export_to_csv)
        layout.addWidget(self.exportButton)

        self.categoryComboBox = QComboBox()
        layout.addWidget(self.categoryComboBox)

        self.keywords = update_keywords()

        self.tabs = QTabWidget()
        self.tab_data = {}
        for prefix in self.keywords.keys():
            self.categoryComboBox.addItem(prefix)
            tab = QTextEdit()
            tab.setReadOnly(True)
            tab.setFont(QFont("Verdana", 10))
            self.tabs.addTab(tab, prefix.upper())
            self.tab_data[prefix] = tab

        self.updateKeywordButton = QPushButton("Update Keywords")
        self.updateKeywordButton.setFont(QFont("Verdana", 12))
        self.updateKeywordButton.clicked.connect(self.update_keywords_db)
        layout.addWidget(self.updateKeywordButton)

        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def choose_dir(self):
        self.folder_path = QFileDialog.getExistingDirectory()
        if self.folder_path:
            self.label.setText(f"Selected Directory: {self.folder_path}")

    def update_keywords_db(self):
        category = self.categoryComboBox.currentText()
        keyword, okPressed = QInputDialog.getText(self, "Update Keywords", "Keyword:", QLineEdit.Normal, "")
        if okPressed and keyword != '':
            update_keyword_in_db(category.lower(), keyword.lower())
            self.keywords = update_keywords()

    def run_report(self):
        results = search_files(self.folder_path, self.keywords)
        for prefix, tab in self.tab_data.items():
            tab.clear()
            lines = results.get(prefix, [])
            for line in lines:
                tab.append(line)

    def export_to_csv(self):
        selected_tab = self.tabs.currentIndex()
        selected_prefix = list(self.tab_data.keys())[selected_tab]
        tab_content = self.tab_data[selected_prefix].toPlainText().strip().split('\n')
        csv_file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "CSV Files (*.csv)")
        if csv_file_path:
            with open(csv_file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([f"Results for {selected_prefix.upper()}"])
                for line in tab_content:
                    writer.writerow([line])

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        ex = KeywordSearchApp()
        ex.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        ex.show()
        ex.resize(800, 600)
        sys.exit(app.exec_())
    except Exception as e:
        print(f"An error occurred: {e}")
