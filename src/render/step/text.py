from ..render import RenderStep
from ..color import get_color

class TextStep(RenderStep):
	def __init__(self):
		super().__init__("text")

	def run(self, ctx, config):
		text = config["text"] \
			.replace("{date}", ctx.model.date)

		ctx.draw.text(
			tuple(config["pos"]),
			text, 
			fill=get_color(ctx, config["fill"])
		)
