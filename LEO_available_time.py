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

# 위성의 속도와 방향을 딕셔너리로 설정
satellites = {
    f'LEO {i + 1}': {
        'position': satellite_positions[i],
        'speed': np.random.uniform(7.0, 8.0) * 5,  # km/s
        'direction': np.random.rand(2)
    } for i in range(num_satellites)
}

# 방향 벡터 정규화
for satellite in satellites.values():
    satellite['direction'] /= np.linalg.norm(satellite['direction'])

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
def update_positions(satellites, dt):
    for satellite in satellites.values():
        satellite['position'] = (
            satellite['position'][0] + satellite['direction'][0] * satellite['speed'] * dt,
            satellite['position'][1] + satellite['direction'][1] * satellite['speed'] * dt
        )

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
    global satellites, text_box

    ax.clear()
    ax.set_xlim([user_position[0] - 3000, user_position[0] + 3000])
    ax.set_ylim([user_position[1] - 3000, user_position[1] + 3000])
    ax.set_xlabel('X (km)')
    ax.set_ylabel('Y (km)')
    ax.set_title('2D LEO Satellite Handover Simulation')

    # 위성 이동 업데이트
    update_positions(satellites, 1)

    # 위성 커버리지 그리기
    draw_coverage(ax, [satellite['position'] for satellite in satellites.values()])

    # 사용자 위치를 표시 (고정된 위치)
    ax.scatter(user_position[0], user_position[1], color='black', s=100, label='User (Fixed Position)')

    # 사용자와 위성 간의 가용 시간 및 신호 세기 계산
    available_times = [calculate_available_time(satellite['position'], user_position, satellite['speed'], satellite['direction'])
                       for satellite in satellites.values()]
    signal_strengths = [calculate_signal_strength(satellite['position'], user_position)
                        for satellite in satellites.values()]

    # 핸드오버 점수 계산 (가용 시간과 자원의 가중치)
    handover_scores = [available_times[i] * time_weight + available_resources[i] * resource_weight
                       for i in range(num_satellites)]

    # 셀 안에 있는 위성만 핸드오버 후보로 고려
    in_coverage = [i for i in range(num_satellites) if is_in_coverage(satellites[f'LEO {i + 1}']['position'], user_position)]

    if in_coverage:
        # 핸드오버할 위성 선택 (가장 긴 가용 시간)
        longest_available_time_idx = in_coverage[np.argmax([available_times[i] for i in in_coverage])]
        handover_satellite = f'LEO {longest_available_time_idx + 1}'
        handover_time = available_times[longest_available_time_idx]

        # 콘솔에 핸드오버 정보 출력
        print(f'Handover to {handover_satellite} with available time {handover_time:.2f}s')

        # 사용자와 핸드오버될 위성 간의 연결선 (빨간색으로 표시)
        ax.plot([user_position[0], satellites[handover_satellite]['position'][0]],
                [user_position[1], satellites[handover_satellite]['position'][1]],
                'r-', label='Handover Connection')

    # 각 위성의 위치와 가용 시간 및 신호 세기 표시
    for i, (satellite_name, satellite) in enumerate(satellites.items()):
        ax.scatter(satellite['position'][0], satellite['position'][1], color='blue', s=100, label=satellite_name)
        ax.text(satellite['position'][0], satellite['position'][1], satellite_name, fontsize=12, ha='right')

    # 오른쪽 상단에 값 업데이트
    textstr = '\n'.join([f'{satellite_name}: AT={available_times[i]:.2f}s, Res={available_resources[i]:.2f}'
                         for i, satellite_name in enumerate(satellites.keys())])
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

    if text_box:
        text_box.remove()
    text_box = ax.text(0.95, 0.95, textstr, transform=ax.transAxes, fontsize=10,
                       verticalalignment='top', horizontalalignment='right', bbox=props)

    plt.legend(loc='upper right')

# 애니메이션 설정
ani = animation.FuncAnimation(fig, update, frames=100, interval=200, repeat=False)

plt.show()
