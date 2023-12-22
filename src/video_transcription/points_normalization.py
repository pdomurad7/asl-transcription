import math


def rotate_points(points):
    # Ustawienie współrzędnych nadgarstka jako punkt odniesienia (origin)
    origin = points[0]
    rotated_points_x = [origin[0]]
    rotated_points_y = [origin[1]]

    # Obliczenie różnicy między współrzędnymi nadgarstka i dolnej części palca środkowego
    p0, p9 = points[0], points[9]
    dx, dy = p9[0] - p0[0], p9[1] - p0[1]
    # Obliczenie kąta obrotu na podstawie różnicy współrzędnych
    alpha = math.atan(dx / dy)

    # Sprawdzenie, czy punkty są ustawione pionowo
    is_vertical = True
    if alpha > 3.14 / 4:
        is_vertical = False
    elif alpha < -3.14 / 4:
        is_vertical = False

    # Obracanie każdego punktu oprócz punktu odniesienia
    for x, y in points[1:]:
        dx, dy = x - origin[0], y - origin[1]

        # Obliczenie nowych współrzędnych po obrocie
        new_x = origin[0] + (dx * math.cos(alpha) - dy * math.sin(alpha))
        new_y = origin[1] + (dx * math.sin(alpha) + dy * math.cos(alpha))

        # Dodanie nowych współrzędnych do list
        rotated_points_x.append(new_x)
        rotated_points_y.append(new_y)

    return rotated_points_x, rotated_points_y, is_vertical


def normalize_lists(xs, ys, rotate=True):
    is_vertical = None
    if rotate:
        xs, ys, is_vertical = rotate_points(list(zip(xs, ys)))

    # Znalezienie minimalnych i maksymalnych wartości w obu listach
    min_x = min(xs)
    max_x = max(xs)
    min_y = min(ys)
    max_y = max(ys)

    # Obliczenie różnicy między maksymalnymi i minimalnymi wartościami
    diff_x = max_x - min_x
    diff_y = max_y - min_y

    # Ustalenie skali normalizacji
    scale = max(diff_x, diff_y)

    # Normalizacja współrzędnych X i Y
    normalized_xs = [(x - min_x) / scale for x in xs]
    normalized_ys = [(y - min_y) / scale for y in ys]

    return normalized_xs, normalized_ys, is_vertical
