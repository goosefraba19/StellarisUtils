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
					#color = tuple([min(x+60,255) for x in color])
					color = tuple([int(0.25*a + 0.75*b) for a,b in zip((256,256,256), color)])
				else:
					color = (255,255,255)

				p = convert_position_to_point(ctx, system.pos)
				r = int(1.5 * math.sqrt(pops / math.pi) + 0.5)
				ctx.draw.ellipse(
					(p[0]-r,p[1]-r,p[0]+r, p[1]+r), 
					fill=color,
					outline=tuple(config["outline"])
				)
				