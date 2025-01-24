from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QSpinBox, QLineEdit


class ColorEditorWidget(QWidget):
    colorChanged = Signal(QColor)

    def __init__(self, color, orientation):
        super().__init__()
        self.__current_color = color
        self.__initUi(color, orientation)


    def __initUi(self, color, orientation):
        self.__hLineEdit = QLineEdit()
        self.__hLineEdit.setInputMask("HHHHHH")
        self.__hLineEdit.setReadOnly(False)

        self.__rSpinBox = QSpinBox()
        self.__gSpinBox = QSpinBox()
        self.__bSpinBox = QSpinBox()

        self.__rSpinBox.valueChanged.connect(self.__rColorChanged)
        self.__gSpinBox.valueChanged.connect(self.__gColorChanged)
        self.__bSpinBox.valueChanged.connect(self.__bColorChanged)

        # Connect the hex input field
        self.__hLineEdit.textEdited.connect(self.__hexColorChanged)
  

        self.__hLineEdit.setAlignment(Qt.AlignCenter)
        self.__hLineEdit.setFont(QFont('Roboto', 12))

        spinBoxs = [self.__rSpinBox, self.__gSpinBox, self.__bSpinBox]
        for spinBox in spinBoxs:
            spinBox.setRange(0, 255)
            spinBox.setAlignment(Qt.AlignCenter)
            spinBox.setFont(QFont('Roboto', 12))

        lay = QFormLayout()
        lay.addRow(self.__hLineEdit)
        lay.setContentsMargins(0, 0, 0, 0)

        colorEditor = QWidget()
        colorEditor.setLayout(lay)
        if orientation == 'horizontal':
            lay = QVBoxLayout()
        elif orientation == 'vertical':
            lay = QHBoxLayout()
        lay.addWidget(colorEditor)

        lay.setContentsMargins(0, 0, 0, 0)

        self.setLayout(lay)

        self.setCurrentColor(color)

    def setCurrentColor(self, color):
        self.__current_color = color
        self.__hLineEdit.setText(self.__current_color.name())

        # Prevent infinite valueChanged event loop
        self.__rSpinBox.valueChanged.disconnect(self.__rColorChanged)
        self.__gSpinBox.valueChanged.disconnect(self.__gColorChanged)
        self.__bSpinBox.valueChanged.disconnect(self.__bColorChanged)

        r, g, b = self.__current_color.red(), self.__current_color.green(), self.__current_color.blue()

        self.__rSpinBox.setValue(r)
        self.__gSpinBox.setValue(g)
        self.__bSpinBox.setValue(b)

        self.__rSpinBox.valueChanged.connect(self.__rColorChanged)
        self.__gSpinBox.valueChanged.connect(self.__gColorChanged)
        self.__bSpinBox.valueChanged.connect(self.__bColorChanged)

    def __rColorChanged(self, r):
        self.__current_color.setRed(r)
        self.__procColorChanged()

    def __gColorChanged(self, g):
        self.__current_color.setGreen(g)
        self.__procColorChanged()

    def __bColorChanged(self, b):
        self.__current_color.setBlue(b)
        self.__procColorChanged()

    def __hexColorChanged(self):
        hex_value = self.__hLineEdit.text().strip()

        if len(hex_value) == 6:
            try:
                color = QColor("#" + hex_value)
                if color.isValid():
                    self.__current_color.setRgb(color.red(), color.green(), color.blue())
                    print("Current color: ", self.__current_color)
                    self.colorChanged.emit(self.__current_color)
            except ValueError:
                pass  # Ignore invalid hex value

    def __procColorChanged(self):
        self.__hLineEdit.setText(self.__current_color.name())
        self.colorChanged.emit(self.__current_color)

    def getCurrentColor(self):
        return self.__current_color

