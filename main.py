import pygame
import math


class Planet:
    ASTRO_UNIT = 149.6e6 * 1000
    GRAV_CONST = 6.67428e-11
    SCALE = 75 / ASTRO_UNIT # 1 ASTRO_UNIT = 100 px
    TIMESTEP = 3600 * 48 # Amount of time each movement represents (1 day)

    def __init__(self, name, x, y, radius, color, mass):
        self.name = name
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
        x = self.x * self.SCALE + game.WIDTH / 2
        y = self.y * self.SCALE + game.HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + game.WIDTH / 2
                y = y * self.SCALE + game.HEIGHT / 2

                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 1)

        pygame.draw.circle(win, self.color, (x, y), self.radius)
        if not self.sun:
            distance_text = game.FONT.render(self.name + ": " + f'{round(self.distance_to_sun/1000), 1} km', True, 'white')
            win.blit(distance_text, (x - distance_text.get_width() / 2, y + 10))

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.GRAV_CONST * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y
    
    def update_position(self, planets):
        total_force_x = total_force_y = 0
        for planet in planets:
            if self == planet:
                continue
            
            force_x, force_y = self.attraction(planet)
            total_force_x += force_x
            total_force_y += force_y

        self.x_vel += total_force_x / self.mass * self.TIMESTEP
        self.y_vel += total_force_y / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))

class Game():
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 1000, 1000
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.FONT = pygame.font.SysFont('comicsans', 16)
        pygame.display.set_caption("Planet Simulator")

    def run(self):
        run = True
        clock = pygame.time.Clock()
        real_time_elapsed = 0
        sim_time_elapsed = 0

        sun = Planet("Sun", 0, 0, 24, 'Yellow', 1.98892 * 10**30)
        sun.sun = True

        mercury = Planet("Mercury", 0.387 * Planet.ASTRO_UNIT, 0, 4,'Dark Grey', 3.30 * 10**23)
        mercury.y_vel = -47.4 * 1000

        venus = Planet("Venus", 0.723 * Planet.ASTRO_UNIT, 0, 14, 'Orange', 4.8685 * 10**24)
        venus.y_vel = -35.02 * 1000

        earth = Planet("Earth", -1 * Planet.ASTRO_UNIT, 0, 16,'Cyan', 5.972 * 10**24)
        earth.y_vel = 29.783 * 1000

        mars = Planet("Mars", -1.524 * Planet.ASTRO_UNIT, 0, 12, 'Red', 6.39 * 10**23)
        mars.y_vel = 24.077 * 1000

        jupiter = Planet("Jupiter", 5.2 * Planet.ASTRO_UNIT, 0, 24, 'Brown', 1.898 * 10**27)
        jupiter.y_vel = 13.72 * 1000

        planets = [sun, mercury, venus, earth, mars, jupiter]

        while run:
            clock.tick(60)
            real_time_elapsed += 1
            sim_time_elapsed += sun.TIMESTEP
            self.WIN.fill('Black')

            
            # Check if the orbit line overlaps
                # Print day passed
            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Real time elapsed: " + str(round((real_time_elapsed / 60), 1)) + "s")
                    print("Earth months simulated: " + str(round((sim_time_elapsed / 60 / 24 / 1800), 1)))
                    run = False
                    

            for planet in planets:
                planet.update_position(planets)
                planet.draw(self.WIN)

            pygame.display.update()

        pygame.quit()

game = Game()
if __name__ == '__main__':
    game.run()