import os
from unicodedata import category
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category, db
from settings import DB_NAME, DB_USER, DB_PASSWORD


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(DB_USER, DB_PASSWORD,'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            
            self.new_question = {
            "question": "Who was the 45th president of United State of America?",
            "category": 3,
            "answer": "Donald Trump",
            "difficulty": 3
        }

    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories_success(self):
         res = self.client().get("/categories")
         self.assertEqual(res.status_code, 200)

    
    def test_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["categories"]))

    def test_get_paginated_questions_not_found(self):
        res = self.client().get("/questions?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["error"], 404)

    def test_add_question_success(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)
        question = Question.query.get(data["added"])

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(question)

    def test_add_question_bad_request(self):
        res = self.client().post("/questions", json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["error"], 400)

    def test_delete_question_success(self):
        question = Question(
            question=self.new_question["question"],
            answer=self.new_question["answer"],
            difficulty=self.new_question["difficulty"],
            category=self.new_question["category"],
        )
        question.insert()
        question_id = question.id

        res = self.client().delete("/questions/" + str(question_id))
        data = json.loads(res.data)

        question = Question.query.get(question_id)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIsNone(question)

    def test_delete_question_not_found(self):
        res = self.client().delete("/questions/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")
        
    def test_search_questions_success(self):
        res = self.client().post("/questions/search", json={"searchTerm": "World Cup"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["total_questions"])
        

    def test_search_questions_not_found(self):
            res = self.client().post("/questions", json={"searchTerm": "abcdxyz"})
            data = json.loads(res.data)
            
            self.assertEqual(res.status_code, 200)
            #self.assertEqual(data['success'], True)
            #self.assertTrue(data['total_questions'])
            self.assertEqual(len(data['questions']), 0)

    def test_get_questions_in_category_success(self):
        res = self.client().get("/categories/2/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["total_questions"])

    def test_get_question_for_quiz_success(self):
        self.new_quiz = {
            "previous_questions": [],
            "quiz_category": {'type': "Science", 'id': "1"}
        }
        res = self.client().post('/quizzes', json=self.new_quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        #self.assertEqual(data['success'], True)
        self.assertTrue(data["question"])


    def test_get_question_for_quiz_bad_request(self):
         res = self.client().post('/quizzes')
         data = json.loads(res.data)

         self.assertEqual(res.status_code, 400)
        #self.assertEqual(data["error"], 404)
         self.assertEqual(data["success"], False)
         self.assertEqual(data["message"], "bad request")


# Make the tests conveniently executable 

    if __name__ == "__main__":
        unittest.main()