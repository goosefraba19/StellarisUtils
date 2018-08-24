from ..render import RenderStep
from ..color import get_color
from ..utils import convert_position_to_point

class HyperlaneStep(RenderStep):
	def __init__(self):
		super().__init__("hyperlanes")

	def run(self, ctx, config):
		exclude = set()
		for src in ctx.model.systems.values():
			for hyperlane in src.hyperlanes:
				if hyperlane.dest in exclude:
					continue
				
				dest = ctx.model.systems[hyperlane.dest]
				a = convert_position_to_point(ctx, src.pos)
				b = convert_position_to_point(ctx, dest.pos)
				ctx.draw.line(
					(a[0],a[1],b[0],b[1]), 
					fill=get_color(ctx, config["fill"]),
					width=config["width"]
				)

			exclude.add(src.id)
			