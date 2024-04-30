
from qt_core import *
from functools import partial
import re


from gui.widgets import PyIconButton, PySlider, PyGraphicsTextItem, PyGraphicsScene, PyGraphicsView

dark_style = """
            background-color: #2C313C; border-radius: 8px;
        """

bright_style = """
            background-color: #343B48; border-radius: 8px;
        """


class PyVideoPlayer(QWidget):

    text_preview_done = Signal(list, QWidget)
    
    def __init__(self, parent):
        super(PyVideoPlayer, self).__init__(parent)
        self.parent = parent

        self.text_preview_widgets = []
        self.text_data=[]
        self.previous_text = {}

        self.mediaPlayer = QMediaPlayer()
        self.audioOutput = QAudioOutput()

        ##########################################################################################################
    

        self.graphics_view = PyGraphicsView()
        self.graphic_scene = PyGraphicsScene()

        self.graphics_view.setScene(self.graphic_scene)
        self.graphic_scene.setBackgroundBrush(Qt.black)
        self.graphics_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphics_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.video_item = QGraphicsVideoItem()

        self.graphic_scene.addItem(self.video_item)

        self.graphics_view.setStyleSheet("background-color: transparent; border: 0px solid transparent;")
        

        ###########################################################################################################
        
        self.sliders_widget = QWidget()
        self.sliders_layout = QVBoxLayout()
        self.sliders_widget.setLayout(self.sliders_layout)


        self.position_slider_widget = QWidget()
        self.position_slider_layout = QVBoxLayout()
        self.position_slider_widget.setLayout(self.position_slider_layout)
        self.position_slider_widget.setStyleSheet(dark_style)
        self.position_slider_layout.setSpacing(0)


        self.position_slider = PySlider(margin=3, orientation=Qt.Horizontal)
        self.position_slider.setRange(0, 0)
        
        
        video_button_widget = QWidget()
        video_button_layout = QHBoxLayout()
        video_button_widget.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)

        bg_btn_widget = QWidget()
        bg_btn_widget.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        bg_btn_widget.setStyleSheet(dark_style)
        bg_btn_layout = QHBoxLayout()
        bg_btn_widget.setLayout(bg_btn_layout)

        video_button_layout.setContentsMargins(5, 0, 5, 0)
        video_button_widget.setLayout(video_button_layout)


        video_button_widget.setStyleSheet(bright_style)


        self.play_button = PyIconButton(icon_path= r"gui\images\svg_icons\icon_pause.svg", 
                                        width=45, 
                                        height=45,
                                        icon_margin=15,
                                        bg_color_hover = "#343B48",
                                        bg_color="#343B48"
                                    )
        self.play_button.setEnabled(False)
        self.play_button.clicked.connect(self.play)

        self.volume_button = PyIconButton(icon_path= r"gui\images\svg_icons\icon_volume.svg", 
                                            width=45, 
                                            height=45,
                                            icon_margin=15,
                                            bg_color_hover = "#343B48",
                                            bg_color="#343B48"
                                        )
        self.volume_button.clicked.connect(self.showVolumeSlider)

        self.volume_slider = PySlider(margin=3, orientation=Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(int(self.audioOutput.volume() * 100))
        self.volume_slider.setMaximumWidth(100)
        self.volume_slider.sliderMoved.connect(self.setVolume)
        self.volume_slider.hide()

        self.time_label = QLabel()
        self.time_label.setStyleSheet(
            "color: #4f5b6e; font-family: 'Roboto'; font-size: 9pt; font-weight: bold;"
        )


        self.add_button = PyIconButton(icon_path= r"gui\images\svg_icons\icon_add.svg", 
                                    width=45, 
                                    height=45,
                                    icon_margin=15,
                                    bg_color_hover = "#343B48",
                                    bg_color="#343B48"
                                )
        
        self.remove_button = PyIconButton(icon_path= r"gui\images\svg_icons\icon_minus.svg", 
                                        width=45, 
                                        height=45,
                                        icon_margin=15,
                                        bg_color_hover = "#343B48",
                                        bg_color="#343B48"
                                    )
        
        self.done_button = PyIconButton(icon_path= r"gui\images\svg_icons\icon_check.svg", 
                                   width=40, 
                                   height=40,
                                   icon_margin=15,
                                   bg_color_hover = "#343B48",
                                   bg_color="#343B48"
                                )

        # Set up the layout
        self.position_slider_layout.addWidget(self.position_slider)
        self.sliders_layout.addWidget(self.position_slider_widget)
        
        video_button_layout.addWidget(self.play_button)
        video_button_layout.addWidget(self.volume_button)
        video_button_layout.addWidget(self.volume_slider)
        video_button_layout.addWidget(self.time_label)

        bg_btn_layout.addWidget(video_button_widget)


        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.addWidget(self.graphics_view, stretch=1)
        layout.addWidget(self.sliders_widget)
        layout.addWidget(bg_btn_widget)


        self.setLayout(layout)

        # Slots Section
        self.mediaPlayer.setVideoOutput(self.video_item)
        self.mediaPlayer.playbackStateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.errorOccurred.connect(self.handleError)


        self.position_slider.sliderMoved.connect(self.setPosition)


        self.graphic_scene.sceneRectChanged.connect(self.itemsPos)




    def setMedia(self, fileName):
        self.mediaPlayer.setSource(QUrl.fromLocalFile(fileName))
        self.mediaPlayer.setAudioOutput(self.audioOutput)
        self.play_button.setEnabled(True)
        self.play()
        self.video_item.setSize(self.mediaPlayer.videoSink().videoSize())
        for text in self.text_preview_widgets:
            text.setPos(self.graphic_scene.sceneRect().center().x() - text.boundingRect().center().x(), self.graphic_scene.sceneRect().center().y() - text.boundingRect().center().y())



    def play(self):
        if self.mediaPlayer.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):

        if state == QMediaPlayer.PlaybackState.PlayingState:
            self.play_button.set_icon("gui/images/svg_icons/icon_pause.svg")
        else:
            self.play_button.set_icon("gui/images/svg_icons/icon_play.svg")

    def positionChanged(self, position):
        # Update position slider
        self.position_slider.setValue(position)

        duration_ms = self.mediaPlayer.duration()
        if duration_ms >= 3600000:  # If duration is 1 hour or more
            self.time_label.setText(
                f"{position // 3600000:02}:{(position // 60000) % 60:02}:{(position // 1000) % 60:02},{position % 1000:03} / "
                f"{duration_ms // 3600000:02}:{(duration_ms // 60000) % 60:02}:{(duration_ms // 1000) % 60:02},{duration_ms % 1000:03}"
            )
        elif duration_ms >= 60000:  # If duration is 1 minute or more
            self.time_label.setText(
                f"{position // 60000:02}:{(position // 1000) % 60:02},{position % 1000:03} / "
                f"{duration_ms // 60000:02}:{(duration_ms // 1000) % 60:02},{duration_ms % 1000:03}"
            )
        else:  # If duration is less than 1 minute
            self.time_label.setText(
                f"{(position // 1000):02},{position % 1000:03} / {(duration_ms // 1000):02},{duration_ms % 1000:03}"
            )

        # Update visibility of text previews based on position
        for text_preview, duration_line_edit, text_edit_widget, start_total_milliseconds, end_total_milliseconds in self.text_data:
            if start_total_milliseconds <= position <= end_total_milliseconds and not text_preview.isVisible():
                text_preview.show()
                print("Start: ", start_total_milliseconds)
            elif text_preview.isVisible() and not start_total_milliseconds <= position <= end_total_milliseconds:
                print("Hide")
                text_preview.hide()

    def durationChanged(self, duration):
        self.position_slider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def setVolume(self, volume):
        self.audioOutput.setVolume(volume / 100)

    def showVolumeSlider(self):
        if self.volume_slider.isHidden():
            self.volume_slider.show()
        else:
            self.volume_slider.hide()

    def handleError(self):
        self.play_button.setEnabled(False)
        print("Error: " + self.mediaPlayer.errorString())

    def reset_media(self):
        self.mediaPlayer.stop()

    
    def create_preview_text(self, data_list):

        for duration_line_edit, text_edit_widget, start_total_milliseconds, end_total_milliseconds in data_list:
            text_preview = PyGraphicsTextItem(parent=self.video_item)
            text_preview.setDefaultTextColor(QColor("White"))
            text_edit_widget.font().setPointSize(int(90))
            text_preview.setFont(text_edit_widget.font())
            text_preview.setPlainText(text_edit_widget.toPlainText())
            
            text_preview.setFlags(QGraphicsTextItem.ItemIsSelectable | QGraphicsTextItem.ItemIsMovable | QGraphicsTextItem.ItemIsFocusable)

            self.text_preview_widgets.append(text_preview)
            self.text_data.append([text_preview, duration_line_edit, text_edit_widget, start_total_milliseconds, end_total_milliseconds])

            text_preview.document().contentsChange.connect(partial(self.text_changed, text_item=text_preview))
            text_edit_widget.textChanged.connect(partial(self.text_edit_changed, text_edit_widget))
            duration_line_edit.textChanged.connect(partial(self.change_text_duration, duration_line_edit))

        self.text_preview_done.emit(self.text_preview_widgets, self.graphic_scene)

    def text_changed(self, position, charsRemoved, charsAdded, text_item):
        current_text = text_item.toPlainText()
        previous_text = self.previous_text.get(text_item, None)
        
        # Check if there's a change in text
        if current_text != previous_text:
            for text_preview, duration_line_edit, text_edit_widget, start_total_milliseconds, end_total_milliseconds in self.text_data:
                if text_preview == text_item:
                    text_edit_widget.blockSignals(True)  # Disconnect signal temporarily
                    text_edit_widget.setPlainText(current_text)
                    self.previous_text[text_item] = current_text
                    text_edit_widget.blockSignals(False)  # Reconnect signal
                    break


    def text_edit_changed(self, text_edit):
        new_text = text_edit.toPlainText()
        cursor_position = text_edit.textCursor().position()

        for text_preview, duration_line_edit, text_edit_widget, start_total_milliseconds, end_total_milliseconds in self.text_data:
            if text_edit_widget == text_edit:
                text_preview.blockSignals(True)  # Disconnect signal temporarily
                text_preview.setPlainText(new_text)
                # Restore cursor position in text_edit
                cursor = text_edit_widget.textCursor()
                cursor.setPosition(cursor_position)
                text_edit_widget.setTextCursor(cursor)
                text_edit_widget.blockSignals(False)  # Reconnect signal
                break

    def change_text_duration(self, time, *args):
        for index, (text_preview, duration_line_edit, text_edit_widget, start_total_milliseconds, end_total_milliseconds) in enumerate(self.text_data):
            if duration_line_edit == time:
                text = duration_line_edit.text()
                match = re.match(r'(\d{2}:\d{2}:\d{2},\d{2,3}) \-\-\> (\d{2}:\d{2}:\d{2},\d{2,3})', text)
                print("Update: ", text)
                if match:
                    start_time, end_time = match.group(1, 2)
                    
                    start_parts = start_time.split(':')
                    start_hours = int(start_parts[0])
                    start_minutes = int(start_parts[1])
                    start_seconds, start_milliseconds = map(int, start_parts[2].split(','))
                    start_total_milliseconds = (start_hours * 3600 + start_minutes * 60 + start_seconds) * 1000 + start_milliseconds
                    
                    end_parts = end_time.split(':')
                    end_hours = int(end_parts[0])
                    end_minutes = int(end_parts[1])
                    end_seconds, end_milliseconds = map(int, end_parts[2].split(','))
                    end_total_milliseconds = (end_hours * 3600 + end_minutes * 60 + end_seconds) * 1000 + end_milliseconds

                    print("Start Time (ms):", start_total_milliseconds)
                    print("End Time (ms):", end_total_milliseconds)
                    
                    # Update the tuple in self.text_data with new start and end times
                    self.text_data[index] = (text_preview, duration_line_edit, text_edit_widget, start_total_milliseconds, end_total_milliseconds)
                else:
                    print("Invalid time format")
                




    def itemsPos(self, sceneRect):
            if sceneRect != self.graphics_view.rect():
                self.graphic_scene.setSceneRect(self.video_item.boundingRect())


    def resize_graphic_scene(self):
        self.graphics_view.fitInView(self.graphic_scene.sceneRect(), Qt.KeepAspectRatio)
        self.graphic_scene.resizeGuides()

    def showEvent(self, event):
        self.resize_graphic_scene()

    def resizeEvent(self, event):
        self.resize_graphic_scene()




            
    


    
    

    


