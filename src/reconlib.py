import logging
from src.sqllib import SqlLib

class ReconLib:

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.logger = logging.getLogger(__name__)

