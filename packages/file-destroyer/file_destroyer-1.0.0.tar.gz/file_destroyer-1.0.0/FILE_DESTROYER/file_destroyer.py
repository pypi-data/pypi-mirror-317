from pathlib import Path
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog
from PyQt6.QtCore import Qt


class FileDestroyer:
    def __init__(self):
        self.app = QApplication([])
        self.window = QWidget()
        self.window.setWindowTitle("File Destroyer")
        self.layout = QVBoxLayout()
        self.filenames = []

        # Description label
        description = QLabel(
            'Select the files you want to destroy. The files will be <font color="red">permanently</font> deleted.'
        )
        self.layout.addWidget(description)

        # Open files button
        self.open_btn = QPushButton('Open Files')
        self.open_btn.setFixedWidth(100)
        self.open_btn.clicked.connect(self.open_files)
        self.layout.addWidget(self.open_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        # Destroy files button
        self.destroy_btn = QPushButton('Destroy Files')
        self.destroy_btn.setFixedWidth(100)
        self.destroy_btn.clicked.connect(self.destroy_files)
        self.layout.addWidget(self.destroy_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        # Message label
        self.message = QLabel('')
        self.layout.addWidget(self.message, alignment=Qt.AlignmentFlag.AlignCenter)

        # Set layout
        self.window.setLayout(self.layout)

    def open_files(self):
        self.filenames, _ = QFileDialog.getOpenFileNames(self.window, 'Select files')
        self.message.setText('\n'.join(self.filenames))

    def destroy_files(self):
        for filename in self.filenames:
            path = Path(filename)
            with open(path, 'wb') as file:
                file.write(b'')  # Overwrite the file with empty content
            path.unlink()  # Delete the file
        self.message.setText('Destruction Successful!')

    def run(self):
        self.window.show()
        self.app.exec()
        
if __name__ == "__main__":
    app = FileDestroyer()
    app.run()
