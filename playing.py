from smth import world_data, portal_x_dis, portal_y_dis, x_pos_en1, y_pos_en1, enemy_amount_1, displacement_x, \
    displacement_y, enemy_amount_2, x_pos_en2, y_pos_en2
import random

import pygame
import math

# from pygame.locals import *

pygame.init()

width = 1000
height = 600

screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

White = (255, 255, 255)
Gray = (140, 140, 140)
Black = (0, 0, 0)
Green = (0, 255, 0)
Dark_Green = (0, 150, 0)
Red = (255, 0, 0)
Dark_Red = (150, 0, 0)
Cyan = (0, 255, 255)
Purple = (255, 0, 255)


class Camera:
    def __init__(self, cam_x, cam_y):
        self.cam_x = cam_x
        self.cam_y = cam_y

    def screen_change(self, new_width, new_height):
        diff_x = (width - new_width)
        diff_y = (height - new_height)

        print(diff_x / 2, diff_y / 2)

        self.cam_x = self.cam_x + diff_x / 2
        self.cam_y = self.cam_y + diff_y / 2

    def next_level(self):
        self.cam_x = (1000 - width) / 2
        self.cam_y = (600 - height) / 2


class Physics:
    def __init__(self, gravity, acceleration, g, c, p):
        self.gravity = gravity
        self.max_speed = 20
        self.velocity = 0

        self.Camera = c
        self.Grid = g
        self.Player = p

        self.acceleration = acceleration

    def collisions(self, x, y, e_width, e_height):
        for column in range(self.Grid.column_amount):
            for row in range(self.Grid.row_amount):
                grid_rect = pygame.Rect(
                    self.Grid.grid_pos_x[column],
                    self.Grid.grid_pos_y[row],
                    self.Grid.grid_width,
                    self.Grid.grid_height
                )
                if self.Grid.world_grid[row][column] == 1 or self.Grid.world_grid[row][column] == 3 or \
                        self.Grid.world_grid[row][column] == 4:
                    # check for x direction
                    if grid_rect.colliderect(x + self.velocity, y - 5, e_width, e_height):
                        self.velocity *= 0

                    # check on block
                    if grid_rect.colliderect(x, y + self.gravity, e_width, e_height):
                        self.velocity *= .9
                        if self.gravity > 0:
                            y = self.Grid.grid_pos_y[row] - e_height
                            self.gravity = 0
                        elif self.gravity < 0:
                            y = self.Grid.grid_pos_y[row] + self.Grid.grid_width
                            self.gravity = 0

                elif self.Grid.world_grid[row][column] == 2:
                    if grid_rect.colliderect(x, y + self.gravity, e_width, e_height):
                        self.gravity = - 20
        return x, y

    def collisions_flying(self, x, y, e_width, e_height, dx, dy):
        collide = False
        for column in range(self.Grid.column_amount):
            for row in range(self.Grid.row_amount):
                grid_rect = pygame.Rect(
                    self.Grid.grid_pos_x[column],
                    self.Grid.grid_pos_y[row],
                    self.Grid.grid_width,
                    self.Grid.grid_height
                )
                if self.Grid.world_grid[row][column] == 1 or self.Grid.world_grid[row][column] == 3 or \
                        self.Grid.world_grid[row][column] == 4:
                    # check for x direction
                    if grid_rect.colliderect(x + dx, y - 5, e_width, e_height):
                        dx = 0
                        collide = True
                    # check on block
                    if grid_rect.colliderect(x, y + dy, e_width, e_height):
                        collide = True
                        dy = 0

        return x, y, dx, dy, collide

    def run_physics(self, x, y):
        y += self.gravity
        x += self.velocity
        self.gravity += 1
        if abs(self.velocity) <= self.max_speed:
            if x <= self.Player.P_x + self.Camera.cam_x:
                self.velocity += self.acceleration
            elif x >= self.Player.P_x + self.Camera.cam_x:
                self.velocity -= self.acceleration

        return x, y


