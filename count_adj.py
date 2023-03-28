import argparse
import json
import os
from typing import NamedTuple

import spacy
from tqdm import tqdm


class AdjInfo(NamedTuple):
    file_path: str
    adjectives: list[str]


def _load_book(in_path: str) -> tuple[str, str] | None:
    """
    Reads in the book from in_path and returns the filename and contents.

    This function will return None if the file could not be openend.
    """

    encodings = ['utf-8', 'us-ascii']

    # Try different encodings for the files
    for encoding in encodings:
        try:
            with open(in_path, 'r', encoding=encoding) as book_file:
                return (in_path, book_file.read())

        except UnicodeDecodeError:
            continue  # Try the next encoding

    print(f'Error: could not find the right encoding to open file {in_path}')
    return None


def _count_adj(book: tuple[str, str], nlp: spacy.language.Language) -> AdjInfo:
    """Counts the adjectives in a book"""

    adj = []
    for line in book[1].splitlines():
        doc = nlp(line)

        for token in doc:
            if token.pos_ == 'ADJ':
                adj.append(token.text)

    return AdjInfo(file_path=book[0], adjectives=adj)


def _save_data(adj: list[AdjInfo], path: str):
    """Saves the data (adj) to the given path"""

    with open(path, 'w') as save_file:
        json.dump(adj, save_file)


def main() -> int:

    # Create argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'in_path', help='Path to folder where the books are stored.',
    )
    parser.add_argument(
        'save_path', type=str,
        help='Path to save the data to.',
    )

    args = parser.parse_args()

    print('Finding books to process')
    base_path = args.in_path
    files = os.listdir(base_path)
    print(f'Found {len(files)} books')

    print('Loading spaCy model')
    # Download using: python -m spacy download en_core_web_sm
    nlp = spacy.load('en_core_web_sm')
    # Make sure that spacy can handle the tex length
    nlp.max_length = 1_000_000
    print('Model loaded')

    print('Starting finding adjectives for all books')
    found_adjectives: list[AdjInfo] = []
    for i, file in enumerate(tqdm(files)):
        book = _load_book(os.path.join(base_path, file))
        if book is not None:
            ret = _count_adj(book, nlp)
            found_adjectives.append(ret)

        # Save data every 10th iteration
        if i % 10 == 0:
            print(f'Saving (temp) to {args.save_path}')
            _save_data(found_adjectives, args.save_path)

    # Save data
    _save_data(found_adjectives, args.save_path)

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
