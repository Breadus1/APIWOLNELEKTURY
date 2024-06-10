import requests

BASE_URL = 'http://localhost:5002'

def add_book(book_data):
    response = requests.post(f'{BASE_URL}/books', json=book_data)
    if response.status_code == 201: print("Book added successfully!")
    else: print(f"Failed to add book: {response.text}")

def add_categories(categories_data):
    response = requests.post(f'{BASE_URL}/categories', json=categories_data)
    if response.status_code == 201: print("Categories added successfully!")
    else: print(f"Failed to add categories: {response.text}")

def get_books(filters=None):
    if filters: response = requests.get(f'{BASE_URL}/books', params=filters)
    else: response = requests.get(f'{BASE_URL}/books')
    
    if response.status_code == 200:
        books = response.json()
        for book in books:
            print(book)
    else: print(f"Failed to retrieve books: {response.text}")

if __name__ == "__main__":
    categories = {
        "epochs": [{"name": "Modern"}, {"name": "Renaissance"}],
        "genres": [{"name": "Fiction"}, {"name": "Non-Fiction"}],
        "kinds": [{"name": "Novel"}, {"name": "Poetry"}],
        "authors": [{"name": "John Doe"}, {"name": "Jane Smith"}]
    }
    add_categories(categories)

    book = {
        "title": "Sample Book",
        "epoch_id": 1,
        "genre_id": 1,
        "kind_id": 1,
        "author_id": 1
    }
    add_book(book)

    filters = {
        "epoch": "Modern",
        "genre": "Fiction"
    }
    get_books(filters)
