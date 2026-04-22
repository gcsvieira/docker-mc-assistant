import logging

class AssistantFormatter(logging.Formatter):
    # ANSI escape codes
    PURPLE = "\x1b[35m"
    RESET = "\x1b[0m"
    
    COLORS = {
        logging.DEBUG: "\x1b[34m",    # Blue
        logging.INFO: "\x1b[32m",     # Green
        logging.WARNING: "\x1b[33m",  # Yellow
        logging.ERROR: "\x1b[31m",    # Red
        logging.CRITICAL: "\x1b[1;41m", # Bold White on Red
    }

    def format(self, record):
        log_fmt = f"{self.PURPLE}[%(asctime)s]{self.RESET} [{self.COLORS.get(record.levelno)}%(levelname)s{self.RESET}] %(name)s: %(message)s"
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)

def setup_logging(level=logging.INFO):
    handler = logging.StreamHandler()
    handler.setFormatter(AssistantFormatter())
    logging.basicConfig(level=level, handlers=[handler])
    return logging.getLogger('mc_assistant')
