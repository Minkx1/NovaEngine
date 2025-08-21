# PyGameEngine V1.5.0

**PyGameEngine** — a lightweight Python Framework that simplifies creating 2D games using [Pygame](https://www.pygame.org/).
It provides an engine, scene management, sprite handling, movement systems, and basic UI elements.

## How to Start

### Installation

Clone the repository:

```bash
git clone https://github.com/Minkx1/PyGameEngine.git
```

### Usage Template

```python
""" ===== template.py ===== """

import pygame, math
import PyGameEngine as pge

""" --- 1. Initialize PyGameEngine --- """

# variables and others
SCREEN_W, SCREEN_H = 900, 600 

Engine = pge.PyGameEngine().init(window_size=(SCREEN_W, SCREEN_H))

""" --- 2. Create Scene, Add assets and Initialize function --- """

# Scene1
Scene1 = pge.Scene(Engine)

with Scene1.sprites():
    player = pge.Sprite(
        engine=Engine,img_path="assets/player.png",
        width=120, height=103
    ).place_centered(SCREEN_W/2, SCREEN_H/2)

@Scene1.init_scene()
def scene1():
    pge.fill_background(engine=Engine, color=pge.Colors.WHITE) # fill BackGround with some color or img

    # If you have objects that dont need any logic, you may just dont use set_update. Basic update() is equal to draw()
    @player.set_update 
    def player_update(self):
        
        # Your Logic Here

        self.draw()

    Scene1.update() # SceneX.update() uses update() method on all objects of scene, be carefull

""" --- 3. Initialize Main function with all your project logics --- """

# you can specify your first scene with Engine.set_active_scene(*Scene)

Engine.run(globals()) 
# globals() is for command_input. If you dont wanna use it or if it's not available, you can erase it.

```

## Features

* Simple game loop (`init`, `run`) for your project.
* Scene management: easy creation and switching between scenes.
* Sprite class for all your logic:
* UI elements such as **Button**.
* Utilities:

  * `Colors` enum for predefined colors.
  * `render_text()` for quick text rendering.
  * `fill_background()` for setting background color or image.
  * `Key_Pressed(), Key_Hold() and MouseClicked` for input handler.

* Automatic registration of sprites in a scene using context manager.
* Solid object management for collision detection.
* Extensible architecture for events, timers, and animations.
* Command input for hot debugging.

## License

This library is free to use for personal and commercial projects.