"""
Project) 오락실 PANG 게임 만들기
[게임 조건]
1. 캐릭터는 화면 아래에 위치, 좌우로만 이동 가능
2. 스페이스를 누르면 무기를 쏘아 올림
3. 큰 공 1개가 나타나서 바운스
4. 무기에 닿으면 공은 작은 크기 2개로 분할, 가장 작은 크기의 공은 사라짐
5. 모든 공을 없애면 게임 종료(성공)
6. 캐릭터는 공에 닿으면 게임 종료(실패)
7. 시간 제한 99초 초과 시 게임 종료(실패)
8. FPS는 30으로 고정(필요시 speed값을 조정)

[게임 이미지]
1. 배경 : 640*480(가로 세로)
2. 무대 : 640*50
3. 캐릭터 : 33*60
4. 무기 : 20*430
5. 공 : 160*160, 80*80, 40*40, 20*20
"""
import os
import pygame
#################################################################
#반드시 해야 하는 기본 초기화
pygame.init()  

#화면 크기 설정
screen_width = 640  #가로 크기
screen_height = 480  #세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

#화면 타이틀 설정
pygame.display.set_caption("JHK_GAME") 

#FPS
clock = pygame.time.Clock()
#################################################################
#1. 사용자 게임 초기화(배경 화면, 게임 이미지, 좌표, 속도, 폰트)

#절대 경로가 아닌 위치 반환 함수를 이용하여 이미지 업로드하기!
current_path = os.path.dirname(__file__) #현재 파일의 위치 반환
image_path = os.path.join(current_path, "pygameproject/images") #images 폴더 위치 반환

#배경 만들기
background = pygame.image.load(os.path.join(image_path, "background.png"))

#스테이지 만들기
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1] #스테이지의 높이 위에 캐릭터를 두기 위해 사용

