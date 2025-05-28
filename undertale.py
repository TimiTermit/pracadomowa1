import pygame
import sys
import random

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (240, 20, 20)
BLUE = (20, 70, 255)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
LIGHT_GRAY = (220, 220, 220)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Undertale Boss Fight - Pygame Tribute")
clock = pygame.time.Clock()
font_small = pygame.font.SysFont('Arial', 24)
font_large = pygame.font.SysFont('Arial', 48)

# Player "Soul" class
class PlayerSoul:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH//2 - 15, HEIGHT - 100, 30, 30)
        self.color = RED
        self.speed = 5
        self.health = 40
        self.max_health = 40
        self.invulnerable = 0  # frames of invulnerability after hit

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        # Clamp inside screen bounds
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(WIDTH, self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(HEIGHT, self.rect.bottom)

    def draw(self, surface):
        if self.invulnerable % 10 < 5:
            pygame.draw.rect(surface, self.color, self.rect)
        # else invisible frame for flicker effect

    def update(self):
        if self.invulnerable > 0:
            self.invulnerable -= 1

    def hit(self, damage):
        if self.invulnerable == 0:
            self.health -= damage
            self.invulnerable = 60  # 1 second invulnerability


# Base Attack class
class Attack:
    def __init__(self):
        self.finished = False

    def update(self):
        pass

    def draw(self, surface):
        pass

    def check_collision(self, player):
        pass


class BoneAttack(Attack):
    # Bones fall vertically or move horizontally depending on type
    def __init__(self, x, y, direction='down', speed=4, horizontal=False):
        super().__init__()
        self.horizontal = horizontal
        if self.horizontal:
            self.rect = pygame.Rect(x, y, 20, 10)
            self.speed = speed
            self.direction = direction  # 'left' or 'right'
        else:
            self.rect = pygame.Rect(x, y, 10, 20)
            self.speed = speed
            self.direction = direction  # 'down' or 'up'

    def update(self):
        if self.horizontal:
            if self.direction == 'left':
                self.rect.x -= self.speed
            else:
                self.rect.x += self.speed
            if self.rect.right < 0 or self.rect.left > WIDTH:
                self.finished = True
        else:
            if self.direction == 'down':
                self.rect.y += self.speed
            else:
                self.rect.y -= self.speed
            if self.rect.top > HEIGHT or self.rect.bottom < 0:
                self.finished = True

    def draw(self, surface):
        pygame.draw.rect(surface, CYAN, self.rect)
        # draw a smaller inner bone decoration
        inner = self.rect.inflate(-8, -8)
        pygame.draw.rect(surface, WHITE, inner)

    def check_collision(self, player):
        return self.rect.colliderect(player.rect)


class BlasterAttack(Attack):
    def __init__(self, x, y, direction='right'):
        super().__init__()
        self.rect = pygame.Rect(x, y, 40, 40)
        self.direction = direction
        self.animation_frame = 0
        self.active = True
        self.damage = 2
        self.duration = 90  # frames blast lasts

    def update(self):
        self.animation_frame += 1
        if self.animation_frame >= self.duration:
            self.finished = True

    def draw(self, surface):
        # draw a cyan circle that pulses
        radius = 20 + 5 * (self.animation_frame % 30) // 30
        pygame.draw.circle(surface, CYAN, self.rect.center, radius, 3)

    def check_collision(self, player):
        if self.rect.colliderect(player.rect) and self.active:
            return True
        return False


class SpearAttack(Attack):
    # Spear starts off screen and moves towards player Y pos, then continues horizontally
    def __init__(self, start_x, start_y, target_y, speed=7, direction='left', delay=0):
        super().__init__()
        self.rect = pygame.Rect(start_x, start_y, 60, 10)
        self.speed = speed
        self.direction = direction
        self.delay = delay  # frames to wait before starting
        self.started = False
        self.target_y = target_y
        self.phase = 0  # 0: waiting, 1: move vertically to target_y, 2: horizontal attack
        self.damage = 3

    def update(self):
        if self.delay > 0:
            self.delay -= 1
            return
        if self.phase == 0:
            # move spear vertically to target_y
            dy = self.target_y - self.rect.y
            if abs(dy) < 5:
                self.phase = 1
            else:
                self.rect.y += 5 if dy > 0 else -5
        elif self.phase == 1:
            # move spear horizontally off screen
            if self.direction == 'left':
                self.rect.x -= self.speed
                if self.rect.right < 0:
                    self.finished = True
            else:
                self.rect.x += self.speed
                if self.rect.left > WIDTH:
                    self.finished = True

    def draw(self, surface):
        pygame.draw.rect(surface, ORANGE, self.rect)
        # add spear tip:
        if self.direction == 'left':
            tip_points = [(self.rect.left, self.rect.centery),
                          (self.rect.left + 10, self.rect.top),
                          (self.rect.left + 10, self.rect.bottom)]
        else:
            tip_points = [(self.rect.right, self.rect.centery),
                          (self.rect.right - 10, self.rect.top),
                          (self.rect.right - 10, self.rect.bottom)]
        pygame.draw.polygon(surface, YELLOW, tip_points)

    def check_collision(self, player):
        return self.rect.colliderect(player.rect)

# Boss base class
class Boss:
    def __init__(self, name):
        self.name = name
        self.max_health = 100
        self.health = self.max_health
        self.attack_timer = 0
        self.attack_cooldown = 90  # frames between attacks
        self.attacks = []
        self.phase = 1

    def update(self, player):
        # Update attacks
        for attack in self.attacks:
            attack.update()
        self.attacks = [atk for atk in self.attacks if not atk.finished]

        # Attack timer counts down
        if self.attack_timer > 0:
            self.attack_timer -= 1
        else:
            self.perform_attack(player)
            self.attack_timer = self.attack_cooldown

    def perform_attack(self, player):
        # To be implemented by subclasses
        pass

    def draw(self, surface):
        # Draw boss health bar
        bar_width = 300
        bar_height = 25
        bar_x = WIDTH//2 - bar_width//2
        bar_y = 30

        pygame.draw.rect(surface, LIGHT_GRAY, (bar_x, bar_y, bar_width, bar_height))
        health_width = int(bar_width * self.health / self.max_health)
        pygame.draw.rect(surface, RED, (bar_x, bar_y, health_width, bar_height))

        # Draw boss name
        name_text = font_large.render(self.name, True, WHITE)
        surface.blit(name_text, (WIDTH//2 - name_text.get_width()//2, bar_y - 40))

        # Draw attacks
        for attack in self.attacks:
            attack.draw(surface)

    def hit(self, damage):
        self.health = max(0, self.health - damage)

    def is_defeated(self):
        return self.health <= 0


class Papyrus(Boss):
    def __init__(self):
        super().__init__("Papyrus")
        self.max_health = 80
        self.health = self.max_health
        self.attack_cooldown = 60

    def perform_attack(self, player):
        # Papyrus shoots bones that fall vertically in a pattern at random x positions
        for i in range(3):
            x = random.randint(50, WIDTH - 50)
            bone = BoneAttack(x, -20, direction='down', speed=5)
            self.attacks.append(bone)

class Sans(Boss):
    def __init__(self):
        super().__init__("Sans")
        self.max_health = 120
        self.health = self.max_health
        self.attack_cooldown = 90
        self.attack_phase = 0
        self.phase_timer = 0

    def perform_attack(self, player):
        # Sans alternates between shooting bones horizontally and firing blasters
        if self.attack_phase == 0:
            # horizontal bones from left or right
            side = random.choice(['left', 'right'])
            y = random.randint(50, HEIGHT - 150)
            speed = 7
            bone = BoneAttack(WIDTH + 20 if side == 'left' else -20, y, horizontal=True, direction='left' if side == 'left' else 'right', speed=speed)
            self.attacks.append(bone)
            self.attack_phase = 1
        else:
            # blaster attack at random center position
            x = WIDTH // 2 + random.randint(-100, 100)
            y = HEIGHT // 2 + random.randint(-100, 100)
            blaster = BlasterAttack(x, y)
            self.attacks.append(blaster)
            self.attack_phase = 0

class Undyne(Boss):
    def __init__(self):
        super().__init__("Undyne")
        self.max_health = 150
        self.health = self.max_health
        self.attack_cooldown = 80

    def perform_attack(self, player):
        # Spear attacks from right moving left at player's current y position with delay
        spear = SpearAttack(WIDTH + 60, random.randint(50, HEIGHT - 100), player.rect.y, speed=10, direction='left')
        self.attacks.append(spear)


def draw_health_bar(surface, x, y, width, height, current_health, max_health, color, border_color=WHITE):
    pygame.draw.rect(surface, border_color, (x, y, width, height))
    inner_width = int((current_health / max_health) * (width - 4))
    pygame.draw.rect(surface, color, (x + 2, y + 2, inner_width, height - 4))


def draw_text_center(surface, text, font, color, x, y):
    rendered = font.render(text, True, color)
    surface.blit(rendered, (x - rendered.get_width() // 2, y))


def main_menu():
    selected = 0
    bosses = ['Papyrus', 'Sans', 'Undyne']

    while True:
        screen.fill(BLACK)
        draw_text_center(screen, "Undertale Boss Fight - Choose your Boss", font_large, WHITE, WIDTH // 2, 100)
        for i, boss_name in enumerate(bosses):
            color = CYAN if i == selected else WHITE
            draw_text_center(screen, boss_name, font_large, color, WIDTH // 2, 220 + i * 70)

        draw_text_center(screen, "Use UP/DOWN keys to select, ENTER to start", font_small, LIGHT_GRAY, WIDTH // 2, HEIGHT - 80)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(bosses)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(bosses)
                elif event.key == pygame.K_RETURN:
                    return bosses[selected]

        pygame.display.flip()
        clock.tick(FPS)


def game_over_screen(win, boss_name):
    while True:
        screen.fill(BLACK)
        if win:
            draw_text_center(screen, "You Defeated " + boss_name + "!", font_large, YELLOW, WIDTH // 2, HEIGHT // 2 - 30)
        else:
            draw_text_center(screen, "You Were Defeated...", font_large, RED, WIDTH // 2, HEIGHT // 2 - 30)

        draw_text_center(screen, "Press ENTER to return to menu", font_small, LIGHT_GRAY, WIDTH // 2, HEIGHT // 2 + 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return

        pygame.display.flip()
        clock.tick(FPS)


def main_game(boss_name: str):
    player = PlayerSoul()

    if boss_name == "Papyrus":
        boss = Papyrus()
        bg_color = (30, 20, 60)  # Purple dark
    elif boss_name == "Sans":
        boss = Sans()
        bg_color = (10, 10, 10)  # Black for Sans
    else: # Undyne
        boss = Undyne()
        bg_color = (0, 40, 100)  # Blue dark

    running = True
    while running:
        screen.fill(bg_color)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Player update
        player.move(keys)
        player.update()

        # Boss update
        boss.update(player)

        # Check collisions for player's hits (ignoring for now, focus on player taking damage)
        for attack in boss.attacks:
            if attack.check_collision(player):
                player.hit(1)

        # Player basic attack: SPACE to shoot short range "attack" upward to damage boss
        # Simple cooldown so player can't spam
        if keys[pygame.K_SPACE]:
            # Create a short vertical rectangle above player to represent attack hitbox
            attack_rect = pygame.Rect(player.rect.centerx - 10, player.rect.top - 20, 20, 20)
            if attack_rect.colliderect(pygame.Rect(WIDTH//2 - 150, 30 + 30, 300, 25)):
                # If boss health bar area is hit (simplified) deal damage
                boss.hit(1)

        # Draw everything
        boss.draw(screen)
        player.draw(screen)

        # Draw player health bar bottom left
        draw_health_bar(screen, 20, HEIGHT - 40, 200, 25, player.health, player.max_health, RED)

        # Draw instructions
        draw_text_center(screen, "Arrow keys to move, SPACE to attack", font_small, WHITE, WIDTH//2, HEIGHT - 30)

        # Check end conditions
        if player.health <= 0:
            running = False
            game_over_screen(False, boss.name)
        elif boss.is_defeated():
            running = False
            game_over_screen(True, boss.name)

        pygame.display.flip()
        clock.tick(FPS)


def main():
    while True:
        boss_name = main_menu()
        main_game(boss_name)


if __name__ == '__main__':
    main()

