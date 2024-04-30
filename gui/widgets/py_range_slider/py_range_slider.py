# IMPORT DATA CLASSES
# ///////////////////////////////////////////////////////////////
from dataclasses import dataclass

# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from qt_core import *

# IMPORT MATHS
# ///////////////////////////////////////////////////////////////
import math


# HANDLE CLASS
# ///////////////////////////////////////////////////////////////
@dataclass
class handle:
	"""handle class which holds information about a handle.
	"""
	value: int
	rect: QRect = None
	pressed: bool = False

# PY RANGE SLIDER
# ///////////////////////////////////////////////////////////////
class PyRangeSlider(QWidget):
	"""
		Methods

			* add_handles: Adds a left and right handle with track
			* remove_handles: Removes last added left and right handle
			* set_value: Sets value for the main handler
			* set_range: Sets the maxium number for the track
			* grab_value: Grabs durations from left and right handles
			* reset_range_widget: Resets every list and delets every tooltip



		Signals

			* slider_moved (int)

	"""

	slider_moved = Signal(int)

	def __init__(
		self,
		parent =None,
		height = 100,
		width = 100,
		left_value=0, 
		right_value=60,
		move_every = 1000, # How much you want the handles to move by on, QT Video player 1000 == 1 Second

		# ALL MAIN HANDLE SECTION
		main_handle_height = 70,
		main_handle_width = 5,
		set_value = 0,
		main_handle_color = QColor("#D9D9D9"),

		# ALL HANDLE SECTION
		left_handle_value=0, 
		right_handle_value=15,
		handle_height = 70,
		handle_width = 5,
		left_handle_color = QColor("#4D96E0"),
		right_handle_color = QColor("#3F6FD1"),
		handle_border_color=QColor("#D9D9D9"),

		# TRACK SECTION
		min_track_range = 10, # Track between left and right handles
	    track_height = 53,
	    track_color = QColor("#4D96E0"),
		track_opacity = 0,
	    track_fill_color = QColor("#4D96E0"),
		track_fill_opacity = 36,

		# ALL TICKS SECTION
	    tick_padding = 1,
		ticks_number = 0,


		text_foreground = "#8a95aa"

	):
		super().__init__()

        # SET DEFAULT PARAMETERS
		self.setSizePolicy(
			QSizePolicy.Expanding,
			QSizePolicy.Fixed
		)
		self.setMinimumWidth(height)
		self.setMinimumHeight(width)

		track_color.setAlpha(track_opacity) 
		track_fill_color.setAlpha(track_fill_opacity)
		
        # PROPERTIES
		self._parent = parent

		self._left_value = left_value
		self._right_value = right_value
		self._move_every = move_every

		self._main_handle = handle(set_value)
		self._main_handle_height = main_handle_height
		self._main_handle_width = main_handle_width
		self._main_handle_color = main_handle_color


		self._left_handle = [handle(left_handle_value)]
		self._right_handle_value = right_handle_value 
		self._right_handle = [handle(self._right_handle_value)]
		self._handle_width = handle_width
		self._handle_height = handle_height
		self._left_handle_color = left_handle_color
		self._right_handle_color = right_handle_color

		self._handle_border_color = handle_border_color
		self._min_track_range = min_track_range
		self._track_height = track_height
		self._track_color = track_color
		self._track_fill_color = track_fill_color

		self._ticks_count = ticks_number
		self._tick_padding = tick_padding
		self.track_padding = handle_width

		self._canvas_width = None
		self._canvas_height = None

		self._text_foreground = text_foreground

		self.handle_pairs = [(self._left_handle[0], self._right_handle[0])]
		self.handle_tooltips = []

		self.add_new_tooltips((self._left_handle[0],self._right_handle[0]))

		

				






    # PAINT EVENT
    # ///////////////////////////////////////////////////////////////
	def paintEvent(self, unused_e):
		del unused_e
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)

		self.__draw_track(self._canvas_width, self._canvas_height, painter) # Draws main track
		self.__draw_ticks(self._canvas_width, self._canvas_height, painter, self._ticks_count)
		self.__draw_track_fill(self._canvas_width, self._canvas_height, painter)

		for left_handle, right_handle in self.handle_pairs:
			self.draw_handle(left_handle, self._canvas_width, self._canvas_height, painter, self._left_handle_color)
			self.draw_handle(right_handle, self._canvas_width, self._canvas_height, painter, self._right_handle_color)
			self.update_tooltips_positions()
		
		
		self.draw_handle(self._main_handle, self._canvas_width, self._canvas_height, painter, self._main_handle_color)


		painter.end()

	def __get_track_y_position(self):
		return self._canvas_height // 2 - self._track_height // 2

	def __draw_track(self, canvas_width, canvas_height, painter):
		del canvas_height
		brush = QBrush()
		brush.setColor(self._track_color)
		brush.setStyle(Qt.SolidPattern)

		rect = QRect(self.track_padding, self.__get_track_y_position(), \
			canvas_width - 2 * self.track_padding, self._track_height)
		painter.fillRect(rect, brush)

	def __draw_track_fill(self, canvas_width, canvas_height, painter):
		del canvas_height
		brush = QBrush()
		brush.setColor(self._track_fill_color)
		brush.setStyle(Qt.SolidPattern)

		available_width = canvas_width - 2 * self.track_padding

		for left_handle, right_handle in  self.handle_pairs:
			
			x1 = left_handle.value / self._right_value * available_width + self.track_padding
			x2 = right_handle.value / self._right_value * available_width + self.track_padding
			rect = QRect(round(x1), self.__get_track_y_position(), \
			round(x2) - round(x1), self._track_height)
			painter.fillRect(rect, brush)


	def __set_painter_pen_color(self, painter, pen_color):
		pen = painter.pen()
		pen.setColor(pen_color)
		painter.setPen(pen)

	def __draw_handle(self, x, y, painter, color):
		brush = QBrush()
		brush.setColor(color)
		brush.setStyle(Qt.SolidPattern)

		self.__set_painter_pen_color(painter, color)

		painter.setBrush(brush)
		
		# Draws handles
		handle_rect = QRect(round(x) - self._handle_width // 2 + self.track_padding, \
			y + self._track_height // 2 - self._handle_height // 2, self._handle_width, self._handle_height)
		painter.drawRect(handle_rect)
        
		return handle_rect


	def draw_handle(self, handle, canvas_width, canvas_height, painter, color):
		del canvas_height

		# Caculates handle shape and where to draw
		available_width = canvas_width - 2 * self.track_padding
		x = round(handle.value / self._right_value * available_width)
		y = self.__get_track_y_position()
		handle.rect = self.__draw_handle(x, y, painter, color)

    # Works with Handles postion
    # ///////////////////////////////////////////////////////////////

	def set_handle_value(self, value, handle):

		if handle != self._main_handle:
			# Grabs oposite handle, previous right handle and next left handle
			oposite_handle, prev_right_handle, front_left_handle = self.find_other_handle(handle)

			# Caculates exactly when to stop the slider to not bump
			right_handle_stop_position = ((self._canvas_width + oposite_handle.value) - self._canvas_width) + ((self._handle_width * 2) / 100)
			left_handle_stop_position = ((self._canvas_width + oposite_handle.value) - self._canvas_width) - ((self._handle_width * 2) / 100)


			if prev_right_handle is not None:
				max_left_handle_position = prev_right_handle.value + (self._move_every / self._move_every)
			
			if front_left_handle is not None:
				max_right_handle_position = front_left_handle.value - (self._move_every / self._move_every)
				

			if handle in self._left_handle:
				if value < 0 or value > left_handle_stop_position - self._min_track_range:
					return
				
				if prev_right_handle is not None:
					if value < max_left_handle_position:
						handle.value = max_left_handle_position
						self.repaint()
						return

			elif handle in self._right_handle:
				if value < right_handle_stop_position + self._min_track_range or value > self._right_value:
					return
				
				if front_left_handle is not None:
					if value > max_right_handle_position:
						handle.value = max_right_handle_position
						self.repaint()
						return
			
			


		else:
			if value < 0 or value > self._right_value:
				return
		

		handle.value = value
		self.repaint()

		# Updates tooltip text and position
		for handles, tooltip in self.handle_tooltips:
				if handles == handle:
					self.move_tooltip(handle, tooltip)
					tooltip.update_text(handle.value)
					
	
	def find_other_handle(self, handle):
		prev_right_handle = None
		front_left_handle = None

		# Finds if there is a handle infront or behind
		for index, handle_tuple in enumerate(self.handle_pairs):
			if handle in handle_tuple:

				if 0 <= index - 1:
					for items in self.handle_pairs[index - 1]:
						if items in self._right_handle:
							prev_right_handle = items
							break

				if len(self.handle_pairs) > index + 1:
					for items in self.handle_pairs[index + 1]:
						if items in self._left_handle:
							front_left_handle = items
							break

					break
				else:
					break


		return handle_tuple[1 - handle_tuple.index(handle)], prev_right_handle, front_left_handle
		
	


    # EVENT HANDLERS
    # ///////////////////////////////////////////////////////////////

	# Changes handlers positions
	def mouseMoveEvent(self, event):
		for handle_list in self.handle_pairs:
			for handle in handle_list:
				if handle.pressed:
					new_val = self.__get_handle_value(event.x(), self._canvas_width, self._right_value) 
					

					if new_val is not None and new_val != handle.value:
						
						self.set_handle_value(new_val, handle)


		if self._main_handle.pressed:
			new_val = self.__get_handle_value(event.x(), self._canvas_width, self._right_value) 

			if new_val is not None and new_val != handle.value:
				self.slider_moved.emit(new_val * self._move_every)
				self.set_handle_value(new_val, self._main_handle)

		super().mouseMoveEvent(event)

	# Checks if handler been released
	def mouseReleaseEvent(self, event):
		for handle_list in self.handle_pairs:
					for handle in handle_list:
						handle.pressed = False
		
		self._main_handle.pressed = False
		super().mouseReleaseEvent(event)
	
	# Checls if handles been clicked
	def mousePressEvent(self, event):
		for handle_list in self.handle_pairs:
			for handle in handle_list:
				if handle.rect.contains(event.x(), event.y()):
					handle.pressed = True



        # Check if the main handle is clicked to deselect any other selected
		if self._main_handle.rect.contains(event.x(), event.y()):
			self._main_handle.pressed = True
		
		if self._main_handle.pressed:
			for handle_list in self.handle_pairs:
				for handle in handle_list:
					handle.pressed = False
		super().mousePressEvent(event)
	


			
	def __get_handle_value(self, x, canvas_width, right_value):
		return math.floor(x / canvas_width * right_value)


    # TICKS SECTION
    # ///////////////////////////////////////////////////////////////

	def set_ticks_count(self, count):
		if count < 0:
			raise ValueError("Invalid ticks count.")
		self._ticks_count = count

	def __draw_ticks(self, canvas_width, canvas_height, painter, ticks_count):
		del canvas_height
		if not self._ticks_count:
			return

		self.__set_painter_pen_color(painter, self._handle_border_color)

		tick_step = (canvas_width - 2 * self.track_padding) // ticks_count
		y1 = self.__get_track_y_position() - self._tick_padding
		y2 = y1 - self._handle_height // 2
		for x in range(0, ticks_count + 1):
			x = x * tick_step + self.track_padding
			painter.drawLine(x, y1, x, y2)

	def resizeEvent(self, event):
		del event
		self._canvas_width = self.width()
		self._canvas_height = self.height()
		self.update_tooltips_positions()

		





	# CALLABLE METHODS
	# ///////////////////////////////////////////////////////////////
	def add_handles(self):
		left_value = self._right_handle[-1].value + ((self._move_every / self._move_every) * 5) # Adds a 5 second space in between new handles
		right_value = left_value + self._min_track_range + (self._handle_width * 2)
		space_left = self._right_value - right_value

		if space_left > self._min_track_range:
			left_handle = handle(left_value)
			right_handle = handle(right_value)

			self._left_handle.append(left_handle)
			self._right_handle.append(right_handle)

			self.handle_pairs.append([left_handle, right_handle])
			self.add_new_tooltips((left_handle, right_handle))

			self.update()
		else:
			print("Not enough space")

	
	# removes latest handle
	def remove_handles(self):
		if len(self.handle_pairs) > 1:
			self._left_handle.pop()
			self._right_handle.pop()
			self.handle_pairs.pop()

			# Grabs and deletes the last 2 handle and its tooltip
			handle1, tooltip1 = self.handle_tooltips.pop()
			handle2, tooltip2 = self.handle_tooltips.pop()
		
			tooltip1.deleteLater()
			tooltip2.deleteLater()
			
			self.update()
		else:
			print("Not enough to remove")

	# updates main handler value
	def set_value(self, value):
		if self._main_handle.pressed == False:
			value= value // self._move_every % self._right_value # Makes it move only on the second
			self.set_handle_value(value, self._main_handle)

	
	# updates max duration
	def set_range(self, duration):
		duration /= self._move_every
		self._right_value = duration
		self.update()
	
	# grabs all handle start and end times
	def grab_handles_values(self):
		handle_values = []
		for left_handle, right_handle in  self.handle_pairs:
			start, end = left_handle.value, right_handle.value
			handle_values.append(["{:02d}:{:02d}".format(*divmod(int(float(start)), 60)), "{:02d}:{:02d}".format(*divmod(int(float(end)), 60))])
		return handle_values
	
	# Resets everything to allow for a new range slider
	def reset_range_widget(self):
		for pairs in self.handle_pairs:
			self._left_handle.pop()
			self._right_handle.pop()
			self.handle_pairs.pop()

			# Grabs and deletes the last 2 handle and its tooltip
			handle1, tooltip1 = self.handle_tooltips.pop()
			handle2, tooltip2 = self.handle_tooltips.pop()
			
			tooltip1.deleteLater()
			tooltip2.deleteLater()
				
			self.update()
	
	

	# TOOLTIP SECTION
    # ///////////////////////////////////////////////////////////////
	def move_tooltip(self, handle, tooltip):
		handle_rect = handle.rect
		handle_pos = handle_rect.topLeft()

		if handle in self._left_handle:
			offsetx = 15
			offsety = 15
		else:
			offsetx = -15
			offsety = -70

		pos_x = handle_pos.x() + offsetx
		pos_y = handle_pos.y() - offsety

        # SET POSITION TO WIDGET
        # Move tooltip position
		tooltip.move(pos_x, pos_y)
		return

	# adds a new tooltip
	def add_new_tooltips(self, handles):
		for handle in handles:
			handle_tooltip = _ToolTip(self._parent, str(handle.value), self._text_foreground)
			self.handle_tooltips.append([handle, handle_tooltip])
			handle_tooltip.show()
	
	# updates all the tooltips positions
	def update_tooltips_positions(self):
		for handle, tooltip in self.handle_tooltips:
			if handle.rect:
				self.move_tooltip(handle, tooltip)
		
	
# TOOLTIP
# ///////////////////////////////////////////////////////////////
class _ToolTip(QLabel):
    # TOOLTIP / LABEL StyleSheet
    style_tooltip = """ 
    QLabel {{		
        background-color: transparent;	
        color: {_text_foreground};
        padding-left: 2px;
        padding-right: 2px;
        border-radius: 2px;
        border: 0px solid transparent;
        font: 800 7pt "Segoe UI";
    }}
    """
    def __init__(
        self,
        parent, 
        text,
        text_foreground
    ):
        super().__init__(parent)
		# LABEL SETUP
        style = self.style_tooltip.format(
            _text_foreground = text_foreground
        )
        self.setObjectName(u"label_tooltip")
        self.setStyleSheet(style)
        self.setMinimumHeight(34)
        self.setParent(parent)
        self.setText("{:02d}:{:02d}".format(*divmod(int(float(text)), 60)))
        self.adjustSize()
        self.setWordWrap(True)

        # SET DROP SHADOW
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(30)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 80))
        self.setGraphicsEffect(self.shadow)
	
    def update_text(self, text):
        self.setText("{:02d}:{:02d}".format(*divmod(int(float(text)), 60)))
        self.adjustSize()
        self.setWordWrap(True)
	
	






