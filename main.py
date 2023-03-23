from queue import PriorityQueue

def a_star_search(start, goal, graph):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = dict()
    cost_so_far = dict()
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + graph.heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current

    return came_from, cost_so_far


class PacmanGraph:
    def __init__(self, walls):
        self.walls = walls

    def in_bounds(self, pos):
        x, y = pos
        return 0 <= x < self.walls.width and 0 <= y < self.walls.height

    def passable(self, pos):
        x, y = pos
        return not self.walls[x][y]

    def neighbors(self, pos):
        x, y = pos
        neighbors = [(x + dx, y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
        neighbors = filter(self.in_bounds, neighbors)
        neighbors = filter(self.passable, neighbors)
        return list(neighbors)

    def cost(self, current, next):
        return 1

    def heuristic(self, goal, next):
        return manhattanDistance(goal, next)

class SimpleExtractor(FeatureExtractor):
    def getFeatures(self, state, action):
        # Extract the grid of walls
        walls = state.getWalls()
        graph = PacmanGraph(walls)

        ghosts = state.getGhostStates()
        ghost_positions = [ghost.getPosition() for ghost in ghosts]
        ghost_distances = [manhattanDistance(ghost_position, state.getPacmanPosition()) for ghost_position in ghost_positions]

        features = util.Counter()
        features["bias"] = 1.0
        features["#-of-ghosts-1-step-away"] = sum(distance < 2 for distance in ghost_distances)

        # Change the action of Pacman
        x, y = state.getPacmanPosition()
        dx, dy = Actions.directionToVector(action)
        next_x, next_y = int(x + dx), int(y + dy)

         # Calculate the nearest food distance
        food = state.getFood()
        food_list = [(i, j) for i in range(walls.width) for j in range(walls.height) if food[i][j]]
        food_distances = [len(a_star_search((next_x, next_y), food_pos, graph)[0]) for food_pos in food_list]
        if food_distances:
            features["closest-food"] = min(food_distances)

        return features
