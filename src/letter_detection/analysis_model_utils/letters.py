from abc import abstractmethod

from .hand import Hand


class Letter:
    def __init__(self, hand: Hand):
        self.hand = hand

    @abstractmethod
    def check_rules(self) -> bool:
        pass


class A(Letter):
    def __init__(self, hand: Hand):
        super().__init__(hand)

    def check_rules(self) -> bool:
        try:
            assert self.hand.is_vertical()
            assert self.hand.index.is_folded()
            assert self.hand.middle.is_folded()
            assert self.hand.ring.is_folded()
            assert self.hand.pinky.is_folded()
            assert self.hand.is_front()
            assert self.hand.is_thumb_near_hand()
            assert not self.hand.is_thumb_under_top_index()
            assert self.hand.thumb_position() == 0
            assert self.hand.is_closed_hand()
        except AssertionError:
            return False
        else:
            return True


class B(Letter):
    def __init__(self, hand: Hand):
        super().__init__(hand)

    def check_rules(self) -> bool:
        try:
            assert self.hand.is_vertical()
            assert not self.hand.thumb.is_folded()
            assert not self.hand.index.is_folded()
            assert not self.hand.middle.is_folded()
            assert not self.hand.ring.is_folded()
            assert not self.hand.pinky.is_folded()
            assert self.hand.is_front()
            assert self.hand.is_thumb_near_hand()
        except AssertionError:
            return False
        else:
            return True


class C(Letter):
    def __init__(self, hand: Hand):
        super().__init__(hand)

    def check_rules(self) -> bool:
        try:
            assert self.hand.is_vertical()
            assert not self.hand.thumb.is_almost_folded()
            assert self.hand.index.is_folded()
            assert self.hand.middle.is_folded()
            assert self.hand.ring.is_folded()
            assert self.hand.pinky.is_folded()
            assert self.hand.is_thumb_under_top_index()
            assert not self.hand.is_index_and_thumb_touching()
            assert not self.hand.is_closed_hand()
        except AssertionError:
            return False
        else:
            return True


class D(Letter):
    def __init__(self, hand: Hand):
        super().__init__(hand)

    def check_rules(self) -> bool:
        try:
            assert self.hand.is_vertical()
            assert not self.hand.thumb.is_folded()
            assert not self.hand.index.is_almost_folded()
            assert self.hand.middle.is_folded()
            assert self.hand.ring.is_folded()
            assert self.hand.pinky.is_folded()
            assert self.hand.is_front()
            assert self.hand.is_thumb_near_hand()
        except AssertionError:
            return False
        else:
            return True


class E(Letter):
    def __init__(self, hand: Hand):
        super().__init__(hand)

    def check_rules(self) -> bool:
        try:
            assert self.hand.is_vertical()
            assert self.hand.thumb.is_almost_folded()
            assert self.hand.index.is_folded()
            assert self.hand.middle.is_folded()
            assert self.hand.ring.is_folded()
            assert self.hand.pinky.is_folded()
            assert self.hand.is_front()
            assert self.hand.is_thumb_near_hand()
            assert self.hand.is_thumb_under_top_index()
            assert not self.hand.is_closed_hand()
        except AssertionError:
            return False
        else:
            return True


class F(Letter):
    def __init__(self, hand: Hand):
        super().__init__(hand)

    def check_rules(self) -> bool:
        try:
            assert self.hand.is_vertical()
            assert not self.hand.thumb.is_folded()
            assert self.hand.index.is_folded()
            assert not self.hand.middle.is_folded()
            assert not self.hand.ring.is_folded()
            assert not self.hand.pinky.is_folded()
            assert self.hand.is_index_and_thumb_touching()
        except AssertionError:
            return False
        else:
            return True


class G(Letter):
    def __init__(self, hand: Hand):
        super().__init__(hand)

    def check_rules(self) -> bool:
        try:
            assert self.hand.is_front()
            assert not self.hand.is_vertical()
            assert not self.hand.index.is_folded()
            assert self.hand.middle.is_folded()
            assert self.hand.ring.is_folded()
            assert self.hand.pinky.is_folded()
        except AssertionError:
            return False
        else:
            return True


class H(Letter):
    def __init__(self, hand: Hand):
        super().__init__(hand)

    def check_rules(self) -> bool:
        try:
            assert self.hand.is_front()
            assert not self.hand.is_vertical()
            assert not self.hand.index.is_folded()
            assert not self.hand.middle.is_folded()
            assert self.hand.ring.is_folded()
            assert self.hand.pinky.is_folded()
        except AssertionError:
            return False
        else:
            return True


class I(Letter):
    def __init__(self, hand: Hand):
        super().__init__(hand)

    def check_rules(self) -> bool:
        try:
            assert self.hand.is_vertical()
            assert not self.hand.thumb.is_folded()
            assert self.hand.index.is_folded()
            assert self.hand.middle.is_folded()
            assert self.hand.ring.is_folded()
            assert not self.hand.pinky.is_folded()
            assert self.hand.is_front()
            assert self.hand.is_thumb_near_hand()
        except AssertionError:
            return False
        else:
            return True


