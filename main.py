def getFeatures(self, state, action):
        food = state.getFood()
        capsules = state.getCapsules()
        walls = state.getWalls()
        ghosts = state.getGhostPositions()

        features = util.Counter()
        features["bias"] = 1.0

        x, y = state.getPacmanPosition()
        dx, dy = Actions.directionToVector(action)
        next_x, next_y = int(x + dx), int(y + dy)

        scared_ghosts = [
            ghost for ghost in state.getGhostStates() if ghost.scaredTimer > 0
        ]
        non_scared_ghosts = [
            ghost for ghost in state.getGhostStates() if ghost.scaredTimer == 0
        ]

        # New feature: Remaining scared time
        scared_ghost_remaining_times = [ghost.scaredTimer for ghost in scared_ghosts]
        if scared_ghost_remaining_times:
            features["remaining-scared-time"] = sum(scared_ghost_remaining_times)

        # Updated feature: distance to the closest non-scared ghost
        non_scared_ghost_distances = [
            util.manhattanDistance((next_x, next_y), ghost.getPosition())
            for ghost in non_scared_ghosts
        ]
        if non_scared_ghost_distances:
            features["closest-non-scared-ghost"] = min(
                non_scared_ghost_distances
            ) / (walls.width * walls.height)

            # New feature: Avoiding ghosts when necessary
            if min(non_scared_ghost_distances) <= 1:
                features["avoid-ghost"] = 1.0

        # Updated feature: distance to the closest scared ghost
        scared_ghost_distances = [
            util.manhattanDistance((next_x, next_y), ghost.getPosition())
            for ghost in scared_ghosts
        ]
        if scared_ghost_distances:
            features["closest-scared-ghost"] = min(
                scared_ghost_distances
            ) / (walls.width * walls.height)

        # New feature: chasing a ghost with low scared time
        closest_scared_ghost_index = scared_ghost_distances.index(min(scared_ghost_distances))
        closest_scared_ghost = scared_ghosts[closest_scared_ghost_index]
        if closest_scared_ghost.scaredTimer <= 3:
            features["chase-low-scared-time"] = 1.0

        # Feature: check if Pacman will eat food
        if food[next_x][next_y]:
            features["eats-food"] = 1.0

        # Feature: distance to the closest food
        dist = closestFood((next_x, next_y), food, walls)
        if dist is not None:
            features["closest-food"] = float(dist) / (walls.width * walls.height)

        # Feature: check if Pacman will eat a capsule
        if (next_x, next_y) in capsules:
            features["eats-capsule"] = 1.0

        # Feature: count the number of remaining food
        features["remaining-food"] = float(food.count()) / (walls.width * walls.height)

        # Feature: count the number of remaining capsules
        features["remaining-capsules"] = float(len(capsules)) / (walls.width * walls.height)

        # Normalize the features
        features.divideAll(10.0)

        return features


Traceback (most recent call last):
  File "pacman.py", line 680, in <module>
    runGames( **args )
  File "pacman.py", line 646, in runGames
    game.run()
  File "/home/vboxuser/pacman-main/game.py", line 637, in run
    observation = agent.observationFunction(self.state.deepCopy())
  File "/home/vboxuser/pacman-main/learningAgents.py", line 213, in observationFunction
    self.observeTransition(self.lastState, self.lastAction, state, reward)
  File "/home/vboxuser/pacman-main/learningAgents.py", line 133, in observeTransition
    self.update(state,action,nextState,deltaReward)
  File "/home/vboxuser/pacman-main/qlearningAgents.py", line 211, in update
    qValueForState = self.getQValue(state,action)
  File "/home/vboxuser/pacman-main/qlearningAgents.py", line 199, in getQValue
    features = self.featExtractor.getFeatures(state,action)
  File "/home/vboxuser/pacman-main/featureExtractors.py", line 125, in getFeatures
    closest_scared_ghost_index = scared_ghost_distances.index(min(scared_ghost_distances))
ValueError: min() arg is an empty sequence

Beginning 90 episodes of Training
Training Done (turning off epsilon and alpha)
---------------------------------------------
Pacman died! Score: -522
Pacman died! Score: -538
Pacman died! Score: -523
Pacman died! Score: -542
Pacman died! Score: -513
Pacman died! Score: -537
Pacman died! Score: -527
Pacman died! Score: -550
Pacman died! Score: -645
Pacman died! Score: -579
Reinforcement Learning Status:
        Completed 10 test episodes
        Average Rewards over testing: -547.60
        Average Rewards for last 100 episodes: -539.56
        Episode took 19.70 seconds
Pacman died! Score: -628
Pacman died! Score: -615
Pacman died! Score: -592
Pacman died! Score: -548
Pacman died! Score: -543
Pacman died! Score: -525
Pacman died! Score: -589
Pacman died! Score: -612
Pacman died! Score: -533
Pacman died! Score: -595
Average Score: -562.8
Scores:        -522.0, -538.0, -523.0, -542.0, -513.0, -537.0, -527.0, -550.0, -645.0, -579.0, -628.0, -615.0, -592.0, -548.0, -543.0, -525.0, -589.0, -612.0, -533.0, -595.0
Win Rate:      0/20 (0.00)
Record:        Loss, Loss, Loss, Loss, Loss, Loss, Loss, Loss, Loss, Loss, Loss, Loss, Loss, Loss, Loss, Loss, Loss, Loss, Loss, Loss
