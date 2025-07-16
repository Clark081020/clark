import streamlit as st
import streamlit.components.v1 as components

# Streamlit 페이지 설정
st.title("인터랙티브 중력렌즈 시뮬레이션")

# Pyodide와 Pygame을 실행하기 위한 HTML/JS 코드
html_code = """
<script src="https://cdn.jsdelivr.net/pyodide/v0.23.4/full/pyodide.js"></script>
<script>
async function main() {
    let pyodide = await loadPyodide();
    await pyodide.loadPackage("micropip");
    await pyodide.runPythonAsync(`
import micropip
await micropip.install('pygame')
import pygame
import math
import random
import asyncio

# 화면 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravitational Lensing Simulation")

# 색상
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# 상수 (중력렌즈 계산용)
G = 6.67430e-11
c = 3e8
M = 1e12 * 1.989e30
SCALE = 1e-10

# 별 생성
stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(50)]

def calculate_deflection_angle(x, y, lens_pos):
    dx = x - lens_pos[0]
    dy = y - lens_pos[1]
    r = max(math.sqrt(dx**2 + dy**2), 10)
    theta = (4 * G * M) / (c**2 * r) * SCALE
    angle = math.atan2(dy, dx)
    new_x = x + math.cos(angle) * theta * r
    new_y = y + math.sin(angle) * theta * r
    return new_x, new_y

def setup():
    pygame.init()

def update_loop():
    screen.fill(BLACK)
    lens_pos = pygame.mouse.get_pos()
    pygame.draw.circle(screen, YELLOW, lens_pos, 20)
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

asyncio.ensure_future(main())
    `);
}
main();
</script>
<canvas id="pygame-canvas" width="800" height="600"></canvas>
"""

# Streamlit에서 HTML 렌더링
components.html(html_code, height=600, width=800)
