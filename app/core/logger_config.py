import logging
import os

# 🔁 Smart: Use /tmp only in Lambda, otherwise use local 'logs' folder
if os.getenv("AWS_LAMBDA_FUNCTION_NAME"):  # Detect if running in Lambda
    LOG_DIR = os.path.join("/tmp", "logs")
else:
    LOG_DIR = os.path.join(os.getcwd(), "logs")  # Local project folder

os.makedirs(LOG_DIR, exist_ok=True)

INFO_LOG_FILE = os.path.join(LOG_DIR, "info.log")
ERROR_LOG_FILE = os.path.join(LOG_DIR, "error.log")


def configure_logger(name: str = "justplay"):
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger  # avoid duplicate handlers

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # 🟡 Optional: File logging (safe in both environments)
    try:
        # Info handler (INFO, WARNING)
        info_handler = logging.FileHandler(INFO_LOG_FILE)
        info_handler.setLevel(logging.INFO)
        info_handler.setFormatter(formatter)
        info_handler.addFilter(lambda record: record.levelno < logging.ERROR)
        logger.addHandler(info_handler)

        # Error handler (ERROR, CRITICAL)
        error_handler = logging.FileHandler(ERROR_LOG_FILE)
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        logger.addHandler(error_handler)
    except Exception as e:
        print(f"Warning: Could not set up file logging: {e}")

    # ✅ Console handler (goes to terminal or CloudWatch)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # ✅ This will appear in terminal (local) or CloudWatch (Lambda)
    logger.info(f"Logger initialized. Writing logs to:")
    logger.info(f"  Info log: {INFO_LOG_FILE}")
    logger.info(f"  Error log: {ERROR_LOG_FILE}")

    return logger