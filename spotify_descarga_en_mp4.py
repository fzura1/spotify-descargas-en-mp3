import os
import subprocess
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QFileDialog
from PyQt5.QtCore import Qt, QThread, pyqtSignal

class DownloadThread(QThread):
    update_signal = pyqtSignal(str)

    def __init__(self, url, download_folder):
        super().__init__()
        self.url = url
        self.download_folder = download_folder

    def run(self):
        try:
            subprocess.run(["spotdl", self.url, "--output", os.path.join(self.download_folder, "{title}.mp3")], check=True)
            self.update_signal.emit(f"✅ Descarga completada: {self.url}")
        except subprocess.CalledProcessError as e:
            self.update_signal.emit(f"❌ Error al descargar: {self.url}")

class MusicDownloaderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Spotify Music Downloader")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        # URL Input
        self.url_label = QLabel("🎵 Ingresa el enlace de la canción o playlist de Spotify:")
        self.url_input = QLineEdit()
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)

        # Folder Selection
        self.folder_label = QLabel("📁 Selecciona la carpeta de descarga:")
        self.folder_button = QPushButton("Seleccionar Carpeta")
        self.folder_button.clicked.connect(self.select_folder)
        self.folder_display = QLabel("Carpeta seleccionada: Ninguna")
        layout.addWidget(self.folder_label)
        layout.addWidget(self.folder_button)
        layout.addWidget(self.folder_display)

        # Download Button
        self.download_button = QPushButton("Descargar")
        self.download_button.clicked.connect(self.start_download)
        layout.addWidget(self.download_button)

        # Progress List
        self.progress_label = QLabel("Progreso de descargas:")
        self.progress_list = QListWidget()
        layout.addWidget(self.progress_label)
        layout.addWidget(self.progress_list)

        self.setLayout(layout)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta")
        if folder:
            self.download_folder = folder
            self.folder_display.setText(f"Carpeta seleccionada: {folder}")

    def start_download(self):
        url = self.url_input.text()
        if not url:
            self.progress_list.addItem("❌ Por favor, ingresa un enlace válido.")
            return

        if not hasattr(self, 'download_folder'):
            self.progress_list.addItem("❌ Por favor, selecciona una carpeta de descarga.")
            return

        self.progress_list.addItem(f"⏳ Descargando: {url}")
        self.download_thread = DownloadThread(url, self.download_folder)
        self.download_thread.update_signal.connect(self.update_progress)
        self.download_thread.start()

    def update_progress(self, message):
        self.progress_list.addItem(message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MusicDownloaderApp()
    window.show()
    sys.exit(app.exec_())
