# Reddit scraper (main.py)

The script collects the following information from Reddit.com: post URL; post date; number of comments; number of votes; post category; username; user karma; user cake day;post karma;comment karma. The collected information is saved to a file called reddit-YYYYMMDDHHMM.txt, where YYYY is year; MM is month; DD is day; HH is hours; MM is minutes. The output file contains 100 records. The script logs all significant events.

# RESTful service (server.py)

Service impliments CRUD operations with file made by Reddit scrapper. GET /posts/ returns the contents of the entire file in JSON format. GET /posts/<UNIQUE_ID>/ returns the contents of the string with UNIQUE_ID. POST /posts/ adds a new string to the file; if the file does not exist, it creates a new file and checks the content of the file for UNIQUE_ID duplicates before creating the string. DELETE /posts/UNIQUE_ID/ deletes the file string with UNIQUE_ID. PUT /posts/UNIQUE_ID/ changes the content of the UNIQUE_ID file string

# GET request

- do GET request to /posts/ to get all data from file.

# POST request

- do POST request to /posts/ with JSON data to save it in file.

# DELETE request

- do DELETE request to /posts/UNIQUE_ID/ to delete post by unique id in file

# PUT request

- do PUT request to /posts/UNIQUE_ID/ to update existing post by unique id in file with JSON data you write using e.g. postman.

# GIT Hooks

- install pre-commit & commit-msg files to your local git/hooks to prohibit push to master and commit messages with less than 10 characters and less than two words, as well as those containing letters of the Russian alphabet

# Need to run 
- libs (check it in "libs in-use"),
- Google Chrome browser & Google [geckodriver](https://chromedriver.chromium.org/),
- e.g. POSTMAN.
- pgAdmin 4
- mongoDBCompass

# How to run
- install main.py to your local dir to work with postgres or main_mongo.py to work with mongo,
- install server.py to your local dir to work with postgres or server_mongo.py to work with mongo,
- install databese.py (work with postgres),
- install database_mongo.py (work with postgres)
- use "python3 server.py" or "python 3 server_mongo.py" to run the service,
- look forward the files .log ( the info & errors ),
- use GET, POST, UPDATE, DELETE requests, e.g. using POSTMAN.

# Libs in-use
- logging, 
- bs4,
- selenium,
- lxml,
- multiprocessing,
- threading.
- psycopg2
- pymongo