class Grid:
    def __init__(self, grid_width, grid_height, screen_width, screen_height, wg, c, spawn_x, spawn_y):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.grid_width = grid_width
        self.grid_height = grid_height

        self.world_grid = wg
        self.row_amount = len(self.world_grid)
        self.column_amount = len(self.world_grid[0])

        self.Camera = c

        self.grid_pos_x = [column * self.grid_width - spawn_x for column in range(self.column_amount)]
        self.grid_pos_y = [row * self.grid_height - spawn_y for row in range(self.row_amount)]

        self.color = [[White for _ in range(self.column_amount)] for _ in range(self.row_amount)]
        self.color_2 = [[[Red for _ in range(self.column_amount)] for _ in range(self.row_amount)],
                        [[Cyan for _ in range(self.column_amount)] for _ in range(self.row_amount)],
                        [[Green for _ in range(self.column_amount)] for _ in range(self.row_amount)]]

        self.temp_cooldown = 0

    def draw(self):
        for column in range(self.column_amount):
            for row in range(self.row_amount):

                if self.world_grid[row][column] == 1:
                    pygame.draw.rect(screen, self.color[row][column],
                                     (self.grid_pos_x[column] - self.Camera.cam_x,
                                      self.grid_pos_y[row] - self.Camera.cam_y, self.grid_width, self.grid_height),
                                     5)
                elif self.world_grid[row][column] == 2:
                    pygame.draw.rect(screen, self.color_2[0][row][column],
                                     (self.grid_pos_x[column] - self.Camera.cam_x,
                                      self.grid_pos_y[row] - self.Camera.cam_y, self.grid_width, self.grid_height),
                                     5)
                elif self.world_grid[row][column] == 3:
                    pygame.draw.rect(screen, self.color_2[1][row][column],
                                     (self.grid_pos_x[column] - self.Camera.cam_x,
                                      self.grid_pos_y[row] - self.Camera.cam_y, self.grid_width, self.grid_height),
                                     5)
                elif self.world_grid[row][column] == 4:
                    pygame.draw.rect(screen, self.color_2[2][row][column],
                                     (self.grid_pos_x[column] - self.Camera.cam_x,
                                      self.grid_pos_y[row] - self.Camera.cam_y, self.grid_width, self.grid_height),
                                     5)

    def detection(self):
        # update camera movement to

        pos = pygame.mouse.get_pos()
        for column in range(self.column_amount):
            for row in range(self.row_amount):
                if self.grid_pos_x[column] <= pos[0] + self.Camera.cam_x <= self.grid_pos_x[
                    column] + self.grid_width and self.grid_pos_y[
                    row] <= pos[1] + self.Camera.cam_y <= self.grid_pos_y[row] + self.grid_height:
                    self.color[row][column] = (100, 100, 100)

                    self.temp_cooldown += 1
                    click = pygame.mouse.get_pressed()
                    if click[0] and self.temp_cooldown % 5 == 0:
                        print(self.world_grid)
                        self.world_grid[row][column] += 1
                        if self.world_grid[row][column] > 4:
                            self.world_grid[row][column] = 0


