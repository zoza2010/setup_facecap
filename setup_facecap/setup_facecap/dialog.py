from .widgets.dialog import Ui_Form
from .character_setup import CharacterSetup
from PySide2.QtWidgets import QWidget, QMessageBox
from pyfbsdk import *
import os


class Dialog(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)
        self.setupUi(self)
        self._character_setup = CharacterSetup()
        self._configs_path = os.path.join(os.path.dirname(__file__), "configs")
        self.setFixedHeight(100)
        self._fill_defaults()

        # bind signals
        self.setupPushButton.clicked.connect(self._on_setup_button_clicked)

    def _fill_defaults(self):
        for i in os.listdir(self._configs_path):
            config_name = os.path.basename(i)
            self.configsComboBox.addItem(config_name)

    def _get_selected(self):
        sel = FBModelList()
        FBGetSelectedModels(sel)
        return sel

    def _show_info_message(self, title, text):
        message_box = QMessageBox(self)
        message_box.setWindowTitle(title)
        message_box.setText(text)
        message_box.exec_()

    def _on_setup_button_clicked(self):
        config_path = os.path.join(
            self._configs_path, self.configsComboBox.currentText()
        )
        selected = self._get_selected()
        if selected.count() == 0:
            self._show_info_message(
                "Nothing is selected!!!",
                "No meshes were selected,\n select one and retry.",
            )
            return
        elif selected.count() > 1:
            self._show_info_message(
                "Multiple selection!!!",
                "More than one meshes were selected,\n select one and retry.",
            )
            return
        else:
            mesh_model = selected.GetModel(0)
        try:
            self._character_setup.setup(mesh_model, config_path)
        except Exception:
            self._show_info_message(
                "Error",
                "Errors occurred during execution.\n For details read script editor.",
            )
            raise
