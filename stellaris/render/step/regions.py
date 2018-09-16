from ..render import RenderStep
from ..color import get_color
from ..utils import convert_position_to_point



class RegionsStep(RenderStep):

	def __init__(self):
		super().__init__("regions")

	def run(self, ctx, config):
		(vor, system_indices) = ctx.data[config["input"]]
		
		# render system regions
		for (id, index) in system_indices:
			system = ctx.model.systems[id]
			region = vor.regions[vor.point_region[index]]
			if -1 not in region:
				color = get_color(ctx, config["fill"], { "system": system })
				if color:
					points = [tuple(map(int, vor.vertices[index])) for index in region]
					ctx.draw.polygon(points, fill=color)
