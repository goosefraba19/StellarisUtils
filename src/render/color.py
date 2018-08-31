import random

def get_color(ctx, obj, args={}):
    if type(obj)==tuple:
        return obj
    elif type(obj)==list:
        return tuple(obj)
    elif type(obj)==str:
        if obj == "none":
            return None
        elif obj in ctx.config["color"]:
            return tuple(ctx.config["color"][obj])
        else:
            print(f"WARNING: Color '{obj}' not found.'")
            return None
    elif "key" in obj:
        if obj["key"] == "blend":
            return blend_colors(
                get_color(ctx, obj["first"], args),
                get_color(ctx, obj["second"], args),
                obj["weight"]
            )
        elif obj["key"] == "or":
            return _get_color_or(ctx, obj, args)
        elif obj["key"] == "system_owner":
            return _get_color_system_owner(ctx, obj, args)
        elif obj["key"] == "system_controller":
            return _get_color_system_controller(ctx, obj, args)
        else:
            print(f"WARNING: Key '{obj['key']}' not recognized.")
            return None
    else:
        print("WARNING: Unrecognized color setting.")
        return None

def _get_color_or(ctx, obj, args):
    first = get_color(ctx, obj["first"], args)
    if first:
        return first
    else:
        return get_color(ctx, obj["second"], args)
    
def _get_color_system_owner(ctx, obj, args):
    system = args["system"]
    if system.starbase:
        return _get_country_color(ctx, system.starbase.owner)
    else:
        return None

def _get_color_system_controller(ctx, obj, args):
    controller = args["system"].planets[0].controller
    if controller:
        return _get_country_color(ctx, controller)
    else:
        return None

random.seed(2)
COUNTRY_OFFSETS = [(random.randint(-40,40), random.randint(-40,40), random.randint(-40,40)) for _ in range(500)]

def _get_country_color(ctx, country):
    colors = country.flag.colors

    color = (0,0,0)
    if len(colors) == 1:
        color = get_color(ctx, country.flag.colors[0])
    elif len(colors) > 1:
        color = get_color(ctx, country.flag.colors[1])


    if color == None:
        return None

    offset = (0,0,0)
    try:
        offset = COUNTRY_OFFSETS[int(country.id)]					
    except IndexError:
        offset = (0,0,0)

    color = tuple([max(0, min(a+b, 256)) for a,b in zip(color, offset)])

    base = None
    if ctx.config["use_federation_or_overlord_color"]:
        if country.alliance:
            base = country.alliance.members[0]
        elif country.overlord:
            base = country.overlord

    if base != None and base != country:
        base_color = _get_country_color(ctx, base)
        if base_color == None:
            return None
        else:
            return blend_colors(base_color, color, 0.75)
    else:
        return color

def blend_colors(first, second, weight):
    if first != None and second != None:
        return tuple([int(weight*a + (1-weight)*b) for a,b in zip(first, second)])
    elif first == None:
        return second
    else:
        return first