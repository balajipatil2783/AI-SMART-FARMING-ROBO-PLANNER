
from collections import deque
import heapq

# =========================
# AI SMART FARMING ROBO PLANNER
# =========================

GRID = []
ROWS = 0
COLS = 0
MOVES = [(0,1),(1,0),(-1,0),(0,-1)]

CROPS = {
    "Wheat": 50,
    "Rice": 90,
    "Cotton": 60,
    "Sugarcane": 120,
    "Maize": 70
}

def create_farm():
    global GRID, ROWS, COLS

    ROWS = int(input("Enter Farm Rows: "))
    COLS = int(input("Enter Farm Columns: "))

    GRID = [[0 for _ in range(COLS)] for _ in range(ROWS)]

    obs = int(input("Enter Number of Obstacles: "))

    for i in range(obs):
        r = int(input(f"Obstacle {i+1} Row: "))
        c = int(input(f"Obstacle {i+1} Column: "))

        if 0 <= r < ROWS and 0 <= c < COLS:
            GRID[r][c] = 1

def valid(pos):
    r, c = pos
    return (
        0 <= r < ROWS and
        0 <= c < COLS and
        GRID[r][c] == 0
    )

def display_farm():
    if not GRID:
        print("No farm created. Choose Option 1 first.")
        return

    print("\n========== FARM MAP ==========")
    print("   ", end="")
    for c in range(COLS):
        print(c, end=" ")
    print()

    for r, row in enumerate(GRID):
        print(r, end="  ")
        for cell in row:
            print("X" if cell == 1 else "0", end=" ")
        print()

    print(f"\nFarm Size : {ROWS} x {COLS}")

def display_path(path, start, goal):
    if not path:
        print("No path found.")
        return

    temp = [row[:] for row in GRID]

    for r, c in path:
        temp[r][c] = "*"

    temp[start[0]][start[1]] = "S"
    temp[goal[0]][goal[1]] = "G"

    print("\nPATH VISUALIZATION")
    for row in temp:
        print(" ".join(str(x) for x in row))

def bfs(start, goal):
    queue = deque([(start, [start])])
    visited = set()

    while queue:
        node, path = queue.popleft()

        if node == goal:
            return path

        if node in visited:
            continue

        visited.add(node)

        for dx, dy in MOVES:
            nxt = (node[0] + dx, node[1] + dy)

            if valid(nxt):
                queue.append((nxt, path + [nxt]))

    return None

def dfs(start, goal):
    stack = [(start, [start])]
    visited = set()

    while stack:
        node, path = stack.pop()

        if node == goal:
            return path

        if node in visited:
            continue

        visited.add(node)

        for dx, dy in MOVES:
            nxt = (node[0] + dx, node[1] + dy)

            if valid(nxt):
                stack.append((nxt, path + [nxt]))

    return None

def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def astar(start, goal):
    pq = [(0, start, [start])]
    visited = set()

    while pq:
        _, node, path = heapq.heappop(pq)

        if node == goal:
            return path

        if node in visited:
            continue

        visited.add(node)

        for dx, dy in MOVES:
            nxt = (node[0]+dx, node[1]+dy)

            if valid(nxt):
                heapq.heappush(
                    pq,
                    (len(path)+heuristic(nxt, goal), nxt, path+[nxt])
                )

    return None

def irrigation_scheduler():
    n = int(input("Number of Fields: "))

    data = []

    for i in range(n):
        field = input("Field Name: ")
        crop = input("Crop Type: ").title()
        moisture = float(input("Soil Moisture (%): "))

        data.append((field, crop, moisture))

    data.sort(key=lambda x: x[2])

    slots = ["Morning", "Afternoon", "Evening", "Night"]

    print("\nSMART IRRIGATION SCHEDULE")

    for i, (field, crop, moisture) in enumerate(data):
        water = CROPS.get(crop, 50)

        print(
            f"{field} | {crop} | "
            f"Moisture={moisture}% | "
            f"Water={water}L | "
            f"{slots[i % 4]}"
        )

def pest_control():

    print("\n========== PEST CONTROL SYSTEM ==========")

    print("\nPest Severity Guide")
    print("--------------------------------")
    print("1 - 4  : Low Pest Attack")
    print("         Recommendation -> Monitor Crop")
    print()
    print("5 - 7  : Medium Pest Attack")
    print("         Recommendation -> Organic Treatment")
    print()
    print("8 - 10 : High Pest Attack")
    print("         Recommendation -> Spray Pesticide")
    print("--------------------------------")

    severity = int(
        input(
            "\nEnter Pest Severity (1-10): "
        )
    )

    if severity >= 8:

        print("\nHigh Pest Attack Detected")
        print("Recommendation: Spray Pesticide")

    elif severity >= 5:

        print("\nMedium Pest Attack Detected")
        print("Recommendation: Organic Treatment")

    else:

        print("\nLow Pest Attack Detected")
        print("Recommendation: Monitor Crop")


def rain_prediction():
    humidity = float(input("Humidity (%): "))
    temp = float(input("Temperature (C): "))

    p = 0.2

    if humidity > 70:
        p += 0.4

    if temp < 28:
        p += 0.2

    p = min(p, 1.0)

    print(f"Rain Probability: {p*100:.2f}%")
    return p

def save_report():
    report = "AI SMART FARMING REPORT\n"
    report += f"Farm Size : {ROWS} x {COLS}\n"

    obstacles = sum(row.count(1) for row in GRID)
    report += f"Obstacles : {obstacles}\n"

    with open("farm_report.txt", "w") as f:
        f.write(report)

    print("Report saved as farm_report.txt")

while True:

    print("\n1.Create Farm")
    print("2.View Farm")
    print("3.BFS")
    print("4.DFS")
    print("5.A*")
    print("6.Irrigation Scheduler")
    print("7.Pest Control")
    print("8.Rain Prediction")
    print("9.Save Report")
    print("10.Exit")

    choice = input("Choice: ")

    if choice == "1":
        create_farm()

    elif choice == "2":
        display_farm()

    elif choice in ["3", "4", "5"]:

        if not GRID:
            print("Create farm first.")
            continue

        start = (int(input("Start Row: ")), int(input("Start Col: ")))
        goal = (int(input("Goal Row: ")), int(input("Goal Col: ")))

        if not valid(start):
            print("Invalid Start Position")
            continue

        if not valid(goal):
            print("Invalid Goal Position")
            continue

        if choice == "3":
            path = bfs(start, goal)
            print("BFS Path:", path)

        elif choice == "4":
            path = dfs(start, goal)
            print("DFS Path:", path)

        else:
            path = astar(start, goal)
            print("A* Path:", path)

        display_path(path, start, goal)

    elif choice == "6":
        irrigation_scheduler()

    elif choice == "7":
        pest_control()

    elif choice == "8":
        rain_prediction()

    elif choice == "9":
        save_report()

    elif choice == "10":
        print("Thank You!")
        break
