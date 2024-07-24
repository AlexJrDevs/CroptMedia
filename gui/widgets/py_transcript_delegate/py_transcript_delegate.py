from qt_core import *

class PyTranscriptDelegate(QStyledItemDelegate):
    add_transcript = Signal(int)
    remove_transcript = Signal(int)

    def __init__(
            self, 
            parent=None,
            add_icon=QIcon("gui/images/svg_icons/icon_add.svg"),
            remove_icon=QIcon("gui/images/svg_icons/icon_minus.svg"),
            add_button_color='#3c4454',
            remove_button_color='#3c4454',
            button_width=20,
            button_height=20,
            icon_margin=4,
            border_radius=5
        ):
        super().__init__(parent)
        self.button_rects = {}

        # Initialize button properties
        self._add_icon = add_icon
        self._remove_icon = remove_icon
        self._add_button_color = QColor(add_button_color)
        self._remove_button_color = QColor(remove_button_color)
        self._button_width = button_width
        self._button_height = button_height
        self._icon_margin = icon_margin
        self._border_radius = border_radius

    def paint(self, painter, option, index):
        super().paint(painter, option, index)

        if index.row() % 4 == 0:  # Button row
            subtitle_index = index.row() // 4
            button_rects = self.button_rects.setdefault(subtitle_index, {})

            # Define button rectangles
            button_y = option.rect.bottom() - self._button_height
            add_button_rect = QRect(option.rect.x(), button_y, self._button_width, self._button_height)
            remove_button_rect = QRect(option.rect.x() + self._button_width + 5, button_y, self._button_width, self._button_height)

            button_rects['add'] = add_button_rect
            button_rects['remove'] = remove_button_rect

            # Draw Add button
            self._draw_rounded_rect(painter, add_button_rect, self._add_button_color)
            self._draw_icon(painter, self._add_icon, add_button_rect)

            # Draw Remove button
            self._draw_rounded_rect(painter, remove_button_rect, self._remove_button_color)
            self._draw_icon(painter, self._remove_icon, remove_button_rect)


    # Draw a rounded rectangle
    def _draw_rounded_rect(self, painter, rect, color):
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, self._border_radius, self._border_radius)

    # Draw the icon inside the button rectangle
    def _draw_icon(self, painter, icon, button_rect):
        icon_size = QSize(self._button_width - 2 * self._icon_margin, self._button_height - 2 * self._icon_margin)
        icon_pixmap = icon.pixmap(icon_size)
        icon_rect = QRect(
            button_rect.x() + self._icon_margin,
            button_rect.y() + self._icon_margin,
            icon_size.width(),
            icon_size.height()
        )
        painter.drawPixmap(icon_rect, icon_pixmap)

    # Display text with newlines removed
    def displayText(self, text, locale):
        return text.replace('\n', '')

    def editorEvent(self, event, model, option, index):
        if index.row() % 4 == 0:  # Button row
            subtitle_index = index.row() // 4
            button_rects = self.button_rects.get(subtitle_index, {})

            if event.type() == QEvent.MouseButtonRelease:
                if button_rects['add'].contains(event.pos()):
                    self._add_row(model, subtitle_index)
                    return True
                elif button_rects['remove'].contains(event.pos()):
                    self._remove_row(model, subtitle_index)
                    return True
                
        return super().editorEvent(event, model, option, index)

    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        if index.row() % 4 == 1:  # Apply input mask to every second row in every block of four rows
            editor.setInputMask("99:99:99,999 \-\-\> 99:99:99,999")  # Example input mask (date format)
        editor.setText(index.data(Qt.EditRole))
        return editor

    def setEditorData(self, editor, index):
        editor.setText(index.data(Qt.EditRole))

    def setModelData(self, editor, model, index):
        model.setData(index, editor.text(), Qt.EditRole)

    # Emit signal to add a row
    def _add_row(self, model, subtitle_index):
        self.add_transcript.emit(subtitle_index)

    # Emit signal to remove a row
    def _remove_row(self, model, subtitle_index):
        self.remove_transcript.emit(subtitle_index)
