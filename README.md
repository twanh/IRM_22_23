# The use of adjectives in adventure novels VS biographies.

Twan Huiskens (S4781619)


## General Information

I am studying the use of adjectives in adventure novels and biographies because I want to find
out how the use of adjectives is different between these two genres in order to help my reader
understand the difference in language between the genres. This research might in the future help to better understand
the difference in language between adventure novels and biographies but also novels and biographies in general.


## Background Information

There is not much research being done on the difference in use of adjectives between (adventure) novels and biographies. However
some research is done on adjectives in novels. Two well known novels have been analysed to see how much adjectives are used.

Nuhiu (2021) looked at the use of adjectives in the novel 'The Great Gatsby'. There are in total 2701 adjectives used in 'The Great Gatsby' (Nuhiu, 2021).

Salim (2016) investigated how adjectives were used in the Harry Potter book 'The Deathly Hallows', and more specifically how they where used to portray the protagonists.

Since there is no research like this done for biographies it's hard to compare the two based on literature alone, that's where my research might fill in a gap.


## Research Question & Hypothesis

**Research question:** Is there a difference between adjective use in adventure novels and biographies?

**Hypothesis:** Adjectives are descriptive. This is more important in novels then in biographies, therefor I expect there to be more adjectives in novels.

## Method

For this project I will use adventure novels and biographies from the project Gutenberg.

I will make sure that the novels and biographies are sourced from the same time periods. This is to ensure that differences in the use of adjectives
are not due to the fact that language changes throughout time.

Next to controlling the time of publishing I will also make sure that size of the adventure novel corpus and the size
of the biography corpus are about the same size so the size of the corpus will not affect the frequency of the adjectives.

To find the adjectives I will use part-of-speech (POS) tagger. There are a quite some (good) options available as python libraries. I will include the model used to
find the POS-tags with the code, and the found adjectives and in which book they where found in this repository.

## Usage of the scripts

There are three programs that can be used to get and analyze the data.

Before using any of the programs make sure that the requirements are installed.

For this project we used the spaCy model: `en_core_web_sm`

Install this using: `python3 -m spacy download en_core_web_sm`

### `download.py`

This program can be used to download the books from Project Gutenberg.

#### Usage

```
usage: download.py [-h] [--max-pages MAX_PAGES] [--start-page START_PAGE]
                   [--date-start DATE_START] [--date-end DATE_END]
                   [--language LANGUAGE]
                   genre

positional arguments:
  genre

options:
  -h, --help            show this help message and exit
  --max-pages MAX_PAGES
                        The maximum amount of pages to fetch.
  --start-page START_PAGE
                        The page number to start with.
  --date-start DATE_START
                        The start of the date range to get the books from.
  --date-end DATE_END   The end of the date range to get the books from.
  --language LANGUAGE   The language of the books.

```

Note: language is set to English by default.

#### Commands used to get the data

For adventure novels
```
python3 download.py adventure --date-start 1901 --date-end 2000 --max-pages 10
```

For biographies
```
python3 download.py biography --date-start 1901 --date-end 2000 --max-pages 10
```

### `count_adj.py`

Tokenizes and POS-tags the books.

#### Usage

```
usage: count_adj.py [-h] in_path save_path

positional arguments:
  in_path     Path to folder where the books are stored.
  save_path   Path to save the data to.

options:
  -h, --help  show this help message and exit
```

#### Commands used to get the data

```
$ python3 process_data.py adj_count_adventure.json
$ python3 process_data.py adj_count_biography.json
```

### `process_data.py`

Used to count the adjectives, and show the results.

#### Usage

```
usage: process_data.py [-h] data_file

positional arguments:
  data_file   File containing the (result) data.

options:
  -h, --help  show this help message and exit
```

#### Commands used to process the data

```
$ python3 process_data.py adj_count_biography.json
$ python3 process_data.py adj_count_adventure.json
```

## Note on data stored in the repository

Due to the large size and time it takes to download and process all the books (3h+ for each genre)
I have included the gathered data in this repository.

- `books/` Stores the raw text of all the books, each genre has it's own subfolder
- `adj_count_adventure.json` The processed data, contains the adjectives (and filenames) of the adventure books.
- `adj_count_biography.json` The processed data, contains the adjectives (and filenames) of the biography books.

## References

- Nuhiu, Remzije. “QUANTITATIVE APPROACH TO ADJECTIVES IN THE NOVEL ‘THE GREAT GATSBY.’” ANGLISTICUM. Journal of the Association-Institute for English Language and American Studies 10, no. 2 (March 15, 2021)
- Salim, Hishamuddin, and Nadia Nabila Saad. “Portraying the Protagonists: A Study of the Use of Adjectives in Harry Potter and the Deathly Hallows.” International Journal of Applied Linguistics and English Literature 5, no. 6 (November 1, 2016) https://doi.org/10.7575/aiac.ijalel.v.5n.6p.259.
