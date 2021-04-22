from pymongo import MongoClient
import json


def get_connection():
    """Connect to MongoDB"""

    client = MongoClient('db_mongo', 27017)
    db = client.RedditDB

    posts = db.posts
    users = db.users

    return posts, users


def get_json():
    """Form the lists"""

    jsn, unique, u_id = [], [], []
    posts, users = get_connection()

    posts_dict = posts.find()
    users_dict = users.find()
    posts_list = list(posts_dict)
    users_list = list(users_dict)
    posts_len = len(posts_list)
    users_len = len(users_list)

    diff = posts_len - users_len

    if diff:
        for post in posts_list[users_len:]:
            author = post["author"]
            user = users.find_one({"username": author})
            users_list.append(user)

    for post_info, user_info in zip(posts_list, users_list):
        _, uid, post_url, post_date, author, number_of_comments, number_of_votes, post_category = dict(
            post_info).values()
        _, _, user_cake_day, user_karma, post_karma, user_comment_karma = dict(user_info).values()

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

    return j, unique, u_id, jsn


def write_in_database(data):
    """Insert data to database"""

    print(data)

    uid, author, post_date, post_url, number_of_comments, number_of_votes, post_category, user_karma, \
    user_comment_karma, post_karma, user_cake_day = data

    posts, users = get_connection()

    count = len(list(users.find({"username": author})))

    if count:
        users.update_one({"username": author},
                         {"$set": {"user_cake_day": user_cake_day,
                                   "user_karma": user_karma,
                                   "post_karma": post_karma,
                                   "comment_karma": user_comment_karma
                                   }})
    else:
        users.insert_one({"username": author,
                          "user_cake_day": user_cake_day,
                          "user_karma": user_karma,
                          "post_karma": post_karma,
                          "comment_karma": user_comment_karma
                          })

    posts.insert_one({
        "uid": uid,
        "post_url": post_url,
        "post_date": post_date,
        "author": author,
        "number_of_comments": number_of_comments,
        "number_of_votes": number_of_votes,
        "post_category": post_category
    })

    print('Data inserted into db!')


def delete_data(uid):
    """Delete row following uid"""

    posts, _ = get_connection()
    posts.delete_one({"uid": uid})


def update_data(uid, author, post_date, post_url, number_of_comments, number_of_votes, post_category, user_karma,
                user_comment_karma, post_karma, user_cake_day):
    """Update existing data with new values"""

    posts, users = get_connection()

    print(uid, author, post_date, post_url, number_of_comments, number_of_votes, post_category, user_karma,
                user_comment_karma, post_karma, user_cake_day)

    posts.update_one({"uid": uid},
                     {"$set": {
                         "post_url": post_url,
                         "post_date": post_date,
                         "post_category": post_category,
                         "number_of_comments": number_of_comments,
                         "number_of_votes": number_of_votes
                     }})

    users.update_one({"username": author},
                     {"$set": {
                         "user_cake_day": user_cake_day,
                         "user_karma": user_karma,
                         "post_karma": post_karma,
                         "comment_karma": user_comment_karma
                     }})
