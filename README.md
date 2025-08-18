# PyGameEngine V1.4.0

**PyGameEngine** — a lightweight Python library that simplifies creating 2D games using [Pygame](https://www.pygame.org/).
It provides an engine, scene management, sprite handling, movement systems, and basic UI elements.

## How to Start

### Installation

Clone the repository:

```bash
git clone https://github.com/yourname/PyGameEngine.git
```

### Usage Template

```python
# template.py
import pygameengine as pge

# 1. Create Engine
Engine = pge.PyGameEngine()

# 2. Initialize Engine (window size, title, optional icon)
Engine.init(
    window_size=(900, 600),
    app_name="My Game",
    icon_path="assets/icon.png"
)

# 3. Create a Scene
Scene1 = pge.Scene(Engine)

with Scene1.sprites():
    player = pge.Player(
        engine=Engine,
        img_path="assets/hero.png",
        x=450, y=100,
        width=50, height=75,
        movement_type=pge.PlatformerMovement()
    )
    
    ground = pge.Sprite(
        engine=Engine,
        img_path="assets/ground.png",
        Width=500, Height=50,
        solid=True
    ).place_centered(250, 485)

    button = pge.Button(
        engine=Engine,
        img_path="assets/button.png",
        width=128, height=128
    ).place_centered(250, 250)

# 4. Scene update logic
@Scene1.init_scene()
def scene1():
    Engine.screen.fill(pge.Colors.WHITE)
    
    ground.draw()
    player.update()
    
    if button.draw():
        print("Button pressed!")

# 5. Main loop
@Engine.main()
def main():
    Engine.run_scene(Scene1)

# 6. Run the engine
Engine.run()
```

## Features

* Simple game loop (`init`, `run`) for your project.
* Scene management: easy creation and switching between scenes.
* Sprites and Player class with movement systems:

  * **PlatformerMovement**: 2D platformer controls with gravity and jumping.
  * **TopDownMovement**: 4-directional movement for top-down games.
* UI elements such as **Button**.
* Utilities:

  * `Colors` enum for predefined colors.
  * `render_text()` for quick text rendering.
  * `fill_background()` for setting background color or image.
* Automatic registration of sprites in a scene using context manager.
* Solid object management for collision detection.
* Extensible architecture for events, timers, and animations.

## Plans / Upcoming Features

* FPS limiter and FPS display.
* ResourceManager for easy loading of images, sounds, and fonts.
* Enhanced animations system.
* Input fields and more UI elements.
* Multi-player support and custom controls.
* Event callbacks for Player (on\_jump, on\_land, etc.) and Scene (on\_enter, on\_exit).

## License

This library is free to use for personal and commercial projects.