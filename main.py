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
    #debug-info {
        color: #00FF00;
        font-family: Arial, sans-serif;
    }
</style>
<div>
    <canvas id="lensing-canvas" width="800" height="600"></canvas>
    <p id="error-message"></p>
    <p id="debug-info"></p>
    <p class="info">마우스를 움직여 노란색 원(질량체)을 조작하세요. 흰색 별들이 질량체 주변으로 왜곡됩니다.</p>
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
    const SCALE = 1e8; // 왜곡 효과 크기 조정
    
    // 별 생성 (캔버스 내에서 보장)
    const stars = Array.from({ length: 50 }, () => ({
        x: Math.random() * (WIDTH - 40) + 20,
        y: Math.random() * (HEIGHT - 40) + 20
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
        const r = Math.max(Math.sqrt(dx * dx + dy * dy), 20);
        const theta = (4 * G * M) / (c * c * r) * SCALE;
        const angle = Math.atan2(dy, dx);
        const deflection = theta * r * 500; // 왜곡 거리 증폭
        let newX = x - Math.cos(angle) * deflection;
        let newY = y - Math.sin(angle) * deflection;
        // 캔버스 내로 좌표 제한
        newX = Math.max(0, Math.min(newX, WIDTH));
        newY = Math.max(0, Math.min(newY, HEIGHT));
        console.log(`Star: (${x.toFixed(2)}, ${y.toFixed(2)}) -> Distorted: (${newX.toFixed(2)}, ${newY.toFixed(2)}), theta: ${theta.toFixed(10)}`);
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
        ctx.fillStyle = '#FFFFFF';
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.5)';
        stars.forEach(star => {
            const distorted = calculateDeflectionAngle(star.x, star.y, lensPos.x, lensPos.y);
            // 왜곡된 별
            ctx.beginPath();
            ctx.arc(distorted.x, distorted.y, 5, 0, 2 * Math.PI);
            ctx.fill();
            // 디버깅: 원래 별 위치 (연한 회색)
            ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
            ctx.beginPath();
            ctx.arc(star.x, star.y, 2, 0, 2 * Math.PI);
            ctx.fill();
            // 곡선 경로 (Quadratic Bezier Curve, 반대 방향으로 휘도록)
            ctx.beginPath();
            ctx.moveTo(star.x, star.y);
            // 제어점: 렌즈 반대쪽으로 곡선이 휘도록
            const controlX = star.x + (star.x - lensPos.x) * 0.3;
            const controlY = star.y + (star.y - lensPos.y) * 0.3;
            ctx.quadraticCurveTo(controlX, controlY, distorted.x, distorted.y);
            ctx.stroke();
            ctx.fillStyle = '#FFFFFF'; // 색상 복원
        });
        
        // 디버깅 정보 표시
        document.getElementById('debug-info').innerText = `Lens Position: (${lensPos.x.toFixed(2)}, ${lensPos.y.toFixed(2)})`;
        
        requestAnimationFrame(draw);
    }
    
    draw();
    console.log("Simulation started with stars:", stars);
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
마우스를 캔버스 위에서 움직여 노란색 원(질량체)을 조작하세요. 흰색 별들이 질량체 주변으로 왜곡됩니다.
- 흰색 점: 왜곡된 별 위치
- 연한 회색 점: 원래 별 위치
- 회색 곡선: 빛의 왜곡 경로 (질량체 반대 방향으로 휨)
만약 왜곡이 보이지 않으면, 브라우저 콘솔(F12)을 열어 좌표를 확인하세요.
""")
