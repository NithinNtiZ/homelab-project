import logging
from datetime import datetime
import helper 


logger = logging.getLogger(__name__)
# Generate log file name with timestamp
log_filename = datetime.now().strftime("app_%Y-%m-%d_%H-%M-%S.log")

# Handlers
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler(log_filename)

# Formatter
formatter = logging.Formatter('%(asctime)s - %(process)d - %(name)s - %(filename)s - %(funcName)s - %(lineno)d -%(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    handlers=[console_handler, file_handler],
    force=True
)

def main():
    logger.debug('Debug message')
    logger.info('Info message')
    logger.warning('Warning message')
    logger.error('Error message')
    logger.critical('Critical message')

if __name__ == "__main__":
    # Test logs
    main()
    helper.test_logs()

