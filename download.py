import os
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


def _download_book(book: Book, output_dir: str, exist_ok=False) -> None:

    if book.gutenberg_text_url is None or book.gutenberg_text_url == 'no-url':
        raise Exception('Could not download book, no download url')

    if not os.path.isdir(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    clean_title = book.title.replace(' ', '_')
    clean_author = book.title.replace(' ', '_')
    save_path = os.path.join(
        output_dir, f'{book.gutenberg_id}_{clean_title}_{clean_author}.txt',
    )

    # Do no download books that are already downloaded
    if not exist_ok and os.path.exists(save_path):
        raise Exception(f'Book already is downloaded, see: {save_path}')

    with requests.get(book.gutenberg_text_url, stream=True) as r:
        r.raise_for_status()
        with open(save_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)


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

    # TODO: Remove the license from the books

    adv_books = _get_books_by_genre('adventure', max_pages=1)

    for book in adv_books:
        try:
            print(f'Downloading book ({book.gutenberg_id}): {book.title}')
            _download_book(
                book, os.path.join(
                    os.getcwd(), 'books', 'adventure/',
                ),
            )
        except Exception as e:
            print(f'Error: {e} for book: {book.gutenberg_id}, skipping...')
            continue

    return 0


if __name__ == '__main__':

    raise SystemExit(main())
