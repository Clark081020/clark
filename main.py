import pygame
import math
import random
import asyncio
import platform

# 화면 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravitational Lensing Simulation")

# 색상
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# 상수 (중력렌즈 계산용)
G = 6.67430e-11  # 만유인력 상수
c = 3e8          # 빛의 속도
M = 1e12 * 1.989e30  # 질량체 (태양질량 10^12개로 가정)
SCALE = 1e-10    # 시각화를 위한 스케일링

# 별 생성
stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(50)]

def calculate_deflection_angle(x, y, lens_pos):
    # 질량체와의 거리 계산
    dx = x - lens_pos[0]
    dy = y - lens_pos[1]
    r = max(math.sqrt(dx**2 + dy**2), 10)  # 0 나누기 방지
    # 아인슈타인 각도: theta = 4GM / (c^2 * r)
    theta = (4 * G * M) / (c**2 * r) * SCALE
    # 왜곡된 위치 계산
    angle = math.atan2(dy, dx)
    new_x = x + math.cos(angle) * theta * r
    new_y = y + math.sin(angle) * theta * r
    return new_x, new_y

def setup():
    pygame.init()

def update_loop():
    screen.fill(BLACK)
    
    # 마우스 위치로 질량체 설정
    lens_pos = pygame.mouse.get_pos()
    
    # 질량체 그리기 (노란색 원)
    pygame.draw.circle(screen, YELLOW, lens_pos, 20)
    
    # 별 그리기 (왜곡 적용)
    for star in stars:
        distorted_x, distorted_y = calculate_deflection_angle(star[0], star[1], lens_pos)
        pygame.draw.circle(screen, WHITE, (int(distorted_x), int(distorted_y)), 2)
    
    pygame.display.flip()

async def main():
    setup()
    clock = pygame.time.Clock()
    FPS = 60
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        update_loop()
        clock.tick(FPS)
        await asyncio.sleep(1.0 / FPS)

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())
