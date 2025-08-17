"""    ===== template.py =====    """

import pygameengine as pge

Engine = pge.PyGameEngine()
Engine.init(app_name="Testik") 

player = pge.Player(
    engine=Engine,
    img_path='img.png',
    x=200, y=200,
    width=50, height=50,
    movement_type="platformer"
).place_centered(250, 250)

ground = pge.Asset(
    engine=Engine,
    img_path='img.png',
    Width=500, Height=50,
    solid=True
).place_centered(250, 485)

run = True
while run:
    run = Engine.run()

    # --- your game cod is here ---
    Engine.screen.fill(pge.BLACK)

    ground.draw()
    player.update()
