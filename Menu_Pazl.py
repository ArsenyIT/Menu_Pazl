import sys
import abc
import pygame
from pygame.event import event_name

pygame.init()
pygame.font.init()

class State(abc.ABC):
    @abc.abstractmethod
    def handle_events(self, events):
        pass

    @abc.abstractmethod
    def update(self):
        pass

    @abc.abstractmethod
    def draw(self, screen):
        pass

class SplashScreen(State):
    def __init__(self):
        self.text = 'Заставка'
        self.surface = font.render(self.text, True, (255, 255, 255))
        self.hit = 'Нажмите для продолжения'
        self.hit_surface = font.render(self.hit, True, (255, 255, 255))
        self.hit_visible = True
        self.hit_time = pygame.time.get_ticks()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                return MenuScreen()
        return self

    def update(self):
        currect_time = pygame.time.get_ticks()
        if currect_time - self.hit_time > 800:
            self.hit_visible = not self.hit_visible
            self.hit_time = currect_time

    def draw(self, screen):
        screen.fill(Background)
        rect = self.surface.get_rect()
        rect.centerx = screen.get_rect().centerx
        rect.centery = screen.get_rect().centery - 100
        screen.blit(self.surface, rect)
        if self.hit_visible:
            hit_rect = self.hit_surface.get_rect()
            hit_rect.centerx = screen.get_rect().centerx
            hit_rect.centery = screen.get_rect().centery + 100
            screen.blit(self.hit_surface, hit_rect)

class MenuScreen(State):
    def __init__(self):
        self.items = ['Играть', 'Выбрать имя игрока', 'Выйти']
        self.surfaces = [font.render(item, True, (255, 255, 255)) for item in self.items]
        self.selected = 0

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.prev()
                if event.key == pygame.K_DOWN:
                    self.next()
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    return self.process_item()
        return self

    def update(self):
        pass

    def draw(self, screen):
        screen.fill(Background)
        for i, surface in enumerate(self.surfaces):
            rect = surface.get_rect()
            rect.centerx = screen.get_rect().centerx
            rect.top = screen.get_rect().top + 100 * (i + 1)
            if i == self.selected:
                surface = font.render(self.items[i], True, (255, 0, 0))
            screen.blit(surface, rect)

    def next(self):
        if self.selected < len(self.items) - 1:
            self.selected += 1

    def prev(self):
        if self.selected > 0:
            self.selected -= 1

    def process_item(self):
        if self.selected == 0:
            return GameScreen()
        if self.selected == 1:
            return NameScreen()
        if self.selected == 2:
            pygame.quit()
            sys.exit()

class NameScreen(State):
    def __init__(self):
        self.text = 'Введите имя игрока'
        self.surface =  font.render(self.text, True, (255, 255, 255))
        self.name = ''
        self.name_surface = None

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if len(self.name) > 0:
                        self.name = self.name[:-1]
                elif event.key == pygame.K_RETURN:
                    global player_name
                    player_name = self.name
                    return MenuScreen()
                else:
                    if event.unicode.isalnum() and len(self.name)< 10:
                        self.name += event.unicode
                        self.name_surface = font.render(self.name, True, (255, 255, 255))
        return self

    def update(self):
        pass

    def draw(self, screen):
        screen.fill(Background)
        rect = self.surface.get_rect()
        rect.centerx = screen.get_rect().centerx
        rect.top = screen.get_rect().top + 100
        screen.blit(self.surface, rect)
        if self.name_surface is not None:
            name_rect = self.name_surface.get_rect()
            name_rect.centerx = screen.get_rect().centerx
            name_rect.top = screen.get_rect().top + 200
            screen.blit(self.name_surface, name_rect)

