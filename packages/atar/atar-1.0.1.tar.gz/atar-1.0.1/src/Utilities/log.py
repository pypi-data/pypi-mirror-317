import logging

# Define custom color codes
class Colors:
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'


# Custom log formatter with colors
class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': Colors.BLUE,
        'INFO': Colors.GREEN,
        'WARNING': Colors.YELLOW,
        'ERROR': Colors.RED,
        'CRITICAL': Colors.PURPLE,
    }

    def format(self, record):
        log_message = super().format(record)
        color = self.COLORS.get(record.levelname, Colors.RESET)
        return f"{color}{log_message}{Colors.RESET}"


# Create and configure the logger
logger = logging.getLogger("ATAR")
logger.setLevel(logging.DEBUG)  # Adjust logging level as needed

# Create a stream handler with the custom formatter
handler = logging.StreamHandler()
formatter = ColoredFormatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Avoid duplicate logs if the logger is already configured
if not logger.hasHandlers():
    logger.addHandler(handler)

# Disable propagation to prevent duplicate logs in some setups
logger.propagate = False
