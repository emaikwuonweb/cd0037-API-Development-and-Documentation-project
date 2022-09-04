from random import randint, choice
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={'/api/*': {'origin': '*'}})


    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization,true")
        response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
        
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def list_categories():
        
        query = Category.query.all()
        categories = [category.format() for category in query]
        return jsonify({
            "success": True,
            'categories': categories,
        })

    
    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def list_questions():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        query = Question.query.all()
        questions = [question.format() for question in query][start:end]
        
        if len(questions) > 0:
            return jsonify({
                'success': True,
                'questions': questions,
                'total_questions': len(query),
                'categories': [category.format() for category in Category.query.all()],
                'current_category': 'entertainment'
            })
        abort(404)

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def function(question_id):
        question = Question.query.filter_by(id=question_id).one_or_none()
        if question is None:
            abort(404)
        question.delete()
        return jsonify({
            'success': True,
            'id': question.id,
            'deleted': True
        })


    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def add_question():
        if request.method == 'POST':
            error = False
            try:
                question = Question(
                    question = request.get_json()['question'],
                    answer = request.get_json()['answer'],
                    category = request.get_json()['category'],
                    difficulty = request.get_json()['difficulty'],
                ) 
                db.session.add(question)
                db.session.commit()
            except:
                db.session.rollback()
                error = True
            finally:
                db.session.close()

            if error:
                abort(500)
            return jsonify({
                "success": True,
                "created": True
            })
        abort(405)
   
   
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.


    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/search', methods=['POST'])
    def search():
        term = request.get_json()['searchTerm']
        query = Question.query.filter(Question.question.ilike(f"%{term}%")).all()
        if len(query) > 0:
            return jsonify({
                'success': True,
                'questions': [question.format() for question in query],
                'total_questions': len(query),
                'current_category': 'a'
            })
        abort(404)


    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route("/categories/<category_id>/questions")
    def category_questions(category_id):
        category = Category.query.filter(Category.id==category_id).one_or_none()
        
        if category is not None:
            query = Question.query.filter(Question.category==category_id).all()
            return ({
                "success": True,
                "questions": [question.format() for question in query],
                "total_questions": len(query),
                "categories": [category.format() for category in Category.query.all()],
                "current_category": category.type
            })  
        abort(404)      

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def quizzes():
        category = request.get_json()['quiz_category']
        prev_quesitons = request.get_json()['previous_questions']

        if category['type'] == 'all':
            questions_query = Question.query.filter(Question.id.not_in(prev_quesitons)).all()
        else:
            questions_query = Question.query.filter(Question.category==category['id'], Question.id.not_in(prev_quesitons)).all()
        
        if len(questions_query) > 0:
            question = choice([question.format() for question in questions_query])
            return jsonify({
                'success': True,
                'question': question
            })
        return jsonify({
            'success': True,
            'question': False
        })


    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not found'
        }), 404

    @app.errorhandler(422)
    def unproccessable_entity(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable entity"
        }), 422

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not allowed"
        }), 405

    @app.errorhandler(409)
    def request_conflict(error):
        return jsonify({
            "success": False,
            "error": 409,
            "message": "Request conflict"
        }), 409

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "messae": "Internal server error"
        }), 500
    
    return app

