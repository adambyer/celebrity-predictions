from dotenv import load_dotenv

load_dotenv()

# This has to be imported after `load_dotenv`.
from . import events  # noqa: F401, E402
