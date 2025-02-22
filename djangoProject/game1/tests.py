from django.test import TestCase, Client
from django.urls import reverse

class QuizTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.quiz_url = reverse('quiz')

    #tests to make sure the page loads correctly
    def test_quiz_get_request(self):
        response = self.client.get(self.quiz_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'game1/quiz.html')
        self.assertIn('questions', response.context)


    #Tests all correct questions are correct
    def test_quiz_post_request_correct_answers(self):
        data = {
            'question_0': '2030',
            'question_1': 'EMS',
            'question_2': 'Climate',
            'question_3': 'Strategy2030',
            'question_4': 'Penryn',
            'question_5': '17',
            'question_6': 'Nature',
        }
        response = self.client.post(self.quiz_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'game1/quiz_result.html')
        self.assertEqual(response.context['correct_answers'], 7)
        self.assertEqual(response.context['total_questions'], 7)


    #Tests if only some of the answers are correct
    def test_quiz_post_request_partial_answers(self):
        data = {
            'question_0': '2030',
            'question_1': 'Wrong Answer',
            'question_2': 'Climate',
            'question_3': 'Wrong Answer',
            'question_4': 'Penryn',
            'question_5': '17',
            'question_6': 'Wrong Answer',
        }
        response = self.client.post(self.quiz_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['correct_answers'], 4)
        self.assertEqual(response.context['total_questions'], 7)

    #Tests if no fields are filled
    def test_quiz_post_request_empty_answers(self):
        data = {}
        response = self.client.post(self.quiz_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['correct_answers'], 0)
        self.assertEqual(response.context['total_questions'], 7)