class Player(Physics):
    def __init__(self, player_x, player_y, player_width, player_height, g, c):
        super().__init__(0, 0, g, c, 0)
        self.P_x = player_x
        self.P_y = player_y
        self.P_width = player_width
        self.P_height = player_height
        self.Grid = g
        self.Camera = c

        self.timer = 0

        self.amount = 0
        self.bul_x = []
        self.bul_y = []
        self.bul_x_vel = []
        self.bul_y_vel = []
        self.bull_speed = 15
        self.bullet_radius = 20

        self.jump = False
        self.multi_jump = 0

        self.max_hp = 100
        self.hp = 100

        self.y_vel = 10
        self.x_vel = 10

    def player_bullets(self):
        # bullet logic
        pos = pygame.mouse.get_pos()
        clicky = pygame.mouse.get_pressed()

        self.timer -= 1

        if clicky[0] and self.timer <= 0:
            self.bul_x.append(self.P_x + self.Camera.cam_x + self.P_width / 2)
            self.bul_y.append(self.P_y + self.Camera.cam_y + self.P_height / 2)
            diff_x = pos[0] - self.P_x
            diff_y = pos[1] - self.P_y
            hypo = math.sqrt(diff_x ** 2 + diff_y ** 2)

            self.bul_x_vel.append(diff_x / hypo)
            self.bul_y_vel.append(diff_y / hypo)
            self.amount += 1
            self.timer = 0
            # print("click")

        # move bullet
        for bullet in reversed(range(self.amount)):
            dx = 0
            dy = 0

            # print(bullet)
            # print(self.bul_x_vel)

            # print(bullet)
            dx += self.bul_x_vel[bullet] * self.bull_speed
            dy += self.bul_y_vel[bullet] * self.bull_speed

            _, _, _, _, collide = self.collisions_flying(self.bul_x[bullet] - self.bullet_radius / 2,
                                                         self.bul_y[bullet] - self.bullet_radius / 2,
                                                         self.bullet_radius,
                                                         self.bullet_radius, dx, dy)
            self.bul_x[bullet] += dx
            self.bul_y[bullet] += dy

            if collide or abs(self.bul_y[bullet]) >= 3000 or abs(self.bul_x[bullet]) >= 3000:
                self.amount -= 1
                self.bul_x.pop(bullet)
                self.bul_y.pop(bullet)
                self.bul_x_vel.pop(bullet)
                self.bul_y_vel.pop(bullet)
            # print(self.amount)

    def draw_player(self):
        for bullet in range(self.amount):
            pygame.draw.circle(screen, Cyan,
                               (self.bul_x[bullet] - self.Camera.cam_x, self.bul_y[bullet] - self.Camera.cam_y),
                               self.bullet_radius)
        pygame.draw.rect(screen, (0, 255, 0), (self.P_x, self.P_y, self.P_width, self.P_height))

    def collide_with_grid(self, dx, dy):
        self.P_x = width / 2
        self.P_y = height / 2
        for column in range(self.Grid.column_amount):
            for row in range(self.Grid.row_amount):
                if self.Grid.world_grid[row][column] == 1 or self.Grid.world_grid[row][column] == 2 or \
                        self.Grid.world_grid[row][column] == 4:
                    grid_rect = pygame.Rect(
                        self.Grid.grid_pos_x[column] - self.Camera.cam_x,
                        self.Grid.grid_pos_y[row] - self.Camera.cam_y,
                        self.Grid.grid_width,
                        self.Grid.grid_height
                    )
                    # check for x direction

                    if grid_rect.colliderect(self.P_x + dx, self.P_y, self.P_width, self.P_height):
                        self.Grid.color[row][column] = (0, 255, 0)
                        dx = 0
                    else:
                        self.Grid.color[row][column] = White

                    # check for y direction
                    if grid_rect.colliderect(self.P_x, self.P_y + dy, self.P_width, self.P_height):
                        # check if hit head
                        self.Grid.color[row][column] = (0, 255, 0)

                        if self.y_vel < 0:
                            self.Camera.cam_y = self.Grid.grid_pos_y[row] - self.P_y + self.Grid.grid_height
                            self.y_vel = 0
                            dy = 0

                        # check if on block
                        elif self.y_vel > 0:

                            self.Camera.cam_y = self.Grid.grid_pos_y[row] - self.P_y - self.P_height
                            dy = 0
                            self.multi_jump = 2
                    else:
                        self.Grid.color[row][column] = White
        return dx, dy

    def movements(self):
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0

        # left and right movements
        if keys[pygame.K_SPACE] and not self.jump and self.multi_jump > 0:
            self.y_vel = - 20
            self.jump = True
            self.multi_jump -= 1
        if not keys[pygame.K_SPACE]:
            self.jump = False

        if keys[pygame.K_a]:
            dx -= self.x_vel
        if keys[pygame.K_d]:
            dx += self.x_vel

        # gravity
        self.y_vel += 1
        if self.y_vel > 12:
            self.y_vel = 12
        dy += self.y_vel

        # check collisions
        dx, dy = self.collide_with_grid(dx, dy)

        self.camera(dx, dy)

    def player_ui(self):
        hp_bar = (self.hp / self.max_hp) * 100

        pygame.draw.rect(screen, Gray, (15, 15, 110, 20))
        pygame.draw.rect(screen, Dark_Red, (20, 20, 100, 10))
        pygame.draw.rect(screen, Dark_Green, (20, 20, hp_bar, 10))

    def camera(self, dx, dy):
        self.Camera.cam_x += dx
        self.Camera.cam_y += dy


