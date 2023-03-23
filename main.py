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




class BetterExtractor(FeatureExtractor):
    def getFeatures(self, state, action):
        # Extract the grid of food and walls, and the Pacman position
        food = state.getFood()
        walls = state.getWalls()
        x, y = state.getPacmanPosition()

        features = util.Counter()

        features["bias"] = 1.0

        # Compute the distance to the nearest food
        min_food_distance = float("inf")
        for food_x, food_y in food.asList():
            distance = util.manhattanDistance((x, y), (food_x, food_y))
            if distance < min_food_distance:
                min_food_distance = distance
        features["closest-food"] = min_food_distance

        # Check if action leads to a wall
        dx, dy = Actions.directionToVector(action)
        next_x, next_y = int(x + dx), int(y + dy)
        if walls[next_x][next_y]:
            features["hit-wall"] = 1
        else:
            features["hit-wall"] = 0

        # Check if action leads to a ghost
        ghost_states = state.getGhostStates()
        ghost_positions = [ghost_state.getPosition() for ghost_state in ghost_states]
        ghost_distances = [util.manhattanDistance((x, y), ghost_position) for ghost_position in ghost_positions]
        if min(ghost_distances) <= 1:
            features["near-ghost"] = 1
        else:
            features["near-ghost"] = 0

        # Compute the distance to the nearest power pellet
        power_pellets = state.getCapsules()
        if power_pellets:
            min_power_pellet_distance = min([util.manhattanDistance((x, y), pellet) for pellet in power_pellets])
            features["closest-power-pellet"] = min_power_pellet_distance
        else:
            features["closest-power-pellet"] = 0

        # Encourage the Pacman to eat power pellets when ghosts are nearby
        features["eat-power-pellet"] = 0
        if features["near-ghost"] and power_pellets:
            features["eat-power-pellet"] = 1

        return features
