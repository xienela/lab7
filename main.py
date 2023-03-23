class SimpleExtractor(FeatureExtractor):
    def getFeatures(self, state, action):
        # Extract the grid of walls
        walls = state.getWalls()
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
        food_distances = [manhattanDistance((next_x, next_y), (i, j)) for i in range(walls.width) for j in range(walls.height) if food[i][j]]
        if food_distances:
            features["closest-food"] = float(min(food_distances)) / (walls.width * walls.height)

        # Calculate the nearest ghost distance
        next_ghost_distances = [manhattanDistance(ghost_position, (next_x, next_y)) for ghost_position in ghost_positions]
        if next_ghost_distances:
            features["closest-ghost"] = float(min(next_ghost_distances)) / (walls.width * walls.height)

        # Calculate the nearest scared ghost distance
        scared_ghosts = [ghost for ghost in ghosts if ghost.scaredTimer > 0]
        scared_ghost_positions = [ghost.getPosition() for ghost in scared_ghosts]
        scared_ghost_distances = [manhattanDistance(ghost_position, (next_x, next_y)) for ghost_position in scared_ghost_positions]
        if scared_ghost_distances:
            features["closest-scared-ghost"] = float(min(scared_ghost_distances)) / (walls.width * walls.height)

        # Calculate the distance to the nearest capsule
        capsules = state.getCapsules()
        capsule_distances = [manhattanDistance((next_x, next_y), capsule) for capsule in capsules]
        if capsule_distances:
            features["closest-capsule"] = float(min(capsule_distances)) / (walls.width * walls.height)

        # Calculate the distance to the nearest dead end
        dead_end_distances = []
        for i in range(walls.width):
            for j in range(walls.height):
                if walls[i][j] == False:
                    neighbors = [(i + dx, j + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
                    walls_count = sum(1 for nx, ny in neighbors if walls[nx][ny])
                    if walls_count == 3:
                        dead_end_distances.append(manhattanDistance((next_x, next_y), (i, j)))
        if dead_end_distances:
            features["closest-dead-end"] = float(min(dead_end_distances)) / (walls.width * walls.height)

        features.divideAll(10.0)
        return features
