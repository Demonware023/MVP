# Flask Application README

---

NB: This code was developed and uses authentication requests. So in order to use this code you must insert a GitHub Token to use authenticated requests in the `github_search` function in the app.py file.
You can find the "HOW TO" from #line 64

## Features

This Flask application (`app.py`) provides a basic user management system with the following features:

- User registration and login
- User profile management (view and update)
- Admin dashboard to manage users
- GitHub API integration to fetch user data and repository information

## How to Run Locally

To run this Flask application locally on your machine, follow these steps:

1. **Clone the Repository:**
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. **Install Dependencies:**
   It's recommended to use a virtual environment (e.g., `venv` or `virtualenv`) to manage dependencies.
   ```bash
   # Create a virtual environment (optional but recommended)
   python -m venv venv

   # Activate the virtual environment (Windows)
   venv\Scripts\activate

   # Activate the virtual environment (macOS/Linux)
   source venv/bin/activate

   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Set Environment Variables:**
   Before running the application, set the necessary environment variables:
   - `SECRET_KEY`: Secret key for Flask session management.

   Example using bash:
   ```bash
   export SECRET_KEY='your_secret_key'
   ```

4. **Initialize the SQLite Database:**
   The SQLite database (`database.db`) is automatically initialized with necessary tables and columns when running the application.

5. **Run the Application:**
   Use Flask CLI to run the application.
   ```bash
   export FLASK_APP=app.py
   flask run
   ```

6. **Access the Application:**
   Open your web browser and go to `http://localhost:5000` to access the application.

## Inserting Your GitHub Token

To use authenticated requests in the `github_search` function, follow these steps:

1. **Generate GitHub Personal Access Token:**
   - Go to your GitHub account settings.
   - Navigate to "Developer settings" > "Personal access tokens" > "Generate new token".
   - Select the scopes (permissions) needed for your application (e.g., `repo` for accessing repositories).
   - Click "Generate token" and copy the generated token.

2. **Insert Token in `app.py`:**
   - Open `app.py` in your code editor.
   - Locate the `github_search` function.
   - Replace `'token ghp_yuBfOFMBDPKpimeJ**************'` with your GitHub token in the `headers` dictionary.

   Example:
   ```python
   headers = {
       'Authorization': 'token your_github_token_here'
   }
   ```

3. **Run the Application:**
   After inserting your token, save `app.py` and run the Flask application as described above.

---

This README provides a clear guide on setting up and running your Flask application (`app.py`) locally, including managing environment variables, initializing the SQLite database, and integrating your GitHub token for authenticated requests. Adjust the instructions and paths as per your specific project structure and deployment environment.
