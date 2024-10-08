def dict_make(message, default_text):
    return {
        'message': message,
        'default_text': default_text
    }

menu_1_messages = {
    1: dict_make('SQL Position Challenges', 'admin'),
    2: dict_make('SQL Position Challenges', 'admin'),
    3: dict_make('SQL Position Challenges', 'username'),
    4: dict_make('SQL Position Challenges', '1'),
    5: dict_make('SQL Position Challenges', '1'),
}


menu_2_messages = {
    1: dict_make('Character Filter Challenges', 'Pork Carnitas Taco'),
    2: dict_make('Character Filter Challenges', 'New Taco!'),
    3: dict_make('Character Filter Challenges', '999999'),
    4: dict_make('Character Filter Challenges', '100'),
    5: dict_make('Character Filter Challenges', 'taco_name'),
}
all_messages = {
    1: menu_1_messages,
    2: menu_2_messages
    # Add more menus and messages here
}

