import math

from ..render import RenderStep
from ..color import get_color
from ..utils import convert_position_to_point

class PopsStep(RenderStep):
	def __init__(self):
		super().__init__("pops")

	def run(self, ctx, config):
		scale = ctx.config["image"]["scale"] * config["scale"]
		for system in ctx.model.systems.values():
			pops = sum([len(planet.pops) for planet in system.planets])
			if pops != 0:
				p = convert_position_to_point(ctx, system.pos)
				r = max(int(scale * math.sqrt(pops / math.pi)), 1)
				ctx.draw.ellipse(
					(p[0]-r,p[1]-r,p[0]+r, p[1]+r), 
					fill=get_color(ctx, config["fill"], { "system": system }),
					outline=get_color(ctx, config["outline"])
				)
				