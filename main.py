"""
Stock Technical Analyzer - GUI Version
Main Entry Point
"""
import sys
import traceback
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtGui import QFont

def main():
    """Run application"""
    try:
        # Create Qt application
        app = QApplication(sys.argv)
        
        # Set default font
        font = QFont("Segoe UI", 10)
        app.setFont(font)
        
        # Import main window (do this AFTER creating QApplication)
        from gui.main_window import MainWindow
        
        # Create and show main window
        window = MainWindow()
        window.show()
        
        # Run event loop
        sys.exit(app.exec())
    
    except Exception as e:
        print(f"[CRITICAL ERROR] {str(e)}")
        print("\nTraceback:")
        traceback.print_exc()
        
        # Try to show error in GUI
        try:
            app = QApplication.instance()
            if app is None:
                app = QApplication(sys.argv)
            
            QMessageBox.critical(
                None, 
                "Application Error", 
                f"Failed to start application:\n\n{str(e)}\n\nCheck console for details."
            )
        except:
            pass
        
        sys.exit(1)

if __name__ == '__main__':
    main()