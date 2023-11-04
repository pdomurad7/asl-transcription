import math


def rotate_points(points):
    origin = points[0]
    rotated_points_x = [origin[0]]
    rotated_points_y = [origin[1]]

    p0, p9 = points[0], points[9]
    dx, dy = p9[0] - p0[0], p9[1] - p0[1]
    alpha = math.atan(dx / dy)

    if alpha > 3.14 / 4:
        alpha -= 3.14 / 2
    elif alpha < -3.14 / 4:
        alpha += 3.14 / 2

    for x, y in points[1:]:
        dx, dy = x - origin[0], y - origin[1]

        new_x = origin[0] + (dx * math.cos(alpha) - dy * math.sin(alpha))
        new_y = origin[1] + (dx * math.sin(alpha) + dy * math.cos(alpha))

        rotated_points_x.append(new_x)
        rotated_points_y.append(new_y)

    return rotated_points_x, rotated_points_y


def normalize_lists(xs, ys, rotate=True):
    if rotate:
        xs, ys = rotate_points(list(zip(xs, ys)))
    min_x = min(xs)
    max_x = max(xs)
    min_y = min(ys)
    max_y = max(ys)

    diff_x = max_x - min_x
    diff_y = max_y - min_y

    scale = max(diff_x, diff_y)

    normalized_xs = [(x - min_x) / scale for x in xs]
    normalized_ys = [(y - min_y) / scale for y in ys]

    return normalized_xs, normalized_ys
