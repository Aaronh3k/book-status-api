# Book-Service-REST-API

Welcome to the Book-Service-REST-API, a Flask-based RESTful service designed to empower bibliophiles with the ability to seamlessly manage and maintain their reading lists. This service is inspired by and aims to replicate core functionality of leading book management applications like Basmo.

At its core, this service provides the following features:

- **Book Management:** Keep track of all your favorite books with unique identifiers and essential details such as ISBN, title, and author.
- **Reading List Management:** Create and manage personalized reading lists. Each book in the reading list has a status associated with it (unread, in progress, or finished) allowing you to track your reading journey effectively.
- **Book Rating:** An interactive feature enabling you to rate books on a scale of 1 to 5 and make notes on them. This feature enriches the reading experience, making it possible to reflect on read books and recommend them to others.

The service is backed by a robust SQL database structure and offers a comprehensive suite of unit tests ensuring the reliability of the service.

Take a peek at the tree structure below to understand the project organization:

```plaintext
.
├── alembic
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions
│       ├── 1de117525c0c_add_unique_constraint_to_book_id_in_.py
│       ├── 2cb93d1d7ed6_add_unique_constraint_to_book_id_and_.py
│       ├── 442e00a4d839_add_unique_constraint_and_index_to_isbn_.py
│       ├── 83e85133ceca_create_book_ratings_table.py
│       ├── 8fa5254cdb22_added_book_and_readinglist_tables.py
│       └── __pycache__
├── alembic.ini
├── README.md
├── requirements.txt
├── run.py
├── src
│   ├── app.py
│   ├── config
│   ├── controllers
│   ├── helpers.py
│   ├── libs
│   └── models
├── static
│   └── swagger.yml
└── tests
