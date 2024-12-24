import logging
from textual.app import App, ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Static, Footer, Button, ContentSwitcher
from tfdocs.views.viewer import Viewer
from tfdocs.views.switcher import Switcher
from tfdocs.views.special import Special
from tfdocs.logging import setup_logs


def app():
    comp_view = ComponentViewer()
    comp_view.run()


class ComponentViewer(App):
    CSS_PATH = "styles/component_viewer.tcss"
    BINDINGS = [
        ("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        with Horizontal(id="buttons"):
            yield Button("Viewer", id="viewer")
            yield Button("Switcher", id="switcher")
            yield Button("Special", id="special")
        with ContentSwitcher(id="component_viewer", initial="viewer"):
            yield Special(id="special")
            yield Viewer(id="viewer", classes="")
            yield Switcher(id="switcher", classes="pane")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.query_one(ContentSwitcher).current = event.button.id


if __name__ == "__main__":
    setup_logs(enable_log_streaming=True)
    app()
