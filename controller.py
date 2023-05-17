from model import *
from view import *

class Controller:
    def __init__(self, view, model):
        self.view = view
        self.model = model