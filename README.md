# Backend for Nixacernis Keyboard

## Background and Brief Intro

Hosted in this repository is the open-sourced backend system under the hood of the iOS custom keyboard application [Nixacernis Keyboard](https://github.com/MapleCCC/Nixacernis-Keyboard).

## Prior Knowledge and Jargons

### Terminology and Common Translations

For maximum compatibility with mainstream academic circle, the following translations are mostly taken via reference from Wikipedia pages. Consult [Reference](#reference) section to know more.

| Chinese  | English    | Note                                                         |
| -------- | ---------- | ------------------------------------------------------------ |
| 拼音     | pinyin     |                                                              |
| 声母     | initial    |                                                              |
| 韵母     | final      |                                                              |
| 零声母   | zero onset |                                                              |
| 逐序格式 | LUTP       | Short for *Line Up to Pick*, a desginated representation of keybaord layouts |

### Keyboard Layout Jargon

Nixacernis keyboard has totally 18 keys. For convenience, each of them is binded with a number from 0 to 17. (0-indexed for convenience in under hood data processing)

||First Column|Second Column|Third Column|Fourth Column|Fifth Column|Sixth Column|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| First Row | 0 | 1 | 2 | 3 | 4 | 5 |
| Second Row | 6 | 7 | 8 | 9 | 10 | 11 |
| Third Row | 12 | 13 | 14 | 15 | 16 | 17 |

## API Overview

Note that since the project is still under heavy development, it's very likely that current APIs may undergo dramatic changes in the future. No backward compatibility is promised, and use them to your own risk.

### Transliteration

Go to `/transliterate/<query_string>` for transliteration.

The format of `<query_string>`, represented as regular expression, is `[1-18](-[1-18])*`.

> For example, if the user consecutively typed keys corresponding to number 1, 3, 8, 3, 11, then a `GET` request is sent to url `<hosted_url>/transliterate/1-3-8-3-11`.

Baed on data past froward, transliteration is conducted in the server side and result is packed in JSON format, routed back to client.

### Increase word priority

After user typed some words, you may prefer to update the word's priority so that it shows up more likely next time. We have a wrapped up API for doing this. Just send a `POST` request to url `<hosted_url>/increment/<word>`.

Currently this feature is done by increase the word count by 1 under the hood. Future API update may introduce increment of word priority with different granularity.

## Development

### Prerequisite

Python 3.6 and Django 2.2

```bash
$ pip install django bidict
```

### Get the source code and setup

```bash
$ git clone https://github.com/MapleCCC/Nixacernis-Keyboard-Backend.git

$ cd nixacernis-keyboard-backend/

# Install dependencies
$ pip install -r requirements.txt

# Set up initial database
$ python manage.py migrate

# Set up server at localhost:8000
$ python manage.py runserver
```

Note that the above commands set up only a naive development server as a built-in feature provided by Django. It's not intended for production deployment.

Instead, use Gunicorn as recommended by Django:

```bash
$ gunicorn nixacernis.wsgi
```

### Dev Tools  & Workflows

```bash
# To autoformat `*.py` files under the whole repository
$ make autoformat

# To check linting errors among all `*.py` files under repository
$ make lint

# To preview README file via GitHub style rendering
$ make preview

# To eradicate redundant files for a pristine build state
# NOTE that this command may erase local database that's not version controlled.
$ make clean

# To launch a shell for working around
$ make shell
```

## Live instance for having a taste

There is a heroku app instance setup for automatic CI and testing. Go to [https://nixacernis-keyboard-backend.herokuapp.com/](https://nixacernis-keyboard-backend.herokuapp.com/) to have a check<!--try-->.

## License

[WTFPL 2.0](./LICENSE)

## Reference

[Wikipedia page: "Pinyin"](https://www.wikiwand.com/en/Pinyin)

Wikipedia pages for Pinyin, Pinyin table, Standard Chinese Phonology, Standard Chinese, Historical Chinese Phonology, etc,.
