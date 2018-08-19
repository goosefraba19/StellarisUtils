from PIL import Image, ImageDraw, ImageFont
from ..model import Model

class Render:
	def __init__(self, model, config):
		self._model = model
		self._config = config
		self._image = Image.new("RGB", tuple(config["image"]["size"]), color=tuple(config["image"]["color"]))
		self._draw = ImageDraw.Draw(self._image, "RGBA")
		self._load_step_handlers()

	def _load_step_handlers(self):
		import src.render.step
		self._step_handlers = {}
		for c in RenderStep.__subclasses__():
			i = c()
			self._step_handlers[i.name] = i

	def steps(self):
		ctx = RenderContext(
			self._config,
			self._model,
			self._draw,
			self._convert_position_to_point
		)

		for step in self._config["steps"]:
			key = step["key"]
			if key in self._step_handlers:
				self._step_handlers[key].run(ctx, step)
			else:
				print(f"Error: unrecognized step '{key}'.")
	
	def _convert_position_to_point(self, p):
		scale = self._config["image"]["scale"]
		size = self._config["image"]["size"]
		center = self._config["image"]["center"]
	
		return (
			-1 * scale * p[0] + (size[0] - center[0]),
			scale * p[1] + center[1]
		)
	
	def export(self, path):
		self._image.save(path)

class RenderStep:
	def __init__(self, name):
		self.name = name
	def run(self, config):
		pass
	
class RenderContext:
	def __init__(self, config, model, draw, convert_func):
		self.config = config
		self.model = model
		self.draw = draw
		self.convert_position_to_point = convert_func