class J(Letter):
    def __init__(self, hand: Hand):
        super().__init__(hand)

    def check_rules(self) -> bool:
        # TODO: moving letter
        return False


class K(Letter):
    def __init__(self, hand: Hand):
        super().__init__(hand)

    def check_rules(self) -> bool:
        try:
            assert self.hand.is_vertical()
            assert not self.hand.thumb.is_folded()
            assert not self.hand.index.is_folded()
            assert not self.hand.middle.is_folded()
            assert self.hand.ring.is_folded()
            assert self.hand.pinky.is_folded()
            assert self.hand.is_front()
            assert self.hand.is_thumb_near_hand()
            assert self.hand.thumb_position() == 1
            assert (
                self.hand.index.top.width - self.hand.middle.top.width
                > self.hand.TOUCHING_THRESHOLD
            )
            assert (
                self.hand.thumb.top.height < self.hand.index.bottom.height
                and self.hand.thumb.top.height < self.hand.middle.bottom.height
            )
        except AssertionError:
            return False
        else:
            return True


class L(Letter):
    def __init__(self, hand: Hand):
        super().__init__(hand)

    def check_rules(self) -> bool:
        try:
            assert self.hand.is_vertical()
            assert not self.hand.index.is_folded()
            assert self.hand.middle.is_folded()
            assert self.hand.ring.is_folded()
            assert self.hand.pinky.is_folded()
            assert self.hand.is_front()
            assert not self.hand.is_thumb_near_hand()
        except AssertionError:
            return False
        else:
            return True


class M(Letter):
    def __init__(self, hand: Hand):
        super().__init__(hand)

    def check_rules(self) -> bool:
        try:
            assert self.hand.is_vertical()
            assert self.hand.index.is_folded()
            assert self.hand.middle.is_folded()
            assert self.hand.ring.is_folded()
            assert self.hand.pinky.is_folded()
            assert self.hand.is_front()
            assert self.hand.is_thumb_near_hand()
            assert not self.hand.is_thumb_under_top_index()
            assert self.hand.thumb_position() == 3
            assert self.hand.is_closed_hand()
        except AssertionError:
            return False
        else:
            return True


class N(Letter):
    def __init__(self, hand: Hand):
        super().__init__(hand)

    def check_rules(self) -> bool:
        try:
            assert self.hand.is_vertical()
            assert self.hand.index.is_folded()
            assert self.hand.middle.is_folded()
            assert self.hand.ring.is_folded()
            assert self.hand.pinky.is_folded()
            assert self.hand.is_front()
            assert self.hand.is_thumb_near_hand()
            assert not self.hand.is_thumb_under_top_index()
            assert self.hand.thumb_position() == 2
            assert self.hand.is_closed_hand()
        except AssertionError:
            return False
        else:
            return True


class O(Letter):
    def __init__(self, hand: Hand):
        super().__init__(hand)

    def check_rules(self) -> bool:
        try:
            assert self.hand.is_vertical()
            assert not self.hand.thumb.is_folded()
            assert self.hand.index.is_folded()
            assert self.hand.middle.is_folded()
            assert self.hand.ring.is_folded()
            assert self.hand.pinky.is_folded()
            assert self.hand.is_index_and_thumb_touching()
            assert not self.hand.is_closed_hand()
        except AssertionError:
            return False
        else:
            return True


class P(Letter):
    def __init__(self, hand: Hand):
        super().__init__(hand)

    def check_rules(self) -> bool:
        try:
            assert not self.hand.is_front()
            assert not self.hand.is_vertical()
            assert not self.hand.index.is_folded()
            assert self.hand.middle.is_folded()
            assert self.hand.ring.is_folded()
            assert self.hand.pinky.is_folded()
        except AssertionError:
            return False
        else:
            return True


class Q(Letter):
    def __init__(self, hand: Hand):
        super().__init__(hand)

    def check_rules(self) -> bool:
        try:
            assert not self.hand.is_front()
            assert not self.hand.is_vertical()
            assert self.hand.index.is_folded()
        except AssertionError:
            return False
        else:
            return True


class R(Letter):
    def __init__(self, hand: Hand):
        super().__init__(hand)

    def check_rules(self) -> bool:
        try:
            assert self.hand.is_vertical()
            assert not self.hand.thumb.is_folded()
            assert not self.hand.index.is_folded()
            assert not self.hand.middle.is_folded()
            assert self.hand.ring.is_folded()
            assert self.hand.pinky.is_folded()
            assert self.hand.is_front()
            assert self.hand.is_thumb_near_hand()
            assert self.hand.index.top.width < self.hand.middle.top.width
        except AssertionError:
            return False
        else:
            return True


