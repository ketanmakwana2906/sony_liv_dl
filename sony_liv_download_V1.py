import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QComboBox, QProgressBar, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
import requests
import youtube_dl

class VideoDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('SonyLiv Video Downloader')
        self.setFixedSize(900, 250)
        self.setStyleSheet("background-color: #defff4;")
        icon_url = "https://raw.githubusercontent.com/ketanmakwana2906/Project_Images_Storage/main/liv_download/app_icon.jpg"
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(requests.get(icon_url).content)
        self.setWindowIcon(QtGui.QIcon(pixmap))

        self.video_url_label = QLabel('Video URL:')
        self.video_url_input = QLineEdit()
        self.video_url_input.setFixedSize(700, self.video_url_input.sizeHint().height())

        self.quality_label = QLabel('Select Quality:')
        self.quality_combo = QComboBox()
        self.quality_combo.addItems(['144p', '240p', '360p', '480p', '540p', '720p', '1080p'])
        self.quality_combo.setCurrentText("720p")
        self.quality_combo.setFixedSize(700, self.quality_combo.sizeHint().height())
      

        self.path_label = QLabel('Select Download Path:')
        self.path_display = QLineEdit()
        self.path_display.setFixedSize(515, self.path_display.sizeHint().height())
        self.browse_button = QPushButton('Browse')
        self.browse_button.setFixedSize(180, self.browse_button.sizeHint().height())
        self.browse_button.clicked.connect(self.select_download_path)

        self.download_button = QPushButton('Download')
        self.download_button.clicked.connect(self.download_video)

        url_layout = QHBoxLayout()
        url_layout.addWidget(self.video_url_label)
        url_layout.addWidget(self.video_url_input)

        quality_layout = QHBoxLayout()
        quality_layout.addWidget(self.quality_label)
        quality_layout.addWidget(self.quality_combo)


        path_layout = QHBoxLayout()
        path_layout.addWidget(self.path_label)
        path_layout.addWidget(self.path_display)
        path_layout.addWidget(self.browse_button)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.download_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(url_layout)
        main_layout.addLayout(quality_layout)
        main_layout.addLayout(path_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def select_download_path(self):
        download_path = QFileDialog.getExistingDirectory(self, 'Select Download Path')
        if download_path:
            self.path_display.setText(download_path)

    def download_video(self):
        video_url = self.video_url_input.text()
        download_path = self.path_display.text()
        quality = self.quality_combo.currentText()

        if not video_url or not download_path:
            return

        video_format = ''
        audio_format = 'dash-10'

        if quality == '144p':
            video_format = 'dash-8'
        elif quality == '240p':
            video_format = 'dash-8'
        elif quality == '360p':
            video_format = 'dash-7'
        elif quality == '480p':
            video_format = 'dash-6'
        elif quality == '540p':
            video_format = 'dash-5'
        elif quality == '720p':
            video_format = 'dash-3'
        elif quality == '1080p':
            video_format = 'dash-1'

        ydl_opts = {
            'format': f'{video_format}[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': f'{download_path}/%(title)s - Format: {video_format} [{audio_format}].%(ext)s',
        }
        
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            
        QMessageBox.information(self, 'Download Complete', 'Video downloaded successfully!')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    downloader = VideoDownloader()
    downloader.show()
    sys.exit(app.exec_())
