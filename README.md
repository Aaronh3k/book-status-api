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
```

## Getting Started

Here's a quick guide on how to get the Book-Service-REST-API up and running on your local machine for development and testing purposes.

### Prerequisites

The following tools are required to setup and run this project:

- **Python:** The application is built with Python. Make sure you have Python version 3.9.0 or above. You can download it from [here](https://www.python.org/downloads/).

- **Flask:** The application uses Flask as a web framework. It will be installed when setting up the project.

- **Pip:** Pip is a package management system used to install and manage software packages written in Python. Usually, it's installed with Python. If not, you can install it from [here](https://pip.pypa.io/en/stable/installing/).

### Installation

Please follow these steps to install the application and its dependencies:

**Step 1:** Clone this repository to your local machine using:

```bash
git clone https://github.com/Aaronh3k/Book-Service-REST-API.git
```

**Step 2**: Navigate to the project directory:
```bash
cd Book-Service-REST-API
```
**Step 3**: Install the required Python dependencies:
```bash
pip install -r requirements.txt
```
**Step 4**: Run the application:
```bash
./run.py
```

# API Functionality

This API is a comprehensive tool designed for effective book management, with distinct capabilities spanning across book creation, information retrieval, updates, deletion, and uploads. It supports a range of operations:

- **Book Management:** It offers the ability to create a new book record through a POST request, inclusive of all necessary book data. Book information can be retrieved in various ways, such as fetching details of a specific book using its ID, multiple books, or even utilizing a book's ISBN. Update operations are facilitated using the book's ID in a PATCH request with the required changes, while book deletion is achieved using the book's ID. A unique feature of this API is the capacity to upload books via the Google Books API, using a specified number of books and a keyword.

- **Reading List Management:** Another core feature of this API is the effective management of reading lists. Users can create a new reading list with a book_id and a reading status, fetch details of a single or multiple reading lists, and update or delete a reading list. The API ensures robust validation and sanitization of user inputs, has a strong error handling framework, and provides user-friendly error messages.

- **Rating Management:** The API is also equipped with functionalities for managing book ratings. It allows users to create new book ratings, fetch details of a specific or multiple book ratings, update a book rating, and delete a book rating. This suite of operations supports a high level of user interaction and feedback, enhancing the overall user experience.

In terms of data management, the book data is maintained in a `books` table, with attributes including a unique identifier, ISBN, title, author, creation date, and last updated date. The `Book` model incorporates the necessary methods to interact with this database, reinforcing the API's robustness and user-friendliness.


# Deployment Process

The deployment of this API is facilitated through a robust AWS architecture, leveraging several Amazon Web Services' products for a scalable and efficient system. 

- **AWS Elastic Beanstalk:** The core application is hosted and managed using AWS Elastic Beanstalk, which allows for easy and automated deployment of applications on the cloud.

- **AWS SQS:** Amazon Simple Queue Service (SQS) is used as a fully managed message queuing service that enables the decoupling and scaling of microservices, distributed systems, and serverless applications.

- **AWS Lambda:** AWS Lambda is utilized to run the application's code in response to events and automatically manages the computing resources required, ensuring efficient and responsive behavior.

- **Amazon RDS (PostgreSQL):** The API's database is hosted on Amazon RDS, specifically using the PostgreSQL database engine, providing a secure, scalable and managed database environment.

- **Boto3 (Python AWS SDK):** The AWS Software Development Kit (SDK) for Python, Boto3, is used to create, configure, and manage AWS services. It allows for direct interaction and management of AWS services using Python.

An architectural diagram of the deployment is included in the repository to provide a visual understanding of how these services work together to provide a reliable and efficient service.

![Book-Service-Arch drawio](https://github.com/Aaronh3k/book-status-api/assets/24919671/903e9b5b-9f90-4889-981c-3c128e7a2f82)

# API Testing

The testing for this API is performed using the `pytest` framework. 

When the application is set in a 'test' environment, an SQLite in-memory database is leveraged to perform tests isolated from the production environment.

A 'fixture' in pytest is a setup function, which allows test methods to use a specific database and application context. Each test runs in its own isolated environment, meaning changes in one test won't affect others. Before each test is run, a new instance of the application with a new database is created, and at the end of each test, this instance is torn down to ensure no state is shared between tests.

Test cases have been written to cover all major functionalities of the API. In each test case, operations like creation, retrieval, update, and deletion are performed. At the end of each test, any changes made are reverted, ensuring the database returns to its initial state. This approach ensures that every part of the application is thoroughly tested, and that it behaves as expected under various conditions.

# Continuous Integration/Continuous Deployment (CI/CD)

The API adopts a CI/CD pipeline through GitHub Actions to automate the testing, building, and deployment process. The workflow, named "Book Service CI/CD", is triggered every time there is a push to the `master` branch.

The pipeline is designed to run on an `ubuntu-latest` environment and performs a series of actions:

1. **Code Checkout:** The repository is checked out using `actions/checkout@v2`.

2. **Python Setup:** Python 3.9 is set up using `actions/setup-python@v2`.

3. **Dependency Installation:** All required dependencies are installed with pip.

4. **Test Execution:** The `APP_ENVIRONMENT` is set to `test` and all unit tests are executed with pytest.

5. **Deployment Package Creation:** Upon successful execution of the tests, a deployment package is created excluding any `.git`, `__pycache__`, and `tests` files/directories.

6. **Deployment to Elastic Beanstalk:** The deployment package is then deployed to AWS Elastic Beanstalk using `einaregilsson/beanstalk-deploy@v14`. This action is performed with the AWS access key and secret key stored as GitHub Secrets to ensure secure access.

This CI/CD workflow allows for reliable, efficient, and secure software delivery by automating the entire process of integration, testing, and deployment.

# API Documentation

## Postman Collection

To make it easier to test the API endpoints, a Postman collection is provided. Postman is an API testing tool that allows you to send different HTTP requests to the API. You can use the collection to send requests to our API and observe the responses. 

Access the Postman collection [here](https://documenter.getpostman.com/view/5044011/2s946h6rKL). 

## Swagger Documentation

The API also comes with a comprehensive Swagger documentation that provides details about all the available endpoints, their expected parameters and responses, and possible status codes and their meanings. This documentation can be of great help when trying to understand what functionality is available and how to use it. 

Access the Swagger documentation [here](http://book-service.us-east-1.elasticbeanstalk.com/api/docs/).

# Access the API

Interact with the API directly using the base URL provided below. Remember to include the `/v1/` suffix to ensure the use of version 1 of the API:

[http://book-service.us-east-1.elasticbeanstalk.com/v1/](http://book-service.us-east-1.elasticbeanstalk.com/v1/)


