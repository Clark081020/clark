import pygame
import math

# 초기화
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("중력렌즈 효과 시뮬레이션")
clock = pygame.time.Clock()

# 색상 정의
WHITE = (255, 255, 255)
BLUE = (100, 100, 255)
RED = (255, 50, 50)
YELLOW = (255, 255, 100)
BLACK = (0, 0, 0)

# 고정된 위치
earth_pos = (700, 300)       # 지구 (관측자)
blackhole_pos = (400, 300)   # 블랙홀 (중력렌즈 중심)

# 빛 경로 계산 함수
def get_light_path(source, lens, observer, segments=50):
    path = []
    for i in range(segments + 1):
        t = i / segments
        # 직선 좌표
        x = (1 - t) * source[0] + t * observer[0]
        y = (1 - t) * source[1] + t * observer[1]

        # 블랙홀 중심으로 휘어지게 하기 위한 계산
        dx = x - lens[0]
        dy = y - lens[1]
        dist_sq = dx ** 2 + dy ** 2
        strength = 50000 / (dist_sq + 1000)  # 휘어짐 강도 조절

        # 방향 회전하여 경로 왜곡
        x += -dy * strength * 0.001
        y += dx * strength * 0.001

        path.append((x, y))
    return path

# 메인 루프
running = True
while running:
    screen.fill((10, 10, 30))  # 어두운 배경

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 마우스 위치 → 행성
    planet_pos = pygame.mouse.get_pos()

    # 빛 경로 계산
    light_path = get_light_path(planet_pos, blackhole_pos, earth_pos)

    # 객체 그리기
    pygame.draw.circle(screen, BLUE, earth_pos, 10)       # 지구
    pygame.draw.circle(screen, RED, blackhole_pos, 20)    # 블랙홀
    pygame.draw.circle(screen, YELLOW, planet_pos, 8)     # 행성 (광원)

    # 빛 경로 그리기 (곡선처럼 보임)
    if len(light_path) > 1:
        pygame.draw.lines(screen, WHITE, False, light_path, 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
