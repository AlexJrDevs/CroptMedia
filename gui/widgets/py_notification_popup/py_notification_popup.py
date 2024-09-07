from qt_core import *

from PySide6.QtSvg import QSvgRenderer

class PyNotificationPopup(QWidget):
    def __init__(self, parent, message):
        super().__init__(parent)
        
        layout = QHBoxLayout(self)
        bg_widget = QWidget()
        bg_widget.setLayout(layout)

        # Set stylesheet for background widget
        bg_widget.setStyleSheet('background-color: #2C313C; border-top-left-radius: 10px; border-bottom-left-radius: 10px;')
        
        # Icon
        icon_width = 24
        self.iconLabel = QLabel(self)
        svg_renderer = QSvgRenderer("gui\images\svg_icons\icon_info.svg")
        pixmap = QPixmap(icon_width, icon_width)  # Adjust size as needed
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        svg_renderer.render(painter)
        painter.end()
        
        self.iconLabel.setPixmap(pixmap)
        self.iconLabel.setFixedSize(icon_width, self.height())  # Ensure the QLabel does not expand beyond the icon size
        layout.addWidget(self.iconLabel)
        
        # Message
        self.messageLabel = QLabel(message, self)
        self.messageLabel.setStyleSheet("color: #C3CCDF;")
        self.messageLabel.setWordWrap(True)
        layout.addWidget(self.messageLabel)
        
        # Set layout and fixed size
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(bg_widget)  # Add bg_widget to the main layout
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.setFixedSize(300, 80)  # Adjust width and height as needed
        
        # Adjust font size
        self.adjustFontSize()
        
        # Animations
        self.animation = QSequentialAnimationGroup(self)
        self.slideIn = QPropertyAnimation(self, b'geometry')
        self.pause = QPauseAnimation(3000)
        self.slideOut = QPropertyAnimation(self, b'geometry')
        
        self.animation.addAnimation(self.slideIn)
        self.animation.addAnimation(self.pause)
        self.animation.addAnimation(self.slideOut)

    def adjustFontSize(self):
        font = QFont("Roboto", 11)
        self.messageLabel.setFont(font)
        
        # Check if the text fits
        metrics = QFontMetrics(font)
        text_rect = metrics.boundingRect(self.rect(), Qt.TextWordWrap, self.messageLabel.text())
        
        # If text doesn't fit, reduce font size
        while text_rect.height() > self.height() - 10 and font.pointSize() > 7:
            font.setPointSize(font.pointSize() - 1)
            self.messageLabel.setFont(font)
            metrics = QFontMetrics(font)
            text_rect = metrics.boundingRect(self.rect(), Qt.TextWordWrap, self.messageLabel.text())

    def updateGeometry(self, startRect, endRect):
        self.slideIn.setStartValue(startRect)
        self.slideIn.setEndValue(endRect)
        self.slideOut.setStartValue(endRect)
        self.slideOut.setEndValue(startRect)