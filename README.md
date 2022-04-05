
# la-plateforme-a-caractere-associatif.org

The last student project made for the project 13 from [OpenClassrooms](https://openclassrooms.com/)'s Python course.

From scratch, I have to create a complete project in order to synthesize acquired knowledge.


## Tech Stack

* Python 3.9
* Django 3.2
* PostgreSQL
* Love 💙



## Environement

In `src/config/settings/` add an `.env` file with your environment variables

```bash
# PostgreSQL
NAME=your-database-name
USER=your-username
PASSWORD=your-will-never-guess
HOST=127.0.0.1-or-whatever
PORT=5432-or-whatever

#DJANGO SECRET-KEY
SECRET_KEY=your-very-secret-key


######################### optional #################################


# Reset password feature
EMAIL_USER=maybe-your-email
EMAIL_PASS=your-will-never-guess-again

# Sentry
SENTRY=your-secret-url

# Production
PRODUCTION=1
```


## Run Locally

👉 Before, you need to install [Tox](https://tox.readthedocs.io/en/latest/)

Clone the project

```bash
  git clone https://github.com/CamClrt/P13-volunteering
```

Go to the root of the project `P13-volunteering` and start the server

```bash
  tox -e py39
```


## Running Tests

To run tests, run the following command

```bash
  tox -e test
```

To run coverage and build HTML report, run the following command

```bash
  tox -e coverage
```


## Author

- **Camille Clarret** aka **Camoulty** or **CamClrt** : https://github.com/CamClrt
