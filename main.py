import streamlit as st
import streamlit.components.v1 as components

# Streamlit 페이지 설정
st.title("인터랙티브 중력렌즈 시뮬레이션")

# Pyodide와 Pygame을 실행하기 위한 HTML/JS 코드
html_code = """
<script src="https://cdn.jsdelivr.net/pyodide/v0.26.1/full/pyodide.js"></script>
<script>
async function main() {
    try {
        let pyodide = await loadPyodide();
        console.log("Pyodide loaded successfully");
        
        // Pygame 설치
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
stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(30)]

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
    FPS = 30
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
        console.log("Pygame simulation started");
    } catch (error) {
        console.error("Error in Pyodide execution:", error);
        document.getElementById("error-message").innerText = "Failed to load simulation: " + error.message;
    }
}
main();
</script>
<style>
    #pygame-canvas {
        border: 2px solid #FFD700;
        background-color: #000;
    }
</style>
<div>
    <canvas id="pygame-canvas" width="800" height="600"></canvas>
    <p id="error-message" style="color: red;"></p>
    <p style="color: white;">Move your mouse to control the gravitational lens (yellow circle) and see how the stars distort!</p>
</div>
"""

# Streamlit에서 HTML 렌더링
components.html(html_code, height=700, width=850)

# 대체 콘텐츠 (캔버스 로드 실패 시)
st.markdown("""
### 시뮬레이션 안내
마우스를 캔버스 위에서 움직여 노란색 원(질량체)을 조작하세요. 배경의 별들이 중력렌즈 효과로 왜곡됩니다.
만약 �ទ캔버스가 보이지 않으면, 브라우저 콘솔(F12)을 열어 오류를 확인해 보세요.
""")
