
---

# NovaEngine 

**Версія:** 1.7.0

**Автор:** Minkx1

**Призначення:** Легкий Python фреймворк на базі PyGame для швидкої розробки 2D ігор із сценами, спрайтами, колізіями, таймерами, звуком та інструментами розробника.

---

## Зміст

1. [Особливості](#особливості)
2. [Встановлення](#встановлення)
3. [Швидкий старт](#швидкий-старт)
4. [Система сцен](#система-сцен)
5. [Класи спрайтів](#класи-спрайтів)
6. [Групи спрайтів](#групи-спрайтів)
7. [Інтервали, таймери, кулдауни](#інтервали-таймери-кулдауни)
8. [Менеджер звуку](#менеджер-звуку)
9. [Використання DevTools](#використання-devtools)
10. [Приклад гри](#приклад-гри)

---

## Особливості

* Легке створення гри, спрощення більшості процесів у Pygame з можливістю більш глибокого використання усіх функцій PyGame.
* Просунута Система сцен, корисна як для початківців так і для просунутих розробників.
* Вбудовані класи Sprite та Group для кращої структури проекту, створення об'єктів у сцені та керування ними.
* Додаткові класи та інстурменти для практично будь-яких цілей: SoundManager, SaveManager, GUI та додаткові Sprite-like класи, накшталт Projectile, Dummy та ProgressBar.
* NovaEngine() має великий набір вбудодваних інструментів, що спрощують написання коду: 
    - Main Features: run(), quit(), @new_thread(), @main().
    - Input Management: MouseClicked(), KeyPressed(), KeyHold().
    - Time Managament: Cooldown, Timer, Interval.
    - Scene Management: set_active_scene(), run_scene(), run_active_scene().
    - Utilities: render_text(), fill_background(Color | pygame.Surface)
* DevTools для створення `.exe` та архівів з грою, готових до релізів.
* Додаткова оптимізація.
* Доступ до виконання python-скриптів прямо у терміналі та паралельна обробка.

---

## Встановлення

```bash
pip install pygame
```

* Скопіювати папку NovaEngine з репозиторію у папку вашого проекта.
* Імпортувати як модуль:

```python
import NovaEngine as nova
```

---

## Швидкий старт

Почати розробку гри можна декількома способами, в залежності від розміру проекту.

Ось один варіант. Тут Eninge.run() автоматично малює білий екран та запускає основну функцію(за замовченням - update() всіх об'єктів сцени) першої оголошеної сцени :

```python
import pygame
import NovaEngine as nova

""" --- 1. Initialize PyGameEngine and others --- """

Engine = nova.NovaEngine(window_size=(900, 600))

""" --- 2. Create Scene, Add assets and Initialize function --- """

Scene1 = nova.Scene(Engine) 

with Scene1.sprites(): # initilizes all sprites you wanna see in one specific scene. Also if not specified, scene's main function just updates all scene's sprites
    text = nova.TextLabel(Engine, 450, 300, "Hello NovaEngine!", size=40, center=True)
    # Creates text on the screen

""" --- 3. Initialize Main function with all your project logics --- """

Engine.run() # input scene you wanna see first, if not inputed - you will see first scene that you have initialized
```

Інший варіант. Тут сцени не оголошені, тому Enigne.run() шукає власну main функцію, яка оголошується @Engine.main():

```python
import pygame 
import NovaEngine as nova

Engine = nova.NovaEngine(window_size=(900, 600)).set_debug(True)

@Engine.main()
def game_loop():
    Engine.fill_background(nova.Colors.WHITE)
    Engine.render_text("Hello NovaEngine!", 450, 300, size=40, center=True)

Engine.run() 
```

---

## Система сцен

**Scene** — основний клас для організації об’єктів:

* `add_sprite()` — ручне додавання спрайтів.
* Контекстний менеджер `with Scene.sprites():` автоматично реєструє створені об’єкти.
* `Scene.function()` — декоратор для встановлення основної функції сцени(за замовченням - апедейт всіх об'єктів), яка буде викликана NovaEngine.run().
* `update()` — оновлення всіх спрайтів сцени.

Перемикання сцен:

```python
Engine.set_active_scene(Main)
Engine.run_active_scene()
```

---

## Класи спрайтів

**Sprite**

* `Sprite(engine, img_path, width=None, height=None, solid=False)` — створення спрайта.
* Методи:

| Метод                                               | Опис                                        |
| --------------------------------------------------- | ------------------------------------------- |
| `draw()`                                            | Малює спрайт на екрані                      |
| `set_update()`                                      | Декоратор для кастомного оновлення          |
| `set_position(x, y)`                                | Задати координати                           |
| `place_centered(x, y)`                              | Центрувати спрайт                           |
| `move(dx, dy)`                                      | Рух на відстань                             |
| `move_to(target, speed)`                            | Рух до точки або іншого спрайта             |
| `scale(width, height)`                              | Масштабування                               |
| `rotate(angle)`                                     | Обертання                                   |
| `look_at(target)`                                   | Повернутися до цілі                         |
| `collide(other/rect)`                               | Колізія                                     |
| `kill()`                                            | Вбити спрайт                                |
| `update()`                                          | Виконати кастомну логіку або draw           |
| `set_animation(name, frames, speed=0.1, loop=True)` | Додати анімацію                             |
| `play_animation(name=None)`                         | Відтворити анімацію                         |
| `CreateImage(path, width=None, height=None)`        | Статичний метод для завантаження зображення |

**Button(Sprite)**

* `check()` — повертає `True`, якщо кнопка натиснута.

**ProgressBar(Sprite)**

* `set_value(value)` — задати значення
* `add_value(delta)` — змінити значення
* `draw()` — малює прогрес-бар

---

## Групи спрайтів

**Group** — контейнер для декількох спрайтів:

```python
bullets = nova.Group()
bullets.add(bullet1, bullet2)
bullets.update()
colliding = bullets.collide(player)  # список спрайтів, що колізуються
```

---

## Інтервали, таймери, кулдауни

**Таймер:** виконує функцію через `duration` секунд

```python
@Engine.Timer(2)
def say_hi():
    print("Hello after 2 seconds")
```

**Кулдаун:** перевірка чи кулдаун пройшов або початок кулдауна

```python
if Engine.Cooldown('shoot', 0.5):
    shoot()
```

**Інтервал:** повторення N разів з паузою

```python
@Engine.Interval(5, 1)  # 5 разів з інтервалом 1 сек
def spawn_enemy():
    print("Enemy!")
```

---

## Менеджер звуку

```python
from sound import SoundManager

sound = SoundManager()
sound.load_sound("shot", "assets/shot.wav")
sound.play_sound("shot", volume=0.5)

sound.play_music("assets/bg_music.mp3", volume=0.8)
sound.pause_music()
sound.continue_music()
sound.stop_music()
sound.stop_all()
```

---

## Використання DevTools

**Створення `.exe`:**

```python
nova.DevTools.build_exe(main_file="main.py", name="MyGame", noconsole=True)
```

**Створення архіву:**

```python
nova.DevTools.build_archive(
    main_file="main.py",
    name="MyGame",
    sprite_dir="assets",
    archive_dist="releases"
)
```

---

## Приклад гри з декількома сценами

```python
import pygame, NovaEngine as nova

SCREEN_W, SCREEN_H = 900, 600

Engine = nova.NovaEngine(window_size=(SCREEN_W, SCREEN_H))

Main = nova.Scene(Engine)
Menu = nova.Scene(Engine)

# Initializing sprites in Main scene
with Main.sprites():
    player = nova.Sprite(Engine, "assets/player.png", 100, 100) #creating player
    player.place_centered(SCREEN_W/2, SCREEN_H/2) # placing player center in coordinates
    
    @player.set_update() # what will be happening when called player.update()
    def player_update(): # function to be called - can be named absolutelly as you wish
        
        player.draw() # MUST be in almost every .update()
        player.look_at(pygame.mouse.get_pos()) # makes sprite look at target, that can be point (x, y) or other Sprite object.
        if Engine.MouseClicked(): 
            # When mouse is clicked - moves player in direction he is looking with speed 50.
            player.move_angle(50) 

with Menu.sprites():
    menu_text = nova.TextLabel(Engine, SCREEN_W/2, SCREEN_H/2-100, "M E N U", size=32, center=True)
    hint = nova.TextLabel(Engine, SCREEN_W/2, SCREEN_H/2, "Press M for game", size=16, center=True)

@Menu.function() #Sets main function for Menu
def _():
    Menu.update() 
    if Engine.KeyPressed(pygame.K_m): Engine.set_active_scene(Main) # if M is pressed, active_scene is set to Main, so Engine will render Main scene.

Engine.run(Menu) # Menu is the first scene to see.
```

NovaEngine має практично усі інструменти, що можуть знадобитися розробнику ігор через Pygame.

--- 
