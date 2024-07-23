from qt_core import *

class PyTranscriptDelegate(QStyledItemDelegate):
    add_transcript = Signal(int)
    remove_transcript = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.button_rects = {}

        # Default properties
        self.add_icon = QIcon("gui/images/svg_icons/icon_add.svg")
        self.remove_icon = QIcon("gui/images/svg_icons/icon_minus.svg")
        self.add_button_color = QColor('#3c4454')  # Use QColor for colors
        self.remove_button_color = QColor('#3c4454')
        self.button_width = 20
        self.button_height = 20  # Adjust this height as needed
        self.icon_margin = 4  # Margin between icon and button edges
        self.border_radius = 5  # Border radius for the rounded corners

    def paint(self, painter, option, index):
        super().paint(painter, option, index)

        if index.row() % 4 == 0:  # Button row
            subtitle_index = index.row() // 4
            button_rects = self.button_rects.setdefault(subtitle_index, {})

            # Define button rectangles with customizable size, positioned at the bottom left
            button_y = option.rect.bottom() - self.button_height  # Bottom edge of the row
            add_button_rect = QRect(option.rect.x(), button_y, self.button_width, self.button_height)
            remove_button_rect = QRect(option.rect.x() + self.button_width + 5, button_y, self.button_width, self.button_height)  # Added a 5-pixel gap

            button_rects['add'] = add_button_rect
            button_rects['remove'] = remove_button_rect

            # Draw Add button with custom background color and border radius
            self._draw_rounded_rect(painter, add_button_rect, self.add_button_color)
            self._draw_icon(painter, self.add_icon, add_button_rect)

            # Draw Remove button with custom background color and border radius
            self._draw_rounded_rect(painter, remove_button_rect, self.remove_button_color)
            self._draw_icon(painter, self.remove_icon, remove_button_rect)

    def _draw_rounded_rect(self, painter, rect, color):
        # Draw a rounded rectangle with the given color
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.NoPen)  # No border line
        painter.drawRoundedRect(rect, self.border_radius, self.border_radius)

    def _draw_icon(self, painter, icon, button_rect):
        # Draw the icon with a margin inside the button rectangle
        icon_size = QSize(self.button_width - 2 * self.icon_margin, self.button_height - 2 * self.icon_margin)
        icon_pixmap = icon.pixmap(icon_size)
        icon_rect = QRect(
            button_rect.x() + self.icon_margin,
            button_rect.y() + self.icon_margin,
            icon_size.width(),
            icon_size.height()
        )
        painter.drawPixmap(icon_rect, icon_pixmap)

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

    def _add_row(self, model, subtitle_index):
        # Insert new row above the selected subtitle row
        self.add_transcript.emit(subtitle_index)

    def _remove_row(self, model, subtitle_index):
        # Remove the selected subtitle
        self.remove_transcript.emit(subtitle_index)
