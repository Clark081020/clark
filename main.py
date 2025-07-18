import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.collections import LineCollection

def calculate_deflection(x, y, bh_x, bh_y, mass, intensity):
    """중력에 의한 빛의 휨 계산 (반대 방향으로 휨, 더 강한 왜곡)"""
    dx = bh_x - x
    dy = bh_y - y
    distance_sq = dx**2 + dy**2
    distance = np.sqrt(distance_sq)
    
    if distance < mass * 0.6:  # 슈바르츠실트 반경 내부
        return 0, 0
    
    deflection = 5 * intensity * mass / (distance_sq + 1e-6)  # 더 강한 왜곡을 위해 5배 스케일링
    return -dx * deflection, -dy * deflection  # 반대 방향으로 휨

def generate_light_ray(start_x, start_y, width, height, bh_x, bh_y, mass, intensity, steps=150):
    """빛의 경로 생성"""
    x, y = start_x, start_y
    ray_path = [(x, y)]
    
    if start_x == 0:  # 왼쪽에서 오는 빛
        dx, dy = 3, 0
    else:  # 위에서 오는 빛
        dx, dy = 0, 3
    
    for _ in range(steps):
        # 중력 휨 효과 적용
        deflection_x, deflection_y = calculate_deflection(x, y, bh_x, bh_y, mass, intensity)
        dx += deflection_x
        dy += deflection_y
        
        # 방향 벡터 정규화
        length = np.sqrt(dx**2 + dy**2)
        if length > 0:
            dx = (dx / length) * 3
            dy = (dy / length) * 3
        
        x += dx
        y += dy
        ray_path.append((x, y))
        
        # 화면 밖으로 나가면 중지
        if x < 0 or x > width or y < 0 or y > height:
            break
            
    return np.array(ray_path)

def main():
    # Streamlit 설정
    st.set_page_config(
        page_title="중력 렌즈 시뮬레이터",
        page_icon="🌌",
        layout="wide"
    )
    
    # 제목 및 설명
    st.title("🌠 블랙홀 중력 렌즈 효과 시뮬레이터")
    st.markdown("""
    이 시뮬레이션은 블랙홀 주변의 빛 경로가 반대 방향으로 휘는 가상의 효과를 보여줍니다. 
    빛이 블랙홀을 피해 바깥쪽으로 강하게 휘어지는 모습을 관찰해보세요.
    """)
    
    # 컨트롤 패널
    with st.sidebar:
        st.header("제어판")
        mass = st.slider("블랙홀 질량", 30, 150, 80, help="질량이 클수록 휨 효과가 강해집니다")
        intensity = st.slider("왜곡 강도", 0.5, 10.0, 2.0, 0.1, help="빛의 휨 강도를 조절합니다")
        ray_count = st.slider("광선 개수", 5, 30, 12, help="표시할 빛의 경로 수")
        show_grid = st.checkbox("시공간 그리드 표시", value=True)
        show_photon = st.checkbox("광자 구 표시", value=True)
        
        st.markdown("---")
        st.header("블랙홀 위치")
        col1, col2 = st.columns(2)
        with col1:
            bh_x = st.slider("X 좌표", 100, 700, 400)
        with col2:
            bh_y = st.slider("Y 좌표", 100, 500, 300)
        
        st.markdown("---")
        if st.button("기본값으로 초기화"):
            st.session_state.mass = 80
            st.session_state.intensity = 2.0
            st.session_state.ray_count = 12
            st.session_state.bh_x = 400
            st.session_state.bh_y = 300
    
    # 시뮬레이션 영역
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_xlim(0, 800)
    ax.set_ylim(0, 600)
    ax.set_facecolor('#0a0a20')  # 어두운 우주 배경
    ax.axis('off')
    
    # 시공간 그리드 그리기
    if show_grid:
        grid_size = 40
        for x in np.arange(0, 801, grid_size):
            grid_line = []
            for y in np.arange(0, 601, 5):
                def_x, def_y = calculate_deflection(x, y, bh_x, bh_y, mass, intensity)
                grid_line.append([x + def_x, y + def_y])
            ax.plot(*zip(*grid_line), color=(100/255, 200/255, 255/255, 0.3), linewidth=0.8)
            
        for y in np.arange(0, 601, grid_size):
            grid_line = []
            for x in np.arange(0, 801, 5):
                def_x, def_y = calculate_deflection(x, y, bh_x, bh_y, mass, intensity)
                grid_line.append([x + def_x, y + def_y])
            ax.plot(*zip(*grid_line), color=(100/255, 200/255, 255/255, 0.3), linewidth=0.8)
    
    # 빛의 경로 생성 및 그리기
    rays = []
    vertical_spacing = 600 / (ray_count + 1)
    horizontal_spacing = 800 / (ray_count + 1)
    
    for i in range(1, ray_count + 1):
        # 왼쪽에서 오는 빛
        ray = generate_light_ray(0, i * vertical_spacing, 800, 600, bh_x, bh_y, mass, intensity)
        rays.append(ray)
        # 위에서 오는 빛
        ray = generate_light_ray(i * horizontal_spacing, 0, 800, 600, bh_x, bh_y, mass, intensity)
        rays.append(ray)
    
    # 빛 경로 그리기
    line_collection = LineCollection(rays, colors='white', linewidths=1.0)
    ax.add_collection(line_collection)
    
    # 블랙홀 (검은 원) 및 광자 구 그리기
    black_hole = Circle((bh_x, bh_y), mass * 0.6, color='black')
    ax.add_patch(black_hole)
    if show_photon:
        photon_sphere = Circle((bh_x, bh_y), mass * 0.9, color='yellow', fill=False, linestyle='--')
        ax.add_patch(photon_sphere)
    
    # Matplotlib 그래프를 Streamlit에 표시
    st.pyplot(fig)

if __name__ == "__main__":
    main()
