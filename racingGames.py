import pygame
from pygame.locals import *
import random
import button 
import vehicle
import tree
import pandas as pd

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
height = 650
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
# full màn hình
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('Racing Games')
# khoi tao menu
# load lane select menu button images
select_button_images_name = ['button_3.png','button_4.png','button_5.png','button_6.png']
number_of_button=len(select_button_images_name)
select_buttons = []
for button_number,name in enumerate (select_button_images_name):
    image = pygame.image.load('images/' + name)
    scale=(width/number_of_button*(number_of_button-0.5))/number_of_button/image.get_width()
    button_temp = button.Button( (width/number_of_button)*(button_number+0.5)-image.get_width()/2*scale,(height-image.get_height()*scale)/3*2, image, scale)
    select_buttons.append(button_temp)
# load car select menu button images
select_car_images_name = ['car_1.png','car_2.png','car_3.png','car_4.png','car_5.png','car_6.png','car_7.png','car_8.png']
number_of_button=len(select_car_images_name)
select_cars = []
for button_number,name in enumerate (select_car_images_name):
    image = pygame.image.load('images/' + name)
    scale=(width/number_of_button*(number_of_button-0.5))/number_of_button/image.get_width()
    button_temp = button.Button( (width/number_of_button)*(button_number+0.5)-image.get_width()/2*scale,(height-image.get_height()*scale)/3*2, image, scale)
    select_cars.append(button_temp)
# load menu button images
button_images_name = ['button_start.png','button_select_car.png','button_high_scores.png','button_quit.png']
number_of_button=len(button_images_name)+1
buttons = []
for button_number,name in enumerate (button_images_name):
    image = pygame.image.load('images/' + name)
    scale=(height/number_of_button*(number_of_button-0.5))/number_of_button/image.get_height()
    button_temp = button.Button((width-image.get_width()*scale)/2, (height/number_of_button)*(button_number+1.5)-image.get_height()/2*scale, image, scale)
    buttons.append(button_temp)
#load game over and return button
yes_img=pygame.image.load('images/button_yes.png')
no_img=pygame.image.load('images/button_no.png')
pause_img=pygame.image.load('images/pause.png')
quit_img=pygame.image.load('images/button_quit.png')
yes_button=button.Button((width-yes_img.get_width())/2*0.5,(height-yes_img.get_height())/7*5.0,yes_img,1)
no_button=button.Button((width-no_img.get_width())/2*1.5,(height-no_img.get_height())/7*5.0,no_img,1)
pause_button=button.Button(width-100,height-100,pause_img,85/pause_img.get_width())
continue_img=pygame.image.load('images/continue.png')
scale=170/continue_img.get_width()
continue_button=button.Button((width-continue_img.get_width()*scale)/2,(height-continue_img.get_height()*scale)/2,continue_img,scale)
quit_button=button.Button((width-no_img.get_width())/2.3,(height-no_img.get_height())/1.3,quit_img,1)
return_img=pygame.image.load('images/button_return.png')
return_button=button.Button((width-return_img.get_width())/2,height*0.8,return_img,1)
# load button của high score menu
all_img=pygame.image.load('images/button_all.png')
your_img=pygame.image.load('images/button_your.png')
all_button=button.Button(20,height*0.2,all_img,1)
your_button=button.Button(20,height*0.5,your_img,1)

# load boost, extra score and return image
boost_image=pygame.image.load('images/boost.png')
alert_image=pygame.image.load('images/alert.png')
extra_score_image=pygame.image.load('images/extra_score.png')
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
# khoi tao bien
car_name='car_1.png'
score = 0
score_for_speed_up = 4
# Read CSV
h_scores = pd.read_csv('highScore.csv', usecols=['name', 'highScore'])
h_scores=h_scores.drop_duplicates(keep='first')
h_scores.sort_values(["highScore"],axis=0, ascending=[False],inplace=True) 
h_scores.fillna('', inplace=True)
number_of_lane = 5
gameOver = False
running=True
waiting=True
not_pause=True
boost_start_time=pygame.time.get_ticks()
boost_spawn_time=pygame.time.get_ticks()
extra_spawn_time=pygame.time.get_ticks()
alert_time=pygame.time.get_ticks()
alert_tick=8
# khoi tao input box 
input_font = pygame.font.Font(None, 50)
input_box = pygame.Rect(width/2-70, height/number_of_button*0.35, 140, 50)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
active = False
player_name = ''

