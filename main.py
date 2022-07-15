import pygame

pygame.init()  #초기화(반드시 필요)

#화면 크기 설정
screen_width = 480  #가로 크기
screen_height = 640  #세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

#화면 타이틀 설정
pygame.display.set_caption("JunHyuk Game")  #게임 이름

#FPS : Frame Per Second (fps가 높을수록 캐릭터가 선명하게 움직임)
clock = pygame.time.Clock()


#배경 이미지 불러오기
background = pygame.image.load("/home/runner/pythongameproject/background.png")

#캐릭터 불러오기
character = pygame.image.load("/home/runner/pythongameproject/character.png")
character_size = character.get_rect().size  #이미지의 크기를 구해옴
character_width = character_size[0]  #첫번째값이 가로 크기
character_height = character_size[1]  #두번째값이 세로 크기
character_x_pos = (screen_width -
                   character_width) / 2  #화면 가로의 절반 크기에 해당하는 곳에 위치하도록 설정
character_y_pos = screen_height - character_height
#화면 세로 크기 가장 아래에 해당하는 곳에 위치하도록 설정

#이동할 좌표
to_x = 0
to_y = 0

#이동 속도
character_speed = 0.3

#적 enemy 캐릭터
enemy = pygame.image.load("/home/runner/pythongameproject/enemy.png")
enemy_size = enemy.get_rect().size  #이미지의 크기를 구해옴
enemy_width = enemy_size[0]  #첫번째값이 가로 크기
enemy_height = enemy_size[1]  #두번째값이 세로 크기
enemy_x_pos = (screen_width -
                   enemy_width) / 2  
enemy_y_pos = (screen_height - enemy_height) / 2




#pygame에서는 event loop가 실행 되고 있어야 화면이 꺼지지 않는다.
#이벤트 루프
running = True  #게임이 진행 중인가?
while running:
  dt = clock.tick(40) #게임화면의 초당 프레임 수를 설정
  
  
  for event in pygame.event.get():  #어떤 이벤트가 발생한다면
    if event.type == pygame.QUIT:  #창이 닫히는 이벤트가 발생한다면
        running = False  #게임 진행을 종료

    #키보드 이벤트
    if event.type == pygame.KEYDOWN:  #키가 눌러졌는지 확인
      if event.key == pygame.K_LEFT:
          to_x -= character_speed
      elif event.key == pygame.K_RIGHT:
          to_x += character_speed
      elif event.key == pygame.K_UP:
          to_y -= character_speed
      elif event.key == pygame.K_DOWN:
          to_y += character_speed

      if event.type == pygame.KEYUP:  #방향키를 떼면 멈춤
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
          to_x = 0
        elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
          to_y = 0

    #캐릭터의 현재 좌표에서 움직인 만큼 갱신
    character_x_pos += to_x * dt
    character_y_pos += to_y * dt
    #캐릭터가 화면 밖으로 나가지 못하도록 막기
    #가로 경계값 처리
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width
    #세로 경계값 처리
    if character_y_pos < 0:
        character_y_pos = 0
    elif character_y_pos > screen_height - character_height:
        character_y_pos = screen_height - character_height

    #충돌 처리를 위한 rect 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    enemy_rect =enemy.get_rect()
    enemy_rect.left = enemy_x_pos
    enemy_rect.top = enemy_y_pos

    #충돌 체크
    if character_rect.colliderect(enemy_rect): #좌표가 겹쳤는지를 확인해주는 함수
      print("충돌했어요")
      running = False
    
    screen.blit(background, (0, 0))  #왼쪽위 모서리에서부터 background를 그려줌(blit)
    screen.blit(character, (character_x_pos, character_y_pos))
    screen.blit(enemy, (enemy_x_pos, enemy_y_pos))
    pygame.display.update()  #pygame에서는 매순간 배경을 업데이트해줘야한다.

#pygame 종료
pygame.quit()