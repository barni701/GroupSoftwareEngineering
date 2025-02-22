from django.test import TestCase, Client
from django.urls import reverse

class QuizViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.quiz_url = reverse('quiz')

    def test_quiz_get_request(self):
        """Test that the quiz page loads correctly with a GET request."""
        response = self.client.get(self.quiz_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'game1/quiz.html')
        self.assertIn('questions', response.context)

    def test_quiz_post_request_correct_answers(self):
        """Test that the quiz correctly evaluates answers."""
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

    def test_quiz_post_request_partial_answers(self):
        """Test that the quiz handles partially correct answers."""
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

    def test_quiz_post_request_empty_answers(self):
        """Test that the quiz correctly handles empty responses."""
        data = {}
        response = self.client.post(self.quiz_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['correct_answers'], 0)
        self.assertEqual(response.context['total_questions'], 7)
