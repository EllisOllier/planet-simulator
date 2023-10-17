import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulator")

class Planet:
    ASTRO_UNIT = 149.6e6 * 1000
    GRAV_CONST = 6.67428e-11
    SCALE = 250 / ASTRO_UNIT # 1 ASTRO_UNIT = 100 px
    TIMESTEP = 3600 * 24 # Amount of time each movement represents (1 day)

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2
        pygame.draw.circle(win, self.color, (x, y), self.radius)

def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 30, 'Yellow', 1.98892 * 10**30)
    sun.sun = True

    earth = Planet(-1 * Planet.ASTRO_UNIT, 0, 16,'Cyan', 5.9742 * 10*24)
    mars = Planet(-1.524 * Planet.ASTRO_UNIT, 0, 12, 'Red', 6.39 * 10**23)
    mercury = Planet(0.387 * Planet.ASTRO_UNIT, 0 ,8, 'Dark Grey', 3.30 * 10*23)
    venus = Planet(0.723 * Planet.ASTRO_UNIT, 0, 14, 'White', 4.8685 * 10**24)

    planets = [sun, earth, mars, mercury, venus]

    while run:
        clock.tick(60)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                

        for planet in planets:
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()

main()