import math, time

class Surface(object):
	def __init__(self, width=80, height=22):
		self._width = width
		self._height = height
		self._front = [[' ' for _ in range(self._width)] for _ in range(self._height)]
		self._back  = [[' ' for _ in range(self._width)] for _ in range(self._height)]

	def display(self):
		self._front, self._back = self._back, self._front
		print('+', '-' * self._width, '+', sep='')
		for line in self._front:
			print('|', ''.join(line), '|', sep='')
		print('+', '-' * self._width, '+', sep='')

	def clear(self, color=' '):
		for line in self._back:
			for i in range(len(line)):
				line[i] = color

	def __getitem__(self, line):
		assert 0 <= line < self._height
		return self._back[line]

	def __iter__(self):
		yield from self._back


class Point(object):
	__slots__ = ('x', 'y')

	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y

	def __sub__(self, other):
		result = Point(self.x, self.y)
		if isinstance(other, Point):
			result.x -= other.x
			result.y -= other.y
		elif isinstance(other, (int, float)):
			result.x -= other
			result.y -= other
		else:
			raise TypeError()
		return result


class Canvas(object):
	def __init__(self, surface):
		assert isinstance(surface, Surface)
		self._surface = surface

	def pixel(self, x, y, color='*'):
		x = int(x + 0.5)
		y = int(y + 0.5)
		if 0 <= x < self._surface._width and 0 <= y < self._surface._height:
			self._surface[y][x] = color

	def line(self, start, stop, color='*'):
		assert isinstance(start, Point)
		assert isinstance(stop, Point)
		if stop.x < start.x:
			start, stop = stop, start
		delta = stop - start
		for x in range(delta.x):
			x = start.x + x
			y = start.y + (x / delta.x) * (delta.y)
			self.pixel(x, y, color)

	def sine(self, offset_x=0, offset_y=None, amplitude=6, stretching=6, color='*'):
		if offset_y is None:
			offset_y = amplitude
		last_y = None
		for x in range(self._surface._width):
			y = math.sin((x + offset_x) / stretching) * amplitude
			y += offset_y
			y = int(y + 0.5)
			if not last_y or y == last_y:
				self.pixel(x, y, color)
			else:
				step = 1 if last_y < y else -1
				for smooth in range(last_y, y, step):
					self.pixel(x, smooth + step, color)
			last_y = y


if __name__ == '__main__':
	# Initialize canvas
	surface = Surface()
	canvas = Canvas(surface)
	scroll = 0
	while True:
		# Update parameters
		scroll += 1
		scale = math.sin(scroll / 10)
		# Render and display
		surface.clear()
		canvas.line(Point(2, 3), Point(70, 18), '.')
		canvas.sine(offset_x=1*scroll, offset_y=10, amplitude=6*scale, stretching=4)
		surface.display()
		time.sleep(0.2)
