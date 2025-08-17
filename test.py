"""    ===== template.py =====    """

import pygameengine as pge

# SCREEN_WIDTH = 700
# SCREEN_HEIGHT = 450
# APPLICATION_NAME = "PGE Test"

Engine = pge.PyGameEngine()

# Engine.init(window_size = (SCREEN_WIDTH, SCREEN_HEIGHT), app_name = APPLICATION_NAME)
Engine.init()

run = True
while run:
    
    # your code

    run = Engine.run()