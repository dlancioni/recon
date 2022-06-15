import logging

class EtlLib:

    def __init__(self):       
        self.logger = logging.getLogger(__name__)
    
    def import_file(self):
        self.logger.error("Hello from EtlLib")
