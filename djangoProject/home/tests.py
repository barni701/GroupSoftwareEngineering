from django.test import TestCase
from django.urls import reverse

# Create your tests here.

class HomeViewTests(TestCase):

    # Test to check if the home view returns the 200 status code
    def test_home_view_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
    
    # Test to check if the home view has the correct template
    def test_home_view_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home/home.html')

    # Test to check if certain content on the home.html page is present
    def test_home_view_content(self):
        response = self.client.get(reverse('home'))
        # Check if the main heading is present
        self.assertContains(response, 'Sustainability Bingo')
        # Check if the subheading is present
        self.assertContains(response, 'How does it work?')
        # Check if the content is present
        self.assertContains(response, 'Sustainability bingo lets you help the environment while having fun!')
