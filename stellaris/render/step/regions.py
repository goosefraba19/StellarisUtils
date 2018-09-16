from ..render import RenderStep
from ..color import get_color
from ..utils import convert_position_to_point

class RegionsStep(RenderStep):

	def __init__(self):
		super().__init__("regions")

	def run(self, ctx, config):
		vor = ctx.data[config["input"]]
		for region in vor.regions:
			color = get_color(ctx, config["fill"], { "system": region.system })
			if color:
				points = [convert_position_to_point(ctx, v) for v in region.vertices]
				ctx.draw.polygon(points, fill=color)
