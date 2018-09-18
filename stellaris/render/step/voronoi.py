import math, numpy, random
import scipy.spatial 

from ..render import RenderStep
from ..color import get_color
from ..utils import convert_position_to_point

class RegionsStep(RenderStep):

    def __init__(self):
        super().__init__("voronoi")

    def run(self, ctx, config):
        # the voronoi diagram is built from a list of vertices
        vertices = []
        system_indices = []
        
        # add vertices for every system
        index = 0
        for system in ctx.model.systems.values():
            vertices.append(list(system.pos))
            system_indices.append((system.id, index))
            index += 1

        # add vertices for every hyperlane
        c = config["hyperlane_point_count"] + 1
        hyperlanes = set([h for s in ctx.model.systems.values() for h in s.hyperlanes])
        for hyperlane in hyperlanes:
            for weight in [x/c for x in range(1,c)]:
                vertices.append([
                    weight * hyperlane.src.pos[0] + (1 - weight) * hyperlane.dest.pos[0],
                    weight * hyperlane.src.pos[1] + (1 - weight) * hyperlane.dest.pos[1]
                ])

                # tied to the nearest system
                system = hyperlane.src if 0.5 < weight else hyperlane.dest
                system_indices.append((system.id, index))
                index += 1

        # add vertices for rings
        config_rings = config["rings"]
        for ring in self._get_rings(ctx, config_rings):
            angle = 0
            while angle < 360:
                vertex = [
                    ring["x"] + ring["r"] * math.cos(math.radians(angle)),
                    ring["y"] + ring["r"] * math.sin(math.radians(angle))
                ]

                if config_rings["debug"]:
                    point = convert_position_to_point(ctx, vertex)
                    ctx.draw.point(point, fill=get_color(ctx, config_rings["debug_color"]))
                
                vertices.append(list(vertex))

                angle += ring["s"]
        
        # build diagram from vertices
        vor = scipy.spatial.Voronoi(numpy.array(vertices))

        ctx.data[config["output"]] = Voronoi(ctx, vor, system_indices)



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
                if not visited[hyperlane.dest.id]:
                    result += dfs_util(hyperlane.dest.id)
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

        # create rings
        padding = config["autogen_padding"]
        spacing = config["autogen_spacing"]
        results = [self._create_ring(c, r_max + padding, spacing)]
        if padding < r_min:
            results.append(self._create_ring(c, r_min - padding, spacing))
        return results



    def _create_ring(self, center, radius, spacing):
        n = (2*math.pi*radius) / spacing
        s = 360/n
        return { 
            "x": center[0],
            "y": center[1],
            "r": radius,
            "s": s
        }



class Voronoi:
    def __init__(self, ctx, vor, system_indices):
        self.regions = []

        for (system_id, i) in system_indices:
            region = vor.regions[vor.point_region[i]]
            if -1 not in region:
                system = ctx.model.systems[system_id]
                vertices = [tuple(vor.vertices[j]) for j in region]
                self.regions.append(Region(system, vertices))

class Region:
    def __init__(self, system, vertices):
        self.system = system
        self.vertices = vertices