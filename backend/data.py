import json
import logging
from uuid import uuid1

from main import main


def get_json(file_name):
    """Form the files"""

    jsn, unique, u_id = [], [], []
    try:
        with open(file_name, "r+") as f:
            data = f.readlines()
    except Exception:
        logging.basicConfig(filename=f"serverlog-{uuid1().hex[:7]}.log", level=logging.INFO)
        logging.exception("Reddit file not found! Forming new one.")
        main()
        return get_json(file_name)

    for line in data:
        uid, post_date, post_url, number_of_comments, number_of_votes, post_category, \
        author, user_karma, post_karma, user_comment_karma, user_cake_day = line.split("; ")
        jsn.append({"uid": uid,
                    "author": author,
                    "post_date": post_date,
                    "post_url": post_url,
                    "number_of_comments": number_of_comments,
                    "number_of_votes": number_of_votes,
                    "post_category": post_category,
                    "user_karma": user_karma,
                    "user_comment_karma": user_comment_karma,
                    "post_karma": post_karma,
                    "user_cake_day": user_cake_day.split()[0]})
        unique.append(f"/posts/{uid}/")
        u_id.append(uid)

    j = json.dumps(jsn)

    return j, unique, u_id, jsn


def write_in_file(file, file_name, mode="w"):
    """Change the file"""

    r = []
    for i in file:
        j = str(i)[1:-1].split("'")[3:][::4]
        r.append("; ".join(j))

    file_mode = "w+" if mode == "w" else "a"
    with open(file_name, file_mode) as f:
        for i in r:
            f.write(i)
            f.write("\n")
