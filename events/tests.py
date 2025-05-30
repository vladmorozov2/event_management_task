from django.test import TestCase

# Create your tests here.

class CreateEventTestCase(TestCase):
    def setUp(self):
        pass

    def test_create_event(self):
        # Test creating an event
        response = self.client.post('/events/', {
            'title': 'Test Event',
            'description': 'This is a test event.',
            'date': '2023-10-01',
            'event_type': 'Conference',
            'location': 'Test Location'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Test Event', response.content.decode())