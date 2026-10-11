"""
GUI Styling and Themes
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
    QPushButton:pressed {
        background-color: #005a9e;
    }
    QLabel {
        color: #ffffff;
    }
    QTableWidget {
        background-color: #2d2d2d;
        gridline-color: #444444;
    }
    QTableWidget::item {
        padding: 5px;
    }
    QHeaderView::section {
        background-color: #3d3d3d;
        color: #ffffff;
        padding: 5px;
        border: none;
    }
    QScrollBar:vertical {
        background-color: #2d2d2d;
        width: 12px;
    }
    QScrollBar::handle:vertical {
        background-color: #555555;
        border-radius: 6px;
    }
"""

LIGHT_STYLESHEET = """
    QMainWindow {
        background-color: #ffffff;
    }
    QWidget {
        background-color: #ffffff;
        color: #000000;
    }
    QLineEdit, QTextEdit, QComboBox {
        background-color: #f5f5f5;
        color: #000000;
        border: 1px solid #cccccc;
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
        color: #000000;
    }
    QTableWidget {
        background-color: #ffffff;
        gridline-color: #cccccc;
    }
"""

def get_stylesheet(theme='dark'):
    """Get stylesheet for theme"""
    return DARK_STYLESHEET if theme == 'dark' else LIGHT_STYLESHEET