class Enemy(Physics):
    def __init__(self, hp, speed, enemy_height, enemy_width, p, c, x, y, g):
        super().__init__(20, 1, g, c, p)
        self.x = x
        self.y = y

        self.enemy_width = enemy_width
        self.enemy_height = enemy_height
        self.hp = hp

        self.speed = speed
        self.Player = p
        self.Camera = c

        self.sight = False

        self.vel_y = 0
        self.vel_x = 0

    def enemy_fly_ai(self):
        dx = 0
        dy = 0

        diff_x = self.Player.P_x - self.x + self.Camera.cam_x
        diff_y = self.Player.P_y - self.y + self.Camera.cam_y

        hypo = math.sqrt(diff_x ** 2 + diff_y ** 2)

        self.vel_x = diff_x / hypo
        self.vel_y = diff_y / hypo

        dx += self.vel_x * self.speed
        dy += self.vel_y * self.speed

        self.x, self.y, dx, dy, _ = self.collisions_flying(self.x, self.y, self.enemy_width, self.enemy_height, dx, dy)

        self.x += dx
        self.y += dy

    def ground_enemy(self):
        self.x, self.y = self.collisions(self.x, self.y, self.enemy_width, self.enemy_height)
        self.x, self.y = self.run_physics(self.x, self.y)

    def draw_enemy(self):
        pygame.draw.rect(screen, Red,
                         (self.x - self.Camera.cam_x, self.y - self.Camera.cam_y, self.enemy_width, self.enemy_height))

    def kill_detect(self):
        enemy_rect = pygame.Rect(self.x, self.y, self.enemy_width, self.enemy_height)

        for bullet in range(self.Player.amount):
            bullet_x = self.Player.bul_x[bullet] + self.Player.bul_x_vel[
                bullet] * self.Player.bull_speed - self.Player.bullet_radius * 0.5
            bullet_y = self.Player.bul_y[bullet] + self.Player.bul_y_vel[
                bullet] * self.Player.bull_speed - self.Player.bullet_radius * 0.5
            if enemy_rect.colliderect(
                    pygame.Rect(bullet_x, bullet_y, self.Player.bullet_radius, self.Player.bullet_radius)):
                return True

        return False


class RunLevel:
    def __init__(self, pos_x, pos_y, portal_radius, c, g, p, level):
        self.portal_radius = portal_radius
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.Camera = c
        self.Grid = g
        self.Player = p

        self.level = level

    def draw_portal(self):
        pygame.draw.circle(screen, Purple, (self.pos_x - self.Camera.cam_x, self.pos_y - self.Camera.cam_y),
                           self.portal_radius)

    def open_gate(self):
        for column in range(self.Grid.column_amount):
            for row in range(self.Grid.row_amount):
                if self.Grid.world_grid[row][column] == 4:
                    self.Grid.world_grid[row][column] = 0

    def change_lvl(self):
        diff_x = -self.Player.P_x - self.Player.P_width / 2 + (self.pos_x - self.Camera.cam_x)
        diff_y = -self.Player.P_y - self.Player.P_width / 2 + (self.pos_y - self.Camera.cam_y)

        hypo = math.sqrt(diff_x ** 2 + diff_y ** 2)

        dot_pos_x = self.pos_x - (diff_x / hypo) * self.portal_radius
        dot_pos_y = self.pos_y - (diff_y / hypo) * self.portal_radius

        pygame.draw.circle(screen, Cyan, (dot_pos_x - self.Camera.cam_x, dot_pos_y - self.Camera.cam_y), 3)
        pygame.draw.line(screen, Red, (self.pos_x - self.Camera.cam_x, self.pos_y - self.Camera.cam_y),
                         (self.Player.P_x + self.Player.P_width / 2, self.Player.P_y + self.Player.P_height / 2))

        collides = (self.Player.P_x + self.Player.P_width * 1.5 >= dot_pos_x - self.Camera.cam_x and
                    self.Player.P_y + self.Player.P_height * 1.5 >= dot_pos_y - self.Camera.cam_y and
                    self.Player.P_x <= dot_pos_x - self.Camera.cam_x and
                    self.Player.P_y <= dot_pos_y - self.Camera.cam_y)

        if collides:
            if self.level < 3:
                self.level += 1
            return True


