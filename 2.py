import pygame

pygame.init()  #초기화(반드시 필요)

#화면 크기 설정
screen_width = 480  #가로 크기
screen_height = 640  #세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

#화면 타이틀 설정
pygame.display.set_caption("JunHyuk Game")  #게임 이름

#배경 이미지 불러오기
background = pygame.image.load("/home/runner/pythongameproject/background.png")

#pygame에서는 event loop가 실행 되고 있어야 화면이 꺼지지 않는다.
#이벤트 루프
running = True #게임이 진행 중인가?
while running:
  for event in pygame.event.get(): #어떤 이벤트가 발생한다면
    if event.type == pygame.QUIT: #창이 닫히는 이벤트가 발생한다면
      running = False #게임 진행을 종료
  screen.blit(background, (0, 0)) #왼쪽위 모서리에서부터 background를 그려줌(blit)
  #screen.fill((0, 0, 255)) : 화면을 RGB값으로 채워줄 수도 있음
  
  pygame.display.update() #pygame에서는 매순간 배경을 업데이트해줘야한다.

      
#pygame 종료
pygame.quit()