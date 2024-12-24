from textwrap import dedent
from tfdocs.models.blocks.provider import Provider
from tfdocs.models.block import Block


def make_none_provider() -> Provider:
    return Provider(
        type="Provider",
        hash="none",
        name="none",
    )


def make_welcome_block() -> Block:
    return Block(
        document=dedent(
            """
        ```
          ________________
         /_  __/ ____/ __ \\____  __________
          / / / /_  / / / / __ \\/ ___/ ___/
         / / / __/ / /_/ / /_/ / /__(__  )
        /_/ /_/   /_____/\\____/\\___/____/beta
        ```
         > **Terraform Documentation Viewer**
        ## Navigating the UI
        ### Shifting Focus
        ```
        ╭─────────┬─────╮  ╭─────────┬─────╮
        │         │     │  │         │     │
        │  ╭──────┼→─╮  │  │  ╭─←────┼──╮  │
        │  ↑      │  │  │  │  │      │  ↑  │
        │  │      ├──┼──┤  │  │      ├──┼──┤
        │  │      │  ↓  │  │  ↓      │  │  │
        │  ╰─←────┼──╯  │  │  ╰──────┼→─╯  │
        │         │     │  │         │     │
        ╰─────────┴─────╯  ╰─────────┴─────╯
               TAB            SHIFT + TAB
        ```
        Press TAB to cycle your focus CLOCKWISE. Press SHIFT + TAB to cycle your focus COUNTERCLOCKWISE

        ### Moving in menus
        ```txt
                  UP, k
                    ↑
                    │
        LEFT, h ←───┼───→ RIGHT, l
                    │
                    ↓
                 DOWN, j
        ```
        Use [h, j, k, l] or THE ARROW KEYS to move about in focussed panes or menus

        > TIP
        >
        > You can also use your mouse if you prefer! Most modern terminals support mouse interactions; click to change focus or tab, select options, and you can even scroll.
    """
        )
    )
