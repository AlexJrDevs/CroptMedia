from qt_core import *


# DETAILED EXPLANATION OF DOUBLE CLICK EDIT
# https://www.qtcentre.org/threads/20332-QGraphicsTextItem-and-text-cursor-position-via-QPoint?p=234213#post234213

class PyGraphicsTextItem(QGraphicsTextItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._outline_size = 5
        self._outline_color = QColor("black")
        self.setCursor(Qt.SizeAllCursor)

        self.outline_format = QTextCharFormat()
        self.outline_format.setTextOutline(QPen(
            Qt.GlobalColor.black, 5, 
            Qt.PenStyle.SolidLine, 
            Qt.PenCapStyle.RoundCap, 
            Qt.PenJoinStyle.RoundJoin
        ))
        self.dummy_format = QTextCharFormat()
        self.dummy_format.setTextOutline(QPen(Qt.GlobalColor.transparent))

        children = self.findChildren(QObject)
        if not children:
            super().setPlainText('')
            children = self.findChildren(QObject)
        if self.toPlainText():
            # ensure we call our version of setPlainText()
            self.setPlainText(self.toPlainText())

        for obj in children:
            if obj.metaObject().className() == 'QWidgetTextControl':
                self.textControl = obj
                break

    def setTextInteraction(self, state):
        if state and self.textInteractionFlags() == Qt.NoTextInteraction:
            self.setTextInteractionFlags(Qt.TextEditorInteraction)
 
            self.setCursor(Qt.IBeamCursor)
            self.setFocus(Qt.MouseFocusReason)  

 
        elif not state and self.textInteractionFlags() == Qt.TextEditorInteraction:
            self.setTextInteractionFlags(Qt.NoTextInteraction)
 

 
    def mouseDoubleClickEvent(self, event):
        if self.textInteractionFlags() == Qt.TextEditorInteraction:
            super().mouseDoubleClickEvent(event)
            return
 
        self.setTextInteraction(True)
 
        click = QGraphicsSceneMouseEvent(QEvent.GraphicsSceneMousePress)
        click.setButton(event.button())
        click.setPos(event.pos())
        self.mousePressEvent(click)
        
 
    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemSelectedChange \
            and self.textInteractionFlags() != Qt.NoTextInteraction \
            and not value:
 
            self.setTextInteractionFlags(Qt.NoTextInteraction)
            self.setCursor(Qt.SizeAllCursor)
     
 
        return super().itemChange(change, value)

    def setPlainText(self, text):
        super().setPlainText(text)
        if text:
            format = QTextCharFormat()
            format.setFontPointSize(90)
            cursor = QTextCursor(self.document())
            cursor.select(QTextCursor.SelectionType.Document)
            cursor.mergeCharFormat(format)


    def paint(self, painter, option, widget):
        super().paint(painter, option, widget)
        painter.save()
        painter.setClipRect(self.scene().sceneRect())
        super().paint(painter, option, widget)
        painter.restore()
        with QSignalBlocker(self.textControl):
            if self._outline_size > 0:
                super().paint(painter, option, widget) 
                cursor = QTextCursor(self.document())
                cursor.select(QTextCursor.SelectionType.Document)
                cursor.mergeCharFormat(self.outline_format)
                super().paint(painter, option, widget)
                cursor.mergeCharFormat(self.dummy_format)
                super().paint(painter, option, widget)
            else:
                super().paint(painter, option, widget)

    def set_outline_size(self, size):
        self._outline_size = size

        self.outline_format.setTextOutline(QPen(
            self._outline_color, size, 
            Qt.PenStyle.SolidLine, 
            Qt.PenCapStyle.RoundCap, 
            Qt.PenJoinStyle.RoundJoin
        ))

    def set_outline_color(self, color):
        self._outline_color = color

        self.outline_format.setTextOutline(QPen(
            color, self._outline_size, 
            Qt.PenStyle.SolidLine, 
            Qt.PenCapStyle.RoundCap, 
            Qt.PenJoinStyle.RoundJoin
        ))


    def grab_stroke_data(self):
        return (self._outline_size, self._outline_color)