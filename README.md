# RunPLanner Training

<img src="" alt="App device responsiveness" width="1000"/>


## Introduction

  [Click here to visit ](https://.herokuapp.com/)


  [Admin access](https://)

---

## Table of Contents

1. [Introduction](#introduction)
2. [UX - User Experience](#ux---user-experience)
    - [Design Inspiration](#design-inspiration)
    - [Color Choices](#color-choices)
    - [Font Choices](#font-choices)
3. [Project Planning](#project-planning)
    - [Agile Methodologies - Project Management](#agile-methodologies---project-management)
    - [User Stories](#user-stories)
4. [Wireframes](#wireframes)
5. [Database Schema](#database-schema)
6. [Security](#security)
7. [Features](#features)
    - [User Views and Features - Non-members/Members](#user-views-and-features---non-membersmembers)
    - [CRUD Functionality](#crud-functionality)
    - [Feature Showcase](#feature-showcase)
    - [Future Features](#future-features)
8. [Technologies & Languages Used](#technologies--languages-used)
    - [Libraries, Frameworks & APIs](#libraries-frameworks--apis)
    - [Packages](#packages)
    - [Utilities](#utilities)
9. [Testing](#testing)
    - [Validation](#validation)
        - [Lighthouse Testing](#lighthouse-testing)
        - [Code Validation](#code-validation)
            - [HTML Code Validation](#html-code-validation)
            - [CSS Code Validation](#css-code-validation)
            - [Python Code Validation](#python-code-validation)
            - [Javascript Validation](#javascript-validation)
    - [Manual Testing](#manual-testing)
    - [Authentication Features](#authentication-features)
10. [Unit Testing](#unit-testing)
11. [Integration Testing](#integration-testing)
12. [User Acceptance Testing](#user-acceptance-testing)
13. [Deployment](#deployment)
    - [Create a New Github Repository from a Template](#create-a-new-github-repository-from-a-template)
    - [Open Repository on Gitpod](#open-repository-on-gitpod)
    - [Django Project Setup](#django-project-setup)
    - [Cloudinary API](#cloudinary-api)
    - [Postgres SQL](#postgres-sql)
    - [Heroku Deployment](#heroku-deployment)
14. [Bugs](#bugs)
15. [Credits](#credits)
    - [Code Inspiration](#code-inspiration)
    - [Media](#media)
    - [Acknowledgements](#acknowledgements)

---

## UX - User Experience

---

### Design Inspiration


---

## Color Choices



### Font Choices

The font choices are selected to balance readability with a modern feel:


---

## Project Planning

### Agile Methodologies - Project Management

I used Agile methodologies to manage the development process effectively. By utilizing GitHub's project management tools, I created and tracked issues to break down tasks and stay organized. Milestones were used to group related tasks, helping to track progress toward key goals. This approach provided a clear roadmap, allowing for regular assessments and adjustments as needed. GitHub’s tools helped ensure that the project stayed on track and adaptable throughout the development process.

### User Stories
#### Visitor User Stories


---

### Wireframes

 
---

### Database Schema

**Database Schema Diagram**

  <img src="" alt="Database Schema Diagram" width="600"/>

### Database Schema and Relationships

The database schema . Below is an explanation of the key models and their relationships:

1.
3. 
4. **Django's Built-in Models**:
   - The schema also includes several built-in Django models like `Group`, `Permission`, `ContentType`, `Session`, and models from the `django.contrib.auth` and `django.contrib.admin` apps.
   - These models provide functionalities such as user permissions, session management, and content type information.
   - The `LogEntry` model is particularly used for tracking administrative actions within the Django admin interface.

5. **Allauth Models**:
   - Models like `EmailAddress`, `EmailConfirmation`, `SocialAccount`, `SocialApp`, and `SocialToken` are part of the Django Allauth package, which manages user authentication, including email verification and social account integration.
   - These models establish relationships with the `User` model, ensuring that email confirmations and social account data are properly linked to individual users.

6. **Permissions and Groups**:
   

### Relationship Summary

The diagram illustrates the relationships between these models:

- **One-to-One Relationship**: 
   - Between `User` and `Profile`.

- **One-to-Many Relationship**:
   
- **Many-to-Many Relationship**:
   
- **Foreign Key Relationships**:
   

This schema effectively manages the complexity of user data, authentication, and uploaded content, ensuring that the Brendan Doyle Running Club application can serve its members effectively while maintaining robust security and data integrity.

---

## Security

### Overview

Ensuring the security of user data and the integrity of the application is a top priority. The following measures have been implemented to secure the Brendan Doyle Running Club website:

### 1. Environmental Variables

Sensitive information, such as API keys, database credentials, and secret keys, is stored in environment variables. This approach ensures that these details are not hard-coded into the codebase and are not exposed in the version control system (e.g., GitHub).

To manage environment variables, the project uses the `django-environ` package. Key configurations include:

- **SECRET_KEY**: This is the secret key used by Django for cryptographic signing. It is kept as an environment variable to prevent exposure.
- **DATABASE_URL**: Connection string for the PostgreSQL database.
- **CLOUDINARY_URL**: URL for Cloudinary API integration.
- **EMAIL_HOST_PASSWORD**: Password for the email service used by the application.
- **GOOGLE_MAPS_API_KEY**: API key for Google Maps integration.

These environment variables are loaded securely and used throughout the application, ensuring that sensitive data is protected.

### 2. Cross-Site Request Forgery (CSRF) Protection

To prevent Cross-Site Request Forgery (CSRF) attacks, Django provides built-in middleware. The following settings have been enabled to enhance CSRF protection:

- **CSRF_COOKIE_HTTPONLY = True**: This setting ensures that the CSRF cookie is only accessible via HTTP(S) requests, which means it cannot be accessed by client-side JavaScript. This adds a layer of security by preventing malicious scripts from hijacking the CSRF token.
  
- **CSRF_COOKIE_SECURE = True**: This setting ensures that the CSRF cookie is only sent over HTTPS, preventing it from being intercepted in transit. This is particularly important when the site is served over HTTPS, as it ensures that the token is not exposed over insecure connections.

### 3. Secure Cookies

In addition to securing the CSRF cookie, the following settings have been applied to secure the session cookies:

- **SESSION_COOKIE_SECURE = True**: Ensures that the session cookie is only sent over HTTPS, protecting it from being intercepted over insecure connections.

- **SESSION_COOKIE_HTTPONLY = True**: Prevents client-side scripts from accessing the session cookie, reducing the risk of XSS (Cross-Site Scripting) attacks.

### 4. Content Security Policy (CSP)

While Django does not enforce Content Security Policy (CSP) by default, implementing a CSP is recommended to prevent a wide range of attacks, including XSS. A CSP can be configured to restrict the sources from which content can be loaded.

### 5. HTTPS

The application is served over HTTPS, ensuring that all data transmitted between the client and server is encrypted. This helps protect against man-in-the-middle attacks.

### 6. User Authentication and Permissions

- **Django Allauth**: The application uses Django Allauth for robust user authentication, including email verification and social account integration.
- **Custom Permissions**: Certain views and functionalities are restricted to authenticated users. The members area, for example, is accessible only to verified members.


## Features

### User Views and Features - Non-members/Members

### CRUD Functionality
Detail the Create, Read, Update, and Delete functionalities implemented in the project.

### Feature Showcase
Highlight the main features of the project with descriptions and screenshots if available.

### Future Features
- 

## Technologies & Languages Used

- HTML
- CSS
- Python
- JavaScript

### Libraries, Frameworks & APIs

- Django
- Bootstrap5
- Google Fonts

### Packages

- Django Allauth
- Crispyforms
- Crispy Bootstrap5
- Psycopg

### Utilities

- Git
- Github
- Heroku
- PostgreSQL
- Balsamiq Wireframes
- Google Chrome Dev Tools
- Favicon
- Perplexity AI
- ChatGPT-4o

## Testing

## Validation

### Lighthouse Testing

Lighthouse testing was carried out on the desktop and mobile views of the website

**Desktop View Score**

<img src="" alt="Lighthouse Testing Desktop" width="400"/>

**Mobile View Score**

<img src="" alt="Lighthouse Testing Mobile" width="400"/>



### Code Validation

### HTML Code Validation

Homepage Code Validation

<img src="" alt="Homepage Code Validation" width="400"/>

About Page Code Validation

<img src="" alt="About Page Code Validation" width="400"/>

Classes Page Code Validation

<img src="" alt="Classes Page Code Validation" width="400"/>

Events Page Code Validation

<img src="" alt="Events Page Code Validation" width="400"/>

Contact Page Code Validation

<img src="" alt="Contact Page Code Validation" width="400"/>

Login Page Code Validation

<img src="" alt="Login Page Code Validation" width="400"/>

Signup Page Validation

<img src="" alt="Signup Page Validation" width="400"/>

### CSS Code Validation

The CSS code has been validated for compliance.

<img src="" alt="CSS Code Validation" width="400"/>

### Python Code Validation

### running_club App

The `urls.py` file in the  app has been validated for PEP8 compliance.

<img src="" alt="PEP8 Validation for urls.py in  App" width="400"/>

The `settings.py` file in the  app has been validated for PEP8 compliance.

<img src="" alt="PEP8 Validation for settings.py in  App" width="400"/>

### profiles App

The `views.py` file in the profiles app has been validated for PEP8 compliance.

<img src="" alt="PEP8 Validation for views.py in profiles App" width="400"/>

The `signals.py` file in the profiles app has been validated for PEP8 compliance.

<img src="" alt="PEP8 Validation for signals.py in profiles App" width="400"/>

The `urls.py` file in the profiles app has been validated for PEP8 compliance.

<img src="" alt="PEP8 Validation for urls.py in profiles App" width="400"/>

The `models.py` file in the profiles app has been validated for PEP8 compliance.

<img src="" alt="PEP8 Validation for models.py in profiles App" width="400"/>

The `forms.py` file in the profiles app has been validated for PEP8 compliance.

<img src="" alt="PEP8 Validation for forms.py in profiles App" width="400"/>

The `apps.py` file in the profiles app has been validated for PEP8 compliance.

<img src="" alt="PEP8 Validation for apps.py in profiles App" width="400"/>

The `admin.py` file in the profiles app has been validated for PEP8 compliance.

<img src="" alt="PEP8 Validation for admin.py in profiles App" width="400"/>


### Members App

The `views.py` file in the  app has been validated for PEP8 compliance.

<img src="" alt="Views.py Code Validation" width="400"/>

The `signals.py` file in the  app has been validated for PEP8 compliance.

<img src="" alt="Signals.py Code Validation" width="400"/>

The `urls.py` file in the members app has been validated for PEP8 compliance.

<img src="" alt="Urls.py Code Validation" width="400"/>

The `models.py` file in the members app has been validated for PEP8 compliance.

<img src="" alt="Models.py Code Validation" width="400"/>

The `middleware.py` file in the  app has been validated for PEP8 compliance.

<img src="" alt="Middleware.py Code Validation" width="400"/>

The `forms.py` file in the  app has been validated for PEP8 compliance.

<img src="" alt="Forms.py Code Validation" width="400"/>

The `apps.py` file in the  app has been validated for PEP8 compliance.

<img src="" alt="Apps.py Code Validation" width="400"/>

The `admin.py` file in the  app has been validated for PEP8 compliance.

<img src="" alt="Admin.py Code Validation" width="400"/>


### Home App

The `urls.py` file in the home app has been validated for PEP8 compliance.

<img src="" alt="Urls.py Code Validation" width="400"/>

The `forms.py` file in the home app has been validated for PEP8 compliance.

<img src="" alt="Forms.py Code Validation" width="400"/>

The `apps.py` file in the home app has been validated for PEP8 compliance.

<img src="" alt="Apps.py Code Validation" width="400"/>

The `views.py` file in the home app has been validated for PEP8 compliance.

<img src="" alt="Views.py Code Validation" width="400"/>

### Javascript Validation

<img src="" alt="Javascript Code Validation" width="400"/>

### Manual Testing

Manual testing was conducted extensively to ensure the application's responsiveness and usability across different devices and browsers. This testing involved using various tools and techniques to verify that the application renders correctly on mobile devices, tablets, and desktops. 

Testing on physical devices included smartphones with different screen sizes and resolutions to check for any layout issues or touch interactions. Additionally, the application was tested on various browsers such as Chrome, Firefox, Safari, and Edge to ensure cross-browser compatibility and consistent user experience. 

Tools like Google Chrome DevTools were used to simulate different screen sizes and devices, allowing for quick checks of responsive design elements. The application's layout, typography, and interactive elements were adjusted based on feedback from these tests to ensure a seamless experience across all platforms. 

Overall, this rigorous manual testing process ensured that the application is fully responsive, accessible, and performs optimally on a wide range of devices and browsers.

### Authentication Features

To ensure the authentication features of the RunPlanner Training website are functioning correctly, I performed thorough manual testing on the following key areas:

### Signup Page

- **Signup Page**: Verified that new users can register successfully by filling in all required fields. Tested form validations to ensure errors are correctly displayed when invalid data is entered (e.g., weak passwords, mismatched passwords).

Sign Up Page

<img src="" alt="Signup Page" width="400"/>

Sign Up Required Fields

<img src="" alt="Signup Required Fields" width="400"/>

Sign Up Username Requirement

<img src="" alt="Signup Username Requirement" width="400"/>


### Login Page

- **Login Page**: Confirmed that registered users can log in with valid credentials and that appropriate error messages are shown when incorrect details are entered.

Login Form View

<img src="" alt="Login Form View" width="400"/>

Login Incorrect Details Warning

<img src="" alt="Login Incorrect Details Warning" width="400"/>


### Password Reset Request

- **Password Reset Request**: Checked the functionality of the "Forgot Password" link by requesting a password reset. Ensured that users receive a password reset email and that the link directs them to the correct reset page.

Forgotten Password Reset Form

<img src="" alt="Forgotten Password Reset Form" width="400"/>

Password Reset Link Sent by Email

<img src="" alt="Password Reset Link Sent by Email" width="400"/>

Set New Password Form

<img src="" alt="Set New Password Form" width="400"/>

Password Successfully Reset Notification

<img src="" alt="Password Successfully Reset Notification" width="400"/>


Through these tests, I ensured that the authentication mechanisms user-friendly and secure, providing a smooth experience for users interacting with the login, signup, and password reset features.

---

### Unit Testing
Explain the unit testing methodologies used to ensure individual components function correctly.

### Integration Testing
Describe the integration testing processes to ensure different components work together as expected.

### User Acceptance Testing
Detail the user acceptance testing to validate the project meets user requirements.

---

## Deployment

### Create a New Github Repository from a Template

To begin your project deployment, follow these steps to create a new GitHub repository from a template:

1. **Navigate to the Template Repository**:
   - Visit the [Code Institute template repository](https://github.com/Code-Institute-Org/ci-full-template).

2. **Create a New Repository**:
   - Click on the green button labeled "Use this template" located near the top right of the page.
   - Select "Create a new repository" from the dropdown options.
   - Enter a name for your new repository.
   - Add a description for your repository.
   - Set the privacy to **Public**.
   - Click on the "Create repository from template" button to finalize.

### Open Repository on Gitpod

To begin working on your repository in Gitpod, follow these steps:

1. **Log in to GitHub**:
   - Ensure you are logged into your GitHub account.

2. **Navigate to Your Repository**:
   - Find your repository by using the GitHub search bar or by navigating directly to it.

3. **Open in Gitpod**:
   - Once inside the repository, open it in Gitpod. This will initialize a workspace and clone the repository into it.

4. **Start Working**:
   - You can now start working on your project within the Gitpod online IDE.
   - Once changes are made, you can commit and push them back to GitHub using the integrated terminal or source control tools provided by Gitpod.

### Django Project Setup

To set up your Django project, follow these steps:

1. **Install Django**:
   - Since Python is included with the template, install Django directly using:
     ```bash
     pip install django
     ```

2. **Create a Project Structure**:
   - Generate the directory structure for your project:
     ```bash
     django-admin startproject <project_name>
     ```

3. **Run Initial Migration**:
   - Set up the built-in database by running:
     ```bash
     python manage.py migrate
     ```

4. **Create a Superuser**:
   - To access the Django admin interface, create a superuser:
     ```bash
     python manage.py createsuperuser
     ```

5. **Start the Development Server**:
   - Start the Django development server to see your project in action:
     ```bash
     python manage.py runserver
     ```
   - Open a web browser and navigate to `http://127.0.0.1:8000/` to see the Django welcome page.

6. **Access the Django Admin Interface**:
   - Navigate to `http://127.0.0.1:8000/admin/` to access the Django admin interface.



### Postgres SQL

For database management, this project utilizes Postgres SQL:

- The Code Institute provided a Postgres database for this project.
- Environment variables were used to securely manage and store database details, ensuring they are not exposed in the repository.

### Heroku Deployment

To deploy your Django project on Heroku, follow these steps:

1. **Install Required Packages**:
   - Install `gunicorn` (WSGI HTTP Server for Python), `whitenoise` (to serve static files), and `psycopg2` (PostgreSQL database adapter for Python).

2. **Create a Heroku App**:
   - Log in to Heroku and navigate to **Create New App**.
   - Enter your app name and click on **Create App**.

3. **Set Config Vars**:
   - In the **Deploy** section, navigate to **Config Vars** and reveal them.
   - Enter the necessary configuration values. For this project, they were `SECRET_KEY`, `DATABASE_URL`, `CLOUDINARY_URL`, `DEFAULT_FROM_EMAIL`, `GOOGLE_MAPS_API_KEY`, and `RUNNING_CLUB_MAIL`. Additionally, `PORT:8000` and `DISABLE_COLLECTSTATIC` (with a value of 1) were added during deployment.

4. **Configure ALLOWED_HOSTS**:
   - Add the Heroku host name to the `ALLOWED_HOSTS` in `settings.py`.

5. **Deploy the Project**:
   - In the **Deploy** tab, select GitHub as the method of deployment, connect your repository, and manually deploy the branch.

6. **Finalize Deployment**:
   - Ensure `DEBUG` is set to `False` in your settings before final deployment.
   - After a successful deployment, `DISABLE_COLLECTSTATIC` and `PORT:8000` can be removed from the Config Vars.

---

## Bugs

**Existing Bugs**

**Other Bugs**

1. 
---

## Credits

### Code Inspiration

**During this project I relied on the following YouTube videos for guidance with my issues:**

- 
- [Style Django Forms With Bootstrap - Django Blog #5](https://www.youtube.com/watch?v=6-XXvUENY_8)
- [How To Use Django Crispy Forms](https://www.youtube.com/watch?v=HX1mErYy8hU)
- [E 030 Django E commerce Toasts Part 1](https://www.youtube.com/watch?v=cwhROnUBZbQ)
- [How To Modify and Override Django Allauth Template Page](https://www.youtube.com/watch?v=VIoKemDBv8Y&t=3s)
- 
- 

**I also used the following websites for guidance:**
- [Stack Overflow](https://stackoverflow.com/)
- [Django documentation](https://docs.djangoproject.com/en/5.1/)
- [OpenAI's ChatGPT](https://chatgpt.com/)
- [Perplexity](https://www.perplexity.ai/)

### Media



### Acknowledgements



--- 
