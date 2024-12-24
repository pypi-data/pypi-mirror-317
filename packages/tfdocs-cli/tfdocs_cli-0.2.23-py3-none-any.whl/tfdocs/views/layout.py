"""
    This component is used to format and organise the panes that make up the app.
    It is reponsible for ensuring that at whatever screen-size the UI is legible
    and the UX is pleasant.
"""

import logging
from textual import on
from textual.app import ComposeResult
from textual.widgets import Static, OptionList
from textual.reactive import reactive
from textual.containers import Horizontal, Vertical
from textual.binding import Binding

from tfdocs.models.block import Block
from tfdocs.models.blocks.provider import Provider
from tfdocs.models.default_providers import make_welcome_block, make_none_provider
from tfdocs.views.viewer import Viewer
from tfdocs.views.switcher import Switcher
from tfdocs.views.special import Special


log = logging.getLogger()
THIN_WIDTH = 90
SHORT_HEIGHT = 40


class PaneLayout(Static):
    DEFAULT_CSS = """
        .pane {
            width: 1fr;
        }

        RightPanel.thin-layout {
            max-width: 100 !important;
        }

        RightPanel {
            max-width: 50;
        }

        .focussed {
            display: block !important;
        }

        .thin-layout {
            display: none;
        }
    """

    BINDINGS = [
        Binding("tab", "cycle_focus_forward", priority=True),
        Binding("shift+tab", "cycle_focus_back", priority=True),
    ]

    provider: reactive[Provider | None] = reactive(
        # load the 'welcome' provider by default
        make_none_provider()
    )

    open_document: reactive[str | None] = reactive(make_welcome_block().document)

    def __init__(self, open_to: Block | None = None):
        self.open_to = open_to
        super().__init__()

    def compose(self) -> ComposeResult:
        with Horizontal(id="app-grid"):
            yield Viewer(classes="pane focussed").data_bind(PaneLayout.open_document)
            yield RightPanel(classes="").data_bind(PaneLayout.provider)

    @on(OptionList.OptionSelected)
    def handle_select(self, message: OptionList.OptionSelected):
        provider = Provider.from_name(str(message.option.prompt))
        if self.size.width < THIN_WIDTH:
            self.cycle_focus(forward=True)
        if provider is not None:
            self.provider = provider
            self.mutate_reactive(PaneLayout.provider)
        new_block = Block.from_id(str(message.option.id))
        if new_block is not None:
            self.open_document = new_block.document
            self.mutate_reactive(PaneLayout.open_document)
            log.debug(f"Mutating: {self.provider} {self.open_document}")
        else:
            log.warn("Couldn't load the new document page")

    def on_mount(self):
        if self.open_to is not None:
            self.provider = self.open_to
            self.open_document = self.open_to.document
            self.mutate_reactive(PaneLayout.provider)
            self.mutate_reactive(PaneLayout.open_document)
        viewer = self.query_one(Viewer)
        viewer.focus()
        log.debug(f"Viewer Styles: {viewer.styles}")

    async def action_cycle_focus_forward(self):
        self.cycle_focus(forward=True)

    async def action_cycle_focus_back(self):
        self.cycle_focus(forward=False)

    def cycle_focus(self, forward=True):
        """
        Cycles the focus of the application, or resets it onto the first pane
        """
        res = self.query(".pane")
        # get all panes in the layout
        try:
            focussed_index, child = next(
                (
                    (i, child)
                    for i, child in enumerate(res)
                    if child.has_focus or child.has_focus_within
                )
            )
            child.remove_class("focussed")
            # move to next pane
            new_focussed_index = focussed_index + (1 if forward else -1)
            # loop round the panes
            new_focussed_index %= len(res)
            if new_focussed_index not in [1, 2]:
                self.query_one(RightPanel).remove_class("focussed")
            else:
                self.query_one(RightPanel).add_class("focussed")

            log.debug(
                f"""
            prev focus:
             - type       = {child}
             - classes    = {child.classes if child != None else None}
             - visibility = {child.visible}
            """
            )
        except StopIteration:
            # none of the panes are focussed, focus the first one
            new_focussed_index = 0

        new_focus_pane = res[new_focussed_index]
        new_focus_pane.focus()
        new_focus_pane.add_class("focussed")
        log.debug(
            f"""
            new focus classes: 
             - type       = {new_focus_pane}
             - classes    = {new_focus_pane.classes}
             - visibility = {new_focus_pane.visible}
             - can_focus  = {new_focus_pane.can_focus}
        """
        )

        log.debug(f"focussed: {res[new_focussed_index]}")

    def on_resize(self):
        if self.size.width < THIN_WIDTH:
            log.debug("The Window is small, switching to thin-layout")
            self.query_one(Viewer).add_class("thin-layout")
            self.query_one(RightPanel).add_class("thin-layout")
        else:
            self.query_one(Viewer).remove_class("thin-layout")
            self.query_one(RightPanel).remove_class("thin-layout")


class RightPanel(Static):
    DEFAULT_CSS = """
        RightPanel {
            width: 1fr;
            layers: below above;
        }

        #switcher {
            height: 2fr;
            &.short-layout {
                display: block;
                layer: below;
            }
        }

        #special {
            height: 1fr;
            &.short-layout {
                layer: above;
            }
        }

        .short-layout {
            display: none;
        }

    """
    provider: reactive[Provider | None] = reactive(
        Provider.from_name("registry.terraform.io/hashicorp/archive")
    )

    def compose(self):
        with Vertical():
            yield Special(classes="pane")
            yield Switcher(classes="pane").data_bind(RightPanel.provider)

    def on_resize(self):
        if self.size.height < SHORT_HEIGHT:
            log.debug("The Window is short, switching to short-layout")
            self.query_one(Special).add_class("short-layout")
            self.query_one(Switcher).add_class("short-layout")
        else:
            self.query_one(Special).remove_class("short-layout")
            self.query_one(Switcher).remove_class("short-layout")
        if self.size.width >= THIN_WIDTH:
            self.query_one(Vertical).add_class("wide")
        else:
            self.query_one(Vertical).remove_class("wide")

    def on_blur(self):
        # if using short layout and not thin-layout
        if self.size.height < SHORT_HEIGHT and self.size.width > THIN_WIDTH:
            # whenever the element loses focus, add display persistence for most
            # recently focussed pane
            try:
                focussed_pane = next(
                    (
                        child
                        for child in self.query(".pane")
                        if "focussed" in child.classes
                    )
                )
                focussed_pane.add_class("leave-visible")
            except StopIteration:
                focussed_pane = self.query_one(Switcher).add_class("leave-visible")
