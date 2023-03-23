import telebot
import script as s



# @TestLabaShulz_bot
bot = telebot.TeleBot('5459154592:AAFKeGOgEr5TKhtswZLMdfLB12rQsuzXWsE')

value = ""
old_value = ""

keyboard = telebot.types.InlineKeyboardMarkup()
keyboard.row(   telebot.types.InlineKeyboardButton(" ", callback_data="no"),
                telebot.types.InlineKeyboardButton("C", callback_data="C"),
                telebot.types.InlineKeyboardButton("<=", callback_data="<="),
                telebot.types.InlineKeyboardButton("/", callback_data="/") )

keyboard.row(   telebot.types.InlineKeyboardButton("7", callback_data="7"),
                telebot.types.InlineKeyboardButton("8", callback_data="8"),
                telebot.types.InlineKeyboardButton("9", callback_data="9"),
                telebot.types.InlineKeyboardButton("*", callback_data="*") )

keyboard.row(   telebot.types.InlineKeyboardButton("4", callback_data="4"),
                telebot.types.InlineKeyboardButton("5", callback_data="5"),
                telebot.types.InlineKeyboardButton("6", callback_data="6"),
                telebot.types.InlineKeyboardButton("-", callback_data="-") )

keyboard.row(   telebot.types.InlineKeyboardButton("1", callback_data="1"),
                telebot.types.InlineKeyboardButton("2", callback_data="2"),
                telebot.types.InlineKeyboardButton("3", callback_data="3"),
                telebot.types.InlineKeyboardButton("+", callback_data="+") )

keyboard.row(   telebot.types.InlineKeyboardButton(" ", callback_data="no"),
                telebot.types.InlineKeyboardButton("0", callback_data="0"),
                telebot.types.InlineKeyboardButton(",", callback_data="."),
                telebot.types.InlineKeyboardButton("=", callback_data="=") )

@bot.message_handler(commands = ["calculater"] )
def getmessage(message):
    global value
    if value == "":
        bot.send_message(message.from_user.id, "0", reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, value, reply_markup=keyboard)
        
        
@bot.message_handler(commands=['get_url'])
def getmessage(message):
    bot.send_message(message.from_user.id, 'Введите URL:')
    bot.register_next_step_handler(message, get_url)

def get_url(message):
    response = s.get_url(message.text)
    bot.send_message(message.from_user.id, response)
    
    
    
@bot.message_handler(commands=['pop_uniq_words'])
def getmessage(message):
    bot.send_message(message.from_user.id, 'Введите текст:')
    bot.register_next_step_handler(message, get_pop_words)
    
def get_pop_words(message):
    pop_uniq_words = s.count_words_from_text(message.text)
    bot.send_message(message.from_user.id, pop_uniq_words)


@bot.callback_query_handler(func=lambda call: True)
def callback_func(query):
    global value, old_value
    data = query.data

    if data == "no" :
        pass
    elif data == "C" :
        value = ""
    elif data == "=" :
        try:
            value = str(eval(value))
        except:
            value = "Ошибка!"
    else:
        value += data

    if value != old_value:
        if value == "":
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text="0", reply_markup=keyboard)
        else:
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=value, reply_markup=keyboard)

    old_value = value
    if value == "Ошибка!": value = ""

bot.polling(none_stop=False, interval=0)




def getFeatures(self, state, action):
    # Extract the grid of food and walls and the pacman position
    food = state.getFood()
    walls = state.getWalls()
    pacmanPosition = state.getPacmanPosition()
    nextPacmanPosition = Actions.getSuccessor(pacmanPosition, action)

    features = util.Counter()

    # Feature 1: Bias term
    features["bias"] = 1.0

    # Feature 2: Distance to the closest food
    min_food_distance = float("inf")
    for food_position in food.asList():
        distance = util.manhattanDistance(nextPacmanPosition, food_position)
        min_food_distance = min(min_food_distance, distance)
    features["closest-food"] = 1.0 / (min_food_distance + 1)

    # Feature 3: Number of food remaining
    remaining_food = len(food.asList())
    features["remaining-food"] = 1.0 / (remaining_food + 1)

    # Feature 4: Distance to the closest ghost and scared ghost
    min_ghost_distance = float("inf")
    min_scared_ghost_distance = float("inf")
    for ghost_state in state.getGhostStates():
        distance = util.manhattanDistance(nextPacmanPosition, ghost_state.getPosition())
        if ghost_state.scaredTimer > 0:
            min_scared_ghost_distance = min(min_scared_ghost_distance, distance)
        else:
            min_ghost_distance = min(min_ghost_distance, distance)

    if min_ghost_distance < 2:
        features["closest-ghost"] = -100
    else:
        features["closest-ghost"] = 0

    if min_scared_ghost_distance != float("inf"):
        features["scared-ghost"] = 1.0 / (min_scared_ghost_distance + 1)
    else:
        features["scared-ghost"] = 0

    # Feature 5: Number of capsules remaining
    capsules = len(state.getCapsules())
    features["remaining-capsules"] = 1.0 / (capsules + 1)

    # Feature 6: Distance to the closest capsule
    min_capsule_distance = float("inf")
    for capsule_position in state.getCapsules():
        distance = util.manhattanDistance(nextPacmanPosition, capsule_position)
        min_capsule_distance = min(min_capsule_distance, distance)
    features["closest-capsule"] = 1.0 / (min_capsule_distance + 1)

    # Feature 7: Stopped
    features["stopped"] = 0
    if action == Directions.STOP:
        features["stopped"] = 1

    return features

