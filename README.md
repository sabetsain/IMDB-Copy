# IMDB-Copy

A Flask-based web application that replicates core IMDB functionality with a PostgreSQL database backend.

## Prerequisites

- Python 3.8 or higher
- PostgreSQL
- pip (Python package manager)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/sabetsain/IMDB-Copy.git
   cd IMDB-Copy
   ```

2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up the PostgreSQL database:
   - Create a database named "imdb_copy"
   - Create a user named "dis_project" with password "dis_project"
   - Grant this user all privileges on the "imdb_copy" database

4. Initialize the application:
   ```
   export FLASK_APP=flaskr
   export FLASK_ENV=development
   flask init-db
   ```
   You should see the message "Initialized the database."

## Running the Application

To start the development server:
```
flask run
```

Visit http://127.0.0.1:5000/ in your browser to view the application.

## Project Structure

- `flaskr/` - Main application package
  - `__init__.py` - Application factory
  - `db.py` - Database connection and commands
  - `schema.sql` - Database schema definitions

## Contributing

Please make sure to test your changes before submitting pull requests.

## Dansk Version

# IMDB-Copy

En webapplikation baseret på Flask, der replikerer kernefunktionaliteten i IMDB med en PostgreSQL-database backend.

## Forudsætninger

- Python 3.8 eller nyere
- PostgreSQL
- pip (Python pakkemanager)

## Installation

1. Klon dette repository:
   ```
   git clone https://github.com/sabetsain/IMDB-Copy.git
   cd IMDB-Copy
   ```

2. Installer nødvendige afhængigheder:
   ```
   pip install -r requirements.txt
   ```

3. Opsæt PostgreSQL-databasen:
   - Opret en database ved navn "imdb_copy"
   - Opret en bruger ved navn "dis_project" med adgangskoden "dis_project"
   - Giv denne bruger alle rettigheder til "imdb_copy" databasen

4. Initialiser applikationen:
   ```
   export FLASK_APP=flaskr
   export FLASK_ENV=development
   flask init-db
   ```
   Du skulle gerne se meddelelsen "Initialized the database."

## Kørsel af Applikationen

For at starte udviklingsserveren:
```
flask run
```

Besøg http://127.0.0.1:5000/ i din browser for at se applikationen.

## Projektstruktur

- `flaskr/` - Hoved-applikationspakke
  - `__init__.py` - Applikationsfabrik
  - `db.py` - Databaseforbindelse og kommandoer
  - `schema.sql` - Databaseskema-definitioner

## Bidrag

Sørg for at teste dine ændringer, før du indsender pull requests.