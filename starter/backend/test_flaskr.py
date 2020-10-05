import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))

    def test_get_paginated_questions_out_of_bounds(self):
        res = self.client().get('questions?page=9999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    
    def test_get_filtered_questions(self):
        search_term = {'searchTerm': 'a'}

        res = self.client().post('/questions', json = search_term)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['questions'])
        self.assertIsNotNone(data['total_questions'])

    def test_delete_question(self):
        question = Question(question='Test Question',answer='Right Answer',category=1,difficulty=1)
        question.insert()

        res = self.client().delete('/questions/{}'.format(question.id))
        data = json.loads(res.data)

        question = Question.query.get(question.id)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertEqual(question, None)

    def test_delete_question_out_of_bounds(self):
        res = self.client().delete('/questions/20000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'Not Found')
    
    def test_delete_question_bad_request(self):
        res = self.client().delete('/questions/a')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'Question Id needs to be an Integer')

    def test_get_question_by_category(self):
        res = self.client().get('categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))

    def test_get_not_existing_question(self):
        res = self.client().get('categories/1000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'Not Found')

    def test_get_categories(self):
        res = self.client().get('categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(len(data['categories']))

    def test_get_random_question(self):
        params = {
            'previous_questions':[],
            'quiz_category': {
                'type': "click", 'id': 0
            }
        }
        res = self.client().post('quizzes', json = params)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_get_random_question_for_category(self):
        params = {
            'previous_questions':[],
            'quiz_category': {
                'type': "science", 'id': 1
            }
        }
        res = self.client().post('quizzes', json = params)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertEqual(data['question']['category'],1)

    def test_get_random_question_for_not_existing_category(self):
        params = {
            'previous_questions':[],
            'quiz_category': {
                'type': "science", 'id': 100
            }
        }
        res = self.client().post('quizzes', json = params)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'Not Found')

    def test_get_error_as_no_quiz_questions_left(self):
        questions = Question.query.filter_by(category="1").all()
        ids = [question.id for question in questions]

        params = {
            'previous_questions':ids,
            'quiz_category': {
                'type': "science", 'id': "1"
            }
        }
        res = self.client().post('quizzes', json = params)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'No more questions to display')
        

    def test_post_question(self):
        params = {
            "question":"I would have a question",
            "answer":"test",
            "difficulty":1,
            "category":"1"
            }

        res = self.client().post('questions/create', json = params)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

        question_id = data['question']['id']
        new_question = Question.query.get(question_id)
        self.assertTrue(new_question)


    def test_post_question_not_existing_category(self):
        params = {
            "question":"I would have a question",
            "answer":"test",
            "difficulty":1,
            "category":"9999"
            }
        res = self.client().post('questions/create', json = params)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'Category does not exist')

    
    def test_post_question_difficulty_too_low(self):
        params = {
            "question":"I would have a question",
            "answer":"test",
            "difficulty":0,
            "category":"1"
            }
        res = self.client().post('questions/create', json = params)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'Difficulty needs to be an Integer of 1 to 5')

    def test_post_question_difficulty_too_high(self):
        params = {
            "question":"I would have a question",
            "answer":"test",
            "difficulty":6,
            "category":"1"
            }
        res = self.client().post('questions/create', json = params)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'Difficulty needs to be an Integer of 1 to 5')

    def test_post_question_category_not_string(self):
        params = {
            "question":"I would have a question",
            "answer":"test",
            "difficulty":6,
            "category":1
            }
        res = self.client().post('questions/create', json = params)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'Category needs to be a String')

    def test_post_question_difficulty_not_integer(self):
        params = {
            "question":"I would have a question",
            "answer":"test",
            "difficulty":"6",
            "category":"1"
            }
        res = self.client().post('questions/create', json = params)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'Difficulty needs to be an Integer')

    def test_post_question_question_too_short(self):
        params = {
            "question":"I would",
            "answer":"test",
            "difficulty":6,
            "category":"1"
            }
        res = self.client().post('questions/create', json = params)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'Question needs to be at least 10 characters long')

    def test_post_question_answer_too_short(self):
        params = {
            "question":"I would have a question",
            "answer":"",
            "difficulty":6,
            "category":"1"
            }
        res = self.client().post('questions/create', json = params)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'Answer needs to be at least one character')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()