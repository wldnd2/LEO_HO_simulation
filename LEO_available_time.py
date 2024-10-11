import numpy as np
import matplotlib.pyplot as plt

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# LEO 위성의 임의 속도 (km/s)
v_LEO = 7.5  # 예: LEO 위성의 평균 속도

# 셀 반경 (km)
r_cell = 500  # 위성 셀의 반경

def calculate_entry_exit_distance(d_center):
    """LEO 셀 내부에서 UE가 통과하는 거리 계산."""
    return 2 * np.sqrt(r_cell**2 - d_center**2)

def calculate_available_time(entry_exit_distance):
    """가용 시간 계산 (초)."""
    return entry_exit_distance / v_LEO

def create_circle(radius, num_points=100):
    """주어진 반경의 원을 생성."""
    theta = np.linspace(0, 2 * np.pi, num_points)
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    return x, y

def create_leo_path():
    """LEO 위성의 진행 경로 생성."""
    leo_x = np.linspace(-r_cell - 300, r_cell + 300, 100)
    leo_y = 0.2 * leo_x  # Y축으로 약간 기울어짐 (기울기 0.2)
    return leo_x, leo_y

def create_ue_path(ue_x_entry, ue_x_exit, d_center):
    """UE의 진행 경로 생성 (LEO 진행 방향에 맞춰 평행)."""
    ue_x = np.linspace(ue_x_entry, ue_x_exit, 100)
    ue_y = 0.2 * ue_x + d_center  # LEO 진행 방향과 평행
    return ue_x, ue_y

def plot_graph(circle_x, circle_y, ue_x, ue_y, leo_x, leo_y, entry_exit_distance, t_available, ue_start_x, ue_start_y):
    """그래프 그리기."""
    plt.figure(figsize=(8, 8))
    
    # LEO 셀 경계 그리기
    plt.plot(circle_x, circle_y, label="LEO 셀 경계", color="blue")

    # UE 진행 경로 그리기
    plt.plot(ue_x, ue_y, label="UE 진행 경로", color="red", linestyle='--')

    # LEO 위성 진행 경로 그리기
    plt.plot(leo_x, leo_y, label="LEO 위성 진행 경로 (기울기 있음)", color="purple", linestyle='-.')

    # LEO 셀 중심 및 UE 시작 위치 표시
    plt.scatter([0], [0], color="blue", label="LEO 셀 중심")
    plt.scatter([ue_start_x], [ue_start_y], color="green", label="UE 시작 위치 (셀 외부)")

    # 결과 출력 값을 그래프에 표시
    plt.text(0, 10, f"가용 시간: {t_available:.2f} 초", fontsize=10, ha='center', color='black')

    # 그래프 범위 및 설정
    plt.xlim(-r_cell - 400, r_cell + 400)
    plt.ylim(-r_cell - 400, r_cell + 400)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.title("UE와 LEO 위성의 경로 (기울어진 LEO 위성)")
    plt.xlabel("X (km)")
    plt.ylabel("Y (km)")
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    # UE가 셀 중심에서 떨어진 최소 거리 (km)
    d_center = 200  # UE의 경로가 셀 중심에서 떨어진 거리

    # LEO 위성의 셀을 지나가는 경로 길이 계산
    entry_exit_distance = calculate_entry_exit_distance(d_center)

    # 가용 시간 계산 (초)
    t_available = calculate_available_time(entry_exit_distance)

    # 결과 출력
    print(f"LEO 셀 내부에서 UE가 통과하는 거리: {entry_exit_distance:.2f} km")
    print(f"UE가 셀 내부에 머무는 시간 (가용 시간): {t_available:.2f} 초")

    # 좌표 설정
    circle_x, circle_y = create_circle(r_cell)
    leo_x, leo_y = create_leo_path()

    # UE의 진행 경로 (LEO 진행 방향에 맞춰 평행하게 설정)
    ue_x_entry = -r_cell - 300  # UE가 셀 외부에서 시작하는 X 좌표
    ue_x_exit = r_cell + 300    # UE가 셀을 통과하여 나가는 X 좌표
    ue_x, ue_y = create_ue_path(ue_x_entry, ue_x_exit, d_center)

    # 그래프 그리기
    plot_graph(circle_x, circle_y, ue_x, ue_y, leo_x, leo_y, entry_exit_distance, t_available, ue_x_entry, 0.2 * ue_x_entry + d_center)

if __name__ == "__main__":
    main()
