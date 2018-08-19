import math, numpy, random
from scipy.spatial import Voronoi

from ..render import RenderStep
from .utils import get_system_color

class RegionsStep(RenderStep):
	def __init__(self):
		super().__init__("regions")

	def run(self, ctx, config):
		points = []
		voronoi_index = {}
		
		index = 0
		for system in ctx.model.systems.values():
			point = ctx.convert_position_to_point(system.pos)
			voronoi_index[system.id] = index
			points.append(list(point))			
			index += 1
			
		for ring in config["voronoi_rings"]:
			for angle in range(0, 365, ring["s"]):
				point = ctx.convert_position_to_point((
					ring["x"] + ring["r"] * math.cos(math.radians(angle)),
					ring["y"] + ring["r"] * math.sin(math.radians(angle))
				))
				
				if config["debug"]:
					ctx.draw.point(point, fill=tuple(config["debug_color"]))
				
				points.append(list(point))				
		
		vor = Voronoi(numpy.array(points))
		
		for system in ctx.model.systems.values():
			region = vor.regions[vor.point_region[voronoi_index[system.id]]]			
			color = get_system_color(ctx, system)
			if color:
				self._render_region(ctx, vor, region, color)

	def _render_region(self, ctx, vor, region, fill=None, outline=None):
		if -1 in region:
			return

		points = []
		for index in region:
			vertex = vor.vertices[index]
			points.append((int(vertex[0]), int(vertex[1])))		

		if points:
			ctx.draw.polygon(points, fill=fill, outline=outline)