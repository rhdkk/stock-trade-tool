"""
GUI Styling
"""

DARK_STYLESHEET = """
    QMainWindow {
        background-color: #1e1e1e;
    }
    QWidget {
        background-color: #1e1e1e;
        color: #ffffff;
    }
    QLineEdit, QTextEdit, QComboBox {
        background-color: #2d2d2d;
        color: #ffffff;
        border: 1px solid #444444;
        border-radius: 4px;
        padding: 5px;
    }
    QPushButton {
        background-color: #0078d4;
        color: #ffffff;
        border: none;
        border-radius: 4px;
        padding: 8px 16px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #1084d7;
    }
    QLabel {
        color: #ffffff;
    }
    QTableWidget {
        background-color: #2d2d2d;
        gridline-color: #444444;
    }
"""

def get_stylesheet(theme='dark'):
    return DARK_STYLESHEET