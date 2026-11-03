import logging
import sys

# Setting up basic configuration for logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout) # Logs will be output to the Docker console
    ]
)

logger = logging.getLogger("quiz_app")