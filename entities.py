################################################################################
import numpy as np
import math
from config import WIDTH, HEIGHT, CELL_SIZE, MOVE_SPEED, MAX_PLAYERS, MAX_ENEMIES

# Sprite-Klassen
class Player:
    def __init__(self, player_class, x, y):
        self.player_class = player_class
        self.x = x
        self.y = y
        self.max_hp = 100
        self.hp = self.max_hp
        self.is_dead = False
        self.last_shot_time = 0
        self.target_boss = True
        self.recent_actions = []

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.is_dead = True

    def move(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance <= CELL_SIZE / 2:
            return

        if distance > 0:
            dx /= distance
            dy /= distance
            self.x += dx * MOVE_SPEED
            self.y += dy * MOVE_SPEED

class Boss:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.max_hp = 500
        self.hp = self.max_hp
        self.is_enraged = False
        self.enrage_timer = 0
        self.phase = 1
        self.last_shot_time = 0
        self.target_player = None

    def take_damage(self, damage):
        self.hp -= damage

    def check_phase(self):
        if self.hp <= self.max_hp / 2 and self.phase == 1:
            self.phase = 2
            print("Boss in Phase 2 übergegangen!")
        if self.hp <= self.max_hp / 4 and self.phase == 2:
            self.phase = 3
            print("Boss in Phase 3 übergegangen!")

    def move(self, players):
        if players:
            if self.target_player is None or self.target_player not in players:
                self.target_player = self.get_closest_player(players)
            if self.target_player:
                target_x = self.target_player.x
                target_y = self.target_player.y
                dx = target_x - self.x
                dy = target_y - self.y
                distance = math.sqrt(dx**2 + dy**2)

                if distance <= CELL_SIZE / 2:
                    return

                if distance > 0:
                    dx /= distance
                    dy /= distance
                    self.x += dx * MOVE_SPEED / 2
                    self.y += dy * MOVE_SPEED / 2

    def get_closest_player(self, players):
        if not players:
            return None
        closest_player = None
        min_distance = float('inf')
        for player in players:
            distance = np.sqrt((self.x - player.x) ** 2 + (self.y - player.y) ** 2)
            if distance < min_distance:
                min_distance = distance
                closest_player = player
        return closest_player

class Add:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.max_hp = 25
        self.hp = self.max_hp
        self.last_shot_time = 0
        self.target_player = None

    def take_damage(self, damage):
        self.hp -= damage

    def move(self, players):
        if players:
            if self.target_player is None or self.target_player not in players:
                self.target_player = self.get_closest_player(players)
            if self.target_player:
                target_x = self.target_player.x
                target_y = self.target_player.y
                dx = target_x - self.x
                dy = target_y - self.y
                distance = math.sqrt(dx**2 + dy**2)

                if distance <= CELL_SIZE / 2:
                    return

                if distance > 0:
                    dx /= distance
                    dy /= distance
                    self.x += dx * 2
                    self.y += dy * 2

    def get_closest_player(self, players):
        if not players:
            return None
        closest_player = None
        min_distance = float('inf')
        for player in players:
            distance = np.sqrt((self.x - player.x) ** 2 + (self.y - player.y) ** 2)
            if distance < min_distance:
                min_distance = distance
                closest_player = player
        return closest_player
