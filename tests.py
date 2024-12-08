import unittest
from app import app

class LibraryTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_add_book(self):
        response = self.app.post('/books', json={"title": "New Book", "author": "Author", "published_year": 2024})
        self.assertEqual(response.status_code, 201)

    def test_get_books(self):
        response = self.app.get('/books')
        self.assertEqual(response.status_code, 200)

    def test_get_book(self):
        response = self.app.get('/books/1')
        self.assertEqual(response.status_code, 200)

    def test_update_book(self):
        response = self.app.put('/books/1', json={"title": "Updated Book"})
        self.assertEqual(response.status_code, 200)

    def test_delete_book(self):
        response = self.app.delete('/books/1')
        self.assertEqual(response.status_code, 200)

    def test_search_books(self):
        response = self.app.get('/books/search?query=Author')
        self.assertEqual(response.status_code, 200)

    def test_pagination(self):
        response = self.app.get('/books?page=1&per_page=2')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
