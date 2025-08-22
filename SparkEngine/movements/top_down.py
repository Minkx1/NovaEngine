import pygame,math

class TopDownMovement:
    """
    Class for top-down character movement:
    - Movement in 4 directions
    - Collision detection with solid objects
    - Screen boundaries
    """

    def __init__(self, speed=5):
        self.speed = speed
        self.engine = None
        self.rect = None
        self.solids = []

    def update(self, engine, solids, sprite):
        """Updates movement and collisions."""
        self.engine = engine
        self.solids = solids
        self.sprite = sprite
        self.rect = self.sprite.rect
        self.keys = self.engine.keys_pressed

        dx, dy = self._handle_input(self.keys)
        self._move(dx, dy)
        self._stay_in_bounds()
        return self

    def _handle_input(self, keys):
        """Returns movement direction (dx, dy)."""
        dx, dy = 0, 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx = -self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx = self.speed
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy = -self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy = self.speed
        return dx, dy

    def _move(self, dx, dy):
        """Moves and resolves collisions."""
        # Horizontal movement
        self.rect.x += dx
        self._resolve_collisions(dx, 0)

        # Vertical movement
        self.rect.y += dy
        self._resolve_collisions(0, dy)

    def _resolve_collisions(self, dx, dy):
        """Checks collisions along X or Y and stops movement."""
        for sprite in self.solids:
            if not sprite.solid:
                continue
            if self.rect.colliderect(sprite.rect):
                if dx > 0:   # moving right
                    self.rect.right = sprite.rect.left
                elif dx < 0:  # moving left
                    self.rect.left = sprite.rect.right
                if dy > 0:   # moving down
                    self.rect.bottom = sprite.rect.top
                elif dy < 0:  # moving up
                    self.rect.top = sprite.rect.bottom

    def _stay_in_bounds(self):
        """Keeps player inside screen boundaries."""
        screen_w, screen_h = self.engine.screen.get_size()

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_w:
            self.rect.right = screen_w
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_h:
            self.rect.bottom = screen_h

""" Your Classes that use TopDown can be built here """

class ZombieKillerMovement(TopDownMovement):
    def __init__(self, speed=5):
        super().__init__(speed)
    
    def update(self, engine, solids, rect):
        super().update(engine, solids, rect)

        mouse_x,mouse_y = pygame.mouse.get_pos()
        px,py = self.rect.center[0], self.rect.center[1]
        
        mouse_angle_rad = math.atan2(mouse_y - py, mouse_x - px)
        angle_to_mouse = math.degrees(mouse_angle_rad)
        self.sprite.rotate(angle_to_mouse)