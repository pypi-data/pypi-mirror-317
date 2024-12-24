import os
from rich import traceback
from result import Ok, Result
from tfdocs.utils import try_wrap
from tfdocs.logging.setup import setup_logs

traceback.install()

__all__ = ["setup_logs"]