class GameScreen(State):
    def __init__(self):
        self.text = 'Игра'
        self.surface =  font.render(self.text, True, (255, 255, 255))
        self.name_surface = font.render(player_name, True, (255, 255, 255))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                #if event.key == pygame.K_ESCAPE:
                #    return MenuScreen()
                if event.key == pygame.K_SPACE:
                    import random
                    import os

                    def draw_swaps():
                        font = pygame.font.SysFont(None, 32)
                        text = font.render(f'Кол-во перестановок: {swaps}', True, (255, 255, 255))
                        text_rect = text.get_rect()
                        text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200)
                        pygame.draw.rect(screen, (0, 0, 0), text_rect.inflate(4, 4))
                        screen.blit(text, text_rect)

                    def game_over():
                        font = pygame.font.SysFont(None, 32)
                        text = font.render('Ура, картина собрана!', True, (255, 255, 255))
                        text_rect = text.get_rect()
                        text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 250)
                        pygame.draw.rect(screen, (0, 0, 0), text_rect.inflate(4, 4))
                        screen.blit(text, text_rect)

                    def draw_tiles():
                        for i in range(len(tiles)):
                            tile = tiles[i]
                            row = i // rows
                            col = i % cols
                            x = col * (tile_width + margin) + margin
                            y = row * (tile_height + margin) + margin
                            if i == selected:
                                pygame.draw.rect(screen, (0, 255, 0), (
                                x - margin, y - margin, tile_width + margin * 2, tile_height + margin * 2))
                            screen.blit(tile, (x, y))

                    SCREEN_WIDTH = 1000
                    SCREEN_HEIGHT = 800
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                    pygame.display.set_caption("Пазл")
                    Background = (0, 0, 0)
                    screen.fill(Background)
                    rows = 3
                    cols = 3
                    margin = 2
                    FPS = 60
                    clock = pygame.time.Clock()

                    pictures = os.listdir('pictures')
                    picture = random.choice(pictures)
                    image = pygame.image.load('pictures/' + picture)

                    image_width, image_height = image.get_size()
                    tile_width = image_width // cols
                    tile_height = image_height // rows

                    tiles = []
                    for i in range(rows):
                        for j in range(cols):
                            rect = pygame.Rect(j * tile_width, i * tile_height, tile_width, tile_height)
                            tile = image.subsurface(rect)
                            tiles.append(tile)

                    origin_tiles = tiles.copy()
                    random.shuffle(tiles)
                    swaps = 0
                    selected = None

                    running = True
                    while running:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_ESCAPE:
                                    running = False
                                    return MenuScreen()

                                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                                    mouse_x, mouse_y = pygame.mouse.get_pos()
                                    for i in range(len(tiles)):
                                        row = i // rows
                                        col = i % cols
                                        x = col * (tile_width + margin) + margin
                                        y = row * (tile_height + margin) + margin

                                        if x <= mouse_x <= x + tile_width and y <= mouse_y <= y + tile_height:
                                            if selected is not None and selected != i:
                                                tiles[i], tiles[selected] = tiles[selected], tiles[i]
                                                selected = None
                                                swaps += 1
                                            elif selected == i:
                                                selected = None
                                            else:
                                                selected = i

                        screen.fill(Background)
                        draw_tiles()
                        draw_swaps()

                        if tiles == origin_tiles:
                            game_over()

                        pygame.display.flip()
                        clock.tick(FPS)

                    pygame.quit()
        return self

    def update(self):
        pass

    def draw(self, screen):
        screen.fill(Background)
        rect = self.surface.get_rect()
        rect.centerx = screen.get_rect().centerx
        rect.centery = screen.get_rect().centery
        screen.blit(self.surface, rect)
        name_rect = self.name_surface.get_rect()
        name_rect.left = screen.get_rect().left + 10
        name_rect.top = screen.get_rect().top + 10
        screen.blit(self.name_surface, name_rect)

size = (1280, 720)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("My Game")
Background = (0,0,0)
screen.fill(Background)
FPS = 60
clock = pygame.time.Clock()

player_name = 'АНОНИМ'
font = pygame.font.SysFont(None, 64)

state = SplashScreen()

while True:
    events = pygame.event.get()
    state = state.handle_events(events)
    state.update()
    state.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()