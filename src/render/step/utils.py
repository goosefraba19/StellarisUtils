import random

def convert_position_to_point(ctx, p):
    scale = ctx.config["image"]["scale"]
    size = ctx.config["image"]["size"]
    center = ctx.config["image"]["center"]
    return (
        -1 * scale * p[0] + (size[0] - center[0]),
        scale * p[1] + center[1]
    )

random.seed(2)
COUNTRY_OFFSETS = [(random.randint(-40,40), random.randint(-40,40), random.randint(-40,40)) for _ in range(500)]

def get_system_color(ctx, system):
    if system.starbase:

        country = system.starbase.owner
        country_color = _get_color(ctx, country.flag.colors[1])

        offset = (0,0,0)
        try:
            offset = COUNTRY_OFFSETS[int(country.id)]					
        except IndexError:
            offset = (0,0,0)

        country_color = tuple([a+b for a,b in zip(country_color, offset)])

        base = None
        if ctx.config["use_federation_or_overlord_color"]:
            if country.alliance:
                base = country.alliance.members[0]
            if country.overlord:
                base = country.overlord

        if base != None and base != country:
            base_color = _get_color(ctx, base.flag.colors[1])
            return tuple([int(0.75*a + 0.25*b) for a,b in zip(base_color, country_color)])
        else:
            return country_color
    else:
        return None

def _get_color(ctx, color):
    if color in ctx.config["color"]:
        return ctx.config["color"][color]
    else:
        print("WARNING: Missing color '" + color + "'")				
        return (256, 256, 256)
