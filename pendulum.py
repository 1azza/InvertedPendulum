import pygame
import math
import random
# Initialize Pygame
pygame.init()
pygame.font.init()
WIDTH, HEIGHT = 1000, 800
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pendulum Simulation")
my_font = pygame.font.SysFont('Georgia', 30)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Pendulum:
    def __init__(self, length, angle, pivot_x, pivot_y, bob_mass, pivot_mass):
        self.bob_mass = bob_mass
        self.length = length
        self.pivot_mass = pivot_mass
        self.angle = math.radians(angle)
        self.pivot_x = pivot_x
        self.pivot_y = pivot_y
        self.bob_x = pivot_x + length * math.sin(math.radians(angle))
        self.bob_velocity = 0
        self.bob_y = pivot_y + length * math.cos(math.radians(angle))
        self.angular_velocity = 0
        self.pivot_velocity = 0
        self.gfs = 20
        self.anglular_acceleration = 0
        self.pivot_force = 0
        self.pivot_acceleration_x = 0
        self.angular_frequency = math.sqrt(100 / length)
        self.damping_coefficient = 0.01
        self.integral_error = 0
        self.external_pivot_force = 0
        self.Fp = 0
        self.Fd = 0
        self.Fi = 0
        self.error = 0
        self.balance_pendulum = False

    def update(self, dt):
        if self.balance_pendulum == True:

            desired_angle = 180
            self.error = math.radians(math.degrees(self.angle)%360 - desired_angle)
            if abs(math.degrees(self.error)) > 90:
                    Kp = 20
                    Kd = 15
                    Ki =2
            else:
                Kp = 30
                Kd = 15
                Ki =1.5
            self.integral_error += self.error * dt
            self.Fp = -Kp * self.error
            self.Fi = - Ki * self.integral_error
            self.Fd = - Kd * self.angular_velocity
            self.pivot_force = self.Fp + self.Fd + self.Fi

        self.pivot_force += self.external_pivot_force
        self.pivot_acceleration_x = self.pivot_force / self.pivot_mass
        self.pivot_velocity = self.pivot_acceleration_x * dt

        self.pivot_x += self.pivot_velocity
        self.anglular_acceleration = (math.cos(self.angle) * -(self.pivot_acceleration_x / self.length)
                                      - math.sin(self.angle) * (self.gfs / self.length) 
                                      - self.damping_coefficient * self.angular_velocity)
        
        self.angular_velocity += self.anglular_acceleration * dt
        self.angle += self.angular_velocity * dt
        
        if self.pivot_x > WIDTH-300:
            self.pivot_x = WIDTH-300
        if self.pivot_x < 0+300:
            self.pivot_x = 0+300
        self.bob_x = self.pivot_x + self.length * math.sin(self.angle)
        self.bob_y = self.pivot_y + self.length * math.cos(self.angle)

    def draw(self, dt):
        pygame.draw.line(window, (50,200, 200), (WIDTH-300, self.pivot_y), (0+300, self.pivot_y), 2)
        angle_change = self.angular_velocity * dt*20
        next_angle = self.angle + angle_change
        next_pivot_pos = self.pivot_x + self.pivot_acceleration_x
        
        pygame.draw.line(window, (50, 200, 200), (self.bob_x, self.bob_y), (self.pivot_x + self.length * math.sin(next_angle),self.pivot_y + self.length * math.cos(next_angle)), 2)
        # pygame.draw.line(window, (50, 200, 200), (self.bob_x, self.bob_y), (self.pivot_x + self.length * math.sin(angle_change),self.pivot_y + self.length * math.cos(angle_change)), 2)
        pygame.draw.line(window, (50, 100, 250), (self.pivot_x, self.pivot_y), (next_pivot_pos, self.pivot_y), 2)
        
        pygame.draw.line(window, WHITE, (self.pivot_x, self.pivot_y), (self.bob_x, self.bob_y), 2)
        pygame.draw.circle(window, WHITE, (int(self.bob_x), int(self.bob_y)), 10)
    def __str__(self):
        return f'Angular displacement: {round(math.degrees(pendulum.angle))} degrees or {round(pendulum.angle, 2)}rads\nAngular acceleration: {round(pendulum.anglular_acceleration, 3)}rad/s^-2\nAngular velocity: {round(pendulum.angular_velocity, 2)}rad/s^1\nTime: {round(t, 1)}s'

