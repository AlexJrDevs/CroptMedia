from qt_core import *

class PyTranscriptModel(QAbstractItemModel):
    def __init__(self, subtitles=None, parent=None):
        super().__init__(parent)
        self.subtitles = subtitles if subtitles else []

    def rowCount(self, parent=QModelIndex()):
        if parent.isValid():
            return 0
        return len(self.subtitles) * 3  # Each subtitle has a time, text, and an empty row

    def columnCount(self, parent=QModelIndex()):
        if parent.isValid():
            return 0
        return 1  # Single column for alternating Time, Text, and Empty

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < self.rowCount()):
            return None

        subtitle_index = index.row() // 3
        subtitle = self.subtitles[subtitle_index]

        if role == Qt.DisplayRole or role == Qt.EditRole:
            if index.row() % 3 == 0:  # Every third row: Time
                return subtitle['duration']
            elif index.row() % 3 == 1:  # Text row
                return subtitle['text']
            else:  # Empty row
                return ""

        return None

    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid() or not (0 <= index.row() < self.rowCount()):
            return False

        subtitle_index = index.row() // 3
        if role == Qt.EditRole:
            if index.row() % 3 == 0:  # Every third row: Time
                self.subtitles[subtitle_index]['duration'] = value
            elif index.row() % 3 == 1:  # Text row
                self.subtitles[subtitle_index]['text'] = value
            else:  # Empty row
                return False
            self.dataChanged.emit(index, index, [Qt.DisplayRole, Qt.EditRole])
            return True
        return False

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        if index.row() % 3 == 2:  # Empty row
            return Qt.NoItemFlags
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return "Transcript Will Appear Here..."
        return None

    def index(self, row, column, parent=QModelIndex()):
        if self.hasIndex(row, column, parent):
            return self.createIndex(row, column)
        return QModelIndex()

    def parent(self, index):
        return QModelIndex()
