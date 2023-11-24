import pygame
from pygame.locals import *
import random
import button 
import vehicle
import tree

pygame.init()
# color 
gray = (100, 100, 100)
green = (76, 208, 56)
yellow = (255, 232, 0)
red = (200, 0, 0)
white = (255, 255, 255)
black = (0,0,0)
# tao cửa sổ
width= 900
height = 750
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)

# full màn hình
# background
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('Racing Games')
# khoi tao menu
# load menu button images
button_images_name = ['button_start.png','button_select_car.png','button_quit.png']
number_of_button=len(button_images_name)
buttons = []
for button_number,name in enumerate (button_images_name):
    image = pygame.image.load('images/' + name)
    button_temp = button.Button((width-image.get_width())/2, (height/number_of_button)*(button_number+0.5)-image.get_height()/2, image, 1)
    buttons.append(button_temp)
# load lane select menu button images
select_button_images_name = ['button_3.png','button_4.png','button_5.png','button_6.png']
number_of_select_button=len(select_button_images_name)
select_buttons = []
for button_number,name in enumerate (select_button_images_name):
    image = pygame.image.load('images/' + name)
    button_temp = button.Button( (width/number_of_select_button)*(button_number+0.5)-image.get_width()/2,(height-image.get_height())/3*2, image, 1)
    select_buttons.append(button_temp)
# load car select menu button images
select_car_images_name = ['car_1.png','car2.png','car3.png','car4.png','car5.png','car6.png','car7.png','car8.png']
number_of_select_car=len(select_car_images_name)
select_cars = []
for car_number,name in enumerate (select_car_images_name):
    image = pygame.image.load('images/' + name)
    car_temp = button.Button( (width/number_of_select_car)*(car_number+0.5)-image.get_width()/2,(height-image.get_height())/3*2, image, 1)
    select_cars.append(car_temp)
#load game over button
yes_img=pygame.image.load('images/button_yes.png')
no_img=pygame.image.load('images/button_no.png')
pause_img=pygame.image.load('images/pause.png')
quit_img=pygame.image.load('images/button_quit.png')
yes_button=button.Button((width-yes_img.get_width())/2*0.5,(height-yes_img.get_height())/7*5.0,yes_img,1)
no_button=button.Button((width-no_img.get_width())/2*1.5,(height-no_img.get_height())/7*5.0,no_img,1)
pause_button=button.Button(width-100,height-100,pause_img,0.3)
continue_img=pygame.image.load('images/Fast_Forward_Idle.png')
continue_button=button.Button(width/2.3,height/2.9,continue_img,2)
quit_button=button.Button((width-no_img.get_width())/2.3,(height-no_img.get_height())/1.3,quit_img,1)
# khoi tao bien
car_name='car_1.png'
score = 0
f = open("highScore.txt","r")
h_score = int(f.read())
f.close()
number_of_lane = 5
gameOver = False
running=True
waiting=True
not_pause=True

