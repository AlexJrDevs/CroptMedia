from qt_core import *

class PyGraphicsView(QGraphicsView):
    def drawForeground(self, qp, rect):
        qp.resetTransform()
        viewRect = self.viewport().rect()
        sceneRect = self.mapFromScene(self.sceneRect())
        qp.setClipRegion(
            QRegion(viewRect)
            - QRegion(sceneRect.boundingRect())
        )
        qp.fillRect(viewRect, QColor("#343B48"))