class World:
    def __init__(self):
        self.camera = Camera(0, 0)

        self.grid = Grid(50, 50, width, height, world_data[0], self.camera, displacement_x[0], displacement_y[0])
        self.player = Player(width / 2, height / 2, 30, 50, self.grid, self.camera)

        self.enemy = [
            Enemy(100, 5, 30, 30, self.player, self.camera, x_pos_en1[i] - displacement_x[0], y_pos_en1[i], self.grid)
            for i in
            range(enemy_amount_1)]

        self.enemy_2 = [
            Enemy(100, 5, 30, 30, self.player, self.camera, x_pos_en2[i] - displacement_x[0], y_pos_en2[i], self.grid)
            for i
            in range(enemy_amount_2)]

        self.portal = RunLevel(450, 570, 100, self.camera, self.grid, self.player, 0)


world = World()


def draw_all():
    world.grid.draw()

    for i in range(enemy_amount_1):
        world.enemy[i].draw_enemy()
    for i in range(enemy_amount_2):
        world.enemy_2[i].draw_enemy()

    world.portal.draw_portal()
    world.player.draw_player()
    world.player.player_ui()


def collisions():
    global enemy_amount_2
    global enemy_amount_1
    world.grid.detection()

    for i in reversed(range(enemy_amount_1)):
        kill = world.enemy[i].kill_detect()
        if kill:
            world.enemy.pop(i)
            enemy_amount_1 -= 1

    for i in reversed(range(enemy_amount_2)):
        kill = world.enemy_2[i].kill_detect()
        if kill:
            world.enemy_2.pop(i)
            enemy_amount_2 -= 1


def movements():
    world.player.player_bullets()
    world.player.movements()
    for i in range(enemy_amount_1):
        world.enemy[i].enemy_fly_ai()

    for i in range(enemy_amount_2):
        world.enemy_2[i].ground_enemy()


def change_level():
    global grid, player, enemy, enemy_2, enemy_2, portal, enemy_amount_2, enemy_amount_1, camera
    if enemy_amount_2 <= 0 and enemy_amount_1 <= 0:
        world.portal.open_gate()

    change = world.portal.change_lvl()

    if change:
        world.camera = Camera((1000 - width) / 2, (600 - height) / 2)  # Accessing world.camera

        # Update world.grid, world.player, and enemies after level change
        world.grid = Grid(50, 50, width, height, world_data[world.portal.level], world.camera,
                          displacement_x[world.portal.level],
                          displacement_y[world.portal.level])  # Accessing world.grid

        world.player = Player(width / 2, height / 2, 30, 50, world.grid, world.camera)  # Accessing world.player

        enemy_amount_1 = 5
        world.enemy = [
            Enemy(100, 5, 30, 30, world.player, world.camera, x_pos_en1[i] - displacement_x[world.portal.level],
                  y_pos_en1[i], world.grid)
            for i in
            range(enemy_amount_1)]  # Accessing world.enemy

        world.enemy_amount_2 = 5
        world.enemy_2 = [
            Enemy(100, 5, 30, 30, world.player, world.camera, x_pos_en2[i] - displacement_x[world.portal.level],
                  y_pos_en2[i], world.grid)
            for i in
            range(enemy_amount_2)]  # Accessing world.enemy_2

        world.portal = RunLevel(450 + portal_x_dis[world.portal.level], 570 + portal_y_dis[world.portal.level], 100,
                                world.camera, world.grid, world.player, world.portal.level)  # Accessing world.portal


def get_screen_size():
    global width
    global height

    width, height = screen.get_size()

#     num_1 = int(width / 50)
#     num_2 = int(height / 50)
#     bigger_grid = [[0 for _ in range(num_1)] for _ in range(num_2)]
#     print(bigger_grid)
