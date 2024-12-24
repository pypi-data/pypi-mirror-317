from textual.containers import Vertical as TextualVertical


class Vertical(TextualVertical):
    @property
    def has_focus_within(self):
        try:
            focused = self.screen.focused
        except NoScreen:
            return False
        node = focused
        while node is not None:
            if node is self:
                return True
            node = node._parent
        return False
