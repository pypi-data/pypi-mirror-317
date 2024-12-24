import logging
from textwrap import dedent
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Static, MarkdownViewer, Markdown
from textual.binding import Binding
from textual.reactive import reactive
from textual.widget import Widget

from tfdocs.models.block import Block
from tfdocs.models.default_providers import make_welcome_block

log = logging.getLogger()


class Viewer(Widget, can_focus=True, can_focus_children=True):
    CSS_PATH = "styles/viewer.tcss"
    DEFAULT_CSS = """
        Viewer {
            width: 100%;
            background: $panel;
            border: round $primary;
            row-span: 3;
            scrollbar-size: 1 1;
        }

        Viewer > * {
            scrollbar-size-vertical: 1;
        }

        Viewer:focus-within {
            border: round $accent;
        }
    """
    BINDINGS = [
        Binding("j", "scroll_down", "Scroll Down", show=False),
        Binding("k", "scroll_up", "Scroll Up", show=False),
    ]

    open_document: reactive[str | None] = reactive(
        make_welcome_block().document, recompose=True
    )

    @property
    def has_focus_within(self):
        """Are any descendants focused?"""
        try:
            focused = self.screen.focused
        except Exception as e:
            log.debug(e)
            return False
        node = focused
        while node is not None:
            if node is self:
                return True
            node = node._parent
        return False

    def __init__(self, id: str = "viewer", classes: str = ""):
        super().__init__(id=id, classes=classes)

    def compose(self):
        yield MarkdownViewer(markdown=self.open_document, show_table_of_contents=False)

    def on_focus(self):
        self.query_one(MarkdownViewer).focus()

    def action_scroll_up(self):
        self.query_one(MarkdownViewer).action_scroll_up()

    def action_scroll_down(self):
        self.query_one(MarkdownViewer).action_scroll_down()

    # async def on_mount(self):
    #     await self.update(dedent(LOREM_IPSUM))

    # async def update(self, text: str):
    #     md = self.query_one(Markdown)
    #     md.update(text)


LOREM_IPSUM = """
    # Heading 1: Lorem Ipsum

    ## Heading 2: Dolor Sit Amet

    ### Heading 3: Consectetur Adipiscing

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer nec odio. Praesent libero. Sed cursus ante dapibus diam.

    #### Heading 4: Nulla Quis Sem

    1. **Item 1**: Lorem ipsum dolor sit amet, consectetur adipiscing elit.
    2. **Item 2**: Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
        - Subitem 1: Ut enim ad minim veniam.
        - Subitem 2: Quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
    3. **Item 3**: Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.

    ##### Heading 5: Class Aptent Taciti

    - *Bullet 1*: Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium.
    - *Bullet 2*: Totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.

    ###### Heading 6: Ut Wisi Enim

    ```python
    # Example of a Python code block
    def lorem_ipsum(dolor, sit):
        return f"Lorem {dolor} sit {sit} amet."

    result = lorem_ipsum("ipsum", "amet")
    print(result)
    ```

    **Bold text:** Lorem ipsum dolor sit amet.

    *Italic text:* consectetur adipiscing elit.

    ~~Strikethrough text:~~ Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.

    ### Horizontal Rule

    ---

    ### Inline Code

    To run the program, use `python script.py`.

    ### Image Example

    ![Placeholder Image](https://via.placeholder.com/150)

    ### Link Example

    [Visit Lorem Ipsum](https://www.lipsum.com/)

    ### Another Code Block Example

    ```json
    {
        "lorem": "ipsum",
        "dolor": "sit",
        "amet": "consectetur"
    }
"""
