# PyGameEngine

**PyGameEngine** — is a small library, that simplifies creating games using [Pygame](https://www.pygame.org/).  

##  How to Start

### Installing

```bash
git clone https://github.com/yourname/PyGameEngine.git
```

### Usgage template

```python
# template.py
import pygameengine as pge

# Creating Engine
Engine = pge.PyGameEngine()

# Engine Initialization ==> Window 500x500, with caption 'My Name' and icon.
Engine.init(window_size=(500, 500), app_name="My Game", icon_path="icon.png")

run = True
while run:
    # --- your game cod is here ---
    
    # basic game update  
    run = Engine.run()
```

## Features

* Simple game start (`init`, `run`).
* Simple Text Rendering (`RenderText`).
* Simple images creation and control thru class `Asset`.
* Different functions for better QoL .

## Plans

* Scene manager (switch between menu / game / pause).
* FPS-Limiter and FPS display.
* Download resources via ResurceManager.
* Basic classes for **Sprite** and animations.
* Ui-elements system (buttons, input fields).
* Ability to work with timers and events.

## 📝 License

This library is free to use.