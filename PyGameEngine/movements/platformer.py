import pygame


class PlatformerMovement:
    """
    Class for 2D platformer movement:
    - Move left/right
    - Jump with gravity
    - Collisions with solid objects
    """

    def __init__(self, speed=5, gravity=0.8, jump_force=12):
        self.gravity = gravity
        self.jump_force = -jump_force
        self.speed = speed

        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False

        self.engine = None
        self.rect = None
        self.solids = []

    def update(self, engine, keys, solids, rect):
        """
        Updates object movement and position.
        """
        self.engine = engine
        self.solids = solids
        self.rect = rect

        self._handle_input(keys)
        self._apply_gravity()
        self._move()
        self._stay_in_bounds()

    def _handle_input(self, keys):
        """Handles keyboard input."""
        self.vel_x = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vel_x = -self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vel_x = self.speed

        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
            self.vel_y = self.jump_force
            self.on_ground = False

    def _apply_gravity(self):
        """Applies gravity to vertical velocity."""
        self.vel_y += self.gravity

    def _move(self):
        """Updates position and checks collisions."""
        # Horizontal movement
        self.rect.x += self.vel_x
        self._resolve_collisions(dx=self.vel_x, dy=0)

        # Vertical movement
        self.rect.y += self.vel_y
        self.on_ground = False
        self._resolve_collisions(dx=0, dy=self.vel_y)

    def _stay_in_bounds(self):
        """Keeps player inside screen boundaries."""
        screen_w, screen_h = self.engine.screen.get_size()
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_w:
            self.rect.right = screen_w
        if self.rect.bottom > screen_h:  # If falling below screen
            self.rect.bottom = screen_h
            self.vel_y = 0
            self.on_ground = True

    def _resolve_collisions(self, dx, dy):
        """Resolves collisions with solid objects."""
        for sprite in self.solids:
            if not sprite.solid:
                continue
            if self.rect.colliderect(sprite.rect):
                if dx > 0:  # moving right
                    self.rect.right = sprite.rect.left
                elif dx < 0:  # moving left
                    self.rect.left = sprite.rect.right
                if dy > 0:  # falling
                    self.rect.bottom = sprite.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif dy < 0:  # jumping upward
                    self.rect.top = sprite.rect.bottom
                    self.vel_y = 0
