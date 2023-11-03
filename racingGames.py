import pygame
from pygame.locals import *
import random
pygame.init()
# color 
gray = (100, 100, 100)
green = (76, 208, 56)
yellow = (255, 232, 0)
red = (200, 0, 0)
white = (255, 255, 255)
# tao cua so game
width= 500
height = 500
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Racing Games')
# khoi tao bien
gameOver = False
speed = 2
score = 0
# duong xe chay
road_width = 300
street_width = 10
street_height = 50
# lan duong xe chay
lane_left = 150
land_center = 250
lane_right = 350
lanes = [lane_left, land_center, lane_right]
lane_move_y = 0
# road and edge
road = (100, 0 , road_width, height)
left_edge = (95, 0, street_width, height)
right_edge = (395, 0, street_width, height)
# vi tri ban dau xe ng choi
player_x = 250
player_y = 400
# doi tuong xe luu thong
class vehicle(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        # scale img
        image_scale = 45 / image.get_rect().width
        new_width = image.get_rect().width * image_scale
        new_height = image.get_rect().height * image_scale
        self.image = pygame.transform.scale(image, (new_width, new_height))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
# doi tuong xe player
class PlayerVehicle(vehicle):
    def __init__(self, x, y):
        image = pygame.image.load('images/car.png')
        super().__init__(image, x, y)
# sprite groups
player_group = pygame.sprite.Group()
vehicle_group = pygame.sprite.Group()
# tao xe ng choi
player = PlayerVehicle(player_x, player_y)
player_group.add(player)
# load xe luu thong
image_name = ['pickup_truck.png', 'semi_trailer.png', 'taxi.png', 'van.png']
vehicle_images = []
for name in image_name:
    image = pygame.image.load('images/' + name)
    vehicle_images.append(image)
# load hinh va cham
crash = pygame.image.load('images/crash.png')
crash_rect = crash.get_rect()


# cai dat fps
clock = pygame.time.Clock()
fps = 120
# vong lap xu ly game
running = True
while running:
    # chinh frame hinh tren giay
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        # dieu khien xe
        if event.type == KEYDOWN:
            if event.key == K_LEFT and player.rect.center[0] > lane_left:
                player.rect.x -= 100
            if event.key == K_RIGHT and player.rect.center[0] < lane_right:
                player.rect.x += 100
            # check va cham khi dieu khien
            for vehicle_car in vehicle_group:
                if pygame.sprite.collide_rect(player, vehicle_car):
                    gameOver = True
    # check va cham khi xe dung in
    if pygame.sprite.spritecollide(player, vehicle_group, True):
        gameOver = True
        crash_rect.center = [player.rect.center[0], player.rect.top]

    # ve dia hinh co
    screen.fill(green)
    # ve road 
    pygame.draw.rect(screen, gray, road)
    # ve edge - hanh lang duong
    pygame.draw.rect(screen, yellow, left_edge)
    pygame.draw.rect(screen, yellow, right_edge)
    # ve lane duong
    lane_move_y += speed * 2
    if lane_move_y >= street_height * 2:
        lane_move_y = 0
    for y in range(street_height * -2, height, street_height * 2):
        pygame.draw.rect(screen, white, (lane_left + 45, y + lane_move_y, street_width, street_height))
        pygame.draw.rect(screen, white, (land_center + 45, y + lane_move_y, street_width, street_height))
    # ve xe player
    player_group.draw(screen)
    # ve phuong tien giao thong
    if len(vehicle_group) < 2:
        add_vehicle = True
        for vehicle_car in vehicle_group:
            if vehicle_car.rect.top < vehicle_car.rect.height * 1.5:
                add_vehicle = False
        if add_vehicle:
            lane = random.choice(lanes)
            image = random.choice(vehicle_images)
            vehicle_car = vehicle(image, lane, height / -2)
            vehicle_group.add(vehicle_car)
    # cho xe cong cong chay
    for vehicle_car in vehicle_group:
        vehicle_car.rect.y += speed
        # remove the vehicle
        if vehicle_car.rect.top >= height:
            vehicle_car.kill()
            score += 1
            # tang toc do chay
            if score > 0 and score % 5 == 0:
                speed += 1
    # ve nhom xe luu thong
    vehicle_group.draw(screen)
    # hien thi diem
    font = pygame.font.Font(pygame.font.get_default_font(), 16)
    text = font.render(f'Score: {score}', True, white)
    text_rect = text.get_rect()
    text_rect.center = (50, 40)
    screen.blit(text, text_rect)

    if gameOver:
        screen.blit(crash, crash_rect)
        pygame.draw.rect(screen, red, (0, 50, width, 100))
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render(f'Game over! Play again? (Yes / No)', True, white)
        text_rect = text.get_rect()
        text_rect.center = (width/2, 100)
        screen.blit(text, text_rect)
 
    pygame.display.update()

    while gameOver:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == QUIT:
                gameOver = False
                running = False
            # dieu khien xe
            if event.type == KEYDOWN:
                if event.key == K_y:
                    # reset game
                    gameOver = False
                    score = 0
                    speed = 2
                    vehicle_group.empty()
                    player.rect.center = [player_x, player_y]
                elif event.key == K_n:
                    # exit game
                    gameOver = False
                    running = False
pygame.quit()

