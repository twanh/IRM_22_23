import argparse
import os
from typing import Any
from typing import NamedTuple

import requests
from tqdm import tqdm


class Book(NamedTuple):
    """Datastructure to store metadata of the found books"""
    title: str
    gutenberg_id: int
    gutenberg_text_url: str
    author: str
    subjects: list[str]
    bookshelves: list[str]
    genre: str
    date_range: str


def _parse_book_json(data: dict[str, Any], genre: str, date: str) -> Book:
    """Parses the response from the API and returns a Book datastructure."""

    text_url = None
    for key in (
            'text/plain; charset=utf-8',
            'text/plain; charset=us-ascii',
    ):
        if key in data['formats']:
            text_url = data['formats'][key]
            # Stop looking for the other keys since we found a download link
            break

    return Book(
        title=data['title'],
        gutenberg_id=data.get('id', -1),
        gutenberg_text_url=text_url or 'no-url',
        author=data['authors'][0]['name'],
        subjects=data['subjects'],
        bookshelves=data['bookshelves'],
        genre=genre,
        date_range=date,
    )


def _download_book(book: Book, output_dir: str, exist_ok=False) -> None:
    """Downloads the given book (as text) and saves it to the output_dir"""

    if book.gutenberg_text_url is None or book.gutenberg_text_url == 'no-url':
        raise Exception('Could not download book, no download url')

    if not os.path.isdir(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    # Remove whitespace in the title and author
    clean_title = book.title.replace(' ', '_')
    clean_author = book.title.replace(' ', '_')
    save_path = os.path.join(
        output_dir, f'{book.gutenberg_id}_{clean_title}_{clean_author}_{book.date_range}.txt',  # noqa: E501
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
    author_year_start: int | None = None,
    author_year_end: int | None = None,
    max_pages: int = 5,
    language: str | None = None,
) -> list[Book]:
    """Searches for books based on the given arguments"""

    if page is None:
        page = 1

    r_params = {'topic': genre, 'page': page}

    if author_year_start is not None and author_year_end is not None:
        r_params['author_year_start'] = author_year_start
        r_params['author_year_end'] = author_year_end

    if language is not None:
        r_params['languages'] = language

    r = requests.get(
        'https://gutendex.com/books/',
        params=r_params,  # type: ignore
    )
    if not r.ok:
        return []

    data = r.json()
    book_data: list[dict] = data['results']

    # Download all the books (from multiple pages)
    while 'next' in data and page < max_pages:
        r_params['page'] = page
        r = requests.get(
            'https://gutendex.com/books/',
            params=r_params,  # type: ignore
        )
        if not r.ok:
            print('ERROR 1')
            continue
        data = r.json()
        book_data.extend(data['results'])
        page += 1

    books = []
    for book in book_data:
        books.append(
            _parse_book_json(
                book, genre, f'{author_year_start}-{author_year_end}',
            ),
        )

    return books


def main() -> int:

    parser = argparse.ArgumentParser()
    parser.add_argument('genre')
    parser.add_argument(
        '--max-pages', type=int, default=5,
        help='The maximum amount of pages to fetch.',
    )
    parser.add_argument(
        '--start-page', type=int, default=1,
        help='The page number to start with.',
    )
    parser.add_argument(
        '--date-start', type=int,
        help='The start of the date range to get the books from.',
    )
    parser.add_argument(
        '--date-end', type=int,
        help='The end of the date range to get the books from.',
    )
    parser.add_argument(
        '--language', type=str, default='en',
        help='The language of the books.',
    )

    args = parser.parse_args()

    print(
        f'Searching books in genre: {args.genre}, with start between: {args.date_start} and {args.date_end}',  # noqa: E501
    )

    results = _get_books_by_genre(
        args.genre,
        page=args.start_page,
        max_pages=args.max_pages,
        author_year_start=args.date_start,
        author_year_end=args.date_end,
        language=args.language,
    )

    print(f'Found {len(results)}, books')

    downloaded = 0
    for book in tqdm(results):
        try:
            print(f'Downloading book ({book.gutenberg_id}): {book.title}')
            _download_book(
                book, os.path.join(
                    os.getcwd(), 'books', f'{args.genre}/',
                ),
            )
            downloaded += 1
        except Exception as e:
            print(f'Error: {e} for book: {book.gutenberg_id}, skipping...')
            continue

    print(f'Downloaded {downloaded}/{len(results)} for genre: {args.genre}')

    return 0


if __name__ == '__main__':

    raise SystemExit(main())
