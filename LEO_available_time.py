import numpy as np
import matplotlib.pyplot as plt

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# LEO 위성의 임의 속도 (km/s)
v_LEO = 7.5  # 예: LEO 위성의 평균 속도

# 셀 반경 (km)
r_cell = 500  # 위성 셀의 반경

# UE가 셀 중심에서 떨어진 최소 거리 (km)
d_center = 200  # UE의 경로가 셀 중심에서 떨어진 거리

# UE가 셀 외부에서 시작하여 셀 내부로 들어가는 거리 (시작 위치)
d_outside = 700  # UE의 초기 위치

# LEO 위성의 셀을 지나가는 경로 길이 계산
entry_exit_distance = 2 * np.sqrt(r_cell**2 - d_center**2)

# 가용 시간 계산 (초)
t_available = entry_exit_distance / v_LEO

# 결과 출력
print(f"LEO 셀 내부에서 UE가 통과하는 거리: {entry_exit_distance:.2f} km")
print(f"UE가 셀 내부에 머무는 시간 (가용 시간): {t_available:.2f} 초")

# 좌표 설정
theta = np.linspace(0, 2 * np.pi, 100)
circle_x = r_cell * np.cos(theta)
circle_y = r_cell * np.sin(theta)

# LEO 위성의 진행 경로 (X축을 따라 직선 이동)
leo_x = np.linspace(-r_cell - 300, r_cell + 300, 100)
leo_y = np.zeros_like(leo_x)  # LEO가 x축을 따라 직선 이동

# UE의 진행 경로 (셀 외부에서 내부로 진입, 셀을 통과하는 직선 경로)
ue_x_entry = -r_cell - 300  # UE가 셀 외부에서 시작하는 X 좌표
ue_x_exit = r_cell + 300    # UE가 셀을 통과하여 나가는 X 좌표
ue_x = np.linspace(ue_x_entry, ue_x_exit, 100)
ue_y = np.full_like(ue_x, d_center)  # UE는 셀 중심에서 d_center만큼 떨어진 직선으로 이동

# 그래프 그리기
plt.figure(figsize=(8, 8))

# LEO 셀 경계 그리기
plt.plot(circle_x, circle_y, label="LEO 셀 경계", color="blue")

# UE 진행 경로 그리기
plt.plot(ue_x, ue_y, label="UE 진행 경로", color="red", linestyle='--')

# LEO 위성 진행 경로 그리기
plt.plot(leo_x, leo_y, label="LEO 위성 진행 경로", color="purple", linestyle='-.')

# LEO 셀 중심 및 UE 시작 위치 표시
plt.scatter([0], [0], color="blue", label="LEO 셀 중심")
plt.scatter([ue_x_entry], [d_center], color="green", label="UE 시작 위치 (셀 외부)")

# 그래프 범위 및 설정
plt.xlim(-r_cell - 400, r_cell + 400)
plt.ylim(-r_cell - 400, r_cell + 400)
plt.gca().set_aspect('equal', adjustable='box')
plt.title("UE와 LEO 위성의 경로")
plt.xlabel("X (km)")
plt.ylabel("Y (km)")
plt.legend()
plt.grid(True)
plt.show()