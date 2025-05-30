# IMDB-Copy

A Flask-based web application that replicates core IMDB functionality with a PostgreSQL database backend.

## Prerequisites

- Python 3.8 or higher
- PostgreSQL
- pip (Python package manager)
- npm (node package manager)
- Docker Desktop + Docker VS Code extension (optional)

## Docker
If you have docker installed, you can simply run the command 'docker compose up' in the terminal,
and the application will run.

## Installation w/o Docker

1. Clone this repository:
   ```
   git clone https://github.com/sabetsain/IMDB-Copy.git
   cd IMDB-Copy
   ```

2. Install required dependencies:
   ```
   pip install -r flaskr/requirements.txt
   cd frontend
   npm install
   cd ..
   ```

3. Set up the PostgreSQL database:
   - Create a database named "imdb_copy"
   - Create a user named "dis_project" with password "dis_project"
   - Grant this user all privileges on the "imdb_copy" database

4. Initialize the application:
   ```
   flask init-db
   ```
   You should see the message "Initialized the database."

## Running the Application

To start the development server:
* Backend (from the root directory): 'flask --app flaskr run --debug'
* Frontend:
   - cd frontend
   - npm run dev

Visit http://localhost:5173/ in your browser to view the application.