from ..render import RenderStep

from .utils import convert_position_to_point

class HyperlaneStep(RenderStep):
	def __init__(self):
		super().__init__("hyperlanes")

	def run(self, ctx, config):
		exclude = set()
		for system in ctx.model.systems.values():
			for hyperlane in system.hyperlanes:
				if hyperlane.dest not in exclude:
					a = convert_position_to_point(ctx, system.pos)
					b = convert_position_to_point(ctx, ctx.model.systems[hyperlane.dest].pos)
					ctx.draw.line(
						(a[0],a[1],b[0],b[1]), 
						fill=tuple(config["fill"]),
					 	width=config["width"]
					)
			exclude.add(system.id)
			