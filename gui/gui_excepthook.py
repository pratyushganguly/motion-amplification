# gui/gui_excepthook.py
import sys, traceback
from PyQt5.QtWidgets import QApplication, QMessageBox

def excepthook(etype, value, tb):
    """Print traceback to terminal *and* show in a message-box."""
    text = "".join(traceback.format_exception(etype, value, tb))
    # Terminal
    sys.__stderr__.write(text)
    # GUI
    if QApplication.instance():
        QMessageBox.critical(
            None, "Unhandled Exception", f"<pre>{text}</pre>"
        )
    else:
        # fallback if GUI not running
        print(text, file=sys.stderr)

sys.excepthook = excepthook
