from django.test import TestCase
from django.urls import reverse
from bingo import views

class BingoViewTests(TestCase):

    # Checks if the bingo view returns the status code 200
    def test_bingo_status_page(self):
        response = self.client.get(reverse('bingo'))
        self.assertEqual(response.status_code, 200)

    # Checks the bingo.html template is used
    def test_bingo_template(self):
        response = self.client.get(reverse('bingo'))
        self.assertTemplateUsed(response, 'bingo.html')

    # Checks the bingo page contains the table, which is the board
    def test_bingo_content(self):
        response = self.client.get(reverse('bingo'))
        self.assertContains(response, '<table class="board" border="1">')

    # Checks if the board is 4x4
    def test_make_board_size(self):
        response = self.client.get(reverse('bingo'))
        board = views.make_board(4, 4)
        self.assertEqual(len(board), 4)