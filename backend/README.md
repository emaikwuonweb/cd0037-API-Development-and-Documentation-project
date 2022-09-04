# Trivia API Documentation

`GET /categories`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with key success and categories

`success` boolean value of true or false to represent the status of the request

`categories` An object that contains an object of id: category_string key:value pairs.

Example:

    {
      "categories": [
        {
          "id": 1,
          "type": "Science"
        },
        {
          "id": 2,
          "type": "Art"
        },
        {
          "id": 3,
          "type": "Geography"
        },
        {
          "id": 4,
          "type": "History"
        },
        {
          "id": 5,
          "type": "Entertainment"
        },
        {
          "id": 6,
          "type": "Sports"
        }
      ],
      "success": true
    }

`GET '/questions?page=${integer}'`

- Fetches a paginated set of questions, a total number of questions, all categories and current category string.
- Request Arguments: `page` - integer
- Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string

Example

    {
      "categories": [
        {
          "id": 1,
          "type": "Science"
        },
        {
          "id": 2,
          "type": "Art"
        },
        {
          "id": 3,
          "type": "Geography"
        },
        {
          "id": 4,
          "type": "History"
        },
        {
          "id": 5,
          "type": "Entertainment"
        },
        {
          "id": 6,
          "type": "Sports"
        }
      ],
      "current_category": "entertainment",
      "questions": [
        {
          "answer": "Escher",
          "category": 2,
          "difficulty": 1,
          "id": 16,
          "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
        }
      ],
      "success": true,
      "total_questions": 17
    }

`GET '/categories/${id}/questions'`

- Fetches questions for a cateogry specified by id request argument
- Request Arguments: `id` - integer
- Returns: An object with questions for the specified category, total questions, and current category string

Example

    {
      "categories": [
        {
          "id": 1,
          "type": "Science"
        },
        {
          "id": 2,
          "type": "Art"
        },
        {
          "id": 3,
          "type": "Geography"
        },
        {
          "id": 4,
          "type": "History"
        },
        {
          "id": 5,
          "type": "Entertainment"
        },
        {
          "id": 6,
          "type": "Sports"
        }
      ],
      "current_category": "Science",
      "questions": [
        {
          "answer": "The Liver",
          "category": 1,
          "difficulty": 4,
          "id": 20,
          "question": "What is the heaviest organ in the human body?"
        }
      ],
      "success": true,
      "total_questions": 3
    }

`DELETE '/questions/${id}'`

- Deletes a specified question using the id of the question
- Request Arguments: `id` - integer
- Returns: Does not need to return anything besides the appropriate HTTP status code. Optionally can return the id of the question. If you are able to modify the frontend, you can have it remove the question using the id instead of refetching the questions.

`POST '/quizzes'`

- Sends a post request in order to get the next question
- Request Body:

Example

    {
      'previous_questions': [1, 3, 2, 4]
      quiz_category': 'History'
    }

- Return: a single new question object

Example

    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    }

`POST '/questions'`

- Sends a post request in order to add a new question
- Request Body:

Example

    {
      'question': 'Heres a new question string',
      'answer': 'Heres a new answer string',
      'difficulty': 1,
      'category': 3,
    }

- Returns: Does not return any new data

`POST '/questions'`

- Sends a post request in order to search for a specific question by search term
- Request Body:

Example

    {
      'searchTerm': 'this is the term the user is looking for'
    }

- Returns: any array of questions, a number of totalQuestions that met the search term and the current category string

Example:

    {
      'questions': [
        {
          'id': 1,
          'question': 'This is a question',
          'answer': 'This is an answer',
          'difficulty': 5,
          'category': 5
        },
      ],
      'totalQuestions': 100,
      'currentCategory': 'Entertainment'
    }
