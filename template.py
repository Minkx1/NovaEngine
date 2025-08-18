""" ===== template.py ===== """

import PyGameEngine as pge

""" --- 1. Initialize PyGameEngine --- """

Engine = pge.PyGameEngine()
Engine.init(
    window_size=(900, 600),
    app_name="Game",
)

""" --- 2. Create Scene, Add assets and Initialize function --- """

Scene1 = pge.Scene(Engine)

with Scene1.sprites():
    button = pge.Button(
        engine=Engine,
        x=250, y=250,
        img_path="assets/button.png",
        width=128, height=128
    ).place_centered(250, 250)

    ground = pge.Sprite(
        engine=Engine,
        img_path='assets/img.png',
        Width=500, Height=50,
        solid=True
    ).place_centered(250, 485)

    player = pge.Player(
        engine=Engine,
        img_path="assets/hero.png",
        x=450, y=100,
        width=50, height=75,
        movement_type=pge.PlatformerMovement()
    ) 

@Scene1.init_scene()
def scene1():
    Engine.screen.fill(pge.Colors.WHITE)

    ground.draw()
    player.update()

    if button.draw():
        print("Button is Pressed!")

""" --- 3. Initialize Main function with all your project logics --- """

@Engine.main()
def main():
    Engine.run_scene(Scene1)

Engine.run()
