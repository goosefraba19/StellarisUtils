from ..render import RenderStep
from ..color import get_color
from ..utils import convert_position_to_point

from collections import defaultdict

class RegionsStep(RenderStep):

    def __init__(self):
        super().__init__("borders")

    def run(self, ctx, config):
        vor = ctx.data[config["input"]]

        edge_systems = defaultdict(list)

        for region in vor.regions:
            vertices = region.vertices
            edges = [tuple(sorted([vertices[i], vertices[i+1]])) for i in range(-1, len(vertices)-1)]
            for edge in edges:
                edge_systems[edge].append(region.system)
            
        width = config["width"]
        fill = get_color(ctx, config["fill"])

        for (edge, systems) in edge_systems.items():

            owners = set()
            for system in systems:
                if system.starbase:
                    owners.add(system.starbase.owner)
                else:
                    owners.add(None)

            is_rim_controlled = len(systems) == 1 and None not in owners
            is_border = 1 < len(owners)

            if is_border or is_rim_controlled:
                points = [convert_position_to_point(ctx, v) for v in edge]
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
