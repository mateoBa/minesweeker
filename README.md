# Minesweeper

API RESTful to perform the game

Instalation

```sh
$ git clone https://github.com/mateoBa/minesweeper.git
$ cd minesweeper
$ pip3 install -r requirements.txt
$ python3 manage.py migrate
$ python3 manage.py createsuperuser
$ python3 manage.py runserver
```

Implementing api. Examples with http but you can use whatever you want CURL, python requests ...

```sh
$ http post http://127.0.0.1:8000/api/v1/api_token/ username=username_created_from_instalation password=password
```
it retrieves an api token, you need to use this to make the below requests



To see all the games created by user (GET method)
```sh
$ http http://127.0.0.1:8000/api/v1/game 'Authorization: Token Token_from_the_first_step'
```

For creating a new game (POST method)
```sh
$ http post http://127.0.0.1:8000/api/v1/game columns=3 rows=3 mines=3 'Authorization: Token Token_from_the_first_step'
```

To press or do click in a row (PUT method)
```sh
$ http put http://127.0.0.1:8000/api/v1/game x=X y=Y 'Authorization: Token Token_from_the_first_step'
```

I am taking some basic rules to draw the matrix. I am returning list of list to do simpler to test it, but if it will be implemented in a clint we should send the entire information and the client is going to represent it in the best way.

Using the ? sign to represent a hidden box and '*' sign to represent a Bomb. The api returns the matrix in list of list, every list is a column just in case. 
