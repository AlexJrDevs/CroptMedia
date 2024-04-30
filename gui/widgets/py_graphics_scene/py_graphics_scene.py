from qt_core import *

class PyGraphicsScene(QGraphicsScene):
    def __init__(self):
        super().__init__()

        self.vertical_line = QGraphicsLineItem()
        self.vertical_line.setLine
        self.addItem(self.vertical_line)
        self.vertical_line.hide()

        self.horizontal_line = QGraphicsLineItem()
        self.addItem(self.horizontal_line)
        self.horizontal_line.hide()

        self.horizontal_line.setZValue(1)
        self.vertical_line.setZValue(1)

        pen = QPen(Qt.DotLine)
        pen.setDashPattern([5, 5])
        pen.setColor(Qt.red)
        self.vertical_line.setPen(pen)
        self.horizontal_line.setPen(pen)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        selected_item = self.selectedItems()
        for item in selected_item:
            if item.textInteractionFlags() == Qt.NoTextInteraction:
                center_y = self.sceneRect().center().y() - item.sceneBoundingRect().height() / 2
                center_x = self.sceneRect().center().x() - item.sceneBoundingRect().width() / 2

                if abs(item.sceneBoundingRect().center().x() - self.width() / 2)< 15:
                    item.setPos(center_x, item.pos().y())
                    self.vertical_line.show()
                else:
                    self.vertical_line.hide()

                if abs(item.sceneBoundingRect().center().y() - self.height() / 2) < 15:
                    item.setPos(item.pos().x(), center_y)
                    self.horizontal_line.show()
                else:
                    self.horizontal_line.hide()

    def mouseReleaseEvent(self, event):
        self.vertical_line.hide()
        self.horizontal_line.hide()
        super().mouseReleaseEvent(event)

    def resizeGuides(self):
        view_rect = self.sceneRect()

        self.vertical_line.setLine(view_rect.width() / 2, 0, view_rect.width() / 2, view_rect.height())
        self.horizontal_line.setLine(0, view_rect.height() / 2, view_rect.width(), view_rect.height() / 2)
