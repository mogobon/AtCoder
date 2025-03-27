import sys
import webbrowser
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import pyperclip

def convert_url(adt_url: str) -> str:
    parts = adt_url.split("/tasks/", 1)
    if len(parts) < 2:
        return adt_url
    prefix, task_part = parts
    abc_id = task_part.split("_", 1)[0]
    return f"https://atcoder.jp/contests/{abc_id}/tasks/{task_part}"

class URLConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("ADT→ABC Converter")
        self.setGeometry(100, 100, 600, 250)

        # レイアウトの設定
        layout = QVBoxLayout()

        # ラベル
        self.label = QLabel("ADTのURLを入力してください:")
        self.label.setFont(QFont("Arial", 14))
        layout.addWidget(self.label)

        # 入力フィールド
        self.input_field = QLineEdit(self)
        self.input_field.setFont(QFont("Arial", 14))
        self.input_field.setPlaceholderText("ここにURLを入力してください")
        layout.addWidget(self.input_field)

        # 変換ボタン
        self.convert_button = QPushButton("変換", self)
        self.convert_button.setFont(QFont("Arial", 14))
        self.convert_button.clicked.connect(self.convert_url)
        layout.addWidget(self.convert_button)

        # 結果ラベル
        self.result_label = QLabel("")
        self.result_label.setFont(QFont("Arial", 14))
        self.result_label.setStyleSheet("color: white;")
        self.result_label.setTextInteractionFlags(Qt.TextSelectableByMouse)  # 左クリックで選択可能にする
        layout.addWidget(self.result_label)

        # クリップボードにコピーするボタン
        self.copy_button = QPushButton("クリップボードにコピー", self)
        self.copy_button.setFont(QFont("Arial", 14))
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        layout.addWidget(self.copy_button)

        # ブラウザで開くボタン
        self.open_browser_button = QPushButton("このURLをブラウザで開く", self)
        self.open_browser_button.setFont(QFont("Arial", 14))
        self.open_browser_button.clicked.connect(self.open_in_browser)
        layout.addWidget(self.open_browser_button)

        # アプリケーション終了ボタン
        self.exit_button = QPushButton("終了", self)
        self.exit_button.setFont(QFont("Arial", 14))
        self.exit_button.clicked.connect(self.close)
        layout.addWidget(self.exit_button)

        # レイアウトをウィジェットに設定
        self.setLayout(layout)

    def convert_url(self):
        url = self.input_field.text().strip()
        converted = convert_url(url)
        self.result_label.setText(converted)
        pyperclip.copy(converted)

    def copy_to_clipboard(self):
        url = self.result_label.text()
        if url:
            pyperclip.copy(url)

    def open_in_browser(self):
        url = self.result_label.text()
        if url:
            webbrowser.open(url)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = URLConverterApp()
    window.show()
    sys.exit(app.exec_())

