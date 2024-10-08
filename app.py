from flask import Flask, render_template, request, jsonify
from challenges import challenge_functions
from menu_messages import all_messages
from init_db import init_db
import sqlite3
DB_NAME = 'challenges.db'

init_db(DB_NAME)

app = Flask(__name__)
conn = sqlite3.connect(DB_NAME, check_same_thread=False)
conn.row_factory = sqlite3.Row  # Enables dictionary-like access to rows


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/menu<int:menu_id>/challenge<int:challenge_id>',
           methods=['GET', 'POST'])
def handle_challenge(menu_id, challenge_id):

    # Get the message and default text for the current menu
    menu_info = all_messages.get(menu_id, {
    }).get(challenge_id, {
        'message': '❌❌This menu has not been made yet.❌❌',
        'default_text': 'Sowwy...'})

    if request.method == 'POST':
        search_query = request.form['searchQuery']

        # Check if the challenge exists in the mapping
        handler = challenge_functions.get((menu_id, challenge_id))
        if handler:
            # Call the respective challenge handler
            response = handler(search_query, conn)
        else:
            response = {
                'message': "Challenge NOT MADE!",
                'search_query': search_query
            }

        return jsonify(response)

    # Render search page
        # Pass the default text and message to the template
    return render_template('search.html',
                           menu_id=menu_id,
                           challenge_id=challenge_id,
                           default_text=menu_info['default_text'],
                           menu_message=menu_info['message'])

@app.route('/menu<int:menu_id>/intro', methods=['GET'])
def intro(menu_id):

    # Define an explanation for each menu
    explanations = {
        1: "In This section you will be exploring different spots that the injection could occur and different SQL Statements. Keep in mind not all challenges are vulnerable and it will be up to you to distinguish which are and aren't.",
        2: "In this section you will bypass filter restrictions on SQL statements.",
        3: "In this section you will use the context provided in the statement and the webapp to perform Blind SQL queries. Keep in mind ALL changes that occur on the webapp",
        4: "With some practice in blind sql queries, you will take it a step further. Queries in this section are prepared in a way they can only be solved with Error-Based Blind SQL injection",
        5: "In this section you will use your extra spidey senses in order to overcome Time-Based Blind SQL injections",
    }

    # Get the explanation for the selected menu
    explanation = explanations.get(menu_id, "This section has not been made yet :(")

    # Fetch the entire table based on the menu
    
    if all_messages.get(menu_id):
        query = f"SELECT * FROM menu_{menu_id}"
    else:
        query = None
        
    table_data = None
    if query:
        cursor = conn.execute(query)
        rows = cursor.fetchall()
        table_data = [dict(row) for row in rows]  # Convert each row to a dictionary

    # Pass explanation and table data to the template
    return render_template('intro.html', menu_id=menu_id, explanation=explanation, table_data=table_data)


if __name__ == '__main__':
    app.run(debug=True)
