from typing import Any
from typing import NamedTuple

import requests


class Book(NamedTuple):
    title: str
    gutenberg_id: int
    gutenberg_text_url: str
    author: str
    subjects: list[str]
    bookshelves: list[str]
    genre: str


def _process_book_json(data: dict[str, Any]) -> Book:

    return Book(
        title=data['title'],
        gutenberg_id=data.get('id', -1),
        gutenberg_text_url=data['formats'].get(
            'text/plain; charset=utf-8', 'no-url',
        ),
        author=data['authors'][0]['name'],  # TODO: Allow multiple auhtors
        subjects=data['subjects'],
        bookshelves=data['bookshelves'],
        genre='Unknown',  # TODO: Add genre?
    )


def _get_books_by_genre(
    genre: str,
    page: None | int = None,
    date_range=None,
    language='en',
    max_pages: int = 5,
) -> list[Book]:

    # TODO:
    #   - Implement date ranges
    #       (so that books from the same date range can be downloaded)

    if page is None:
        page = 1

    r = requests.get(
        'https://gutendex.com/books/',
        params={'topic': genre, 'page': page},  # type: ignore
    )
    if not r.ok:
        return []

    data = r.json()
    book_data: list[dict] = data['results']

    # Download all the books (from multiple pages)
    # TODO: Add TQDM progress bar
    while 'next' in data and page < max_pages:
        r = requests.get(
            'https://gutendex.com/books/',
            params={'topic': genre, 'page': page},  # type: ignore
        )
        if not r.ok:
            print('ERROR 1')
            continue
        data = r.json()
        book_data.extend(data['results'])
        page += 1

    books = []
    for book in book_data:
        books.append(_process_book_json(book))

    return books


def main() -> int:

    _ = _get_books_by_genre('adventure')
    return 0


if __name__ == '__main__':

    raise SystemExit(main())
