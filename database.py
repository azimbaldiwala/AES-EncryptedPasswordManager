import sqlite3


def run_query(query: str):
        """
        This method is used to run a query.
        :param query: Must be in valid SQL syntax.
        :return: None
        """

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()


def run_query_and_return_all_data(query):
        """
               This method is used to run a query.
               :param query: Must be in valid SQL syntax.
               :return: None
               """

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return data


def create_table_users():
    query = """
        create table users (username varchar2, password varchar2);
    """
    run_query(query=query)



def check_username(username):
    query = f"""
        select * from  users where username='{username}';
    """
    if run_query_and_return_all_data(query):
        return False # Username already taken
    return True 


def signup(username, password):
    query = f"""
        insert into users values('{username}','{password}');
    """
    run_query(query)


def validate_login(username, password):
    query = f"""
        select * from users where username='{username}' and password='{password}';
    """
    if run_query_and_return_all_data(query):
        return True
    return None


def create_password_table():
    query = """

        create table passwords (username varchar2, password_for varchar2, password BLOB);
    """
    run_query(query)

def insert_new_password(username, password_for, password):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO passwords (username,password_for,password) VALUES (?,?,?) """,
                   (username, password_for, password))

        
    conn.commit()
    cursor.close()
    conn.close()



def get_pass(username, password_for):
    query = f"""
        select password from passwords where username='{username}' and password_for='{password_for}';
    """
    
    return run_query_and_return_all_data(query)

def update_pass(username, password_for, new_password):
    query = f"""
        update table passwords set password='{new_password}' where username='{username}' and password_for='{password_for}';
    """

    run_query(query)


def delete_user(username):
    query = f"""
        delete from users where username='{username}';
    """
    run_query(query)
    
    query = f"""
        delete from passwords where username='{username}';
    """
    run_query(query)


def delete_password(username, password_for):
    query = f"""
        delete from passwords where username='{username}' and password_for='{password_for}';
    """
    run_query(query)


def show_titles(username):
    query = f"""
        select password_for from passwords where username='{username}';
    """
    data = run_query_and_return_all_data(query)
    return data

def check_title(title, username):
    query = f"""
        select * from passwords where password_for='{title}' and username='{username}';
    """ 
    if run_query_and_return_all_data(query):
        return True 
    return False 
