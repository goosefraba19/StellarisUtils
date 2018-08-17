from .model import Model
from PIL import Image, ImageDraw, ImageFont
from scipy.spatial import Voronoi
import math, numpy, random

random.seed(2)
COUNTRY_OFFSETS = [(random.randint(-40,40), random.randint(-40,40), random.randint(-40,40)) for _ in range(500)]

class Render:
	def __init__(self, model, config):
		self._model = model
		self._config = config
				
				
		size = tuple(config["image.size"])
		self._image = Image.new("RGB", size, color=tuple(config["image.color"]))
		self._draw = ImageDraw.Draw(self._image, "RGBA")
		
	def _convert_position_to_point(self, p):
		scale = self._config["image.scale"]
		size = self._config["image.size"]
		center = self._config["image.center"]
	
		return (
			-1 * scale * p[0] + (size[0] - center[0]),
			scale * p[1] + center[1]
		)
		
	def hyperlanes(self, fill, width):
		exclude = set()
		for system in self._model.systems.values():
			for hyperlane in system.hyperlanes:
				if hyperlane.dest not in exclude:
					a = self._convert_position_to_point(system.pos)
					b = self._convert_position_to_point(self._model.systems[hyperlane.dest].pos)
					self._draw.line(
						(a[0],a[1],b[0],b[1]), 
						fill=tuple(self._config["hyperlane.fill"]),
					 	width=self._config["hyperlane.width"]
					)
			exclude.add(system.id)
			
	def regions(self):
		points = []
		voronoi_index = {}
		
		index = 0
		for system in self._model.systems.values():
			point = self._convert_position_to_point(system.pos)
			voronoi_index[system.id] = index
			points.append(list(point))			
			index += 1
			
		for ring in self._config["voronoi.rings"]:
			for angle in range(0, 365, ring["s"]):
				point = self._convert_position_to_point((
					ring["x"] + ring["r"] * math.cos(math.radians(angle)),
					ring["y"] + ring["r"] * math.sin(math.radians(angle))
				))
				
				
				if self._config["debug"]:
					self._draw.point(point, fill=tuple(self._config["debug.color"]))
				
				points.append(list(point))				
		
		vor = Voronoi(numpy.array(points))
		
		for system in self._model.systems.values():
			region = vor.regions[vor.point_region[voronoi_index[system.id]]]			
			color = self._get_system_color(system)
			if color:
				self._render_region(vor, region, color)
				
	def _get_system_color(self, system):
		if system.starbase:
			owner = system.starbase.owner
			color = owner.flag["colors"][1]
			if color in self._config["color"]:
				offset = (0,0,0)
				try:
					offset = COUNTRY_OFFSETS[int(owner.id)]					
				except IndexError:
					offset = (0,0,0)
				return tuple([a+b-30 for (a,b) in zip(self._config["color"][color], offset)])
			else:
				print("WARNING: Missing color '" + color + "'")				
				return (256, 256, 256)
		else:
			return None
			
	def _render_region(self, vor, region, fill=None, outline=None):
		if -1 in region:
			return

		points = []
		for index in region:
			vertex = vor.vertices[index]
			points.append((int(vertex[0]), int(vertex[1])))		

		if points:
			self._draw.polygon(points, fill=fill, outline=outline)
			
	def pops(self):
		for system in self._model.systems.values():
			pops = sum([len(planet.pops) for planet in system.planets])
			if pops != 0:
				
				color = self._get_system_color(system)				
				if color:
					color = tuple([min(x+60,255) for x in color])
				else:
					color = (255,255,255)

				p = self._convert_position_to_point(system.pos)
				r = int(2 * math.sqrt(pops / math.pi) + 0.5)
				self._draw.ellipse(
					(p[0]-r,p[1]-r,p[0]+r, p[1]+r), 
					fill=color,
					outline=tuple(self._config["pops.outline"])
				)
	
	def export(self, path):
		self._image.save(path)
	