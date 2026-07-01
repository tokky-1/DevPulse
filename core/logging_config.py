import logging
import sys
from pythonjsonlogger import jsonlogger

def setup_logging():
    handler = logging.StreamHandler(sys.stdout)
    
    format_str = '%(asctime)s %(levelname)s %(name)s %(message)s'
    formatter = jsonlogger.JsonFormatter(format_str, rename_fields={'levelname': 'level', 'asctime': 'timestamp'})
   
    handler.setFormatter(formatter)

    
    root_logger = logging.getLogger()
    root_logger.handlers = []
    root_logger.addHandler(handler)    
    root_logger.setLevel(logging.INFO)
   