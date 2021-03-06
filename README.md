# Web-Backend-With-Django
A personal project to learn Django

## REST API documentation for each service

### Microblogging services:
1) users.py
    - **getUserID(db, username)** -- local python function to find userID given username and db
    - **/users/login/{username}** -- called by get request from timelines service to find password given username
    - **/users** -- returns all users' public info
    - **/users/{username}** -- returns specific user's public info
    - **/users/{username}/followers** -- called by get request from timelines service to find user's followers
2) timelines.py
    - **setLogin(username)** -- local python function that sends get request to "users/login/{username}" to find and set password and username for authentication verify function given username (**does not work correctly**)
    - **/timelines/{username}** -- returns specific user's own posts
    - **/timelines/{username}/{post_id}** -- returns specific post from the specific user
        - ex: the url "/timeline/brandon2306/1" should bring up the user's first post
    - **/timelines/{username}/post** -- create post as a certain user (**authentication needed**)
    - **/home/{username}** -- calls setLogin(username) function and redirects user to "/home/{username}/auth"
    - **/home/{username}/auth** -- sends get request to "/users/{username}/followers" endpoint in users service, returns posts of users that the specific user follows (**authentication needed**)
    - **/public** -- returns all existing posts
3) likes.py
    - **{liker_username}/{username}/{post_id}** -- create a like on a specific post
    - **/likes/count/{username}/{post_id}** -- get request to see how many likes a specific post received
    - **/likes/{liker_username}** -- get request to retrieve a list of posts a specific user liked
    - **/likes/popular** -- get request to see a list of popular posts liked by many users
4) polls.py
    - **/polls** -- returns all existing polls
    - **/polls/create** -- POST method that creates post given username, question, and list of responses
    - **/polls/vote/{poll_id}** -- POST method where user can vote a response from a certain post given username, post_id, and the specific response
        - User cannot vote twice as well.
5) registry.py
    - **Important** -- the registry assumes the url provided by registered services has a "/health" route that can return a 200 response to GET requests
    - **/registry** -- returns all instances of all registered services
    - **/registry/{servicename}** -- returns all instances of servicename
    - **/registry/{servicename} POST** -- registers an instance of servicename. The url is provided in the format: text="url"

You can also create a post as a certain user by running these commands in a new command line:
```
# examples for creating post
http -a bob123:hello123 localhost:8000/timelines/bob123/post text="today sucks!"
http -a bob123:hello123 localhost:8000/timelines/terraria2/post text="i like games"
http -a bob123:hello123 localhost:8000/timelines/brandon2306/post text="i agree!" url ="http://localhost:8000/timeline/bob123/1"
http -a bob123:hello123 localhost:8000/timelines/brandon2306/post text="i agree!" url ="http://localhost:8000/polls/10"
```
Further description on how the data is organized can be seen from the .csv files and .db file

examples using hey:
```
hey -m POST -a bob123:hello123 http://localhost:8000/timelines/bob123/post text="test" 
hey -m POST -a bob123:hello123 http://localhost:8000/timelines/bob123/asyncpost text="test"
```