#캐릭터 만들기
character = pygame.image.load(os.path.join(image_path, "character_basic.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width - character_width) / 2
character_y_pos = screen_height - character_height - stage_height

#캐릭터 이동 방향
character_to_x = 0

#캐릭터 이동 속도
character_speed = 5

#무기 만들기
weapon = pygame.image.load(os.path.join(image_path, "weapon_basic.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

#무기는 한 번에 여러 발 발사 가능하다고 가정
weapons = []

#무기 이동 속도
weapon_speed = 10

#공 만들기(4개 따로 처리)
ball_images = [
  pygame.image.load(os.path.join(image_path, "balloon1.png")),
  pygame.image.load(os.path.join(image_path, "balloon2.png")),
  pygame.image.load(os.path.join(image_path, "balloon3.png")),
  pygame.image.load(os.path.join(image_path, "balloon4.png"))]

#공 크기에 따른 최초 스피드(y축 방향)
ball_speed_y = [-18, -15, -12, -9] #index 0, 1, 2, 3에 대응되는 값

#공 정보 : 공들은 정보들이 많으므로 딕셔너리로 관리
balls = []

#처음 공 추가
balls.append({
  "pos_x" : 50, #공의 x좌표
  "pos_y" : 50, #공의 y좌표
  "img_idx" : 0, #공의 크기 (이미지 index로 설정)
  "to_x" : 3, #공의 x축 이동방향 (양이면 왼쪽, 음이면 오른쪽)
  "to_y" : -6,  #공의 y축 이동방향 
  "init_spd_y" : ball_speed_y[0] #y 최초 속도 (스피드 index로 설정)
})

#사라질 무기, 공 정보 저장 변수
weapon_to_remove = -1
ball_to_remove = -1

#폰트 정의
game_font = pygame.font.Font(None, 40)
total_time = 100 
start_ticks = pygame.time.get_ticks() #시작 시각 정의

#게임 종료 메시지
game_result = "GAME OVER"

running = True  
while running:
  dt = clock.tick(20)  

  #2. 이벤트 처리 (키보드, 마우스 등)
  for event in pygame.event.get():  
    if event.type == pygame.QUIT:  
        running = False  

    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_LEFT:
        character_to_x -= character_speed
      elif event.key == pygame.K_RIGHT:
        character_to_x += character_speed
      elif event.key == pygame.K_SPACE: #무기 발사
        weapon_x_pos = character_x_pos + (character_width - weapon_width) / 2
        weapon_y_pos = character_y_pos
        weapons.append([weapon_x_pos, weapon_y_pos])

    if event.type == pygame.KEYUP:
      if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
        character_to_x = 0

  #3. 게임 캐릭터 위치 정의
  character_x_pos += character_to_x

  if character_x_pos < 0:
    character_x_pos = 0
  elif character_x_pos > screen_width - character_width:
    character_x_pos = screen_width - character_width

  #무기 위치 조정
  weapons = [[w[0], w[1] - weapon_speed] for w in weapons]
  #x는 그대로 두고, y좌표는 원래값에서 weapon_speed만큼 줄어들어야 함 -> 올라가는 동작

  #천장에 닿은 무기 없애기
  weapons = [[w[0], w[1]] for w in weapons if w[1] > 0]
  #weapon의 y좌표값이 0보다 클 경우(천장에 닿지 않은 무기들)의 무기들만 인덱싱하기

  #공 위치 정의
  for ball_idx, ball_val in enumerate(balls): 
    #enumerate 함수 : 리스트의 인덱스와 인덱스에 해당하는 값을 튜플 객체로 만들어서 반복
    ball_pos_x = ball_val["pos_x"]
    ball_pos_y = ball_val["pos_y"]
    ball_img_idx = ball_val["img_idx"]

    ball_size = ball_images[ball_img_idx].get_rect().size
    ball_width = ball_size[0]
    ball_height = ball_size[1]

    #가로벽에 닿았을 때 공의 이동 방향 변경 (튕겨 나오는 효과)
    if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
      ball_val["to_x"] = ball_val["to_x"] * -1 

    #세로 위치
    if ball_pos_y >= screen_height - stage_height - ball_height:
      #stage에 닿았을 때 튕겨 올라가는 처리 : 최초 속도가 순간 속도
      ball_val["to_y"] = ball_val["init_spd_y"] 
    else:
      #공중에 떠있을 때는 순간 속도를 증가 -> 포물선 처럼 이동
      ball_val["to_y"] += 0.5

    ball_val["pos_x"] += ball_val["to_x"]
    ball_val["pos_y"] += ball_val["to_y"]
    
  #4. 충돌 체크
  #rect 정보 저장
  character_rect = character.get_rect()
  character_rect.left = character_x_pos
  character_rect.top = character_y_pos
  
  for ball_idx, ball_val in enumerate(balls): 
    ball_pos_x = ball_val["pos_x"]
    ball_pos_y = ball_val["pos_y"]
    ball_img_idx = ball_val["img_idx"]

    ball_rect = ball_images[ball_img_idx].get_rect()
    ball_rect.left = ball_pos_x
    ball_rect.top = ball_pos_y
    
    #공과 캐릭터 충돌 처리
    if character_rect.colliderect(ball_rect):
      running = False
      break

    #공과 무기들 충돌 처리
    for weapon_idx, weapon_val in enumerate(weapons):
      weapon_pos_x = weapon_val[0]
      weapon_pos_y = weapon_val[1]

      weapon_rect = weapon.get_rect()
      weapon_rect.left = weapon_pos_x
      weapon_rect.top = weapon_pos_y
      
      #충돌하면 공과 무기가 없어지도록 처리
      if weapon_rect.colliderect(ball_rect):
        weapon_to_remove = weapon_idx #공과 닿은 무기의 인덱스
        ball_to_remove = ball_idx #무기와 닿은 공의 인덱스

        #공을 없앤 뒤 (가장 작은 공이 아니라면) 두개로 쪼개야함
        if ball_img_idx < 3: #가장 작은 공이 아니라면
          #현재 공 크기 정보
          ball_width = ball_rect.size[0]
          ball_height = ball_rect.size[1]

          #나눠진 공 정보
          small_ball_rect = ball_images[ball_img_idx + 1].get_rect() 
          #현재 공 보다 한 단계 작은 공 정보를 가져오기 위해 idx + 1
          small_ball_width = small_ball_rect.size[0]
          small_ball_height = small_ball_rect.size[1]
          
          
          #왼쪽으로 튕겨나가는 공
          balls.append({
            "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width / 2), #공의 x좌표 -> 현재 공의 중앙에서 작은 공 너비의 절반만큼 왼쪽으로 
            "pos_y" : ball_pos_y + (ball_height / 2) - (small_ball_height / 2), #공의 y좌표
            "img_idx" : ball_img_idx + 1, #공의 크기 (이미지 index로 설정)
            "to_x" : -3, #공의 x축 이동방향 (양이면 왼쪽, 음이면 오른쪽)
            "to_y" : -6,  #공의 y축 이동방향 
            "init_spd_y" : ball_speed_y[ball_img_idx + 1] #y 최초 속도 
          })
          #오른쪽으로 튕겨나가는 공
          balls.append({
            "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width / 2), #공의 x좌표
            "pos_y" : ball_pos_y + (ball_height / 2) - (small_ball_height / 2), #공의 y좌표
            "img_idx" : ball_img_idx + 1, #공의 크기 (이미지 index로 설정)
            "to_x" : 3, #공의 x축 이동방향 (양이면 왼쪽, 음이면 오른쪽)
            "to_y" : -6,  #공의 y축 이동방향 
            "init_spd_y" : ball_speed_y[ball_img_idx + 1] #y 최초 속도 (스피드 index로 설정)
          })
        break
        
  #충돌된 공과 무기 없애기
  if ball_to_remove > -1: #인덱스가 저장됐다면
    del balls[ball_to_remove] #닿은 공을 없앰
    ball_to_remove = -1 #remove값은 다시 초기화

  if weapon_to_remove > -1:
    del weapons[weapon_to_remove]
    weapon_to_remove = -1

  #모든 공을 없앤 경우 게임 종료
  if len(balls) == 0:
    game_result = "Mission Complete!!"
    running = False
    
  #5. 화면에 출력(위에서부터 아래 순서로 그려짐)
  screen.blit(background, (0, 0))
  
  for weapon_x_pos, weapon_y_pos in weapons:
    screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

  for idx, val in enumerate(balls):
    ball_pos_x = val["pos_x"]
    ball_pos_y = val["pos_y"]
    ball_img_idx = val["img_idx"]
    screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))
    
  screen.blit(stage, (0, screen_height - stage_height))
  screen.blit(character, (character_x_pos, character_y_pos))  

  #경과 시간 계산
  elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
  timer = game_font.render("Time : {}".format(int(total_time - elapsed_time)), True, (255, 255, 255))
  screen.blit(timer, (10, 10))

  #시간 초과할 경우
  if total_time - elapsed_time <= 0:
    game_result = "TIME OVER"
    running = False
  
  pygame.display.update()  
      
#게임 오버 메시지
msg = game_font.render(game_result, True, (255, 255, 0))
msg_rect = msg.get_rect(center = (int(screen_width / 2), int(screen_height / 2))) #화면 중앙 위치 반환
screen.blit(msg, msg_rect)
pygame.display.update()

pygame.time.delay(2000) #2초 정도 대기
pygame.quit()