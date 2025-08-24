# SparkEngine V1.6.0

**SparkEngine** — a lightweight Python Framework that simplifies creating 2D games using [Pygame](https://www.pygame.org/).
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

import pygame
import SparkEngine as SE

""" --- 1. Initialize PyGameEngine and others --- """

SCREEN_W, SCREEN_H = 900, 600 

Engine = SE.SparkEngine(window_size=(SCREEN_W, SCREEN_H))

""" --- 2. Create Scene, Add assets and Initialize function --- """

Scene1 = SE.Scene(Engine)

with Scene1.sprites():
    
    pass 

@Scene1.init_scene()
def scene1():
    SE.fill_background(engine=Engine, color=SE.Colors.WHITE)

    # <-- put here some logic

    Scene1.update()

""" --- 3. Initialize Main function with all your project logics --- """

Engine.run(globals())

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

## Future Plans

* Saves Manager (completed)
* Developer Tools (WorkInProgress)
* Animations and AnimationHandler
* Sprite.look_at, ProgressBar

## License

This library is free to use for personal and commercial projects.