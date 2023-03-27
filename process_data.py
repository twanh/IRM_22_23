import argparse
import json
from collections import Counter
from collections import defaultdict


def _get_data(in_file: str) -> list[tuple[str, list[str]]]:

    with open(in_file, 'r') as f:
        data = json.load(f)

    return data


def main() -> int:

    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', help='File containing the (result) data.')

    args = parser.parse_args()

    data = _get_data(args.data_file)

    book_count: dict[str, int] = defaultdict(int)
    adj_count: dict[str, int] = defaultdict(int)
    unique_adj = set()
    n_adj = 0

    for row in data:
        name = row[0]
        adjectives = row[1]
        book_count[name] = len(adjectives)
        for adj in adjectives:
            n_adj += 1
            adj_count[adj.lower()] += 1
            unique_adj.add(adj)

    adj_counter = Counter(adj_count)
    book_counter = Counter(book_count)

    print('--- GENERAL INFO ---')
    print(f'# books: {len(book_count)}')
    print(f'# adjectives: {n_adj}')
    print(f'# unique adjectives: {len(unique_adj)}')
    print('--- Most Common Adjectives ---')
    for adj, count in adj_counter.most_common(10):
        print(f'{count} - {adj}')
    print('--- Books with most adjectives ---')
    for book, count in book_counter.most_common(10):
        print(f'{count} - {book}')

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
