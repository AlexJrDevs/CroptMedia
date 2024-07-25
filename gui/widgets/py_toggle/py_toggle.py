# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from qt_core import *

class PyToggle(QCheckBox):
    def __init__(
        self,
        width=50,
        bg_color="#777",
        circle_color="#DDD",
        active_color="#00BCFF",
        distance_from_end=4,
        animation_curve=QEasingCurve.OutBounce
    ):
        super().__init__()

        self.setMaximumWidth(width)
        self.setMinimumHeight(28)
        self.setCursor(Qt.PointingHandCursor)

        # COLORS
        self._bg_color = bg_color
        self._circle_color = circle_color
        self._active_color = active_color

        self._distance_from_end = distance_from_end
        self._position = 4  # Initial position
        self.animation = QPropertyAnimation(self, b"position")
        self.animation.setEasingCurve(animation_curve)
        self.animation.setDuration(500)
        self.stateChanged.connect(self.setup_animation)

    @Property(float)
    def position(self):
        return self._position

    @position.setter
    def position(self, pos):
        self._position = pos
        self.update()

    def setup_animation(self, value):
        self.animation.stop()
        if value:
            self.animation.setEndValue(self.width() - 22 - self._distance_from_end)  # Adjust end value based on circle diameter
        else:
            self.animation.setEndValue(4)
        self.animation.start()

    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setFont(QFont("Segoe UI", 9))

        # SET PEN
        p.setPen(Qt.NoPen)

        # DRAW RECT
        rect = QRect(0, 0, self.width(), self.height())
        circle_diameter = 22
        circle_radius = circle_diameter / 2

        # Draw the background rectangle
        if not self.isChecked():
            p.setBrush(QColor(self._bg_color))
        else:
            p.setBrush(QColor(self._active_color))
        p.drawRoundedRect(0, 0, rect.width(), 28, 14, 14)

        # Calculate circle position
        if self.isChecked():
            circle_position = self.width() - circle_diameter - self._distance_from_end
        else:
            circle_position = self._position

        # Ensure circle position is within bounds
        circle_position = min(max(circle_position, 4), self.width() - circle_diameter - 4)

        p.setBrush(QColor(self._circle_color))
        p.drawEllipse(circle_position, 3, circle_diameter, circle_diameter)

        p.end()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Ensure circle position remains within bounds after resize
        if self.isChecked():
            self._position = self.width() - 22 - self._distance_from_end
            self.update()


