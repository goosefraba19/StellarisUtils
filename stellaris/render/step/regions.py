import math, numpy, random
from scipy.spatial import Voronoi

from ..render import RenderStep
from ..color import get_color
from ..utils import convert_position_to_point



class RegionsStep(RenderStep):

	def __init__(self):
		super().__init__("regions")

	def run(self, ctx, config):
		(vor, system_indices) = self._build_voronoi(ctx, config)

		edge_systems = {}
		
		# render system regions and collect border data
		for (id, index) in system_indices:
			system = ctx.model.systems[id]
			region = vor.regions[vor.point_region[index]]
			color = get_color(ctx, config["fill"], { "system": system })
			if color:
				self._render_region(ctx, vor, region, color)

			edges = [tuple(sorted([region[i], region[i+1]])) for i in range(-1, len(region)-1)]
			for edge in edges:
				if edge not in edge_systems:
					edge_systems [edge] = set()
				edge_systems[edge].add(system)

		# render borders
		for (edge, systems) in edge_systems.items():

			owners = set()
			for system in systems:
				if system.starbase:
					owners.add(system.starbase.owner)
				else:
					owners.add(None)

			if 1 < len(owners):
				vertices = [vor.vertices[index] for index in edge]
				points = [tuple(map(int, v)) for v in vertices]

				width = config["border"]["width"]
				fill = get_color(ctx, config["border"]["fill"])

				ctx.draw.line(points, fill=fill, width=width)
				self._draw_circle(ctx.draw, points[0], fill, width/2)
				self._draw_circle(ctx.draw, points[1], fill, width/2)
				
	def _draw_circle(self, draw, center, fill, radius):
		points = (
			center[0] - radius + 1,
			center[1] - radius + 1,
			center[0] + radius - 1,
			center[1] + radius - 1
		)
		draw.ellipse(points, fill=fill)

	def _build_voronoi(self, ctx, config):
		# the voronoi diagram is built from a list of points
		points = []
		system_indices = []
		
		# add points for every system
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

		# add points for every hyperlane
		h = config["hyperlane_point_count"] + 1
		for (src, dest) in hyperlanes:
			for weight in [x/h for x in range(1,h)]:
				point = convert_position_to_point(ctx, (
					weight * src.pos[0] + (1 - weight) * dest.pos[0],
					weight * src.pos[1] + (1 - weight) * dest.pos[1]
				))

				points.append(list(point))
				# tied to the nearest system
				system = src if 0.5 < weight else dest
				system_indices.append((system.id, index))
				index += 1

		# add points for rings
		config_rings = config["voronoi_rings"]
		for ring in self._get_rings(ctx, config_rings):
			angle = 0
			while angle < 360:
				point = convert_position_to_point(ctx, (
					ring["x"] + ring["r"] * math.cos(math.radians(angle)),
					ring["y"] + ring["r"] * math.sin(math.radians(angle))
				))

				if config_rings["debug"]:
					ctx.draw.point(point, fill=get_color(ctx, config_rings["debug_color"]))
				
				points.append(list(point))

				angle += ring["s"]
		
		# build diagram from points
		vor = Voronoi(numpy.array(points))

		return (vor, system_indices)

	def _render_region(self, ctx, vor, region, fill=None, outline=None):
		if -1 in region:
			return
		points = [tuple(map(int, vor.vertices[index])) for index in region]
		ctx.draw.polygon(points, fill=fill, outline=outline)

	def _get_rings(self, ctx, config):
		if config["autogen"]:
			results = []
			for group in self._get_connected_systems(ctx):
				results += self._create_rings_for_group(ctx, config, group)
			return results
		else:
			return config["list"]

	def _get_connected_systems(self, ctx):
		# https://www.geeksforgeeks.org/connected-components-in-an-undirected-graph/
		systems = ctx.model.systems
		visited = dict([(s.id, False) for s in systems.values()])

		def dfs_util(id):
			result = [id]
			visited[id] = True
			system = systems[id]
			for hyperlane in system.hyperlanes:
				if not visited[hyperlane.dest]:
					result += dfs_util(hyperlane.dest)
			return result

		result = []

		for id in systems.keys():
			if not visited[id]:
				result.append(dfs_util(id))

		return result

	def _create_rings_for_group(self, ctx, config, group):
		if len(group) < 2:
			return []

		systems = [ctx.model.systems[id] for id in group]

		# center point
		c = (
			sum([s.pos[0] for s in systems])/len(systems),
			sum([s.pos[1] for s in systems])/len(systems)
		)

		# minimum and maximum radius from the center point
		r_min = 10000
		r_max = 0

		for s in systems:
			r = math.sqrt(math.pow(c[0]-s.pos[0], 2) + math.pow(c[1]-s.pos[1], 2))
			r_min = min(r_min, r)
			r_max = max(r_max, r)

		# create rings
		padding = config["autogen_padding"]
		results = [self._create_ring(config, c, r_max + padding)]
		if padding < r_min:
			results.append(self._create_ring(config, c, r_min - padding))
		return results

	def _create_ring(self, config, c, r):
		n = (2*math.pi*r) / config["autogen_spacing"]
		s = 360/n
		return { 
			"x": c[0],
			"y": c[1],
			"r": r,
			"s": s
		}
