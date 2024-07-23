from qt_core import *

class PyTranscriptModel(QAbstractItemModel):
    def __init__(self, subtitles=None, parent=None):
        super().__init__(parent)
        self.subtitles = subtitles if subtitles else []

    def rowCount(self, parent=QModelIndex()):
        if parent.isValid():
            return 0
        return len(self.subtitles) * 4  # 1 button row + 1 duration row + 1 text row per subtitle + Extra Space

    def columnCount(self, parent=QModelIndex()):
        if parent.isValid():
            return 0
        return 1  # Single column

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < self.rowCount()):
            return None

        subtitle_index = index.row() // 4

        if index.row() % 4 == 0:  # Button row
            return None

        subtitle = self.subtitles[subtitle_index]

        if role in (Qt.DisplayRole, Qt.EditRole):
            if index.row() % 4 == 1:  # Duration row
                return subtitle['duration']
            elif index.row() % 4 == 2:  # Text row
                return subtitle['text']
        
        return None

    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid() or not (0 <= index.row() < self.rowCount()):
            return False

        subtitle_index = index.row() // 4
        if role == Qt.EditRole:
            if index.row() % 4 == 1:  # Duration row
                self.subtitles[subtitle_index]['duration'] = value
                self.dataChanged.emit(index, index, [Qt.DisplayRole, Qt.EditRole])
                return True
            elif index.row() % 4 == 2:  # Text row
                self.subtitles[subtitle_index]['text'] = value
                self.dataChanged.emit(index, index, [Qt.DisplayRole, Qt.EditRole])
                return True
        return False

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        row = index.row()

        # Determine if the row belongs to a valid subtitle
        subtitle_index = row // 4
        if subtitle_index >= len(self.subtitles):
            return Qt.NoItemFlags  # Out of bounds

        # Determine the type of row
        row_type = row % 4

        # Only duration and text rows are editable
        if row_type in [1, 2]:  # Duration row (1) and Text row (2)
            return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
        else:
            return Qt.NoItemFlags  # Button rows (0) and invalid rows


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

    def insertRow(self, position, id, duration):
        self.beginInsertRows(QModelIndex(), position * 4, position * 4 + 2)
        self.subtitles.insert(position, {'id': id, 'duration': duration, 'text': 'New subtitle'})
        self.endInsertRows()
        return position

    def removeRow(self, position):
        self.beginRemoveRows(QModelIndex(), position * 4, position * 4 + 2)  # Remove 4 rows (button, duration, and text)
        del self.subtitles[position]
        self.endRemoveRows()

    def clearAllRows(self):
        self.beginResetModel()
        self.subtitles.clear()
        self.endResetModel()
