import math, numpy, random
import scipy.spatial 

from collections import defaultdict, namedtuple

from ..render import RenderStep
from ..color import get_color
from ..utils import convert_position_to_point



class VoronoiStep(RenderStep):

    def __init__(self):
        super().__init__("voronoi")

    def run(self, ctx, config):
        vor = Voronoi()

        # add vertices for every system
        for system in ctx.model.systems.values():
            vor.add_vertex(system.pos, system)

        # add vertices for every hyperlane
        hyperlanes = set([h for s in ctx.model.systems.values() for h in s.hyperlanes])
        for hyperlane in hyperlanes:

            c = int(hyperlane.length / config["hyperlane_point_spacing"])
            if c%2 == 0:
                c += 1

            for weight in [x/c for x in range(1,c)]:
                vertex = [
                    weight * hyperlane.src.pos[0] + (1 - weight) * hyperlane.dest.pos[0],
                    weight * hyperlane.src.pos[1] + (1 - weight) * hyperlane.dest.pos[1]
                ]
                # tied to the nearest system
                system = hyperlane.src if 0.5 < weight else hyperlane.dest
                vor.add_vertex(vertex, system)

        vor.generate_rings(ctx, config["rings"])

        vor.finalize()

        ctx.data[config["output"]] = vor





Region = namedtuple("Region", ["system", "vertices"])

class Voronoi:
    def __init__(self):
        self._vertices = []
        self._system_indices = defaultdict(list)
        self._index = 0

    def add_vertex(self, vertex, system=None):
        self._vertices.append(list(vertex))
        if system != None:
            self._system_indices[system].append(self._index)
        self._index += 1

    def generate_rings(self, ctx, config):
        rings = []
        for group in self._get_system_groups(ctx):
            rings += self._generate_rings(ctx, config, group)

        for ring in rings:
            angle = 0
            while angle < 360:
                vertex = [
                    ring["x"] + ring["r"] * math.cos(math.radians(angle)),
                    ring["y"] + ring["r"] * math.sin(math.radians(angle)),
                ]

                if config["debug"]:
                    point = convert_position_to_point(ctx, vertex)
                    ctx.draw.point(point, fill=get_color(ctx, config["debug_color"]))

                self.add_vertex(vertex)

                angle += ring["s"]

    def finalize(self):
        vor = scipy.spatial.Voronoi(numpy.array(self._vertices))

        self.regions = []
        for (system, indices) in self._system_indices.items():
            regions = [vor.regions[vor.point_region[i]] for i in indices]
            for region in regions:
                if -1 not in region:
                    vertices = [tuple(vor.vertices[i]) for i in region]
                    self.regions.append(Region(system, vertices))

    def _get_system_groups(self, ctx):
        # https://www.geeksforgeeks.org/connected-components-in-an-undirected-graph/
        systems = ctx.model.systems
        visited = dict([(s.id, False) for s in systems.values()])

        def dfs_util(id):
            result = [id]
            visited[id] = True
            system = systems[id]
            for hyperlane in system.hyperlanes:
                if not visited[hyperlane.dest.id]:
                    result += dfs_util(hyperlane.dest.id)
            return result

        result = []

        for id in systems.keys():
            if not visited[id]:
                result.append(dfs_util(id))

        return result

    def _generate_rings(self, ctx, config, group):
        if len(group) < 2:
            return []

        systems = [ctx.model.systems[id] for id in group]

        # center
        c = (
            sum([s.pos[0] for s in systems])/len(systems),
            sum([s.pos[1] for s in systems])/len(systems)
        )

        # minimum and maximum radius from the center
        r_min = 10000
        r_max = 0

        for s in systems:
            r = math.sqrt(math.pow(c[0]-s.pos[0], 2) + math.pow(c[1]-s.pos[1], 2))
            r_min = min(r_min, r)
            r_max = max(r_max, r)

        padding = config["padding"]
        spacing = config["spacing"]

        def create(center, radius, spacing):
            n = (2*math.pi*radius) / spacing
            s = 360/n
            return { 
                "x": center[0],
                "y": center[1],
                "r": radius,
                "s": s
            }

        # create rings
        results = [create(c, r_max + padding, spacing)]
        if padding < r_min:
            results.append(create(c, r_min - padding, spacing))
        return results
