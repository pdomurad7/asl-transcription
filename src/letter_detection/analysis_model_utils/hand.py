from dataclasses import dataclass

import numpy as np


@dataclass
class Point:
    width: float
    height: float
    depth: float


class Finger:
    def __init__(
        self,
        x_points: list | np.ndarray,
        y_points: list | np.ndarray,
        z_points: list | np.ndarray,
    ) -> None:
        self.__bottom = Point(x_points[0], y_points[0], z_points[0])
        self.__middle_bottom = Point(x_points[1], y_points[1], z_points[1])
        self.__middle_top = Point(x_points[2], y_points[2], z_points[2])
        self.__top = Point(x_points[3], y_points[3], z_points[3])

    def is_folded(self) -> bool:
        return self.__top.height > self.__middle_top.height

    # for the thumb
    def is_almost_folded(self) -> bool:
        return self.__top.height > self.__middle_top.height - 0.1

    @property
    def bottom(self) -> Point:
        return self.__bottom

    @property
    def middle_bottom(self) -> Point:
        return self.__middle_bottom

    @property
    def middle_top(self) -> Point:
        return self.__middle_top

    @property
    def top(self) -> Point:
        return self.__top


class Hand:
    TOUCHING_THRESHOLD = 0.15

    def __init__(self, x_points, y_points, z_points, is_vertical: bool) -> None:
        self.__x_points = x_points
        self.__y_points = y_points
        self.__z_points = z_points
        self.__is_vertical = is_vertical
        self.__wrist = Point(x_points[0], y_points[0], z_points[0])
        self.__thumb = Finger(x_points[1:5], y_points[1:5], z_points[1:5])
        self.__index = Finger(x_points[5:9], y_points[5:9], z_points[5:9])
        self.__middle = Finger(x_points[9:13], y_points[9:13], z_points[9:13])
        self.__ring = Finger(x_points[13:17], y_points[13:17], z_points[13:17])
        self.__pinky = Finger(x_points[17:21], y_points[17:21], z_points[17:21])

    @staticmethod
    def _distance(point1: Point, point2: Point):
        return np.sqrt(
            (point1.width - point2.width) ** 2 + (point1.height - point2.height) ** 2
        )

    def is_vertical(self) -> bool:
        return self.__is_vertical

    def thumb_position(self) -> int:
        if self.__thumb.top.width > self.__index.middle_bottom.width:
            return 0
        elif (
            self.__index.middle_bottom.width
            > self.__thumb.top.width
            > self.__middle.middle_bottom.width
        ):
            return 1
        elif (
            self.__middle.middle_bottom.width
            > self.__thumb.top.width
            > self.__ring.middle_bottom.width
        ):
            return 2
        elif self.__ring.top.width > self.__thumb.top.width < self.__pinky.top.width:
            return 3
        else:
            return 4

    def is_closed_hand(self) -> bool:
        close_hand_threshold = -0.1
        return (
            # index finger in some letters is a little higher even with closed hand
            self.__index.bottom.height - self.__index.top.height < close_hand_threshold
            and self.__middle.bottom.height - self.__middle.top.height
            < close_hand_threshold
            and self.__ring.bottom.height - self.__ring.top.height
            < close_hand_threshold
            and self.__pinky.bottom.height - self.__pinky.top.height
            < close_hand_threshold
        )

    def is_front(self) -> bool:
        return self.__index.bottom.width - self.__pinky.bottom.width > 0.2

    def is_thumb_near_hand(self) -> bool:
        return self.__thumb.top.width < (self.__index.bottom.width + 0.15)

    def is_thumb_under_top_index(self) -> bool:
        return self.__thumb.top.height > self.__index.top.height

    def is_index_and_thumb_touching(self) -> bool:
        return self._distance(self.__thumb.top, self.__index.top) < 0.2

    @property
    def wrist(self) -> Point:
        return self.__wrist

    @property
    def thumb(self) -> Finger:
        return self.__thumb

    @property
    def index(self) -> Finger:
        return self.__index

    @property
    def middle(self) -> Finger:
        return self.__middle

    @property
    def ring(self) -> Finger:
        return self.__ring

    @property
    def pinky(self) -> Finger:
        return self.__pinky


class RightHand(Hand):
    pass


class LeftHand(Hand):
    pass
