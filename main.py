import sys
# import smtplib  # For email sending (Uncomment if using)
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTabWidget, QTextEdit, QFileDialog, QLabel, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from file_processor import search_files
import qdarkstyle
import csv

# For email sending (Uncomment if using)
# def send_email():
#     try:
#         server = smtplib.SMTP('smtp.gmail.com', 587)
#         server.starttls()
#         server.login("your_email", "your_password")
#         msg = "Subject: Keyword Alert
#         server.sendmail("from_email", "to_email", msg)
#         server.quit()
#         QMessageBox.information(None, 'Success', 'Email sent successfully.')
#     except Exception as e:
#         QMessageBox.critical(None, 'Error', f'Could not send email. Error: {e}')

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
        
        self.tabs = QTabWidget()
        self.tab_data = {}
        for prefix in ['cat', 'dog', 'pet']:
            tab = QTextEdit()
            tab.setReadOnly(True)
            tab.setFont(QFont("Verdana", 10))
            self.tabs.addTab(tab, prefix.upper())
            self.tab_data[prefix] = tab
            
        self.special_dog = QTextEdit()
        self.special_dog.setReadOnly(True)
        self.special_dog.setFont(QFont("Verdana", 10))
        self.tabs.addTab(self.special_dog, 'SPECIAL DOG')
        
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def choose_dir(self):
        self.folder_path = QFileDialog.getExistingDirectory()
        if self.folder_path:
            self.label.setText(f"Selected Directory: {self.folder_path}")

    def run_report(self):
        results = search_files(self.folder_path)
        alert_keyword_found = False
        for prefix, tab in self.tab_data.items():
            tab.clear()
            lines = results.get(prefix, [])
            for line in lines:
                tab.append(line)
                if prefix == 'dog' and 'specific_keyword' in line:
                    self.special_dog.append(line)
                    alert_keyword_found = True
        # Uncomment if enabling email alerts
        # if alert_keyword_found:
        #     send_email()

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

