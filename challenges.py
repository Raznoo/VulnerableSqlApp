import sqlite3
import sql_helpers as filters
# Dictionary to map challenges to their respective handler functions
challenge_functions = {}
# Decorator to register challenge handlers


def register_challenge(menu_id, challenge_id):
    def wrapper(func):
        challenge_functions[(menu_id, challenge_id)] = func
        return func
    return wrapper

# Example of handling different challenges with functions


def default_query(query: str, conn, custom_response_succ='Found Data!', custom_response_fail='Search has no results', custom_response_error=None):
    try:
        cursor = conn.execute(query)
        results = cursor.fetchall()
        if results:
            return {
                'message': custom_response_succ,
                'data': [dict(row) for row in results]
            }
        else:
            return {'message': custom_response_fail}
    except sqlite3.Error as e:
        error_message = 'An error occurred: ' + str(e)
        if custom_response_error:
            error_message += f'\n{custom_response_error}'
        return {'message': error_message}


@register_challenge(1, 1)
def challenge_1_1(search_query, conn):
    query = f"SELECT username, password FROM menu_1 WHERE username = '{
        search_query}'"
    return default_query(query, conn)


@register_challenge(1, 2)
def challenge_1_2(search_query, conn):
    query = f"SELECT username, password FROM menu_1 WHERE username LIKE '%{
        search_query}%' ORDER BY 1"
    return default_query(query, conn)


@register_challenge(1, 3)
def challenge_1_3(search_query, conn):
    query = f"SELECT (SELECT {
        search_query} FROM menu_1 WHERE username != 'admin') as 'Custom Query'"
    return default_query(query, conn)


@register_challenge(1, 4)
def challenge_1_4(search_query, conn):
    query = f"SELECT * FROM menu_1 where username != 'admin' order by {
        search_query}"
    return default_query(query, conn)


@register_challenge(1, 5)
def challenge_1_5(search_query, conn):
    query = f"SELECT username, password FROM menu_1 WHERE username = (SELECT username FROM menu_1 WHERE username LIKE '%user%'  LIMIT {
        search_query}) UNION SELECT created_at, created_at FROM menu_1 ORDER BY {search_query}"
    return default_query(query, conn)


@register_challenge(2, 1)
def challenge_2_1(search_query, conn):
    search_query = filters.cyclic_apply_filters(search_query,
                                                [filters.filter_whitespace])
    query = f"SELECT taco_name,sauce_type FROM menu_2 WHERE taco_name LIKE '%{
        search_query}%'"
    return default_query(query, conn,
                         custom_response_succ=f'[DATA Found]\n Query Sent: \n{
                             query}',
                         custom_response_fail=f'[No DATA] \nQuery Sent: \n{
                             query}',
                         custom_response_error=f'[ERROR] \nQuery Sent: \n{query}')


@register_challenge(2, 2)
def challenge_2_2(search_query, conn):
    search_query = filters.cyclic_apply_filters(search_query,
                                                [filters.filter_whitespace,
                                                 filters.filter_dashes,
                                                 filters.filter_union_good,
                                                 filters.filter_single_quote])
    query = f"SELECT '{search_query}' as 'Custom Query' from menu_2"
    return default_query(query, conn)


@register_challenge(2, 3)
def challenge_2_3(search_query, conn):
    search_query = filters.cyclic_apply_filters(search_query,
                                                [filters.filter_dashes,
                                                 filters.filter_union_good,
                                                 filters.filter_double_quote,
                                                 filters.filter_single_quote])
    query = f"SELECT taco_name, meat_portion from menu_2 UNION SELECT 'New Taco', {
        search_query} from menu_2"
    return default_query(query, conn)


@register_challenge(2, 4)
def challenge_2_4(search_query, conn):
    search_query = filters.apply_many_filters(search_query,
                                              [filters.filter_dashes,
                                               filters.filter_whitespace,
                                               filters.filter_union_good,
                                               filters.filter_double_quote,
                                               filters.filter_single_quote,
                                               filters.filter_select_good])
    query = f"SELECT taco_name,sauce_type FROM menu_2 WHERE taco_name LIKE '%{
        search_query}%'"
    return default_query(query, conn)


@register_challenge(2, 5)
def challenge_2_5(search_query, conn):
    query = f"SELECT {search_query} as 'Custom Query' FROM menu_2 WHERE taco_name != 'Hacker Burrito'"
    if filters.crash_filter(search_query, [filters.filter_dashes,
                                           filters.filter_whitespace,
                                           filters.filter_double_quote,
                                           filters.filter_single_quote,
                                           filters.filter_select_bad]):
        return default_query(query, conn)
    else:
        return {
            'message': "BONK! Unsafe Character Submitted",
        }

# Add more challenge functions as needed
# unicode(substr((seLect/**/secret_flag/**/from/**/menu_2/**/ORDER/**/BY/**/1/**/DESC),1,1))