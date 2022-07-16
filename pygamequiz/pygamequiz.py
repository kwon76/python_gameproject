"""
QUIZ) 하늘에서 떨어지는 똥 피하기 게임 만들기
[게임 조건]
1. 캐릭터는 화면 가장 아래에 위치, 좌우로만 이동가능
2. 똥은 화면 가장 위에서 떨어짐. X좌표는 매번 랜덤으로 설정
3. 캐릭터가 똥을 피하면 다음 똥이 다시 떨어짐
4. 캐릭터가 똥과 충동하면 게임 종료
5. FPS는 30으로 설정

[게임 이미지]
1. 배경 : 640*480 
2. 캐릭터 : 70*70
3. 똥 : 70*70
"""
from random import *
import pygame
#################################################################
#반드시 해야 하는 기본 초기화
pygame.init()  

#화면 크기 설정
screen_width = 480  #가로 크기
screen_height = 640  #세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

#화면 타이틀 설정
pygame.display.set_caption("Avoid The DDong") 

#FPS
clock = pygame.time.Clock()
#################################################################
#1. 사용자 게임 초기화(배경 화면, 게임 이미지, 좌표, 속도, 폰트)

#배경 화면
bg = pygame.image.load("/home/runner/pythongameproject/pygamequiz/quiz_background.png")
#캐릭터
chr = pygame.image.load("/home/runner/pythongameproject/pygamequiz/quiz_character.png")
chr_size = chr.get_rect().size
chr_width = chr_size[0]
chr_height = chr_size[1]
chr_x = (screen_width - chr_width) / 2 #x좌표는 가로 절반으로 위치
chr_y = screen_height - chr_height #y좌표는 바닥으로 위치
#똥
ddong = pygame.image.load("/home/runner/pythongameproject/pygamequiz/quiz_ddong.png")
ddong_size = ddong.get_rect().size
ddong_width = ddong_size[0]
ddong_height = ddong_size[1]
ddong_x = (screen_width - ddong_width) / 2
ddong_y = -ddong_height

#이동 좌표 
chr_to_x = 0
ddong_to_y = 0

#이동 속도
chr_speed = 0.2
ddong_speed = 0.4

#폰트
game_font = pygame.font.Font(None, 40)

#피한 똥 개수 설정
ddong_cnt = 0

running = True  
while running:
  dt = clock.tick(30)  

  #2. 이벤트 처리 (키보드, 마우스 등)
  for event in pygame.event.get():  
    if event.type == pygame.QUIT:  
        running = False  

    #키보드
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_LEFT:
        chr_to_x -= chr_speed
      elif event.key == pygame.K_RIGHT:
        chr_to_x += chr_speed
    if event.type == pygame.KEYUP:
      if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
        chr_to_x = 0
  #3. 게임 캐릭터 위치 정의
  ddong_to_y += ddong_speed
  chr_x += chr_to_x * dt
  ddong_y += ddong_speed * dt
  if ddong_y > screen_height:
    ddong_y = -ddong_height
    ddong_x = random()*screen_width
    ddong_cnt += 1
  
  if chr_x < 0:
    chr_x = 0
  elif chr_x > screen_width - chr_width:
    chr_x = screen_width - chr_width
    
  #4. 충돌 체크
  chr_rect = chr.get_rect()
  chr_rect.left = chr_x
  chr_rect.top = chr_y
  ddong_rect =ddong.get_rect()
  ddong_rect.left = ddong_x
  ddong_rect.top = ddong_y
  if chr_rect.colliderect(ddong_rect):
    print("똥 맞았네ㅋㅋ")
    print("피한 똥 개수 : "+str(ddong_cnt))
    running = False
  
  #5. 화면에 출력
  screen.blit(bg, (0, 0))
  screen.blit(chr, (chr_x, chr_y))
  screen.blit(ddong, (ddong_x, ddong_y))
  cnt = game_font.render(str(ddong_cnt), True, (255, 255, 255)) 
  screen.blit(cnt, (10, 10))
  
  pygame.display.update()  
      

pygame.quit()