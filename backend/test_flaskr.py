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
        self.database_path = "postgresql://postgres:admin@localhost:5432/trivia_test"
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


    def test_list_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['categories']))
        self.assertTrue(data['success'])


    def test_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])

    
    def test_404_pagination_value(self):
        res = self.client().get('/questions?page=10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'], False)
        self.assertEqual(data['message'], 'Not found')


    def test_delete_questions(self):
        res = self.client().delete('/questions/14')   
        data = json.loads(res.data)

        question = Question.query.filter(Question.id==14).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success']) 
        self.assertTrue(data['id'])
        self.assertEqual(question, None)

    
    def test_404_delete_question_not_found(self):
        res = self.client().delete('/questions/40000')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success']) 
        self.assertTrue(data['message'])
        self.assertEqual(data['error'], 404)


    def test_add_question(self):
        res = self.client().post('/questions', json={
            "question": "How many dragons has Dina?",
            "answer": 3,
            "category": 2,
            "difficulty": 4
        })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['created'])


    def test_unallowed_methods_to_questions(self):
        res = self.client().patch('/questions', json={'questions': 'What is the prequel to game of thrones?'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 405)
        self.assertTrue(data['message'])

    
    def test_search(self):
        res = self.client().post('/search', json={"searchTerm": 'title'})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])


    def test_not_matched_search(self):
        res = self.client().post('/search', json={'searchTerm': 'ureqq343'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertTrue(data['message'])
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)


    def test_category_questions(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])


    def test_404_category_questions(self):
        res = self.client().get('/categories/999/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertTrue(data['message'])


    def test_quizzes(self):
        res = self.client().post('/quizzes', json={'quiz_category': {'type': 'history', 'id': 4},'previous_questions': [1]})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['question'])
    
    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()