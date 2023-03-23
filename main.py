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
    
    
    
Beginning 90 episodes of Training
Training Done (turning off epsilon and alpha)
---------------------------------------------
Pacman died! Score: -109
Pacman emerges victorious! Score: 357
Pacman died! Score: -258
Pacman died! Score: -461
Pacman died! Score: -171
Pacman died! Score: -241
Pacman died! Score: -280
Pacman died! Score: -445
Pacman died! Score: -419
Pacman died! Score: -501
Reinforcement Learning Status:
        Completed 10 test episodes
        Average Rewards over testing: -252.80
        Average Rewards for last 100 episodes: -305.33
        Episode took 131.58 seconds
Pacman died! Score: -47
Pacman died! Score: -537
Pacman died! Score: -561
Pacman died! Score: -373
Pacman died! Score: -462
Pacman died! Score: -503
Pacman died! Score: -448
Pacman died! Score: -300
Pacman died! Score: -427
Pacman died! Score: -80
Average Score: -313.3
Scores:        -109.0, 357.0, -258.0, -461.0, -171.0, -241.0, -280.0, -445.0, -419.0, -501.0, -47.0, -537.0, -561.0, -373.0, -462.0, -503.0, -448.0, -300.0, -427.0, -80.0
Win Rate:      1/20 (0.05)
Record:        Loss, Win, Loss, Loss, Loss, Loss, Loss, Loss, Loss, Loss, Loss, Loss, Loss, Loss, Loss, Loss, Loss, Loss, Loss, Loss
