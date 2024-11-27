# py-pg-seller-marketplace

This guide will help you set up and run the backend application.

## Prerequisites

Before you begin, ensure that you have the following software installed:

- **Python 3.x**: Download from [python.org](https://www.python.org/downloads/).
- **PostgreSQL**: Install from [postgresql.org](https://www.postgresql.org/download/).
- **Redis**: Install from [redis.io](https://redis.io/download/).
- **Git**: Install from [git-scm.com](https://git-scm.com/).

## Step 1: Clone the Repository

Clone the repository to your local machine using Git:

```bash
git clone [<your-repository-url>](https://github.com/RijalArul/py-pg-seller-marketplace.git)
cd <your-repository-folder>
```

## Step 2: Setup The Environment

Open the .env file and update the following environment variables with your database and Redis connection details:

```bash
POSTGRES_HOST=<postgres-host>
POSTGRES_PORT=<postgres-port>
POSTGRES_DB=<postgres-db-name>
POSTGRES_USER=<postgres-username>
POSTGRES_PASSWORD=<postgres-password>
REDIS_HOST=<redis-host>
REDIS_PORT=<redis-port>
REDIS_DB=<redis-db-number>
```
## Step 3: Install Dependencies

```bash
python -m venv venv
```

### Activate the virtual environment
#### On Windows:
venv\Scripts\activate
#### On macOS/Linux:
source venv/bin/activate


pip install -r requirements.txt

## Step 4: Run Database Migrations

To set up the PostgreSQL database, tables, and generate dummy data, run the migration.py script:

```bash
python migration.py
```

### This script will:

Create the necessary PostgreSQL database and tables.
Insert dummy data into the database for testing purposes.

## Step 5: Run the Backend

Once the database and dummy data are set up, you can start the backend server by running the main.py file:

```bash
python main.py
```
