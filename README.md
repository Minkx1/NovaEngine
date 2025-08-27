
---

# NovaEngine 

**Версія:** 1.6.4

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

* Простий цикл ігор з PyGame, FPS та рендеринг тексту.
* Система сцен із контекстним менеджером для автоматичної реєстрації спрайтів.
* Класи спрайтів з рухом, обертанням, анімаціями та колізіями.
* Групи спрайтів для масових операцій (draw, update, move, kill).
* Кнопки, прогрес-бари, HUD.
* Таймери, кулдауни та інтервали із підтримкою багатопоточності.
* Легке підключення звуку та музики.
* DevTools для створення `.exe` та архівів з грою.
* Кешування тексту для швидкого рендерингу.
* Простий CLI для виконання команд на фоні (`exec`).

---

## Встановлення

```bash
pip install pygame
```

* Скопіювати папку NovaEngine з репозиторію у папку вашого проекта.
* Імпортувати як модуль:

```python
import NovaEngine as SE
```

---

## Швидкий старт

```python
import pygame 
import NovaEngine as nova

Engine = nova.NovaEngine(window_size=(800, 600))
Engine.set_debug(True)

@Engine.main()
def game_loop():
    Engine.fill_background(nova.Colors.WHITE)
    Engine.render_text("Hello NovaEngine!", 400, 300, size=40, center=True)

Engine.run()
```

---

## Система сцен

**Scene** — основний клас для організації об’єктів:

```python
Main = nova.Scene(Engine)

with Main.init():
    player = nova.Sprite(Engine, "player.png", 50, 50).place_centered(400, 300)

@Main.logic()
def scene_logic():
    Engine.fill_background(nova.Colors.BLACK)
    Main.update()  # викликає update() для всіх об’єктів
```

* `add_sprite()` — ручне додавання спрайтів.
* Контекстний менеджер `with Scene.init():` автоматично реєструє створені об’єкти.
* `Scene.logic()` — декоратор для основної логіки сцени.
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

**Кулдаун:** перевірка або створення

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

## Приклад гри

```python
Engine = nova.NovaEngine(window_size=(900, 600))
Main = nova.Scene(Engine)

with Main.init():
    player = nova.Sprite(Engine, "player.png", 100, 100).place_centered(450, 300)

@Main.logic()
def logic():
    Engine.fill_background(nova.Colors.WHITE)
    Main.update()

Engine.set_active_scene(Main)
Engine.run()
```

Тут можна додавати групи ворогів, кулі, інтервали для спавну, прогрес-бари HP, кнопки меню та ін.

--- 
