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

        features.divideAll(10.0)
        return features
