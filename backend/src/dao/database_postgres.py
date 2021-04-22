import psycopg2
import json


def create_connection():
    conn = psycopg2.connect(dbname='RedditDB', user='postgres', password=123456, host='db_postgres', port=5432)
    cursor1 = conn.cursor()
    cursor2 = conn.cursor()

    return cursor1, cursor2, conn


def create_table():
    """Create new table"""
    cursor1, cursor2, conn = create_connection()
    try:
        cursor1.execute('''CREATE TABLE users (
                         Id SERIAL PRIMARY KEY,
                         Username char(100) UNIQUE,
                         User_karma integer,
                         User_cake_day char(100),
                         Post_karma integer,
                         Comment_karma integer);''')

        cursor2.execute('''CREATE TABLE posts (
                        Id SERIAL PRIMARY KEY,
                        UID char(100),
                        Post_url char(100),
                        Author char(100),
                        FOREIGN KEY (Author) REFERENCES users (Username) ON DELETE CASCADE,
                        Post_date char(100),
                        Number_of_comments char(100),
                        Number_of_votes char(100),
                        Post_category char(100));''')
    except Exception as e:
        print("Error while forming tables following:")
        print(e)

    conn.commit()
    conn.close()


def get_json():
    """Form the lists"""
    cursor1, cursor2, conn = create_connection()

    jsn, unique, u_id = [], [], []
    cursor1.execute("SELECT * FROM posts")
    cursor2.execute("SELECT * FROM users")
    for post_info, user_info in zip(cursor1, cursor2):
        post_info = list(map(lambda x: f"{x}".rstrip(), post_info))
        user_info = list(map(lambda x: f"{x}".rstrip(), user_info))
        _, uid, post_url, author, post_date, post_category, number_of_comments, number_of_votes = post_info
        _, _, user_cake_day, user_karma, post_karma, user_comment_karma = user_info
        jsn.append({"uid": uid,
                    "author": author,
                    "post_date": post_date.split()[0],
                    "post_url": post_url,
                    "number_of_comments": number_of_comments,
                    "number_of_votes": number_of_votes,
                    "post_category": post_category,
                    "user_karma": user_karma,
                    "user_comment_karma": user_comment_karma,
                    "post_karma": post_karma,
                    "user_cake_day": user_cake_day})
        unique.append(f"/posts/{uid}/")
        u_id.append(uid)

    j = json.dumps(jsn)

    conn.close()

    return j, unique, u_id, jsn


def write_in_database(data):
    """Insert data to database"""

    cursor1, cursor2, conn = create_connection()

    uid, author, post_date, post_url, number_of_comments, number_of_votes, post_category, user_karma, \
    user_comment_karma, post_karma, user_cake_day = data

    cursor1.execute(f"SELECT username FROM users WHERE username='{author}'")
    count = len(list(cursor1))
    if not count:
        cursor1.execute(f"INSERT INTO users (username, user_cake_day, user_karma, post_karma, comment_karma) \
                     VALUES ('{author}', '{user_cake_day}', '{user_karma}', '{post_karma}', '{user_comment_karma}')")
    else:
        cursor1.execute(f"UPDATE users"
                        f" SET user_cake_day = '{user_cake_day}', user_karma = '{user_karma}',"
                        f" post_karma = '{post_karma}', comment_karma = '{user_comment_karma}'"
                        f" WHERE username = '{author}'")
    cursor2.execute(f"INSERT INTO posts (uid, post_url, post_date, author, number_of_comments, number_of_votes, \
                                        post_category) \
                    VALUES ('{uid}', '{post_url}', '{post_date}', '{author}', '{number_of_comments}', \
                            '{number_of_votes}', '{post_category}')")

    print('Data inserted into db!')
    conn.commit()
    conn.close()


def delete_data(uid):
    """Delete row following uid"""

    cursor1, _, conn = create_connection()

    cursor1.execute(f"DELETE FROM posts WHERE uid = '{uid}'")
    conn.commit()
    conn.close()


def update_data(uid, author, post_date, post_url, number_of_comments, number_of_votes, post_category, user_karma,
                user_comment_karma, post_karma, user_cake_day ):
    cursor1, cursor2, conn = create_connection()

    cursor1.execute(f"UPDATE users"
                    f" SET user_cake_day = '{user_cake_day}', user_karma = '{user_karma}',"
                    f" post_karma = '{post_karma}', comment_karma = '{user_comment_karma}'"
                    f" WHERE username = '{author}'")

    cursor2.execute(f"UPDATE posts"
                    f" SET post_url = '{post_url}', post_date = '{post_date}',"
                    f" post_category = '{post_category}', number_of_comments = '{number_of_comments}',"
                    f" number_of_votes = '{number_of_votes}'"
                    f" WHERE uid = '{uid}'")

    conn.commit()
    conn.close()
