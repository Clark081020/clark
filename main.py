import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# --- 1. 중력렌즈 매개변수 설정 ---
# 모든 거리는 임의의 단위로 설정됩니다 (예: 각도 단위).
# 이 예제에서는 렌즈와 광원 사이의 상대적인 위치를 강조합니다.
lens_mass_factor = 1.0  # 렌즈의 질량에 비례하는 인자 (아인슈타인 반경에 영향을 줌)
einstein_radius = lens_mass_factor # 간단화를 위해 아인슈타인 반경을 직접 설정

# 렌즈의 위치 (중심)
lens_center_x = 0.0
lens_center_y = 0.0

# 시뮬레이션할 영역 범위
view_min = -2.5 * einstein_radius
view_max = 2.5 * einstein_radius
num_points = 200 # 그리드의 해상도

# --- 2. 중력렌즈 함수 정의 (점 질량 렌즈) ---
# 이 함수는 관측된 상의 위치(theta)로부터 실제 광원의 위치(beta)를 계산합니다.
# beta = theta - alpha(theta)
# 여기서 alpha(theta)는 점 질량 렌즈의 경우 (R_E^2 / |theta|^2) * theta 입니다.
def lens_equation_inverse(theta_x, theta_y, einstein_r, lens_cx=0, lens_cy=0):
    """
    관측된 상의 위치(theta)에서 실제 광원의 위치(beta)를 계산합니다.
    (점 질량 렌즈 공식)

    Parameters:
    theta_x, theta_y (float): 관측된 상의 x, y 좌표
    einstein_r (float): 아인슈타인 반경
    lens_cx, lens_cy (float): 렌즈의 중심 x, y 좌표

    Returns:
    tuple: (beta_x, beta_y) 실제 광원의 x, y 좌표
    """
    # 렌즈 중심으로부터의 상대적인 상의 위치
    rel_theta_x = theta_x - lens_cx
    rel_theta_y = theta_y - lens_cy

    # 렌즈 중심으로부터의 거리
    abs_theta = np.sqrt(rel_theta_x**2 + rel_theta_y**2)

    # 발산 방지를 위한 작은 값 추가
    if abs_theta == 0:
        abs_theta = 1e-9

    # 휘어진 각도 alpha
    alpha_x = (einstein_r**2 / abs_theta**2) * rel_theta_x
    alpha_y = (einstein_r**2 / abs_theta**2) * rel_theta_y

    # 렌즈 방정식 역상 매핑: beta = theta - alpha
    beta_x = rel_theta_x - alpha_x
    beta_y = rel_theta_y - alpha_y

    return beta_x, beta_y

# --- 3. 그리드 생성 ---
# 관측 평면 (상의 평면)에 그리드를 생성합니다.
theta_x_grid, theta_y_grid = np.meshgrid(
    np.linspace(view_min, view_max, num_points),
    np.linspace(view_min, view_max, num_points)
)

# 그리드 점들을 실제 광원 평면으로 매핑합니다.
beta_x_grid, beta_y_grid = lens_equation_inverse(
    theta_x_grid, theta_y_grid, einstein_radius, lens_center_x, lens_center_y
)

# --- 4. 광원 정의 (Source) ---
# 광원의 형태를 정의합니다. 여기서는 간단한 원형 광원을 사용합니다.
# 광원의 중심과 반지름을 조정하여 다양한 효과를 볼 수 있습니다.

source_center_x = 0.0  # 광원의 실제 중심 x
source_center_y = -1.2 * einstein_radius # 광원의 실제 중심 y (렌즈 아래)
source_radius = 0.3 * einstein_radius  # 광원의 반지름

# 광원이 존재하는 영역을 마스크로 만듭니다.
# 광원 평면의 각 점(beta_x, beta_y)이 광원 내부에 있는지 확인합니다.
source_mask = (beta_x_grid - source_center_x)**2 + \
              (beta_y_grid - source_center_y)**2 < source_radius**2

# --- 5. 시각화 ---
plt.figure(figsize=(12, 6))

# --- 5.1. 광원 평면 (Source Plane) 시각화 ---
ax1 = plt.subplot(1, 2, 1)
ax1.set_title('Source Plane (Actual Light Source)')
ax1.set_xlabel(r'$\beta_x$ (Arcsec)')
ax1.set_ylabel(r'$\beta_y$ (Arcsec)')
ax1.set_aspect('equal', adjustable='box')
ax1.set_xlim(view_min, view_max)
ax1.set_ylim(view_min, view_max)

# 광원 그리기 (원)
source_circle = patches.Circle(
    (source_center_x, source_center_y), source_radius,
    color='red', alpha=0.7, label='Source'
)
ax1.add_patch(source_circle)
ax1.grid(True, linestyle='--', alpha=0.6)
ax1.legend()


# --- 5.2. 상 평면 (Image Plane) 시각화 ---
ax2 = plt.subplot(1, 2, 2)
ax2.set_title('Image Plane (Observed Image)')
ax2.set_xlabel(r'$\theta_x$ (Arcsec)')
ax2.set_ylabel(r'$\theta_y$ (Arcsec)')
ax2.set_aspect('equal', adjustable='box')
ax2.set_xlim(view_min, view_max)
ax2.set_ylim(view_min, view_max)

# 렌즈 중심 표시
ax2.plot(lens_center_x, lens_center_y, 'o', color='gray', markersize=8, label='Lens Center', zorder=5)

# 아인슈타인 링 반경 표시
einstein_circle = patches.Circle(
    (lens_center_x, lens_center_y), einstein_radius,
    edgecolor='gray', linestyle='--', fill=False, label='Einstein Radius'
)
ax2.add_patch(einstein_circle)


# 광원 마스크에 해당하는 상의 그리드 점들을 플로팅
# source_mask가 True인 (광원 안에 있는) theta_x_grid, theta_y_grid 점들만 선택
image_points_x = theta_x_grid[source_mask]
image_points_y = theta_y_grid[source_mask]

# 상을 점들로 시각화 (해상도에 따라 점이 많아 보임)
ax2.scatter(image_points_x, image_points_y, s=1, color='blue', label='Observed Image', alpha=0.7)

ax2.grid(True, linestyle='--', alpha=0.6)
ax2.legend()

plt.tight_layout()
plt.show()

print(f"Einstein Radius: {einstein_radius:.2f} units")
print(f"Source Center: ({source_center_x:.2f}, {source_center_y:.2f}) units")
print(f"Source Radius: {source_radius:.2f} units")
