from textual.containers import Vertical
from textual.widgets import Static
from textual.widgets.option_list import Option

from tfdocs.views.list import List
from tfdocs.models.blocks.provider import Provider
from tfdocs.models.default_providers import make_none_provider


class ProviderSelectPane(List, can_focus=True):
    def __init__(self):
        providers = Provider.list_providers()
        if len(providers) == 0:
            providers = [make_none_provider()]
        provider_opts = [Option(p.name, id=p.id) for p in providers]
        super().__init__(provider_opts, id="special-pane")
