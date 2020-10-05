# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Endpoints

The Trivia-API Backend provides a couple of Endpoints for providing the full gaming experience. Please find each endpoint documented below:



GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
```
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}
```

GET '/questions'
- Fetches all questions, paginated, max 10 questions per page. Takes current page number as argument.
- Request Arguments: page(int)
- Returns: An object including all categories, the current category (null in this case), all questions, the success status, and the number of total_questions. Categories are provided with the id as key and string as value. Questions are provided as a list of dictionaries each providing values for answer,category,difficulty,id, and question.
```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
  ], 
  "success": true, 
  "total_questions": 2
}
```

POST '/questions'
- Fetches all questions fullfilling a search term, paginated, max 10 questions per page. Takes current page number as argument. The search is run on the question string, ignores case and is independent of where it is found in the string.
- Request Arguments: page(int)
- Request Body:
```
{
    "searchTerm": "Cassius"
}
```
- Returns: An object including all categories, the current category (null in this case), all questions, the success status, and the number of total_questions. Categories are provided with the id as key and string as value. Questions are provided as a list of dictionaries each providing values for answer,category,difficulty,id, and question.
```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }
  ], 
  "success": true, 
  "total_questions": 1
}
```

DELETE '/questions/<question_id>'
- Deletes a question, as defined by a question_id
- Request Arguments: question_id(int)
- Returns: The success of the operation, provided as value of a dict.
```
{
  "success": true
}
```

POST '/questions/create'
- Creates a new question as provided in the json request body. Every provided category id must be of type string & point to an existing category. The difficulty must be an integer between 1 to 5. The question must have at least 10, and the answer at least one character(s).
- Request Arguments: None
- Request Body:
```
{
    "question": "Is this a new question?",
    "answer": "This is a new question",
    "difficulty": 1,
    "category": "4"
}
```
- Returns: a dictionary containing the posted question as well as a success status.
```
{
  "question": {
    "answer": "This is a new question", 
    "category": 4, 
    "difficulty": 1, 
    "id": 35, 
    "question": "Is this a new question?"
  }, 
  "success": true
}
```

GET '/categories/<category_id>/questions'
- Fetches all questions, paginated, max 10 questions per page. Takes category_id & current page number as argument.
- Request Arguments: category_id(str), page(int)
- Returns: A dict including all categories, the current category (as specified in the argument), all related questions, the success status, and the number of total_questions. Categories are provided with the id as key and string as value. Questions are provided as a list of dictionaries each providing values for answer,category,difficulty,id, and question.
```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": 1, 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }
  ], 
  "success": true, 
  "total_questions": 2
}
```

POST 'quizzes'
- Fetches a random question of either all question or a given category. In selecting a random question, previously displayed questions can be excluded by providing question ids as an array. If no particular category shall be chosen, provide '0' for category id.
- Request Arguments: None
- Request Body:
```
{
    "previous_questions": [21],
    "quiz_category": {
        "type": "Science",
        "id": "1"
    }
}
```

- Returns: A random question as specified in the request body. In case no more questions are available for display given by the previous_questions array, a 422 is thrown.
```
{
  "question": {
    "answer": "test", 
    "category": 1, 
    "difficulty": 1, 
    "id": 33, 
    "question": "Is this a question"
  }, 
  "success": true
}
```





## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```