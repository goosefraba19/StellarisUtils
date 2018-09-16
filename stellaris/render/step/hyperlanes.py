from ..render import RenderStep
from ..color import get_color
from ..utils import convert_position_to_point

class HyperlaneStep(RenderStep):
	def __init__(self):
		super().__init__("hyperlanes")

	def run(self, ctx, config):

		hyperlanes = set([h for s in ctx.model.systems.values() for h in s.hyperlanes])
		for hyperlane in hyperlanes:
			src = convert_position_to_point(ctx, hyperlane.src.pos)
			dest = convert_position_to_point(ctx, hyperlane.dest.pos)
			ctx.draw.line(
				(src[0],src[1],dest[0],dest[1]), 
				fill=get_color(ctx, config["fill"]),
				width=config["width"]
			)
