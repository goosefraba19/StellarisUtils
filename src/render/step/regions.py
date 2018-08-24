import math, numpy, random
from scipy.spatial import Voronoi

from ..render import RenderStep
from ..color import get_color
from ..utils import convert_position_to_point

class RegionsStep(RenderStep):
	def __init__(self):
		super().__init__("regions")

	def run(self, ctx, config):
		points = []
		system_indices = []
		
		index = 0
		for system in ctx.model.systems.values():
			point = convert_position_to_point(ctx, system.pos)
			points.append(list(point))			
			system_indices.append((system.id, index))
			index += 1

		hyperlanes = []
		exclude = set()
		for src in ctx.model.systems.values():
			for hyperlane in src.hyperlanes:
				if hyperlane.dest not in exclude:
					dest = ctx.model.systems[hyperlane.dest]
					hyperlanes.append((src, dest))
			exclude.add(system.id)

		h = config["hyperlane_point_count"] + 1
		for (src, dest) in hyperlanes:
			for weight in [x/h for x in range(1,h)]:
				point = convert_position_to_point(ctx, (
					weight * src.pos[0] + (1 - weight) * dest.pos[0],
					weight * src.pos[1] + (1 - weight) * dest.pos[1]
				))

				points.append(list(point))
				system = src if 0.5 < weight else dest
				system_indices.append((system.id, index))
				index += 1

		for ring in config["voronoi_rings"]:
			for angle in range(0, 365, ring["s"]):
				point = convert_position_to_point(ctx, (
					ring["x"] + ring["r"] * math.cos(math.radians(angle)),
					ring["y"] + ring["r"] * math.sin(math.radians(angle))
				))
				
				if config["debug"]:
					ctx.draw.point(point, fill=get_color(ctx, config["debug_color"]))
				
				points.append(list(point))				
		
		vor = Voronoi(numpy.array(points))
		
		for (id, index) in system_indices:
			system = ctx.model.systems[id]
			color = get_color(ctx, config["fill"], { "system": system })
			if color:
				region = vor.regions[vor.point_region[index]]			
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
