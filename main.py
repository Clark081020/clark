import pygame
import numpy as np

# --- 1. Pygame 초기화 및 화면 설정 ---
pygame.init()

WIDTH, HEIGHT = 1000, 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("블랙홀 중력렌즈 시뮬레이션")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# --- 2. 천체 위치 및 크기 설정 ---
# 관찰자 (지구) 위치 - 화면 우측 하단
EARTH_POS = np.array([WIDTH - 100, HEIGHT - 100], dtype=float)
EARTH_RADIUS = 10

# 블랙홀 위치 - 화면 중앙 좌측 상단 (조절 가능)
BLACK_HOLE_POS = np.array([WIDTH // 3, HEIGHT // 3], dtype=float)
BLACK_HOLE_RADIUS = 20 # 시각적 표현을 위한 블랙홀 크기

# 블랙홀의 슈바르츠실트 반지름 또는 중력 효과 강도를 나타내는 매개변수
# 이 값이 클수록 빛이 더 많이 휘어집니다.
# 실제 슈바르츠실트 반지름과는 단위가 다르므로 시뮬레이션에 맞게 조절합니다.
SCHWARZSCHILD_RADIUS_EFFECT = 15000 # 중력 효과의 강도 조절 (픽셀 단위)

# 광원 (행성) 초기 위치 - 마우스 따라 움직임
PLANET_POS = np.array([WIDTH // 2, HEIGHT // 2], dtype=float)
PLANET_RADIUS = 8

# --- 3. 중력렌즈 계산 함수 ---
def calculate_bent_path(start_pos, black_hole_pos, black_hole_effect, num_segments=100):
    """
    지구(관찰자)에서 시작하여 블랙홀 주변을 지나 광원(행성)으로 이어지는
    휘어진 빛의 경로를 계산합니다.

    Parameters:
    start_pos (np.array): 경로 시작점 (지구)
    black_hole_pos (np.array): 블랙홀의 위치
    black_hole_effect (float): 블랙홀의 중력 렌즈 효과 강도
    num_segments (int): 경로를 그릴 세그먼트(점)의 수

    Returns:
    list of np.array: 휘어진 빛의 경로를 이루는 점들의 리스트
    """
    path_points = [start_pos]
    current_pos = np.array(start_pos, dtype=float)

    # 행성과 지구 사이의 벡터
    direction_to_planet_initial = PLANET_POS - EARTH_POS
    initial_dist = np.linalg.norm(direction_to_planet_initial)

    # 지구에서 블랙홀 방향으로의 초기 각도 계산
    initial_angle = np.arctan2(direction_to_planet_initial[1], direction_to_planet_initial[0])

    # 각 세그먼트의 길이 (거리에 따라 동적으로 조절하면 더 부드러워짐)
    segment_length = initial_dist / num_segments

    for _ in range(num_segments):
        # 현재 위치에서 블랙홀까지의 벡터
        r_vector = current_pos - black_hole_pos
        r_distance = np.linalg.norm(r_vector)

        if r_distance < 1.0: # 블랙홀 중심에 너무 가까워지는 것을 방지
            r_distance = 1.0

        # 빛의 굴절 각도 계산 (간략화된 점 질량 중력 렌즈 모델)
        # 굴절 각도 = 4GM / (c^2 * b)
        # 여기서 b는 충격 매개변수(impact parameter), 즉 블랙홀 중심으로부터의 최단 거리
        # 이 시뮬레이션에서는 r_distance에 반비례하도록 설정합니다.
        # 방향은 블랙홀을 향하도록 합니다.
        bend_factor = black_hole_effect / (r_distance**2) # r^2에 반비례하도록 조정

        # 블랙홀 방향으로의 단위 벡터
        black_hole_direction = -r_vector / r_distance

        # 현재 이동 방향
        current_direction = PLANET_POS - current_pos # 광원을 향하는 방향
        current_direction_normalized = current_direction / np.linalg.norm(current_direction)

        # 굴절 효과 적용 (단위 벡터에 굴절 강도와 블랙홀 방향 벡터를 더함)
        # 이 부분은 실제 렌즈 방정식의 근사치이며, 시각적 효과를 위해 조정될 수 있습니다.
        # 역추적을 위해 (관찰자 -> 광원) 방향으로 굴절을 적용합니다.
        # 즉, 블랙홀이 빛을 당기는 방향으로 (블랙홀 방향 벡터) 힘을 가합니다.
        bent_direction = current_direction_normalized + bend_factor * black_hole_direction
        bent_direction_normalized = bent_direction / np.linalg.norm(bent_direction)

        # 다음 위치 계산
        next_pos = current_pos + bent_direction_normalized * segment_length
        path_points.append(next_pos)
        current_pos = next_pos

        # 광원에 충분히 가까워지면 경로 중단 (선택 사항)
        if np.linalg.norm(current_pos - PLANET_POS) < PLANET_RADIUS * 2 and _ > num_segments / 2:
            break

    # 마지막 점을 광원 위치로 강제 설정하여 정확하게 연결
    if len(path_points) > 1:
        path_points[-1] = PLANET_POS

    return path_points

# --- 4. 게임 루프 ---
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            PLANET_POS = np.array(event.pos, dtype=float)

    # 화면 지우기
    SCREEN.fill(BLACK)

    # --- 천체 그리기 ---
    # 블랙홀
    pygame.draw.circle(SCREEN, GRAY, (int(BLACK_HOLE_POS[0]), int(BLACK_HOLE_POS[1])), BLACK_HOLE_RADIUS)
    # 블랙홀 주변 슈바르츠실트 반경 (시각적 참고용)
    pygame.draw.circle(SCREEN, WHITE, (int(BLACK_HOLE_POS[0]), int(BLACK_HOLE_POS[1])), SCHWARZSCHILD_RADIUS_EFFECT / 100, 1)

    # 지구
    pygame.draw.circle(SCREEN, BLUE, (int(EARTH_POS[0]), int(EARTH_POS[1])), EARTH_RADIUS)

    # 행성 (광원)
    pygame.draw.circle(SCREEN, YELLOW, (int(PLANET_POS[0]), int(PLANET_POS[1])), PLANET_RADIUS)

    # --- 빛의 경로 계산 및 그리기 ---
    # 지구에서 출발하여 블랙홀 주변을 휘어져 행성으로 가는 경로
    # 계산된 경로의 첫 시작점은 지구, 마지막 점은 행성이 됩니다.
    bent_light_path = calculate_bent_path(EARTH_POS, BLACK_HOLE_POS, SCHWARZSCHILD_RADIUS_EFFECT)

    if len(bent_light_path) > 1:
        # 경로의 모든 점을 이어서 선으로 그립니다.
        # pygame.draw.lines는 정수 좌표를 요구하므로 변환합니다.
        path_coords = [(int(p[0]), int(p[1])) for p in bent_light_path]
        pygame.draw.lines(SCREEN, GREEN, False, path_coords, 2) # 두께 2 픽셀

    # 화면 업데이트
    pygame.display.flip()

    # 프레임 속도 제한
    clock.tick(60)

pygame.quit()