class S(Letter):
    def __init__(self, hand: Hand):
        super().__init__(hand)

    def check_rules(self) -> bool:
        try:
            assert self.hand.is_vertical()
            assert self.hand.index.is_folded()
            assert self.hand.middle.is_folded()
            assert self.hand.ring.is_folded()
            assert self.hand.pinky.is_folded()
            assert self.hand.is_front()
            assert self.hand.is_thumb_near_hand()
            assert not self.hand.is_thumb_under_top_index()
            assert self.hand.thumb_position() == 1
            assert self.hand.is_closed_hand()
            assert self.hand.index.top.depth - self.hand.thumb.middle_top.depth > -0.02
        except AssertionError:
            return False
        else:
            return True


class T(Letter):
    def __init__(self, hand: Hand):
        super().__init__(hand)

    def check_rules(self) -> bool:
        try:
            assert self.hand.is_vertical()
            assert self.hand.index.is_folded()
            assert self.hand.middle.is_folded()
            assert self.hand.ring.is_folded()
            assert self.hand.pinky.is_folded()
            assert self.hand.is_front()
            assert self.hand.is_thumb_near_hand()
            assert not self.hand.is_thumb_under_top_index()
            assert self.hand.thumb_position() == 1
            assert self.hand.is_closed_hand()
            assert self.hand.index.top.depth - self.hand.thumb.middle_top.depth < -0.02
        except AssertionError:
            return False
        else:
            return True


class U(Letter):
    def __init__(self, hand: Hand):
        super().__init__(hand)

    def check_rules(self) -> bool:
        try:
            assert self.hand.is_vertical()
            assert not self.hand.thumb.is_folded()
            assert not self.hand.index.is_folded()
            assert not self.hand.middle.is_folded()
            assert self.hand.ring.is_folded()
            assert self.hand.pinky.is_folded()
            assert self.hand.is_front()
            assert self.hand.is_thumb_near_hand()
            assert self.hand.index.top.width > self.hand.middle.top.width
            assert (
                self.hand.index.top.width - self.hand.middle.top.width
                < self.hand.TOUCHING_THRESHOLD
            )
            assert self.hand.thumb_position() >= 2
        except AssertionError:
            return False
        else:
            return True


class V(Letter):
    def __init__(self, hand: Hand):
        super().__init__(hand)

    def check_rules(self) -> bool:
        try:
            assert self.hand.is_vertical()
            assert not self.hand.thumb.is_folded()
            assert not self.hand.index.is_folded()
            assert not self.hand.middle.is_folded()
            assert self.hand.ring.is_folded()
            assert self.hand.pinky.is_folded()
            assert self.hand.is_front()
            assert self.hand.is_thumb_near_hand()
            assert (
                self.hand.index.top.width - self.hand.middle.top.width
                > self.hand.TOUCHING_THRESHOLD
            )
            assert self.hand.thumb_position() >= 2
        except AssertionError:
            return False
        else:
            return True


class W(Letter):
    def __init__(self, hand: Hand):
        super().__init__(hand)

    def check_rules(self) -> bool:
        try:
            assert self.hand.is_vertical()
            assert not self.hand.thumb.is_folded()
            assert not self.hand.index.is_folded()
            assert not self.hand.middle.is_folded()
            assert not self.hand.ring.is_folded()
            assert self.hand.pinky.is_folded()
            assert self.hand.is_front()
            assert self.hand.is_thumb_near_hand()
        except AssertionError:
            return False
        else:
            return True


class X(Letter):
    def __init__(self, hand: Hand):
        super().__init__(hand)

    def check_rules(self) -> bool:
        try:
            assert self.hand.is_vertical()
            assert self.hand.index.is_almost_folded()
            assert self.hand.middle.is_folded()
            assert self.hand.ring.is_folded()
            assert self.hand.pinky.is_folded()
            assert self.hand.is_front()
            assert self.hand.is_thumb_near_hand()
            assert self.hand.is_thumb_under_top_index()
            assert (
                self.hand.index.middle_top.height
                < self.hand.middle.middle_bottom.height
            )
        except AssertionError:
            return False
        else:
            return True


class Y(Letter):
    def __init__(self, hand: Hand):
        super().__init__(hand)

    def check_rules(self) -> bool:
        try:
            assert self.hand.is_vertical()
            assert not self.hand.thumb.is_folded()
            assert self.hand.index.is_folded()
            assert self.hand.middle.is_folded()
            assert self.hand.ring.is_folded()
            assert not self.hand.pinky.is_folded()
            assert self.hand.is_front()
            assert not self.hand.is_thumb_near_hand()
        except AssertionError:
            return False
        else:
            return True


class Z(Letter):
    def __init__(self, hand: Hand):
        super().__init__(hand)

    def check_rules(self) -> bool:
        # TODO: moving letter
        return False


letters = Letter.__subclasses__()
