# Blogging Website

A fully-featured blogging platform built with Django, Python, HTML, CSS, JavaScript, and MySQL.

## Features

- User registration and authentication
- Profile management (bio, profile picture)
- Blog post creation and management
- Rich text editor for post content
- Commenting system with nested comments
- Likes and dislikes for posts and comments
- User following system
- Categories and tags for organizing content
- Search and filter functionality
- Admin panel for content moderation

## Technologies Used

- **Backend**: Django, Python
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Database**: MySQL
- **Additional**: CKEditor, Taggit, Crispy Forms

## Installation

### Prerequisites

- Python 3.8 or higher
- MySQL
- pip (Python package manager)

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/blog-site.git
   cd blog-site
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows:
     ```
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install the requirements:
   ```
   pip install -r requirements.txt
   ```
   
   > **Note**: You must install all required packages before proceeding with the next steps.

5. Set up MySQL database:
   - Create a database named `blog_database`
   - Update the database configuration in `settings.py` if needed

6. Run migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

7. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

8. Start the development server:
   ```
   python manage.py runserver
   ```

9. Visit `http://127.0.0.1:8000/` in your browser to access the site

## Project Structure

- **blog/** - Main application
  - **models.py** - Database models
  - **views.py** - View functions
  - **forms.py** - Form classes
  - **urls.py** - URL routing
  - **admin.py** - Admin site configuration
  - **templates/** - HTML templates
  - **static/** - CSS, JavaScript, and images

## Usage

### Admin Panel

- Access the Django admin panel at `/admin/` using your superuser credentials
- You can also access the custom admin panel at `/admin-panel/` after logging in as a superuser

### Creating a Blog Post

1. Register or log in to your account
2. Navigate to your profile page
3. Click on "Create Post"
4. Fill in the post details (title, content, category, tags, etc.)
5. Choose to save as draft or publish immediately
6. Click "Save" to create the post

### Commenting

1. Navigate to a blog post
2. Scroll down to the comments section
3. Enter your comment and click "Submit"
4. To reply to a comment, click the "Reply" link under that comment

### Following Users

1. Navigate to a user's profile page
2. Click the "Follow" button to follow the user
3. You can view the users you follow and your followers on your profile page

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Django](https://www.djangoproject.com/)
- [Bootstrap](https://getbootstrap.com/)
- [CKEditor](https://ckeditor.com/)
- [Font Awesome](https://fontawesome.com/) 