while running:
    # duong xe chay
    speed = 4
    boost_status=False
    road_width = number_of_lane*100
    street_width = 10
    street_height = 50
    score_list=h_scores
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
    extra_score_group = pygame.sprite.Group()
    tree_group = pygame.sprite.Group()
    boost_group = pygame.sprite.Group()
    alert_group = pygame.sprite.Group()

    # tao xe ng choi
    player = vehicle.vehicle(pygame.image.load('images/' + car_name),player_x, player_y)
    player_group.add(player)
    # cai dat fps
    clock = pygame.time.Clock()
    fps = 120
    playing = True
    selecting = False
    selecting_car = False
    seeing_h_scores = False
    #vòng lặp menu bắt đầu
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                waiting = False
                running = False
                playing = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    elif event.key == pygame.K_DELETE:
                        player_name = ''
                    elif len(player_name)<20:
                        player_name += event.unicode
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
        #menu chọn số lượng lane
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
        #menu chọn xe
        elif selecting_car:
            pygame.draw.rect(screen, black, (0, 50, width, 100))
            text = input_font.render(f'Select your car', True, white)
            text_rect = text.get_rect()
            text_rect.center = (width/2, 100)
            screen.blit(text, text_rect)
            for index,select in enumerate (select_cars):
                if select.draw(screen):
                    car_name=select_car_images_name[index]
                    selecting_car = False
        #xem điểm high score
        elif seeing_h_scores:
            pygame.draw.rect(screen, black, (width/2-233, 60, 666, 440))
            text = input_font.render(f'HIGH SCORES', True, white)
            text_rect = text.get_rect()
            text_rect.center = (width/2+100, 100)
            screen.blit(text, text_rect)
            text = input_font.render(f'Name', True, white)
            text_rect = text.get_rect()
            text_rect.left = width/2-218
            text_rect.top = 150
            screen.blit(text, text_rect)
            text = input_font.render(f'Score', True, white)
            text_rect = text.get_rect()
            text_rect.left = width/2+418-text_rect.width
            text_rect.top = 150
            screen.blit(text, text_rect)
            if your_button.draw(screen):
                score_list=h_scores.loc[h_scores['name'] == player_name]
            if all_button.draw(screen):
                score_list=h_scores
            for index in range(min(6,len(score_list.index))):
                #ten nguoi choi
                text = input_font.render(f'{score_list.iloc[[index],[0]].to_string(header=None, index=False)}', True, white)
                text_rect = text.get_rect()
                text_rect.left = width/2-218
                text_rect.top = 200+index*50
                screen.blit(text, text_rect)
                #diem so
                text = input_font.render(f'{score_list.iloc[[index],[1]].to_string(header=None, index=False)}', True, white)
                text_rect = text.get_rect()
                text_rect.left = width/2+418-text_rect.width
                text_rect.top = 200+index*50
                screen.blit(text, text_rect)

            if return_button.draw(screen):
                seeing_h_scores=False
        else:
            if buttons[0].draw(screen):
                selecting= True
            elif buttons[1].draw(screen):
                selecting_car = True
            elif buttons[2].draw(screen):
                seeing_h_scores = True
            elif buttons[-1].draw(screen):
                waiting = False
                running = False
                playing = False
            # Render the current text.
            txt_surface = input_font.render(player_name, True, color)
            # Resize the box if the text is too long.
            input_width = max(200, txt_surface.get_width()+10)
            input_box.w = input_width
            input_box.left= width/2-input_width/2+100
            # Draw input box background
            pygame.draw.rect(screen, black, (input_box.left-225, input_box.y-20, input_width+250, 90))
            text = input_font.render(f'Your name:', True, white)
            text_rect = text.get_rect()
            text_rect.y = input_box.y+7
            text_rect.left = input_box.left-200
            screen.blit(text, text_rect)
            # Blit the text
            screen.blit(txt_surface, (input_box.x+5, input_box.y+7))
            # Blit the input_box rect.
            pygame.draw.rect(screen, color, input_box, 2)     
        pygame.display.update()
    # vong lap xu ly game
    while playing:
        # chinh frame hinh tren giay
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
        for extra_score in extra_score_group:
            if pygame.sprite.collide_rect(player, extra_score):
                score+=2
                extra_score.kill()
        for boost in boost_group:
            if pygame.sprite.collide_rect(player, boost):
                speed+= 3
                boost_start_time=pygame.time.get_ticks()
                boost_status=True
                boost.kill()
        if pygame.time.get_ticks()-boost_start_time>4000 and boost_status:
            speed-=3
            boost_status=False
        # check va cham 
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
                if vehicle_car.rect.top < vehicle_car.rect.height*speed :
                    add_vehicle = False
            vehicle_lanes = list(range(0,number_of_lane))
            random.shuffle(vehicle_lanes)
            while add_vehicle and len(vehicle_lanes)>1:
                add_vehicle = False
                lane = lanes[vehicle_lanes[0]]
                vehicle_lanes.pop(0)
                image = random.choice(vehicle_images)
                vehicle_car = vehicle.vehicle(image, lane, height / -2)
                overlap=False
                for extra_score in extra_score_group:
                    if pygame.sprite.collide_rect(vehicle_car,extra_score):
                        overlap=True
                if not(overlap):
                    vehicle_group.add(vehicle_car)
                    alert = vehicle.vehicle(alert_image, lane, 50)
                    alert_group.add(alert)
                if(random.randint(0,100)<number_of_lane*speed):
                    add_vehicle = True
        if (pygame.time.get_ticks()-extra_spawn_time)%3000<10 and len(extra_score_group)<1:
            extra_spawn_time=pygame.time.get_ticks()
            if(random.randint(0,100)<50):
                lane = lanes[random.randint(0,number_of_lane-1)]
                extra_score = vehicle.vehicle(extra_score_image, lane, height / -2)
                extra_score_group.add(extra_score)
                for vehicle_car in vehicle_group:
                    if pygame.sprite.collide_rect(extra_score, vehicle_car):
                        vehicle_car.kill()
        if (pygame.time.get_ticks()-boost_spawn_time)%4000<10 and(not boost_status )and len(boost_group)<1:
            add_boost=True
            boost_spawn_time=pygame.time.get_ticks()
            if(add_boost and random.randint(0,100)<30):
                lane = lanes[random.randint(0,number_of_lane-1)]
                boost = vehicle.vehicle(boost_image, lane, height / -2)
                boost_group.add(boost)
                for vehicle_car in vehicle_group:
                    if pygame.sprite.collide_rect(boost, vehicle_car):
                        vehicle_car.kill()
        #move extra score
        for extra_score in extra_score_group:
            extra_score.rect.y += speed 
            # remove extra score
            if extra_score.rect.top >= height:
                extra_score.kill()
        #move boost
        for boost in boost_group:
            boost.rect.y += speed 
            # remove boost
            if boost.rect.top >= height:
                boost.kill()
        #draw extra score
        extra_score_group.draw(screen)
        boost_group.draw(screen)
        if pygame.time.get_ticks()-alert_time>150 or alert_tick%2==0:
            alert_group.draw(screen)
            if pygame.time.get_ticks()-alert_time>150:
                alert_tick-=1
                alert_time=pygame.time.get_ticks()
        for alert in alert_group:
            if pygame.sprite.spritecollide(alert, vehicle_group, False)or pygame.sprite.spritecollide(alert, extra_score_group, False)or pygame.sprite.spritecollide(alert, boost_group, False):  
                alert.kill()
        # cho xe cong cong chay
        for vehicle_car in vehicle_group:
            vehicle_car.rect.y += speed 
            # remove the vehicle
            if vehicle_car.rect.top >= height:
                vehicle_car.kill()
                score += 1
        # tang toc do chay
            if score > score_for_speed_up :
                score_for_speed_up+=speed
                speed +=0.5
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
        text_rect.top=40
        text_rect.left=5
        screen.blit(text, text_rect)
        text = font.render(f'Speed: {round(speed,1)}', True, white)
        text_rect = text.get_rect()
        text_rect.top=80
        text_rect.left=5
        screen.blit(text, text_rect)
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
            new_score=[player_name, score]
            h_scores.loc[len(h_scores)]=new_score
            h_scores.sort_values(["highScore"],axis=0, ascending=[False],inplace=True) 
            h_scores=h_scores.drop_duplicates(keep='first')
            h_scores.fillna('', inplace=True)
            boost_status=False
            screen.blit(crash, crash_rect)
            pygame.draw.rect(screen, black, (0, 50, width, 100))
            font = pygame.font.Font(pygame.font.get_default_font(), 40)
            pygame.draw.rect(screen, black, (width/2-195, height/19*5, 390, 190))
            text_h_score = font.render(f'High Score: {h_scores.iloc[[0],[1]].to_string(header=None, index=False)}', True, white)
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
            if quit_button.draw(screen):
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
                score_for_speed_up = 4
                score = 0
                speed = 4
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
                        score_for_speed_up = 4
                        score = 0
                        speed = 4
                        vehicle_group.empty()
                        player.rect.center = [player_x, player_y]
                    elif event.key == K_n:
                        # exit game
                        gameOver = False
                        playing = False
                        waiting = True

h_scores.to_csv("highScore.csv",index=False)
pygame.quit()

