# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from qt_core import *

from gui.widgets import PyIconButton, PyToggle

from pyqt_color_picker import ColorPickerWidget

style_template = """ 
QPushButton::menu-indicator {{ 
    width:0px;
}}

QPushButton {{
    background-color: {};
}}
"""

class PyTextSettings(QWidget):
    def __init__(self, main_player):
        super().__init__()
		
        self.text_widgets = ()
        self.video_player = main_player

        self.item_widget_text = QWidget()
        self.item_layout_text = QGridLayout(self.item_widget_text)

        self._button_color = QColor("#343B48")


        # FIRST ROW
        # ///////////////////////////////////////////////////////////////

        self.text_first_uppercase = PyIconButton(icon_path= r"gui\images\svg_icons\icon_first_uppercase.svg", bg_color_hover = "#343B48", icon_margin=15, width=35, height=35)
        self.text_lowercase = PyIconButton(icon_path= r"gui\images\svg_icons\icon_lowercase.svg", bg_color_hover = "#343B48", icon_margin=15, width=35, height=35)
        self.text_uppercase = PyIconButton(icon_path= r"gui\images\svg_icons\icon_uppercase.svg", bg_color_hover = "#343B48", icon_margin=15, width=35, height=35) 

        # SECOND ROW
        # ///////////////////////////////////////////////////////////////

        self.top_text_align = PyIconButton(icon_path= r"gui\images\svg_icons\icon_align_top.svg", bg_color_hover = "#343B48", icon_margin=10, width=35, height=35)
        self.centre_text_align = PyIconButton(icon_path= r"gui\images\svg_icons\icon_align_middle.svg", bg_color_hover = "#343B48", icon_margin=10, width=35, height=35)
        self.bottom_text_align = PyIconButton(icon_path= r"gui\images\svg_icons\icon_align_bottom.svg", bg_color_hover = "#343B48", icon_margin=10, width=35, height=35)

        # THIRD ROW
        # ///////////////////////////////////////////////////////////////
        self.text_bold = PyIconButton(icon_path= r"gui\images\svg_icons\icon_bold.svg", bg_color_hover = "#343B48", icon_margin=5, width=35, height=35)
        self.text_underline = PyIconButton(icon_path= r"gui\images\svg_icons\icon_underline.svg", bg_color_hover = "#343B48", icon_margin=10, width=35, height=35)
        self.text_italic = PyIconButton(icon_path= r"gui\images\svg_icons\icon_italic.svg", bg_color_hover = "#343B48", icon_margin=15, width=35, height=35)

        # FOURTH ROW
        # ///////////////////////////////////////////////////////////////

        # TEXT SIZE
        self.text_size = QLineEdit(text="90")
        self.text_size.setValidator(QIntValidator())
        self.text_size.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.text_size.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
        self.text_size.setStyleSheet("border: 2px solid #1B1E23")

        # TEXT FONT
        self.text_font = QFontComboBox()
        self.text_font.setCurrentFont("Roboto")
        self.text_font.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
        self.text_font.setStyleSheet("Background-color: #2C313C;")

        # FIFTH ROW
        # ///////////////////////////////////////////////////////////////

        # Stroke Label
        self.stroke_label = QLabel()
        self.stroke_label.setText("Stroke:")
        self.stroke_label.setStyleSheet("color: #c3ccdf")

        # Stroke Size Input
        self.stroke_edit = QLineEdit(text="5")
        self.stroke_edit.setValidator(QIntValidator())
        self.stroke_edit.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.stroke_edit.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
        self.stroke_edit.setStyleSheet("border: 2px solid #1B1E23")

        # SIXTH ROW
        # ///////////////////////////////////////////////////////////////

        # Select All
        self.all_label = QLabel()
        self.all_label.setText("All Text:")
        self.all_label.setStyleSheet("color: #c3ccdf")

        self.select_all = PyToggle(width=80, bg_color="#1b1e23", circle_color="#c3ccdf", active_color="#3F6FD1")

        # BOTTOM ROW
        # ///////////////////////////////////////////////////////////////

        # Text Color Button
        self.text_color_menu = QMenu(self)
        self.text_color_picker = ColorPickerWidget(orientation='vertical')
        text_color_picker_action = QWidgetAction(self)
        text_color_picker_action.setDefaultWidget(self.text_color_picker)
        self.text_color_menu.addAction(text_color_picker_action)

        self.text_color_picker.setStyleSheet("QLineEdit { border: 2px solid #1B1E23; }")
        self.text_color_menu.setStyleSheet("Background-color: #2C313C;")

        self.text_color_btn = QPushButton()
        self.text_color_btn.setText("Text Color")
        self.text_color_btn.setStyleSheet(
            style_template.format(self._button_color.name())
        )
        self.text_color_btn.setMenu(self.text_color_menu)

        # STROKE COLOR
        self.stroke_color_menu = QMenu(self)
        self.stroke_color_picker = ColorPickerWidget(orientation='vertical')
        stroke_color_picker_action = QWidgetAction(self)
        stroke_color_picker_action.setDefaultWidget(self.stroke_color_picker)
        self.stroke_color_menu.addAction(stroke_color_picker_action)

        self.stroke_color_menu.setStyleSheet("QLineEdit { border: 2px solid #1B1E23; }")
        self.stroke_color_menu.setStyleSheet("Background-color: #2C313C;")

        self.stroke_color_btn = QPushButton()
        self.stroke_color_btn.setText("Stroke Color")
        self.stroke_color_btn.setStyleSheet(
            style_template.format(self._button_color.name())
        )
        self.stroke_color_btn.setMenu(self.stroke_color_menu)

        # Highlight Color Button
        self.highlight_color_menu = QMenu(self)
        self.highlight_color_picker = ColorPickerWidget(orientation='vertical')
        highlight_color_picker_action = QWidgetAction(self)
        highlight_color_picker_action.setDefaultWidget(self.highlight_color_picker)
        self.highlight_color_menu.addAction(highlight_color_picker_action)

        self.highlight_color_picker.setStyleSheet("QLineEdit { border: 2px solid #1B1E23; }")
        self.highlight_color_menu.setStyleSheet("Background-color: #2C313C;")

        self.text_highlight_btn = QPushButton()
        self.text_highlight_btn.setText("Highlight")
        self.text_highlight_btn.setStyleSheet(
            style_template.format(self._button_color.name())
        )
        self.text_highlight_btn.setMenu(self.highlight_color_menu)

        # SETTING UP LAYOUT
        # ///////////////////////////////////////////////////////////////

        # ITEMS LAYOUT SETUP
        self.item_layout_text.addWidget(self.text_first_uppercase, 0, 0)
        self.item_layout_text.addWidget(self.text_lowercase, 0, 1)
        self.item_layout_text.addWidget(self.text_uppercase, 0, 2)

        self.item_layout_text.addWidget(self.top_text_align, 1, 0)
        self.item_layout_text.addWidget(self.centre_text_align, 1, 1)
        self.item_layout_text.addWidget(self.bottom_text_align, 1, 2)

        self.item_layout_text.addWidget(self.text_bold, 2, 0)
        self.item_layout_text.addWidget(self.text_underline, 2, 1)
        self.item_layout_text.addWidget(self.text_italic, 2, 2)

        self.item_layout_text.addWidget(self.text_size, 3, 0)
        self.item_layout_text.addWidget(self.text_font, 3, 1, 1, 2)

        self.item_layout_text.addWidget(self.stroke_label, 4, 0)
        self.item_layout_text.addWidget(self.stroke_edit, 4, 1, 1, 2)

        self.item_layout_text.addWidget(self.all_label, 5, 0)
        self.item_layout_text.addWidget(self.select_all, 5, 1, 1, 2)

        self.item_layout_text.setContentsMargins(0, 0, 0, 0)
        self.item_layout_text.setSpacing(5)  # Sets space between each btn

        # BOTTOM LAYOUT SETUP
        self.bottom_widget = QWidget()
        self.bottom_layout = QGridLayout(self.bottom_widget)

        self.bottom_layout.addWidget(self.text_color_btn, 2, 0, 1, 3)
        self.bottom_layout.addWidget(self.stroke_color_btn, 3, 0, 1, 3)
        self.bottom_layout.addWidget(self.text_highlight_btn, 4, 0, 1, 3)
        self.bottom_layout.setSpacing(5)

        # MAIN LAYOUT SETUP
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.item_widget_text)
        main_layout.addStretch(1)
        main_layout.addWidget(self.bottom_widget)
        main_layout.setContentsMargins(0, 10, 0, 10)
        main_layout.setSpacing(0)

        self.setLayout(main_layout)


        # SLOTS
        # ///////////////////////////////////////////////////////////////
        
        self.text_first_uppercase.clicked.connect(self.update_text)
        self.text_lowercase.clicked.connect(self.update_text)
        self.text_uppercase.clicked.connect(self.update_text)

        self.top_text_align.clicked.connect(self.update_text)
        self.centre_text_align.clicked.connect(self.update_text)
        self.bottom_text_align.clicked.connect(self.update_text)

        self.text_bold.clicked.connect(self.update_text)
        self.text_underline.clicked.connect(self.update_text)
        self.text_italic.clicked.connect(self.update_text)

        self.text_font.currentIndexChanged.connect(self.update_text)
        self.text_size.textChanged.connect(self.update_text)

        self.stroke_edit.textChanged.connect(self.update_text)

        self.select_all.clicked.connect(self.update_text)

        self.text_color_picker.colorChanged.connect(self.update_text)
        self.stroke_color_picker.colorChanged.connect(self.update_text)
        self.highlight_color_picker.colorChanged.connect(self.update_text)




    # UPDATES ANYTHING WITH FONT
    # ///////////////////////////////////////////////////////////////


 
        
    def update_text(self, color=None):
        sender = self.sender()

        for widget in self.text_widgets:

            if widget.isSelected() or widget.textCursor().hasSelection():
                new_format = QTextCharFormat()
                
                cursor = widget.textCursor()
                format = cursor.charFormat()

                scene_rect = self.video_player.graphic_scene.sceneRect()
                text_rect = widget.document().size()

                if not cursor.hasSelection():
                    cursor.select(QTextCursor.Document)



                # FIRST ROW
                # ///////////////////////////////////////////////////////////////
                if sender == self.text_first_uppercase:
                    cursor.select(QTextCursor.Document)
                    new_format.setFontCapitalization(QFont.Capitalize)


                elif sender == self.text_lowercase:
                    new_format.setFontCapitalization(QFont.AllLowercase if format.fontCapitalization() != QFont.AllLowercase else QFont.AllUppercase)

                elif sender == self.text_uppercase:
                    new_format.setFontCapitalization(QFont.AllUppercase if format.fontCapitalization() != QFont.AllUppercase else QFont.AllLowercase)

                # SECOND ROW
                # ///////////////////////////////////////////////////////////////
                elif sender == self.text_bold:
                    new_format.setFontWeight(QFont.Bold if not format.font().bold() else QFont.Normal)

                elif sender == self.text_underline:
                    new_format.setFontUnderline(not format.font().underline())

                elif sender == self.text_italic:
                    new_format.setFontItalic(not format.font().italic())

                # THIRD ROW
                # ///////////////////////////////////////////////////////////////
                elif sender == self.top_text_align:
                    x = (scene_rect.width() - text_rect.width()) / 2
                    y = 10
                    widget.setPos(x, y)

                
                elif sender == self.centre_text_align:
                    x = (scene_rect.width() - text_rect.width()) / 2
                    y = (scene_rect.height() - text_rect.height()) / 2
                    widget.setPos(x, y)
                    print("Scene: ", scene_rect.width(), scene_rect.height(), "Text: ",text_rect.width(), text_rect.height())


                elif sender == self.bottom_text_align:
                    x = (scene_rect.width() - text_rect.width()) / 2
                    y = scene_rect.height() - text_rect.height() - 10
                    widget.setPos(x, y)

                # FOURTH ROW
                # ///////////////////////////////////////////////////////////////
                elif sender == self.text_size:
                    size = self.text_size.text()
                    if size == "":
                        size = 0
                    new_format.setFontPointSize(int(size))

                # FIFTH ROW
                # ///////////////////////////////////////////////////////////////
                elif sender == self.text_font:
                    new_format.setFontFamily(self.text_font.currentText())

                
                # SIXTH ROW
                # ///////////////////////////////////////////////////////////////
                elif sender == self.stroke_edit:
                    size = self.stroke_edit.text()
                    if size == '':
                        size = 0

                    widget.set_outline_size(int(size))


                # LAST ROW
                # ///////////////////////////////////////////////////////////////
                elif sender == self.text_color_picker:
                    new_format.setForeground(color)

                elif sender == self.stroke_color_picker:
                    widget.set_outline_color(color)

                elif sender == self.highlight_color_picker:
                    new_format.setBackground(color)



                cursor.mergeCharFormat(new_format)
                widget.setTextCursor(cursor)

            if sender == self.select_all:
                cursor = widget.textCursor()
                
                if self.select_all.isChecked():
                    cursor.select(QTextCursor.Document)
                else:
                    cursor.clearSelection()

                widget.setTextCursor(cursor)
    

    def reset_text_settings(self):
        self.text_size.setText("90")
        self.stroke_edit.setText("5")
        self.text_font.setCurrentFont("Roboto")