while running:

    # duong xe chay
    speed = 4
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
    # vi tri cay
    tree_left_edge_min=min(0,lanes[0]-100)
    tree_left_edge_max=max(0,lanes[0]-100)
    tree_right_edge_min=min(lanes[-1]+100,width)
    tree_right_edge_max=max(lanes[-1]+100,width)
    # sprite groups
    player_group = pygame.sprite.Group()
    vehicle_group = pygame.sprite.Group()
    tree_group = pygame.sprite.Group()

    # tao xe ng choi
    player = vehicle.vehicle(pygame.image.load('images/' + car_name),player_x, player_y)
    player_group.add(player)

    # load xe luu thong
    image_name = ['pickup_truck.png', 'semi_trailer.png', 'taxi.png', 'van.png','canhsat.png','firetruck.png','blackcarvip.png','xecuuthuong.png','publiccar1.png','publiccar2.png','publiccar3.png']
    vehicle_images = []
    for name in image_name:
        image = pygame.image.load('images/' + name)
        vehicle_images.append(image)
    # load hinh va cham
    crash = pygame.image.load('images/crash.png')
    crash_rect = crash.get_rect()
    # create ramdon tree
    tree_images_name=['tree_1.png', 'tree_2.png', 'tree_3.png', 'tree_4.png', 'tree_5.png', 'tree_6.png']
    trees_image=[]
    for i in tree_images_name:
        image = pygame.image.load('images/' + i)
        trees_image.append(image)
    # cai dat fps
    clock = pygame.time.Clock()
    fps = 120
    playing = True
    selecting = False
    selecting_car = False
    #vòng lặp menu bắt đầu
    while waiting:
        clock.tick(fps)
        # ve dia hinh co
        screen.fill(green)
        # ve road 
        pygame.draw.rect(screen, gray, road)
        # ve edge - hanh lang duong
        pygame.draw.rect(screen, yellow, left_edge)
        pygame.draw.rect(screen, yellow, right_edge)
        lane_move_y += speed *1.5
        if lane_move_y >= street_height * 2:
            lane_move_y = 0
        for y in range(street_height * -2, height, street_height * 2):
            for lane in range(number_of_lane-1) : 
                pygame.draw.rect(screen, white, (lanes[lane] + 45, y + lane_move_y, street_width, street_height))
        # draw tree
        if len(tree_group) < 25:
            add_tree = True
            for i in tree_group:
                if i.rect.top < i.rect.height * (random.uniform(0.2,0.5)):
                    add_tree = False
            if add_tree:              
                for i in range(random.randint(0, 10)):
                    image = random.choice(trees_image)
                    area_tree = random.choice([random.randint(tree_left_edge_min,tree_left_edge_max),random.randint(tree_right_edge_min,tree_right_edge_max)])
                    trees = tree.Tree(image, area_tree, -200)
                    tree_group.add(trees)
        # move tree
        for trees in tree_group:
            trees.rect.y += speed*1.5
            # remove the tree
            if trees.rect.top >= height:
                trees.kill()
        tree_group.draw(screen)
        #vẽ nút
        if selecting:
            playing = False
            pygame.draw.rect(screen, black, (0, 50, width, 100))
            font = pygame.font.Font(pygame.font.get_default_font(), 30)
            text = font.render(f'Select number of lanes', True, white)
            text_rect = text.get_rect()
            text_rect.center = (width/2, 100)
            screen.blit(text, text_rect)
            for index,select in enumerate (select_buttons):
                if select.draw(screen):
                    number_of_lane = 3+index
                    selecting = False
                    waiting = False
        elif selecting_car:
            pygame.draw.rect(screen, black, (0, 50, width, 100))
            font = pygame.font.Font(pygame.font.get_default_font(), 30)
            text = font.render(f'Select your car', True, white)
            text_rect = text.get_rect()
            text_rect.center = (width/2, 100)
            screen.blit(text, text_rect)
            for index,select in enumerate (select_cars):
                if select.draw(screen):
                    car_name=select_car_images_name[index]
                    selecting_car = False
        else:            
            if buttons[0].draw(screen):
                selecting= True
            elif buttons[1].draw(screen):
                selecting_car = True
            elif buttons[2].draw(screen):
                waiting = False
                running = False
                playing = False
        for event in pygame.event.get():
            if event.type == QUIT:
                waiting = False
                running = False
                playing = False
        pygame.display.update()
    # vong lap xu ly game
    while playing:
        # chinh frame hinh tren giay
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                waiting = False
                playing = False
                not_pause = True
            # dieu khien xe
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    not_pause = False
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
        # ve edge - hanh lang duong
        pygame.draw.rect(screen, yellow, left_edge)
        pygame.draw.rect(screen, yellow, right_edge)    # ve lane duong
        lane_move_y += speed *1.5
        if lane_move_y >= street_height * 2:
            lane_move_y = 0
        for y in range(street_height * -2, height, street_height * 2):
            for lane in range(number_of_lane-1) : 
                pygame.draw.rect(screen, white, (lanes[lane] + 45, y + lane_move_y, street_width, street_height))
        # ve xe player
        player_group.draw(screen)

        # ve phuong tien giao thong
        if len(vehicle_group) < number_of_lane/2+speed:
            add_vehicle = True 
            for vehicle_car in vehicle_group:
                if vehicle_car.rect.top < vehicle_car.rect.height * 1:
                    add_vehicle = False
            vehicle_lanes = list(range(0,number_of_lane))
            random.shuffle(vehicle_lanes)
            while add_vehicle and len(vehicle_lanes)>1:
                add_vehicle = False
                lane = lanes[vehicle_lanes[0]]
                vehicle_lanes.pop(0)
                image = random.choice(vehicle_images)
                vehicle_car = vehicle.vehicle(image, lane, height / -2)
                vehicle_group.add(vehicle_car)
                if(random.randint(0,100)<number_of_lane*speed):
                    add_vehicle = True
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
        if len(tree_group) < 25:
            add_tree = True
            for i in tree_group:
                if i.rect.top < i.rect.height * (random.uniform(0.2,0.5)):
                    add_tree = False
            if add_tree:              
                for i in range(random.randint(0, 10)):
                    image = random.choice(trees_image)
                    area_tree = random.choice([random.randint(tree_left_edge_min,tree_left_edge_max),random.randint(tree_right_edge_min,tree_right_edge_max)])
                    trees = tree.Tree(image, area_tree, -100)
                    tree_group.add(trees)
        # move tree
        for trees in tree_group:
            trees.rect.y += speed*1.5
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
        # pause icon
        if not_pause:
            if pause_button.draw(screen):
                not_pause = False
            
        if not_pause==False:
            pygame.draw.rect(screen, black, (0, 50, width, 150))
            continue_button.draw(screen)     
            quit_button.draw(screen)
            font = pygame.font.Font(pygame.font.get_default_font(), 40)
            text_pasue_game=font.render('Your Game is PAUSE!!!', True, white)
            text_pasue_rect= text_pasue_game.get_rect()
            text_pasue_rect.center = (width/2, height/5)
            screen.blit(text_pasue_game,text_pasue_rect)

        if gameOver:
            screen.blit(crash, crash_rect)
            pygame.draw.rect(screen, black, (0, 50, width, 100))
            font = pygame.font.Font(pygame.font.get_default_font(), 40)
            pygame.draw.rect(screen, black, (width/2-195, height/19*5, 390, 190))
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
        
        while not_pause == False:
            clock.tick(fps)
            if continue_button.draw(screen):
                gameOver = False
                not_pause=True
            if no_button.draw(screen):
                gameOver = False
                playing = False
                waiting = True   
                not_pause=True 
                
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                    waiting = False
                    playing = False
                    not_pause=True
                

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
                playing = False
                waiting = True
            for event in pygame.event.get():
                if event.type == QUIT:
                    gameOver = False
                    running = False
                    waiting = False
                    playing = False
                # dieu khien xe
                if event.type == KEYDOWN:
                    if event.key == K_y:
                        # reset game
                        gameOver = False
                        score = 0
                        speed = 4
                        vehicle_group.empty()
                        player.rect.center = [player_x, player_y]
                    elif event.key == K_n:
                        # exit game
                        gameOver = False
                        playing = False
                        waiting = True

f = open("highScore.txt","w")
f.write(str(h_score))
f.close()
pygame.quit()

