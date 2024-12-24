from textual.app import App, ComposeResult
from textual.widgets import Footer

from tfdocs.views.layout import PaneLayout
from tfdocs.models.block import Block


class TFDocs(App):
    BINDINGS = [
        ("q", "quit", "Quit"),
    ]

    def __init__(self, open_to: Block | None = None):
        self.open_to = open_to
        super().__init__()

    def compose(self) -> ComposeResult:
        yield PaneLayout(self.open_to) if self.open_to is not None else PaneLayout()
        yield Footer()


def app(open: Block | None = None):
    app = TFDocs(open) if open is not None else TFDocs()
    app.run()
