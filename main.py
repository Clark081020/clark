import streamlit as st
import streamlit.components.v1 as components

# Streamlit 페이지 설정
st.title("인터랙티브 중력렌즈 시뮬레이션")

# 질량 조절 슬라이더
mass_scale = st.slider("질량체의 질량 (태양질량 x 10^12)", 0.1, 10.0, 1.0, 0.1)

# JavaScript와 HTML5 Canvas로 중력렌즈 시뮬레이션 구현
html_code = f"""
<style>
    #lensing-canvas {{
        border: 2px solid #FFD700;
        background-color: #000;
    }}
    #error-message {{
        color: red;
        font-family: Arial, sans-serif;
    }}
    .info {{
        color: white;
        font-family: Arial, sans-serif;
    }}
    #debug-info {{
        color: #00FF00;
        font-family: Arial, sans-serif;
    }}
</style>
<div>
    <canvas id="lensing-canvas" width="800" height="600"></canvas>
    <p id="error-message"></p>
    <p id="debug-info"></p>
    <p class="info">마우스를 움직여 노란색 원(질량체)을 조작하고, 슬라이더로 질량을 조절하세요. 흰색 별들이 아인슈타인 링/아크 형태로 왜곡됩니다.</p>
</div>
<script>
try {{
    const canvas = document.getElementById('lensing-canvas');
    const ctx = canvas.getContext('2d');
    
    // 상수
    const WIDTH = 800;
    const HEIGHT = 600;
    const G = 6.67430e-11;
    const c = 3e8;
    const M = {mass_scale} * 1e12 * 1.989e30;
    const D_LS = 1e25; // 렌즈-소스 거리
    const D_L = 1e24;  // 관측자-렌즈 거리
    const D_S = 2e25;  // 관측자-소스 거리
    
    // 별 생성 (원형 + 무작위 분포)
    const stars = Array.from({{ length: 300 }}, () => {{
        const isRing = Math.random() < 0.6; // 60%는 링 근처, 40%는 무작위
        if (isRing) {{
            const angle = Math.random() * 2 * Math.PI;
            const radius = Math.random() * 100 + 50; // 50~150px
            return {{
                x: WIDTH / 2 + Math.cos(angle) * radius,
                y: HEIGHT / 2 + Math.sin(angle) * radius,
                size: Math.random() * 1 + 1 // 1~2px
            }};
        }} else {{
            return {{
                x: Math.random() * (WIDTH - 40) + 20,
                y: Math.random() * (HEIGHT - 40) + 20,
                size: Math.random() * 1 + 1
            }};
        }}
    }});
    
    // 마우스 위치
    let lensPos = {{ x: WIDTH / 2, y: HEIGHT / 2 }};
    
    canvas.addEventListener('mousemove', (event) => {{
        const rect = canvas.getBoundingClientRect();
        lensPos.x = event.clientX - rect.left;
        lensPos.y = event.clientY - rect.top;
    }});
    
    function calculateDeflectionAngle(x, y, lensX, lensY) {{
        const dx = x - lensX;
        const dy = y - lensY;
        const r = Math.max(Math.sqrt(dx * dx + dy * dy), 20);
        // 아인슈타인 반경
        const theta_E = Math.sqrt((4 * G * M / (c * c)) * (D_LS / (D_L * D_S))) * 1e12;
        // 렌즈 방정식
        const theta = r / 100; // 픽셀 단위 정규화
        const beta = Math.abs(theta - (theta_E * theta_E) / (theta || 0.01)); // 0 나누기 방지
        const angle = Math.atan2(dy, dx);
        // 왜곡된 위치
        const newX = lensX + Math.cos(angle) * beta * 120;
        const newY = lensY + Math.sin(angle) * beta * 120;
        // 캔버스 내로 좌표 제한
        const clampedX = Math.max(0, Math.min(newX, WIDTH));
        const clampedY = Math.max(0, Math.min(newY, HEIGHT));
        console.log(`Star: (${{x.toFixed(2)}}, ${{y.toFixed(2)}}) -> Distorted: (${{clampedX.toFixed(2)}}, ${{clampedY.toFixed(2)}}), Beta: ${{beta.toFixed(10)}}`);
        return {{ x: clampedX, y: clampedY }};
    }}
    
    function draw() {{
        // 캔버스 초기화
        ctx.fillStyle = 'black';
        ctx.fillRect(0, 0, WIDTH, HEIGHT);
        
        // 질량체 (노란색 원)
        ctx.fillStyle = '#FFFF00';
        ctx.beginPath();
        ctx.arc(lensPos.x, lensPos.y, 10, 0, 2 * Math.PI);
        ctx.fill();
        
        // 별 그리기 (왜곡 적용)
        ctx.fillStyle = '#FFFFFF';
        stars.forEach(star => {{
            const distorted = calculateDeflectionAngle(star.x, star.y, lensPos.x, lensPos.y);
            ctx.beginPath();
            ctx.arc(distorted.x, distorted.y, star.size, 0, 2 * Math.PI);
            ctx.fill();
        }});
        
        // 디버깅 정보 표시
        document.getElementById('debug-info').innerText = `Lens Position: (${{lensPos.x.toFixed(2)}}, ${{lensPos.y.toFixed(2)}}), Mass: {mass_scale}x10^12 M☉, Stars: ${stars.length}`;
        
        requestAnimationFrame(draw);
    }}
    
    draw();
    console.log("Simulation started with stars:", stars);
}} catch (error) {{
    document.getElementById('error-message').innerText = "Failed to load simulation: " + error.message;
    console.error("Error:", error);
}}
</script>
"""

# Streamlit에서 HTML 렌더링
components.html(html_code, height=700, width=850)

# 대체 콘텐츠
st.markdown("""
### 시뮬레이션 안내
마우스를 움직여 노란색 원(질량체)을 조작하고, 슬라이더로 질량을 조절하세요. 흰색 별들이 아인슈타인 링/아크 형태로 왜곡됩니다.
- 별은 300개로, 일부는 질량체 주변에 링 형태로 배치됩니다.
만약 왜곡이 보이지 않으면, 브라우저 콘솔(F12)을 열어 좌표와 Beta 값을 확인하세요.
""")
