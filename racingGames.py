import pygame
from pygame.locals import *
import random
import button 
import vehicle

pygame.init()
# color 
gray = (100, 100, 100)
green = (76, 208, 56)
yellow = (255, 232, 0)
red = (200, 0, 0)
white = (255, 255, 255)
# tao cua so 
width= 700
height = 650
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('Racing Games')
# khoi tao menu
# load menu button images
button_images_name = ['button_start.png','button_quit.png']
number_of_button=len(button_images_name)
buttons = []
for button_number,name in enumerate (button_images_name):
    image = pygame.image.load('images/' + name)
    button_temp = button.Button((width-image.get_width())/2, (height/number_of_button)*(button_number+0.5)-image.get_height()/2, image, 1)
    buttons.append(button_temp)
#load game over button
yes_img=pygame.image.load('images/button_yes.png').convert_alpha()
no_img=pygame.image.load('images/button_no.png').convert_alpha()
yes_button=button.Button((width-yes_img.get_width())/2*0.5,(height-yes_img.get_height())/4*3.0,yes_img,1)
no_button=button.Button((width-no_img.get_width())/2*1.5,(height-no_img.get_height())/4*3.0,no_img,1)
#yes_button=button.Button(0,0,yes_img,1)
# khoi tao bien
gameOver = False
speed = 6
score = 0

number_of_lane = 6
h_score = 0


# duong xe chay
road_width = number_of_lane*100
street_width = 10
street_height = 50
# lan duong xe chay
lanes = []
for i in range (number_of_lane):
    lanes.append(width/2-(number_of_lane/2)*100+i*100+50)
lane_move_y = 0
# road and edge
road = (lanes[0]-50, 0 , road_width, height)
left_edge = (lanes[0]-55, 0, street_width, height)
right_edge = (lanes[-1]+45, 0, street_width, height)
# vi tri ban dau xe ng choi

player_x = lanes[int((number_of_lane-1)/2)]
player_y = height/5*4
# sprite groups
player_group = pygame.sprite.Group()
vehicle_group = pygame.sprite.Group()
tree_group = pygame.sprite.Group()

# tao xe ng choi
player = vehicle.PlayerVehicle(player_x, player_y)
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
# area of tree
area_trees=[25,50,75,100,125,150,width-150,width-125,width-100,width-75,width-50,width-25]
area_of_tree_left = (0, 0 , 150, height)
area_of_tree_right = (width-150, 0 , 150, height)
# doi tuong cay
class tree(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        # scale img
        image_scale = 80 / image.get_rect().width
        new_width = image.get_rect().width * image_scale
        new_height = image.get_rect().height * image_scale
        self.image = pygame.transform.scale(image, (new_width, new_height))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
# create ramdon tree
tree_images_name=['tree 1.png', 'tree 2.png', 'tree 3.png']
trees_image=[]
for i in tree_images_name:
    image = pygame.image.load('images/' + i)
    trees_image.append(image)
# cai dat fps
clock = pygame.time.Clock()
fps = 120
waiting=True
running = True

#vòng lặp menu bắt đầu
while waiting:
    screen.fill(green)
    if buttons[0].draw(screen):
        waiting = False
    if buttons[1].draw(screen):
        waiting = False
        running = False
    for event in pygame.event.get():
        if event.type == QUIT:
            waiting = False
            running = False
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                waiting=False

    pygame.display.update()
# vong lap xu ly game

while running:
    # chinh frame hinh tren giay
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        # dieu khien xe
        if event.type == KEYDOWN:
            if event.key == K_LEFT and player.rect.center[0] > lanes[0]:
                player.rect.x -= 100
            if event.key == K_RIGHT and player.rect.center[0] < lanes[-1]:
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
    # draw area_of_tree
    pygame.draw.rect(screen,green,area_of_tree_left)
    pygame.draw.rect(screen,green,area_of_tree_right)   
    # ve edge - hanh lang duong
    pygame.draw.rect(screen, yellow, left_edge)
    pygame.draw.rect(screen, yellow, right_edge)
    # ve lane duong
    lane_move_y += speed * 2
    if lane_move_y >= street_height * 2:
        lane_move_y = 0
    for y in range(street_height * -2, height, street_height * 2):
        for lane in range(number_of_lane-1) : 
            pygame.draw.rect(screen, white, (lanes[lane] + 45, y + lane_move_y, street_width, street_height))
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
            vehicle_car = vehicle.vehicle(image, lane, height / -2)
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
                speed += 0.5
    # ve nhom xe luu thong
    vehicle_group.draw(screen)
     # draw tree
    if len(tree_group) < 20:
        add_tree = True
        for i in tree_group:
            if i.rect.top < i.rect.height * 1.5:
                add_tree = False
        if add_tree:
            area_tree = random.choice(area_trees)
            image = random.choice(trees_image)
            trees = tree(image, area_tree, -100)
            tree_group.add(trees)
    # move tree
    for trees in tree_group:
        trees.rect.y += speed
        # remove the tree
        if trees.rect.top >= height:
            trees.kill()
    tree_group.draw(screen)
    # hien thi diem
    font = pygame.font.Font(pygame.font.get_default_font(), 24)
    text = font.render(f'Score: {score}', True, white)
    text_rect = text.get_rect()
    text_rect.center = (50, 40)
    screen.blit(text, text_rect)
    if(score >= h_score):
        h_score = score

    if gameOver:
        pygame.draw.rect(screen, green, (0, 0, 100, 100))
        screen.blit(crash, crash_rect)
        pygame.draw.rect(screen, red, (0, 50, width, 100))
        font = pygame.font.Font(pygame.font.get_default_font(), 40)
        text_h_score = font.render(f'High Score: {h_score}', True, white)
        text_rect_score= text_h_score.get_rect()
        text_rect_score.center = (width/2, height/3)
        screen.blit(text_h_score, text_rect_score)
        font = pygame.font.Font(pygame.font.get_default_font(), 30)
        text = font.render(f'Your Score: {score}', True, white)
        text_rect = text.get_rect()
        text_rect.center = (width/2,height/3+100)
        screen.blit(text, text_rect)
        text = font.render(f'Game over! Play again? (Yes / No)', True, white)
        text_rect = text.get_rect()
        text_rect.center = (width/2, 100)
        screen.blit(text, text_rect)
        yes_button.draw(screen)
        no_button.draw(screen)
        
 
    pygame.display.update()

    while gameOver:
        clock.tick(fps)
        #nút yes
        if yes_button.draw(screen):
            # reset game
            gameOver = False
            score = 0
            speed = 3
            vehicle_group.empty()
            player.rect.center = [player_x, player_y]
        if no_button.draw(screen):
            gameOver = False
            running = False
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
                    speed = 3
                    vehicle_group.empty()
                    player.rect.center = [player_x, player_y]
                elif event.key == K_n:
                    # exit game
                    gameOver = False
                    running = False
pygame.quit()

