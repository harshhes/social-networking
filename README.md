# Social Networking

Social networking application built with Python Django and Django Rest Framework (DRF), using PostgreSQL as the database.

### APIs and Features

1. **User Authentication**

   - Login and signup using email and password.
   - Authentication required for all APIs except signup/login.

2. **User Search Functionality**

   - API to search users by email and name (paginated).
   - Exact email matches and partial name matches supported.

3. **Friendship Operations**
   - APIs for sending/accepting/rejecting friend requests.
   - List friends (accepted friend requests).
   - List pending friend requests.
   - Limit users to sending 3 friend requests per minute.

## Local Setup

### Installation Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/social-networking.git
   ```

2. Navigate to the project directory:

   ```bash
   cd social-networking
   ```

3. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Database Setup:

   - Ensure PostgreSQL is running.
   - Create a new database for the project.

5. Configuration:

   - Create a `.env` file in the project root.
   - Add the environment variables to the `.env` file:
   - ## Environment Variables

   - `DEBUG`: Set to `True` or `False` for Django debugging.
   - `SECRET_KEY`: Django secret key for encryption.

   ## PostgreSQL Configuration

   - `DJANGO_POSTGRES_HOST`: PostgreSQL host.
   - `DJANGO_POSTGRES_PORT`: PostgreSQL port.
   - `DJANGO_POSTGRES_USER`: PostgreSQL username.
   - `DJANGO_POSTGRES_PASSWORD`: PostgreSQL password.
   - `DJANGO_POSTGRES_DATABASE`: PostgreSQL database name.

   Note: Replace the placeholders with your actual values for the environment variables.

6. Run Migrations:

   ```bash
   python manage.py migrate
   ```

7. Start the Django Development Server:

   ```bash
   python manage.py runserver
   ```

8. Access the application:
   Open your web browser and go to `http://localhost:8000`
