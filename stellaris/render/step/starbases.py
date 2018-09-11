from ..render import RenderStep
from ..color import get_color
from ..utils import convert_position_to_point


class StarbasesStep(RenderStep):
	def __init__(self):
		super().__init__("starbases")
	
	def run(self, ctx, config):
		scale = ctx.config["image"]["scale"] 
		for system in ctx.model.systems.values():
			r = int(scale * self._get_starbase_size(config, system.starbase))
			if r != 0:
				p = convert_position_to_point(ctx, system.pos)
				ctx.draw.ellipse(
					(p[0]-r,p[1]-r,p[0]+r,p[1]+r),
					fill=get_color(ctx, config["fill"], { "system": system }),
					outline=get_color(ctx, config["outline"], { "system": system })
				)

	def _get_starbase_size(self, config, starbase):
		if starbase == None:
			return 0
		elif starbase.level in config["sizes"]:
			return config["sizes"][starbase.level]
		else:
			return 0


