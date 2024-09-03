from qt_core import *

class PyGraphicsScene(QGraphicsScene):
    def __init__(self):
        super().__init__()

        self.item_near_center = 5  # How close an item has to be to center it on x / y

        self.vertical_line = QGraphicsLineItem()
        self.addItem(self.vertical_line)
        self.vertical_line.hide()

        self.horizontal_line = QGraphicsLineItem()
        self.addItem(self.horizontal_line)
        self.horizontal_line.hide()

        # Ensure the guidelines are on top by setting a high Z-value
        self.horizontal_line.setZValue(1)
        self.vertical_line.setZValue(1)

        pen = QPen(Qt.DotLine)
        pen.setDashPattern([2, 5])  # Dashes Width : Dashes Distances
        pen.setColor(Qt.red)
        self.vertical_line.setPen(pen)
        self.horizontal_line.setPen(pen)

        # Make the guidelines non-interactive
        self.vertical_line.setFlag(QGraphicsItem.ItemIsMovable, False)
        self.vertical_line.setFlag(QGraphicsItem.ItemIsSelectable, False)
        self.vertical_line.setFlag(QGraphicsItem.ItemIsFocusable, False)

        self.horizontal_line.setFlag(QGraphicsItem.ItemIsMovable, False)
        self.horizontal_line.setFlag(QGraphicsItem.ItemIsSelectable, False)
        self.horizontal_line.setFlag(QGraphicsItem.ItemIsFocusable, False)

        # Initialize lines
        self.resizeGuides()

        self.moving_item = None  # Track the item that is currently being moved

    def mousePressEvent(self, event):
        # When the mouse is pressed, check if an item is under the cursor
        super().mousePressEvent(event)
        item = self.itemAt(event.scenePos(), QTransform())
        if item and isinstance(item, QGraphicsTextItem):
            self.moving_item = item  # Start tracking the moving item
        else:
            self.moving_item = None

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self.moving_item:
            scene_center = self.sceneRect().center()
            item_rect = self.moving_item.sceneBoundingRect()
            center_y = scene_center.y() - item_rect.height() / 2
            center_x = scene_center.x() - item_rect.width() / 2

            if abs(item_rect.center().x() - scene_center.x()) < self.item_near_center:
                self.moving_item.setPos(center_x, self.moving_item.pos().y())
                self.vertical_line.show()
            else:
                self.vertical_line.hide()

            if abs(item_rect.center().y() - scene_center.y()) < self.item_near_center:
                self.moving_item.setPos(self.moving_item.pos().x(), center_y)
                self.horizontal_line.show()
            else:
                self.horizontal_line.hide()

    def mouseReleaseEvent(self, event):
        self.vertical_line.hide()
        self.horizontal_line.hide()
        self.moving_item = None  # Stop tracking the item after releasing the mouse
        super().mouseReleaseEvent(event)

    def resizeGuides(self):
        view_rect = self.sceneRect()

        # Calculate the center of the scene rect
        center_x = view_rect.left() + view_rect.width() / 2
        center_y = view_rect.top() + view_rect.height() / 2

        # Adjust the vertical and horizontal lines to match the scene's center
        self.vertical_line.setLine(center_x, view_rect.top(), center_x, view_rect.bottom())
        self.horizontal_line.setLine(view_rect.left(), center_y, view_rect.right(), center_y)
