import math

from ..render import RenderStep
from .utils import convert_position_to_point, get_system_color

class PopsStep(RenderStep):
	def __init__(self):
		super().__init__("pops")

	def run(self, ctx, config):
		for system in ctx.model.systems.values():
			pops = sum([len(planet.pops) for planet in system.planets])
			if pops != 0:
				
				color = get_system_color(ctx, system)				
				if color:
					color = tuple([int(0.8*a + 0.2*b) for a,b in zip(color, (0,0,0))])
				else:
					color = (255,255,255)

				p = convert_position_to_point(ctx, system.pos)
				r = max(int(config["scale"] * math.sqrt(pops / math.pi)), 1)
				ctx.draw.ellipse(
					(p[0]-r,p[1]-r,p[0]+r, p[1]+r), 
					fill=color,
					outline=tuple(config["outline"])
				)
				