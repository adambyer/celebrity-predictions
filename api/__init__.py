from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()

# This has to be imported after `load_dotenv`.
from . import events  # noqa: F401, E402
