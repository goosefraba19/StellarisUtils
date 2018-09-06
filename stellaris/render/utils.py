def convert_position_to_point(ctx, p):
    scale = ctx.config["image"]["scale"]
    size = ctx.config["image"]["size"]
    center = ctx.config["image"]["center"]
    return (
        -1 * scale * p[0] + (size[0] - center[0]),
        scale * p[1] + center[1]
    )
