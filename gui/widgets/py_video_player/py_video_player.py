
from qt_core import *

import os

from gui.widgets import PyIconButton, PySlider,  PyGraphicsScene, PyGraphicsView

dark_style = """
            background-color: #2C313C; border-radius: 8px;
        """

bright_style = """
            background-color: #343B48; border-radius: 8px;
        """


class PyVideoPlayer(QWidget):

    text_being_shown = Signal(str)

    def __init__(self, parent):
        super(PyVideoPlayer, self).__init__(parent)
        self.parent = parent

        self.text_data={}

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
        self.video_item.setAspectRatioMode(Qt.KeepAspectRatioByExpanding)

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
        video_button_widget.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        bg_btn_widget = QWidget()
        bg_btn_widget.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
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
        self.mediaPlayer.videoOutputChanged.connect(self.resize_graphic_scene)


        self.position_slider.sliderMoved.connect(self.setPosition)

    def extract_text_data(self):
        text_html = []
        for subtitle_index, (text_preview, subtitle_duration, subtitle_text, start_total_milliseconds, end_total_milliseconds) in self.text_data.items():

            text_preview.toHtml()
            stroke_size, stroke_color = text_preview.grab_stroke_data()
            print(stroke_size)
            
            start_time = self.milliseconds_to_time(start_total_milliseconds)
            end_time = self.milliseconds_to_time(end_total_milliseconds)

            temp_location = os.path.abspath(r'backend\tempfile')
            text_html_location = os.path.join(temp_location, f"Subtitle_{subtitle_index}.html")

            with open(text_html_location, "w") as file:
                file.write(text_preview.toHtml())

            text_html.append([text_html_location, str(text_preview.pos().x()), str(text_preview.pos().y()), stroke_size, stroke_color, start_time, end_time])
            file.close()
        
        return text_html
    
    def milliseconds_to_time(self, milliseconds):
        seconds = milliseconds // 1000
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return "{:02d}:{:02d}:{:02d}.{:02d}".format(hours, minutes, seconds, milliseconds % 1000 // 10)


    def setMedia(self, fileName):
        self.mediaPlayer.setSource(QUrl.fromLocalFile(fileName))
        self.mediaPlayer.setAudioOutput(self.audioOutput)
        self.play_button.setEnabled(True)
        self.mediaPlayer.play()

        self.resize_graphic_scene()

        for subtitle_index, (text_preview, subtitle_duration, subtitle_text, start_total_milliseconds, end_total_milliseconds) in self.text_data.items():
            text_preview.setPos(self.graphic_scene.sceneRect().center().x() - text_preview.boundingRect().center().x(), self.graphic_scene.sceneRect().center().y() - text_preview.boundingRect().center().y())


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
                f"{position // 3600000:02}:{(position // 60000) % 60:02}:{(position // 1000) % 60:02},{position % 1000:03} /\n "
                f"{duration_ms // 3600000:02}:{(duration_ms // 60000) % 60:02}:{(duration_ms // 1000) % 60:02},{duration_ms % 1000:03}"
            )
        elif duration_ms >= 60000:  # If duration is 1 minute or more
            self.time_label.setText(
                f"{position // 60000:02}:{(position // 1000) % 60:02},{position % 1000:03} /\n "
                f"{duration_ms // 60000:02}:{(duration_ms // 1000) % 60:02},{duration_ms % 1000:03}"
            )
        else:  # If duration is less than 1 minute
            self.time_label.setText(
                f"{(position // 1000):02},{position % 1000:03} /\n {(duration_ms // 1000):02},{duration_ms % 1000:03}"
            )

        # Update visibility of text previews based on position
        for subtitle_id, (text_preview, subtitle_duration, subtitle_text, start_total_milliseconds, end_total_milliseconds) in self.text_data.items():
            if start_total_milliseconds <= position <= end_total_milliseconds and not text_preview.isVisible():
                text_preview.show()
                self.text_being_shown.emit(subtitle_id)

            elif text_preview.isVisible() and not start_total_milliseconds <= position <= end_total_milliseconds:
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


    def resize_graphic_scene(self):
        try:
            video_size = self.mediaPlayer.videoSink().videoSize()
            if not video_size.isEmpty():
                self.video_item.setSize(video_size)
                self.graphic_scene.setSceneRect(self.video_item.boundingRect())
                self.graphics_view.fitInView(self.video_item, Qt.AspectRatioMode.KeepAspectRatio)
                self.graphic_scene.resizeGuides()
                self.updateGeometry()
                self.update()
            
        except Exception as e:
            print("Video Unavailable: ", e)

    def showEvent(self, event):
        self.resize_graphic_scene()

    def resizeEvent(self, event):
        self.resize_graphic_scene()

