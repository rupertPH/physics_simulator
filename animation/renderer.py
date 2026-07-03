import pygame

class Renderer:

    def __init__(self, config):

        pygame.init()

        self.width = 800
        self.height = 600

        self.screen = pygame.display.set_mode(
            (self.width, self.height)
        )

        pygame.display.set_caption("Physics Simulation")

        self.clock = pygame.time.Clock()

        # -------------------------
        # RENDER SETTINGS (FROM CONFIG)
        # -------------------------

        render_cfg = config["RENDER"]

        self.scale = float(render_cfg.get("scale", 200))
        self.origin = (
            int(render_cfg.get("origin_x", self.width // 2)),
            int(render_cfg.get("origin_y", self.height // 2))
        )

        self.font = pygame.font.SysFont("Arial", 16)

        self.running = True

        self.t = 0.0

    def world_to_screen(self, x, y):

        px = self.origin[0] + x * self.scale

        py = self.origin[1] - y * self.scale

        return int(px), int(py)
    
    def process_events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

        return self.running
    
    def draw_grid(self):

        color = (230, 230, 230)

        step = self.scale

        # vertical lines
        x0 = self.origin[0] % step
        for x in range(int(x0), self.width, int(step)):
            pygame.draw.line(self.screen, color, (x, 0), (x, self.height))

        # horizontal lines
        y0 = self.origin[1] % step
        for y in range(int(y0), self.height, int(step)):
            pygame.draw.line(self.screen, color, (0, y), (self.width, y))

        # axes
        pygame.draw.line(
            self.screen, (0, 0, 0),
            (self.origin[0], 0),
            (self.origin[0], self.height), 2
        )

        pygame.draw.line(
            self.screen, (0, 0, 0),
            (0, self.origin[1]),
            (self.width, self.origin[1]), 2
        )
    
    def draw_points(self, points):

        for i, (x, y) in enumerate(points):

            sx, sy = self.world_to_screen(x, y)

            # point
            pygame.draw.circle(self.screen, (200, 50, 50), (sx, sy), 8)

            # number
            label = self.font.render(str(i), True, (0, 0, 0))
            self.screen.blit(label, (sx + 10, sy - 10))

    def draw_ui(self):

        text = f"t = {self.t:.2f} s   |   FPS = {int(self.clock.get_fps())}"

        label = self.font.render(text, True, (0, 0, 0))

        self.screen.blit(label, (10, 10))

    def draw(self, points, dt):

        self.t += dt

        self.screen.fill((255, 255, 255))

        self.draw_grid()

        self.draw_points(points)

        self.draw_ui()

        pygame.display.flip()

        self.clock.tick(60)