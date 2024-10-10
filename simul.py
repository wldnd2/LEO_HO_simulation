import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# 위성의 수와 커버리지 반경 설정
num_satellites = 5
coverage_radius = 1000  # km (위성의 셀 반경)

# 위성의 초기 2D 위치 좌표를 랜덤으로 설정
satellite_positions = [(np.random.uniform(-3000, 3000), np.random.uniform(1000, 3000)) for _ in range(num_satellites)]

# 사용자 위치를 임의의 LEO 셀 안에 배치
user_position = [np.random.uniform(-coverage_radius, coverage_radius), 
                 np.random.uniform(2000 - coverage_radius, 2000 + coverage_radius)]

# 위성의 속도를 랜덤으로 설정 (7.0 ~ 8.0 km/s)
satellite_speeds = np.random.uniform(7.0, 8.0, num_satellites)  # km/s 속도
speed_multiplier = 5  # 속도 증가 배율
satellite_speeds *= speed_multiplier

# 위성의 이동 방향을 설정 (위성은 사용자를 지나감)
directions = [np.random.rand(2) for _ in range(num_satellites)]
directions = [dir / np.linalg.norm(dir) for dir in directions]  # 방향 벡터 정규화

# 위성의 Available Resources (가용 리소스) 가정
available_resources = np.random.uniform(0.5, 1.0, num_satellites)  # 50% ~ 100% 자원

# 핸드오버를 결정할 때 가용 리소스 및 가용 시간 기준 가중치 설정
resource_weight = 0.6
time_weight = 0.4

# 사용자와의 가용 시간을 계산하는 함수
def calculate_available_time(satellite_pos, user_pos, speed, direction):
    distance = np.sqrt((satellite_pos[0] - user_pos[0])**2 + (satellite_pos[1] - user_pos[1])**2)
    relative_speed = speed * np.dot(direction, [(user_pos[0] - satellite_pos[0]) / distance, 
                                                (user_pos[1] - satellite_pos[1]) / distance])
    if relative_speed > 0:
        available_time = (coverage_radius - distance) / relative_speed
    else:
        available_time = 0
    return max(available_time, 0)

# 신호 세기를 계산하는 함수 (단순히 거리의 역수로 가정)
def calculate_signal_strength(satellite_pos, user_pos):
    distance = np.sqrt((satellite_pos[0] - user_pos[0])**2 + (satellite_pos[1] - user_pos[1])**2)
    return 1 / distance if distance != 0 else float('inf')

# 위성의 위치 업데이트 함수
def update_positions(positions, directions, speeds, dt):
    return [(pos[0] + dir[0] * speed * dt, pos[1] + dir[1] * speed * dt) 
            for pos, dir, speed in zip(positions, directions, speeds)]

# 핸드오버 수행 여부를 판단하는 함수
def is_in_coverage(satellite_pos, user_pos):
    distance = np.sqrt((satellite_pos[0] - user_pos[0])**2 + (satellite_pos[1] - user_pos[1])**2)
    return distance <= coverage_radius

# 2D 시뮬레이션 애니메이션 설정
fig, ax = plt.subplots(figsize=(10, 10))
text_box = None

# 위성 커버리지를 그리는 함수
def draw_coverage(ax, positions):
    for pos in positions:
        circle = plt.Circle(pos, coverage_radius, color='blue', alpha=0.3)
        ax.add_artist(circle)

# 시뮬레이션 애니메이션 프레임을 업데이트하는 함수
def update(frame):
    global satellite_positions, text_box

    ax.clear()
    ax.set_xlim([user_position[0] - 3000, user_position[0] + 3000])
    ax.set_ylim([user_position[1] - 3000, user_position[1] + 3000])
    ax.set_xlabel('X (km)')
    ax.set_ylabel('Y (km)')
    ax.set_title('2D LEO Satellite Handover Simulation')

    # 위성 이동 업데이트
    satellite_positions = update_positions(satellite_positions, directions, satellite_speeds, 1)

    # 위성 커버리지 그리기
    draw_coverage(ax, satellite_positions)

    # 사용자 위치를 표시 (고정된 위치)
    ax.scatter(user_position[0], user_position[1], color='black', s=100, label='User (Fixed Position)')

    # 사용자와 위성 간의 가용 시간 및 신호 세기 계산
    available_times = [calculate_available_time(satellite_positions[i], user_position, satellite_speeds[i], directions[i]) 
                       for i in range(num_satellites)]
    signal_strengths = [calculate_signal_strength(satellite_positions[i], user_position) 
                        for i in range(num_satellites)]

    # 핸드오버 점수 계산 (가용 시간과 자원의 가중치)
    handover_scores = [available_times[i] * time_weight + available_resources[i] * resource_weight 
                       for i in range(num_satellites)]

    # 셀 안에 있는 위성만 핸드오버 후보로 고려
    in_coverage = [i for i in range(num_satellites) if is_in_coverage(satellite_positions[i], user_position)]
    
    if in_coverage:
        # 핸드오버할 위성 선택
        handover_scores = [handover_scores[i] for i in in_coverage]
        closest_satellite_idx = in_coverage[np.argmax(handover_scores)]
        closest_satellite_position = satellite_positions[closest_satellite_idx]

        # 사용자와 핸드오버될 위성 간의 연결선 (직선으로 표시)
        ax.plot([user_position[0], closest_satellite_position[0]], 
                [user_position[1], closest_satellite_position[1]], 
                'k--', label='Handover Connection')

    # 각 위성의 위치와 가용 시간 및 신호 세기 표시
    for i, pos in enumerate(satellite_positions):
        ax.scatter(pos[0], pos[1], color='blue', s=100, label=f'LEO {i+1}')
        ax.text(pos[0], pos[1], f'LEO {i+1}', fontsize=12, ha='right')

    # 오른쪽 상단에 값 업데이트
    textstr = '\n'.join([f'LEO {i+1}: AT={available_times[i]:.2f}s, Res={available_resources[i]:.2f}' 
                         for i in range(num_satellites)])
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    
    if text_box:
        text_box.remove()
    text_box = ax.text(0.95, 0.95, textstr, transform=ax.transAxes, fontsize=10,
                       verticalalignment='top', horizontalalignment='right', bbox=props)

    plt.legend(loc='upper right')

# 애니메이션 설정
ani = animation.FuncAnimation(fig, update, frames=100, interval=200, repeat=False)

plt.show()
