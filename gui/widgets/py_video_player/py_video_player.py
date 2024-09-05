
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
        self.first_play = True

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
        self.video_item.setAspectRatioMode(Qt.KeepAspectRatio)


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

        # Resizes the video
        self.mediaPlayer.videoOutputChanged.connect(self.resize_graphic_scene)
        self.mediaPlayer.mediaStatusChanged.connect(self.check_and_position_text_preview) # This slot actually resizes the scene


        self.position_slider.sliderMoved.connect(self.setPosition)

    def extract_text_data(self):
        text_html = []
        for subtitle_index, (text_preview, subtitle_duration, subtitle_text, start_total_milliseconds, end_total_milliseconds) in self.text_data.items():

            text_preview.toHtml()
            stroke_size, stroke_color = text_preview.grab_stroke_data()
            
            start_time = self.milliseconds_to_time(start_total_milliseconds)
            end_time = self.milliseconds_to_time(end_total_milliseconds)

            temp_location = os.path.abspath(r'backend\tempfile')
            text_html_location = os.path.join(temp_location, f"Subtitle_{subtitle_index}.html")

            # Calculate relative position of the text to the video
            # Get the size / pos of the text's bounding box
            text_bounding_box = text_preview.boundingRect()
            text_preview_pos =  text_preview.pos()

            # Calculate the center of the text
            text_center_x = text_preview_pos.x() + text_bounding_box.width() / 2
            text_center_y = text_preview_pos.y() + text_bounding_box.height() / 2

            # Calculate the position relative to the video using the center point
            scale_factor = ( self.video_item.nativeSize().toSize().width() / self.graphic_scene.sceneRect().width() )
            relative_pos = ( QPointF(text_center_x, text_center_y) - self.video_item.boundingRect().topLeft() ) * scale_factor


            with open(text_html_location, "w") as file:
                file.write(text_preview.toHtml())
            print("Append: ", stroke_size)
            text_html.append([text_html_location, relative_pos.x(), relative_pos.y(), stroke_size, stroke_color, start_time, end_time, scale_factor])
            print(text_preview.pos(), self.graphic_scene.sceneRect().size())
            file.close()
        
        return text_html
    
    def milliseconds_to_time(self, milliseconds):
        seconds = milliseconds // 1000
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return "{:02d}:{:02d}:{:02d}.{:02d}".format(hours, minutes, seconds, milliseconds % 1000 // 10)
    

    def setMedia(self, fileName):
        self.first_play= True
        self.mediaPlayer.setSource(QUrl.fromLocalFile(fileName))
        self.mediaPlayer.setAudioOutput(self.audioOutput)
        self.play_button.setEnabled(True)
        self.mediaPlayer.play()



    def play(self):
        if self.mediaPlayer.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def check_and_position_text_preview(self):
        self.resize_graphic_scene()
        if self.first_play:
            print("Self.first_play is true")
            self.position_text_preview()
        
        

    def position_text_preview(self):

        # Get the scene rect and calculate its center 
        scene_rect = self.graphic_scene.sceneRect()
        scene_center = scene_rect.center()

        for subtitle_index, (text_preview, subtitle_duration, subtitle_text, start_total_milliseconds, end_total_milliseconds) in self.text_data.items():
            # Ensure the text preview's bounding rect is up-to-date
            text_rect = text_preview.boundingRect()

            # Debug information
            print(f"Scene Center: {scene_center}")
            print(f"Text Bounding Rect: {text_rect}")
            print(f"Text Width: {text_rect.width()}, Text Height: {text_rect.height()}")

            # Calculate the center position for the text
            x = scene_center.x() - (text_rect.width() / 2)
            y = scene_center.y() - (text_rect.height() / 2)

            # Debug information
            print(f"Calculated Position: x={x}, y={y}")

            # Set the position of the text preview
            text_preview.setPos(x, y)
            print(f"Text Preview Position: {text_preview.pos()}")


    def mediaStateChanged(self, state):

        if state == QMediaPlayer.PlaybackState.PlayingState:
            self.play_button.set_icon("gui/images/svg_icons/icon_pause.svg")
        else:
            self.play_button.set_icon("gui/images/svg_icons/icon_play.svg")

    def positionChanged(self, position):
        # Update position slider
        self.position_slider.setValue(position)
        if self.first_play:
            self.first_play = False

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
            if self.video_item.boundingRect().isValid() and not self.video_item.boundingRect().isEmpty():
                self.graphic_scene.setSceneRect(self.video_item.boundingRect())
                self.graphics_view.fitInView(self.graphic_scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
                self.graphic_scene.resizeGuides()
                print("Video Size: ", self.video_item.nativeSize(), self.video_item.boundingRect().size())
            else:
                print("Video item bounding rect is not valid or empty")
        except Exception as e:
            print("Video Unavailable: ", e)

    def resizeEvent(self, event):
        self.resize_graphic_scene()

