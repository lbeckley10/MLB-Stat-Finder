from search import *
from view import *
from model import *
from controller import *


def main(): 
    display = View()
    model = Model()
    controller = Controller(display, model)
    display.setController(controller)
    

if __name__ == "__main__":
    main()
