from textual.widgets import OptionList


class List(OptionList, can_focus=True):
    DEFAULT_CSS = """
        List {
            background: transparent;
            padding: 0 2;
            margin: 0;
            scrollbar-size: 1 1;
            border: none;
        }

        List:focus {
            border: none;
        }

		.option-list--option-highlighted {
			background: $accent !important;
		}
    """
    BINDINGS = [
        ("j", "cursor_down"),
        ("k", "cursor_up"),
        ("h", "cursor_left"),
        ("l", "cursor_right"),
        ("u", "page_up"),
        ("d", "page_down"),
    ]

    def __init__(self, resources, id=None):
        classes = "list"
        if id != None:
            super().__init__(*resources, id=id, classes=classes)
        else:
            super().__init__(*resources, classes=classes)