class Button:
    def __init__(self, x, y, width, height, color, text, text_color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.text_color = text_color

    def draw(self):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))
        text_surface = my_font.render(self.text, False, self.text_color)
        text_x = self.x + (self.width - text_surface.get_width()) // 2
        text_y = self.y + (self.height - text_surface.get_height()) // 2
        window.blit(text_surface, (text_x, text_y))

    def is_clicked(self, mouse_pos):
        if self.x <= mouse_pos[0] <= self.x + self.width and self.y <= mouse_pos[1] <= self.y + self.height:
            return True
        return False

class Slider:
    def __init__(self, x, y, width, height, min_value, max_value, initial_value, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.color = color

    def draw(self):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))
        slider_width = (self.value - self.min_value) / (self.max_value - self.min_value) * self.width
        pygame.draw.rect(window, (0, 100, 255), (self.x, self.y, slider_width, self.height))

    def update(self, mouse_pos):
        if self.x <= mouse_pos[0] <= self.x + self.width and self.y <= mouse_pos[1] <= self.y + self.height:
            self.value = (mouse_pos[0] - self.x) / self.width * (self.max_value - self.min_value) + self.min_value
            self.value = max(self.min_value, min(self.max_value, self.value))
            
slider = Slider(10, 250, 100, 20, 0, 100, 1, WHITE)
slider2 = Slider(10, 350, 100, 20, 0, 20, 0, WHITE)


pendulums = []
pendulum = Pendulum(150, 0, WIDTH // 2, HEIGHT//2, 1, 0.21)

button_force_1 = Button(10, 400, 100, 50, WHITE, "Force ->", BLACK)
button_force_0 = Button(10, 500, 100, 50, WHITE, "Force <-", BLACK)
button_reset = Button(10, 50, 100, 50, WHITE, "Reset", BLACK)
button_balance = Button(WIDTH-300, HEIGHT-100, 300, 50, WHITE, "Balance Pendulum", BLACK)

running = True
clock = pygame.time.Clock()  
t = 0
elapsed = 0
positive = False
while running:
    dt = clock.tick(60) / 250  # Target 60 frames per second, dt in seconds
    t += dt
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_reset.is_clicked(pygame.mouse.get_pos()):
                pendulum = Pendulum(150, random.randint(-360, 360), WIDTH // 2, HEIGHT//2, 1, 0.21)
            if button_force_1.is_clicked(pygame.mouse.get_pos()):
                pendulum.external_pivot_force = slider.value
            if button_force_0.is_clicked(pygame.mouse.get_pos()):
                pendulum.external_pivot_force = -slider.value
            if button_balance.is_clicked(pygame.mouse.get_pos()):
                pendulum.balance_pendulum = not pendulum.balance_pendulum
                pendulum.pivot_force = 0
                pendulum.integral_error = 0
        if event.type == pygame.MOUSEBUTTONUP:
            pendulum.external_pivot_force = 0
        
                
    if slider2.value != 0:
        elapsed += dt
        if elapsed >= slider2.value:
            elapsed = 0
            positive = not positive
            if positive:
                pendulum.external_pivot_force = slider.value
            else:
                pendulum.external_pivot_force = -slider.value
    
    mouse = pygame.mouse.get_pos()
    window.fill(BLACK)


    mouse_velocity = pygame.mouse.get_rel()
    pendulum.draw(dt)
    pendulum.update(dt)
    slider.update(mouse)
    slider2.update(mouse)
    
    button_force_1.draw()
    button_force_0.draw()
    button_reset.draw()
    button_balance.draw()
    slider.draw()
    slider2.draw()
    
    text_slider_force = my_font.render(f'Force magnitude: {round(slider.value)}N', False, (255, 0, 30))
    text_slider_period = my_font.render(f'Force period: {round(slider2.value)}s', False, (255, 0, 30))
    text_bob = my_font.render(pendulum.__str__(), False, (255, 0, 30))
    text_pivot = my_font.render(f'Force acting on pivot:\n{round(pendulum.pivot_force, 1)}N', False, (255, 0, 30))
    text_Fs = my_font.render(f'Fd: {round(pendulum.Fd, 1)}\nFp: {round(pendulum.Fp)}\n Fi: {round(pendulum.Fi)}', False, (255, 0, 30))
    text_error = my_font.render(f'Error: {round(math.degrees(pendulum.error), 2)}', False, (255, 0, 30))
    window.blit(text_slider_force, (10,190))
    window.blit(text_slider_period, (10,290))
    window.blit(text_Fs, (WIDTH-200, 300))
    window.blit(text_bob, (5,600))
    window.blit(text_error, (WIDTH-200,100))
    
    window.blit(text_pivot, (5,100))
    
    pygame


    pygame.display.flip()

pygame.quit()