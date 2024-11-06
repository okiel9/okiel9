import pygame
from playing import draw_all, collisions, movements, get_screen_size, world, change_level

pygame.init()


def main():
    width_main = 1000
    height_main = 600

    screen = pygame.display.set_mode((width_main, height_main), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.WINDOWRESIZED:
                width_main, height_main = screen.get_size()

                world.camera.screen_change(width_main, height_main)
                get_screen_size()

        movements()

        collisions()
        screen.fill((0, 0, 0))
        clock.tick(32)
        draw_all()
        change_level()

        pygame.display.update()


if __name__ == "__main__":
    main()
