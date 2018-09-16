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
		import stellaris.render.step
		self._step_handlers = {}
		for c in RenderStep.__subclasses__():
			i = c()
			self._step_handlers[i.name] = i

	def steps(self):
		ctx = RenderContext(self._config, self._model, self._draw)

		for step in self._config["steps"]:
			key = step["key"]
			if key in self._step_handlers:
				self._step_handlers[key].run(ctx, step)
			else:
				print(f"Error: unrecognized step '{key}'.")
	
	def export(self, path, format=None):
		self._image.save(path, format)

class RenderStep:
	def __init__(self, name):
		self.name = name
	def run(self, config):
		pass
	
class RenderContext:
	def __init__(self, config, model, draw):
		self.config = config
		self.model = model
		self.draw = draw
		self.data = {}
