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
        owner = system.starbase.owner
        color = owner.flag["colors"][1]
        if color in ctx.config["color"]:
            offset = (0,0,0)
            try:
                offset = COUNTRY_OFFSETS[int(owner.id)]					
            except IndexError:
                offset = (0,0,0)
            return tuple([a+b-30 for (a,b) in zip(ctx.config["color"][color], offset)])
        else:
            print("WARNING: Missing color '" + color + "'")				
            return (256, 256, 256)
    else:
        return None
