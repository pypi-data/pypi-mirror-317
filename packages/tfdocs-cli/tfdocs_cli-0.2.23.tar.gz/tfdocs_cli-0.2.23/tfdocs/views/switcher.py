import logging
from textual.app import ComposeResult, App
from textual import log, work
from textual.containers import Vertical
from textual.reactive import reactive
from textual.message import Message
from textual.widgets import (
    Static,
    OptionList,
    TabbedContent,
    TabPane,
    MarkdownViewer,
    ContentSwitcher,
)
from textual.binding import Binding
from textual.widgets.option_list import Option

from tfdocs.models.blocks.provider import Provider
from tfdocs.views.list import List
from tfdocs.views.vertical import Vertical


class Switcher(Vertical, can_focus=True):
    DEFAULT_CSS = """
        Switcher {
            background: $panel;
            border: round $primary;
            width: 100%;
        }

        Switcher:focus-within {
            border: round $accent;
        }

		TabPane {
		    margin: 0;
		    padding: 0 0 !important;
		}

		TabbedContent > ContentSwitcher {
		    width: 100%;
		    height: 1fr;
            scrollbar-size: 1 1;
		}
    """
    BINDINGS = [
        ("h", "cursor_left"),
        ("l", "cursor_right"),
    ]

    provider: reactive[Provider | None] = reactive(
        Provider.from_name("registry.terraform.io/hashicorp/archive")
    )

    def __init__(self, id: str = "switcher", classes: str = ""):
        self.tabs = ["resources", "data", "functions"]
        super().__init__(id=id, classes=classes)

    def watch_provider(self, old, new):
        self.load_resources(new)
        self.load_datasources(new)

    def compose(self) -> ComposeResult:
        functions = [
            Option(f"Function Documentation isn't available yet", id="not-implemented")
        ]
        with TabbedContent():
            with TabPane("resources", id="resources"):
                yield List([], id="resource-list")
            with TabPane("data", id="data"):
                yield List([], id="datasource-list")
            with TabPane("functions", id="functions"):
                yield List(functions, id="list")

    def action_cursor_left(self):
        tabbed_content = self.query_one(TabbedContent)
        n = self.tabs.index(tabbed_content.active)
        tabbed_content.active = self.tabs[n - 1 % tabbed_content.tab_count]
        tabbed_content.active_pane.query_children(".list")[0].focus()

    def action_cursor_right(self):
        tabbed_content = self.query_one(TabbedContent)
        n = self.tabs.index(tabbed_content.active)
        tabbed_content.active = self.tabs[(n + 1) % tabbed_content.tab_count]
        tabbed_content.active_pane.query_children(".list")[0].focus()

    def scroll_to_option(self, name):
        opt = self.get_option(name)
        self.highlighted = opt.index
        self.scroll_to_highlight(top=True)

    def on_focus(self):
        active_pane = self.query_one(TabbedContent).active_pane
        active_pane.query_children(".list")[0].focus()

    @work(thread=True)
    async def load_resources(self, provider: Provider | None):
        if provider is not None:
            resources = [Option(r[1], id=r[0]) for r in provider.list_resources()]
            self.post_message(self.LoadedEntities("Resource", resources))

    @work(thread=True)
    async def load_datasources(self, provider: Provider | None):
        if provider is not None:
            datasources = [Option(d[1], id=d[0]) for d in provider.list_datasources()]
            self.post_message(self.LoadedEntities("DataSource", datasources))

    def on_switcher_loaded_entities(self, msg):
        olist = None
        block_type = msg.block_type
        log(f"Loaded Option Type: {block_type}")
        if block_type == "Resource":
            olist = self.query_one("#resource-list", expect_type=List)
            olist.clear_options()
        elif block_type == "DataSource":
            olist = self.query_one("#datasource-list", expect_type=List)
            olist.clear_options()
        else:
            raise ValueError("Tried to load an unexpected type of option")
        olist.add_options(msg.blocks)
        log("I RAN")

    class LoadedEntities(Message):
        def __init__(self, block_type: str, blocks: list[Option]):
            self.block_type = block_type
            self.blocks = blocks
            super().__init__()
