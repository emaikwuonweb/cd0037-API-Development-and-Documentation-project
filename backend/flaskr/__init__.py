from random import randint, choice
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
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, \
            Authorization, true")
        response.headers.add("Access-Control-Allow-Methods", "GET, PUT, POST, \
            DELETE, OPTIONS")
        return response

    @app.route('/categories')
    def list_categories():
        query = Category.query.all()
        categories = [category.format() for category in query]
        if len(categories) > 0:
            return jsonify({
                "success": True,
                'categories': categories,
            })
        abort(404)

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
                'categories': [category.format() for category in
                               Category.query.all()],
                'current_category': 'entertainment'
            })
        abort(404)

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

    @app.route('/questions', methods=['POST'])
    def add_question():
        if request.method == 'POST':
            error = False
            try:
                question = Question(
                    question=request.get_json()['question'],
                    answer=request.get_json()['answer'],
                    category=request.get_json()['category'],
                    difficulty=request.get_json()['difficulty'],
                )
                db.session.add(question)
                db.session.commit()
            except Exception:
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

    @app.route('/search', methods=['POST'])
    def search():
        term = request.get_json()['searchTerm']
        query = Question.query.filter(Question.
                                      question.ilike(f"%{term}%")).all()
        if len(query) > 0:
            return jsonify({
                'success': True,
                'questions': [question.format() for question in query],
                'total_questions': len(query),
                'current_category': 'a'
            })
        abort(404)

    @app.route("/categories/<category_id>/questions")
    def category_questions(category_id):
        category = \
            Category.query.filter(Category.id == category_id).one_or_none()
        if category is not None:
            query = Question.query.filter(Question.category ==
                                          category_id).all()
            return ({
                "success": True,
                "questions": [question.format() for question in query],
                "total_questions": len(query),
                "categories": [category.format() for category in
                    Category.query.all()],
                "current_category": category.type
            })
        abort(404)

    @app.route('/quizzes', methods=['POST'])
    def quizzes():
        quiz_category = request.get_json()['quiz_category']
        prev_quesitons = request.get_json()['previous_questions']
        category = Category.query.filter(Category.id ==
                                         quiz_category['id']).one_or_none()
        if category:
            if quiz_category['type'] == 'all':
                query = \
                    Question.query.filter(Question.id.not_in(
                        prev_quesitons)).all()
            else:
                query = Question.query.filter(Question.category ==
                                              quiz_category['id'], Question.id.
                                              not_in(prev_quesitons)).all()
            if len(query) > 0:
                question = choice([question.format() for question in query])
                return jsonify({
                    'success': True,
                    'question': question
                })
            return jsonify({
                'success': True,
                'question': False
            })
        abort(404)

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
