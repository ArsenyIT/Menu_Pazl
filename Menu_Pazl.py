import sys
import abc
import random
import os
import pygame
from pygame.event import event_name
pygame.init()
pygame.font.init()

size = (1280, 720)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("My Game")
Background = (0,0,0)
screen.fill(Background)
FPS = 60
clock = pygame.time.Clock()

player_name = 'АНОНИМ'
font = pygame.font.SysFont(None, 64)

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
        self.surface = font.render(self.text, True, (255, 255, 255))
        self.name_surface = font.render(player_name, True, (255, 255, 255))

        self.rows = 3
        self.cols = 3
        self.margin = 2
        self.selected = None
        self.swaps = 0
        self.game_over = False

        pictures = os.listdir('pictures')
        picture = random.choice(pictures)
        image = pygame.image.load('pictures/' + picture)

        self.tile_width = image.get_width() // self.cols
        self.tile_height = image.get_height() // self.rows

        self.tiles = []
        for i in range(self.rows):
            for j in range(self.cols):
                rect = pygame.Rect(j * self.tile_width, i * self.tile_height, self.tile_width, self.tile_height)
                tile = image.subsurface(rect)
                self.tiles.append(tile)

        self.origin_tiles = self.tiles.copy()
        random.shuffle(self.tiles)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return MenuScreen()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.game_over:
                    return MenuScreen()
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for i in range(len(self.tiles)):
                    row = i // self.rows
                    col = i % self.cols
                    x = col * (self.tile_width + self.margin) + self.margin
                    y = row * (self.tile_height + self.margin) + self.margin
                    if x <= mouse_x <= x + self.tile_width and y <= mouse_y <= y + self.tile_height:
                        if self.selected is not None and self.selected != i:
                            self.tiles[i], self.tiles[self.selected] = self.tiles[self.selected], self.tiles[i]
                            self.selected = None
                            self.swaps += 1
                        elif self.selected == i:
                            self.selected = None
                        else:
                            self.selected = i
        return self

    def update(self):
        if self.tiles == self.origin_tiles:
            self.game_over = True

    def draw(self, screen):
        screen.fill(Background)
        for i, tile in enumerate(self.tiles):
            row = i // self.rows
            col = i % self.cols
            x = col * (self.tile_width + self.margin) + self.margin
            y = row * (self.tile_height + self.margin) + self.margin
            if i == self.selected:
                pygame.draw.rect(screen, (0, 255, 0), (
                    x - self.margin, y - self.margin, self.tile_width + self.margin * 2, self.tile_height + self.margin * 2))
            screen.blit(tile, (x, y))

        screen.blit(self.name_surface, (800, 10))

        text = pygame.font.SysFont(None, 32).render(f'Перестановок: {self.swaps}', True, (255, 255, 255))
        screen.blit(text, (800, 50))

        if self.game_over:
            over = pygame.font.SysFont(None, 48).render('Ура, картина собрана!', True, (0, 255, 0))
            screen.blit(over, (800, 100))

state = SplashScreen()

while True:
    events = pygame.event.get()
    state = state.handle_events(events)
    state.update()
    state.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()