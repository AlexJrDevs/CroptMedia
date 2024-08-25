
from qt_core import *

from gui.widgets import PyIconButton, PySlider, PyRangeSlider, PyGraphicsScene, PyGraphicsView

import cv2

dark_style = """
            background-color: #2C313C; border-radius: 8px;
        """

bright_style = """
            background-color: #343B48; border-radius: 8px;
        """

class PyThumbnailCapture(QThread):
    thumbnail_completed = Signal(list)

    def __init__(self, file_location):
        super().__init__()
        self.file_location = file_location
        print("File location: ", file_location)

    def run(self):

        # Takes Screenshots from video to get images from it
        video_capture = cv2.VideoCapture(self.file_location)
        total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
        visible_frames = 15 # Generate 15 frames
        interval = total_frames // visible_frames

        thumbnails = []

        for i in range(visible_frames):
            video_capture.set(cv2.CAP_PROP_POS_FRAMES, i * interval)
            ret, frame = video_capture.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert frame to RGB
                height, width, _ = frame.shape
                img = QPixmap.fromImage(
                    QImage(frame.data, width, height, width * 3, QImage.Format_RGB888)
                )
                thumbnails.append(img)

        video_capture.release()
        self.thumbnail_completed.emit(thumbnails)



class PySubclipPlayer(QWidget):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

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
        
        self.thumbnail_label = []

        self.thumbnail_widget = QWidget()
        self.thumbnail_layout = QHBoxLayout()
        self.thumbnail_layout.setSpacing(0)
        self.thumbnail_widget.setLayout(self.thumbnail_layout)
        self.thumbnail_widget.setStyleSheet(dark_style)

        self.sliders_widget = QWidget()
        self.sliders_layout = QVBoxLayout()
        self.sliders_widget.setLayout(self.sliders_layout)
        

        self.range_slider = PyRangeSlider(parent=self.sliders_widget)
        
        video_button_widget = QWidget()
        video_button_layout = QHBoxLayout()

        bg_btn_widget = QWidget()
        bg_btn_widget.setStyleSheet(dark_style)
        bg_btn_layout = QVBoxLayout()
        bg_btn_layout.setSpacing(0)
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

        self.segments_button_widget = QWidget()
        segments_button_layout = QHBoxLayout()
        segments_button_layout.setSpacing(0)
        segments_button_layout.setContentsMargins(0, 0, 0, 0)
  
        self.segments_button_widget.setLayout(segments_button_layout)
        self.segments_button_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.segments_button_widget.setStyleSheet(dark_style)

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
                                   width=45, 
                                   height=45,
                                   icon_margin=15,
                                   bg_color_hover = "#343B48",
                                   bg_color="#343B48"
                                )

        # Set up the layout
        self.sliders_layout.addWidget(self.range_slider)
        

        
        video_button_layout.addWidget(self.play_button)
        video_button_layout.addWidget(self.volume_button)
        video_button_layout.addWidget(self.volume_slider)
        video_button_layout.addWidget(self.time_label)

        

        segments_button_layout.addWidget(self.add_button)
        segments_button_layout.addWidget(self.remove_button)
        segments_button_layout.addWidget(self.done_button)

        control_layout = QHBoxLayout()
        bg_btn_layout.addWidget(video_button_widget)

        control_layout.addWidget(bg_btn_widget)
        control_layout.addStretch(1)
        control_layout.addWidget(self.segments_button_widget, stretch=2)
        control_layout.addStretch(2)
        control_layout.setSpacing(0)
        control_layout.setContentsMargins(0, 0, 0, 0)


        
        # Create a stacked layout to overlap thumbnail_layout widget with position slider
        stack_layout = QStackedLayout()
        stack_layout.addWidget(self.thumbnail_widget)
        stack_layout.addWidget(self.sliders_widget)
        stack_layout.setStackingMode(QStackedLayout.StackAll)
        stack_layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        stack_layout.setStackingMode(QStackedLayout.StackAll)

        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.addWidget(self.graphics_view, stretch=1)
        layout.addLayout(stack_layout)
        layout.addLayout(control_layout)


        self.setLayout(layout)

        # Slots Section
        self.mediaPlayer.setVideoOutput(self.video_item)
        self.mediaPlayer.playbackStateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.errorOccurred.connect(self.handleError)

        # Resizes the video
        self.mediaPlayer.videoOutputChanged.connect(self.resize_graphic_scene)
        self.mediaPlayer.mediaStatusChanged.connect(self.resize_graphic_scene)


        self.range_slider.slider_moved.connect(self.setPosition)

        self.add_button.clicked.connect(self.add_segg)
        self.remove_button.clicked.connect(self.remove_segg)
        self.done_button.clicked.connect(self.create_video)

        self.thumbnail_widget.resizeEvent = lambda event: self.show_hide_thumbnail()
    
    def add_segg(self):
        self.range_slider.add_handles()
    
    def remove_segg(self):
        self.range_slider.remove_handles()
    
    def create_video(self):
        self.mediaPlayer.stop()
        self.mediaPlayer.setSource(QUrl())
        if self.range_slider.isVisible():
            subclip_durations = self.range_slider.grab_handles_values()
            self.parent.save_subclips(subclip_durations)



    def setMedia(self, fileName, images = None):
        self.add_thumbnails(images)

        self.mediaPlayer.setSource(QUrl.fromLocalFile(fileName))
        self.mediaPlayer.setAudioOutput(self.audioOutput)
        self.play_button.setEnabled(True)
        self.play()

    

    # Creates thumbnail_layout labels to display later
    def add_thumbnails(self, thumbnails):
        # Clear the current thumbnails from the layout
        while self.thumbnail_layout.count() > 0:
            item = self.thumbnail_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.thumbnail_label.clear()

        for i, thumbnail_layout in enumerate(thumbnails):
            label = QLabel()
            label.setAlignment(Qt.AlignCenter)
            label.setPixmap(thumbnail_layout)
            label.setScaledContents(True)  # Ensure pixmap scales with label size
            label.setMinimumSize(0, 53)  # Set minimum width & height keeps 16:9
            label.setMaximumHeight(53)
            label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)  # Allow shrinking
            self.thumbnail_layout.addWidget(label)
            label.setVisible(False)
            label.setEnabled(False)
            self.thumbnail_label.append(label)
        
        # Update the layout and repaint the widget
        self.show_hide_thumbnail()  # Ensure the thumbnails are shown/hidden correctly

    
    def show_hide_thumbnail(self):

        widget_width = self.thumbnail_widget.width()
        thumbnail_width = 80
        num_thumbnails = max((widget_width // thumbnail_width), 0) # Caculates how many thumbnails can fit

        # Enables / Disables Images
        for i, label in enumerate(self.thumbnail_label):
            if i < num_thumbnails:
                label.setVisible(True)
                label.setEnabled(True)
            else:
                label.setVisible(False)
                label.setEnabled(False)


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
        self.range_slider.set_value(position)
        self.time_label.setText(
            f"{position // 60000:02}:{(position // 1000) % 60:02} / {self.mediaPlayer.duration() // 60000:02}:{(self.mediaPlayer.duration() // 1000) % 60:02}"
        )

    def durationChanged(self, duration):
        if duration > 0:
            self.range_slider.set_range(duration)

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
                print("Update Video size")
                self.graphic_scene.setSceneRect(self.video_item.boundingRect())
                self.graphics_view.fitInView(self.graphic_scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
            else:
                print("Video item bounding rect is not valid or empty")
        except Exception as e:
            print("Video Unavailable: ", e)
        


    def resizeEvent(self, event):
        self.resize_graphic_scene()