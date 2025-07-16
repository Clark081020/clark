import streamlit as st
import streamlit.components.v1 as components

# Streamlit 페이지 설정
st.title("인터랙티브 중력렌즈 시뮬레이션")

# JavaScript와 HTML5 Canvas로 중력렌즈 시뮬레이션 구현
html_code = """
<style>
    #lensing-canvas {
        border: 2px solid #FFD700;
        background-color: #000;
    }
    #error-message {
        color: red;
        font-family: Arial, sans-serif;
    }
    .info {
        color: white;
        font-family: Arial, sans-serif;
    }
</style>
<div>
    <canvas id="lensing-canvas" width="800" height="600"></canvas>
    <p id="error-message"></p>
    <p class="info">마우스를 움직여 노란색 원(질량체)을 조작하세요. 배경의 별들이 중력렌즈 효과로 왜곡됩니다.</p>
</div>
<script>
try {
    const canvas = document.getElementById('lensing-canvas');
    const ctx = canvas.getContext('2d');
    
    // 상수
    const WIDTH = 800;
    const HEIGHT = 600;
    const G = 6.67430e-11;
    const c = 3e8;
    const M = 1e12 * 1.989e30;
    const SCALE = 1e-10;
    
    // 별 생성
    const stars = Array.from({ length: 30 }, () => ({
        x: Math.random() * WIDTH,
        y: Math.random() * HEIGHT
    }));
    
    // 마우스 위치
    let lensPos = { x: WIDTH / 2, y: HEIGHT / 2 };
    
    canvas.addEventListener('mousemove', (event) => {
        const rect = canvas.getBoundingClientRect();
        lensPos.x = event.clientX - rect.left;
        lensPos.y = event.clientY - rect.top;
    });
    
    function calculateDeflectionAngle(x, y, lensX, lensY) {
        const dx = x - lensX;
        const dy = y - lensY;
        const r = Math.max(Math.sqrt(dx * dx + dy * dy), 10);
        const theta = (4 * G * M) / (c * c * r) * SCALE;
        const angle = Math.atan2(dy, dx);
        const newX = x + Math.cos(angle) * theta * r;
        const newY = y + Math.sin(angle) * theta * r;
        return { x: newX, y: newY };
    }
    
    function draw() {
        // 캔버스 초기화
        ctx.fillStyle = 'black';
        ctx.fillRect(0, 0, WIDTH, HEIGHT);
        
        // 질량체 (노란색 원)
        ctx.fillStyle = '#FFFF00';
        ctx.beginPath();
        ctx.arc(lensPos.x, lensPos.y, 20, 0, 2 * Math.PI);
        ctx.fill();
        
        // 별 그리기 (왜곡 적용)
        ctx.fillStyle = 'white';
        stars.forEach(star => {
            const distorted = calculateDeflectionAngle(star.x, star.y, lensPos.x, lensPos.y);
            ctx.beginPath();
            ctx.arc(distorted.x, distorted.y, 2, 0, 2 * Math.PI);
            ctx.fill();
        });
        
        requestAnimationFrame(draw);
    }
    
    draw();
    console.log("Simulation started");
} catch (error) {
    document.getElementById('error-message').innerText = "Failed to load simulation: " + error.message;
    console.error("Error:", error);
}
</script>
"""

# Streamlit에서 HTML 렌더링
components.html(html_code, height=700, width=850)

# 대체 콘텐츠
st.markdown("""
### 시뮬레이션 안내
마우스를 캔버스 위에서 움직여 노란색 원(질량체)을 조작하세요. 배경의 별들이 중력렌즈 효과로 왜곡됩니다.
만약 캔버스가 보이지 않으면, 브라우저 콘솔(F12)을 열어 오류를 확인해 보세요.
""")