Traceback (most recent call last):
  File "pacman.py", line 680, in <module>
    runGames( **args )
  File "pacman.py", line 646, in runGames
    game.run()
  File "/home/vboxuser/pacman-main/game.py", line 686, in run
    action = agent.getAction(observation)
  File "/home/vboxuser/pacman-main/qlearningAgents.py", line 159, in getAction
    action = QLearningAgent.getAction(self,state)
  File "/home/vboxuser/pacman-main/qlearningAgents.py", line 108, in getAction
    return self.computeActionFromQValues(state) 
  File "/home/vboxuser/pacman-main/qlearningAgents.py", line 89, in computeActionFromQValues
    return random.choice(maxActions)
  File "/usr/lib/python2.7/random.py", line 277, in choice
    return seq[int(self.random() * len(seq))]  # raises IndexError if seq is empty
IndexError: list index out of range
  
  
  
Traceback (most recent call last):
  File "pacman.py", line 680, in <module>
    runGames( **args )
  File "pacman.py", line 646, in runGames
    game.run()
  File "/home/vboxuser/pacman-main/game.py", line 700, in run
    self.state = self.state.generateSuccessor( agentIndex, action )
  File "pacman.py", line 107, in generateSuccessor
    PacmanRules.applyAction( state, action )
  File "pacman.py", line 343, in applyAction
    raise Exception("Illegal action " + str(action))
Exception: Illegal action None
  
  
def computeActionFromQValues(self, state):
    """
      Compute the best action to take in a state.  Note that if there
      are no legal actions, which is the case at the terminal state,
      you should return None.
    """
    # Get the list of legal actions
    legal_actions = self.getLegalActions(state)
    
    # If there are no legal actions, return None
    if not legal_actions:
        return None

    max_q_value = float('-inf')
    max_actions = []

    for action in legal_actions:
        q_value = self.getQValue(state, action)
        if q_value > max_q_value:
            max_q_value = q_value
            max_actions = [action]
        elif q_value == max_q_value:
            max_actions.append(action)

    # Return a random action among the actions with the maximum Q-value
    if max_actions:
        return random.choice(max_actions)
    else:
        return legal_actions[0]  # If max_actions is empty, return the first legal action
      
def getFeatures(self, state, action):
        # extract the grid of food and wall locations and get the ghost locations
        food = state.getFood()
        capsules = state.getCapsules()
        walls = state.getWalls()
        ghosts = state.getGhostPositions()

        features = util.Counter()

        features["bias"] = 1.0

        # compute the location of pacman after he takes the action
        x, y = state.getPacmanPosition()
        dx, dy = Actions.directionToVector(action)
        next_x, next_y = int(x + dx), int(y + dy)

        # check for imminent ghost collisions
        features["#-of-not-scared-ghosts-1-step-away"] = sum((next_x, next_y) in Actions.getLegalNeighbors(g, walls) for g in ghosts)

        # check for ghosts one step away
        features["#-of-not-scared-ghosts-2-step-away"] = sum(1 for g in ghosts if manhattanDistance((next_x, next_y), g) == 2)

        # check if pacman will eat food
        if food[next_x][next_y]:
            features["eats-food"] = 1.0

        # compute the distance to the closest food
        dist = closestFood((next_x, next_y), food, walls)
        if dist is not None:
            # make the distance a number less than one otherwise the update
            # will diverge wildly
            features["closest-food"] = float(dist) / (walls.width * walls.height)

        # check if pacman will eat a capsule
        if (next_x, next_y) in capsules:
            features["eats-capsule"] = 1.0

        # count the number of remaining food
        features["remaining-food"] = float(food.count()) / (walls.width * walls.height)

        # count the number of remaining capsules
        features["remaining-capsules"] = float(len(capsules)) / (walls.width * walls.height)

        # normalize the features
        features.divideAll(10.0)

        return features

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

        # Feature: distance to the closest non-scared ghost
        non_scared_ghost_distances = [
            util.manhattanDistance((next_x, next_y), ghost.getPosition())
            for ghost in non_scared_ghosts
        ]
        if non_scared_ghost_distances:
            features["closest-non-scared-ghost"] = min(
                non_scared_ghost_distances
            ) / (walls.width * walls.height)

        # Feature: distance to the closest scared ghost
        scared_ghost_distances = [
            util.manhattanDistance((next_x, next_y), ghost.getPosition())
            for ghost in scared_ghosts
        ]
        if scared_ghost_distances:
            features["closest-scared-ghost"] = min(
                scared_ghost_distances
            ) / (walls.width * walls.height)

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
