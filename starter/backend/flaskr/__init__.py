import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
  page = (request.args.get('page', 1, type=int))
  start = (page - 1) * 10 
  end = start + 10
  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions



def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, origins=['*'])

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response

  
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''

  @app.route('/categories', methods=['GET',])
  def get_categories():

    selection = Category.query.all()

    categories = [category.format() for category in selection]

    if len(categories) == 0:
      abort(404)
  
    return jsonify({
            'success': True,
            'categories': {category.id: category.type for category in selection}
        })
  

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  @app.route('/questions', methods=['GET','POST'])
  def get_questions():

    if request.method == 'GET':
      selection = Question.query.all()
      
    if request.method == 'POST':
      content = request.json
      search_term = content['searchTerm']
      print(format(search_term))
      selection = Question.query.filter(Question.question.ilike('%' + search_term + '%')).all()
    
    questions = paginate_questions(request, selection)
    categories = Category.query.all()

    if len(questions) == 0:
      abort(404)


    
  
    return jsonify({
      'success': True,
      'questions': questions,
      'categories': {category.id: category.type for category in categories},
      'total_questions': len(selection),
      'current_category': None,
    })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  @app.route('/questions/<question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question_id = int(question_id)
    except:
      abort(400, {'message':'Question Id needs to be an Integer'})
    
    try:
      question = Question.query.get(question_id)
      question.delete()
    except:
      abort(404)
    return jsonify({'success' : True})
    
    
  
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  @app.route('/questions/create', methods=['POST'])
  def create_question():

  
    content = request.json
    question = content['question']
    answer = content['answer']
    category = content['category']
    difficulty = content['difficulty']

    if len(question) < 10:
      abort(400, {'message':'Question needs to be at least 10 characters long'})

    if len(answer) < 1:
      abort(400, {'message':'Answer needs to be at least one character'})

    if not isinstance(category, str):
      abort(400, {'message':'Category needs to be a String'})

    if not isinstance(difficulty, int):
      abort(400, {'message':'Difficulty needs to be an Integer'})

    category_full = Category.query.get(category)
    if category_full is None:
      abort(400, {'message':'Category does not exist'})

    if (difficulty < 1 or difficulty > 5):
      abort(400, {'message':'Difficulty needs to be an Integer of 1 to 5'})
    
    new_question = Question(question,answer,category,difficulty)
    new_question.insert()

    return jsonify({
      'success': True,
      'question': new_question.format()
    })


  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  #done & combined with get endpoint

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

  @app.route('/categories/<category_id>/questions', methods=['GET'])
  def get_questions_by_category(category_id):

    selection = Question.query.filter_by(category=category_id).all()
     
    
    questions = paginate_questions(request, selection)
    categories = Category.query.all()

    if len(questions) == 0:
      abort(404)


    
    return jsonify({
      'success': True,
      'questions': questions,
      'categories': {category.id: category.type for category in categories},
      'total_questions': len(selection),
      'current_category': None,
    })


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  @app.route('/quizzes', methods=['POST'])
  def get_random_quiz_question():

    content = request.json
    category = content['quiz_category']
    previous_questions = content['previous_questions']

    if category['id'] is 0:
      questions = Question.query.all()
    else:
      questions = Question.query.filter_by(category=category['id']).all()

    if len(questions) is 0:
      abort(404)

    for prev_question in previous_questions:
      questions = [question for question in questions if question.id !=prev_question]

    if len(questions) is 0:
      abort(422, {'message':'No more questions to display'})

    random_question = random.choice(questions)

    return jsonify({
      'success': True,
      'question': random_question.format()
    })


  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success' : False,
      'error' : 404,
      'message' : 'Not Found'
    }), 404

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success' : False,
      'error' : 400,
      'message' : error.description['message']
    }), 400

  @app.errorhandler(422)
  def bad_request(error):
    return jsonify({
      'success' : False,
      'error' : 422,
      'message' : error.description['message']
    }), 422
  
  return app

    