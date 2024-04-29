# User Management Backend

This project is a Django backend for managing users, addresses, and organizations.

## Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/hamzakhalil90/BitsolAssessmentBackend.git
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```
3. Create .env file
   ```bash
    JWT_ENCODING_ALGO=
    JWT_ENCODING_SECRET_KEY=
    JWT_TOKEN_EXPIRY_DELTA=
    DATABASE_HOST=
    DATABASE_NAME=
    DATABASE_USERNAME=
    DATABASE_PASSWORD=
    DATABASE_PORT=
    ```
   
4. Apply database migrations:

    ```bash
    python manage.py migrate
    ```
   By default SQLite is configured, but database engine can be changed easily.

5. Run the development server:

    ```bash
    python manage.py runserver
    ```

## API Endpoints

### Users

- **List Users**: `GET /user/`
- **Create User**: `POST /user/`
- **Update User**: `PATCH /user/`
- **Delete User**: `DELETE /user/?id={user_id}`

## Testing

To run the test suite:

```bash
python manage.py test
```
For Postman API documentation
```bash
https://documenter.getpostman.com/view/24030933/2sA3JDfjXn
```
Create bulk amount of users using following command:
```bash
 python manage.py createbulkusers [NUMBER]
```
NUMBER to be replaced with numbers of users to be created
