from ..render import RenderStep

class TextStep(RenderStep):
	def __init__(self):
		super().__init__("text")

	def run(self, ctx, config):
		text = config["text"] \
			.replace("{date}", ctx.model.date)

		ctx.draw.text(
			tuple(config["pos"]),
			text, 
			fill=tuple(config["fill"])
		)