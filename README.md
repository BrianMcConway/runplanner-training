# RunPLanner Training

<img src="static/images/readme_images/responsive-image-readme.jpg" alt="App device responsiveness" width="1000"/>


## Introduction

  [Click here to visit ](https://runplanner-training-cfec4c16a60a.herokuapp.com/)


  [Admin access](https://runplanner-training-cfec4c16a60a.herokuapp.com/admin/)

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
    - [Postgres SQL](#postgres-sql)
    - [Stripe Integration](#stripe-integration)
    - [Heroku Deployment](#heroku-deployment)
14. [Bugs](#bugs)
15. [Credits](#credits)
    - [Code Inspiration](#code-inspiration)
    - [Media](#media)
    - [Acknowledgements](#acknowledgements)

---

## UX - User Experience

## Project Planning

### Agile Methodologies - Project Management

I used Agile methodologies to manage the development process effectively. By utilizing GitHub's project management tools, I created and tracked issues to break down tasks and stay organized. Issues were used to lay out specific tasks, helping to track progress toward key goals. This approach provided a clear roadmap, allowing for regular assessments and adjustments as needed. GitHub’s tools helped ensure that the project stayed on track and adaptable throughout the development process.

### User Stories

#### **1. As a shopper, I want to view training plans by distance so that I can easily find plans for specific race distances (e.g., 5k, 10k, marathon).**

- **Acceptance Criteria**:
  - The training plans page should provide options to filter plans by race distance.
  - Filters should include common distances such as 5k, 10k, half marathon, and marathon.
  - Selecting a distance should dynamically update the list of displayed plans.

---

#### **2. As a site user, I want to register for an account so that I can view and purchase training plans.**

- **Acceptance Criteria**:
  - The registration form should include the following fields:
    - Username
    - Email
    - Password
    - Password confirmation
  - Upon successful registration:
    - The user should receive an email verification link to confirm their account.
  - If invalid or incomplete information is entered:
    - Appropriate error messages should be displayed next to the relevant fields.
  - The form should not submit until all fields are valid.

---

#### **3. As a site user, I want to log in and log out securely so that I can access my personal information and keep my account secure.**

- **Acceptance Criteria**:
  - The login form should require the user to input either their username/email and password.
  - Upon successful login, the user should be redirected to the homepage.
  - If login details are incorrect, an appropriate error message should be displayed to the user.

---

#### **4. As a site user, I want the option to delete my account and personal information so that I can ensure my data is no longer stored or used by the site.**

- **Acceptance Criteria**:
  - The user dashboard should have a "Delete Account" option under account settings.
  - Selecting the "Delete Account" option should prompt a confirmation dialog to prevent accidental deletions.
  - Upon confirming deletion, the user's account and all associated personal information should be permanently removed from the system.

---

#### **5. As a shopper, I want to view and manage a shopping basket so that I can keep track of the items I intend to purchase.**

- **Acceptance Criteria**:
  - Users should be able to add items to the shopping basket.
  - Users should be able to remove items from the shopping basket.
  - The shopping basket should display a running total of the costs of all items.
  - Users should receive a confirmation message when items are added to or removed from the basket.


### Wireframes

<img src="static/images/readme_images/wireframes.jpg" alt="Wireframes" width="600"/>

- Wireframes are based on two views. The landing page view and the second wireframe that shows the central location of each feature to be displayed. There is a minimal design here on purpose to show that most users will be accessing the app through a mebile device. RunPlanner Training has been designed with the mobile user in mind, and focuses strongly on small screen responsiveness for a better user experience.

 
---

### Database Schema

**Database Schema Diagram**

<img src="static/images/schema.png" alt="Database Schema Diagram" width="600"/>

### Database Schema and Relationships

The database schema represents the structure of the application, including custom models, built-in Django models, and third-party app integrations. Below is an explanation of the key models and their relationships:

1. **User Model**:
   - Built on Django's `AbstractBaseUser` and `PermissionsMixin`.
   - Fields: `username`, `email`, `first_name`, `last_name`, `is_active`, `is_staff`, `is_superuser`, and more.
   - **Relationships**:
     - Many-to-Many with `Group` for role-based permissions.
     - Many-to-Many with `Permission` for individual user permissions.
     - Related to `BasketItem`, `Purchase`, `Order`, `SocialAccount`, and comments/posts.

2. **Product Model**:
   - Represents items available for purchase, such as training plans.
   - Fields: `name`, `category`, `price`, `difficulty`, `description`, etc.
   - **Relationships**:
     - One-to-Many with `BasketItem`.
     - One-to-Many with `OrderLineItem`.

3. **Order and OrderLineItem Models**:
   - **Order**:
     - Represents a purchase order.
     - Fields: `full_name`, `email`, `grand_total`, `stripe_pid`, and address fields.
     - **Relationships**:
       - One-to-Many with `OrderLineItem` (an order can contain multiple items).
   - **OrderLineItem**:
     - Tracks individual items in an order.
     - Fields: `quantity`, `lineitem_total`.
     - **Relationships**:
       - Belongs to an `Order`.
       - Refers to a `Product`.

4. **BasketItem Model**:
   - Represents items added to a user's basket (shopping cart).
   - Fields: `quantity`.
   - **Relationships**:
     - Belongs to a `User`.
     - Refers to a `Product`.

5. **Purchase Model**:
   - Tracks specific training plans purchased by users.
   - Fields: `payment_verified`, `purchase_date`.
   - **Relationships**:
     - Belongs to a `User`.
     - Refers to a `Product` (training plan).

6. **Django's Built-in Models**:
   - The schema includes built-in Django models like `Group`, `Permission`, `ContentType`, `Session`, and models from `django.contrib.auth`.
   - **Functionality**:
     - Manage user permissions, session handling, and content types.
     - The `LogEntry` model tracks administrative actions within the Django admin interface.

7. **Allauth Models**:
   - Includes `EmailAddress`, `EmailConfirmation`, `SocialAccount`, `SocialApp`, and `SocialToken`.
   - Part of the Django Allauth package, managing user authentication, email verification, and social account integrations.
   - **Relationships**:
     - Establish links between `User` and social authentication services or email confirmation records.

8. **ContactMessage Model**:
   - Stores messages submitted via a "Contact Us" form.
   - Fields: `name`, `email`, `subject`, `message`.

9. **Comment and Post Models**:
   - Implements a simple blog or post-comment system.
   - **Post**:
     - Represents blog posts or updates.
     - Related to `User` as `author`.
   - **Comment**:
     - Tracks comments on posts.
     - Related to `Post` and `User`.

---

### Relationship Summary

The diagram illustrates the relationships between these models:

- **One-to-One Relationships**:
   - Between `User` and models for social account data or email verification (via Allauth).

- **One-to-Many Relationships**:
   - Between `Order` and `OrderLineItem` (an order contains multiple items).
   - Between `Product` and `BasketItem` or `OrderLineItem`.

- **Many-to-Many Relationships**:
   - Between `User` and `Group` for role-based permissions.
   - Between `User` and `Permission` for individual user permissions.

- **Foreign Key Relationships**:
   - `BasketItem` links `User` to `Product`.
   - `Purchase` links `User` to `Product`.
   - `OrderLineItem` links `Order` to `Product`.

This schema effectively organizes user data, authentication, purchases, and content, ensuring scalability and security for the application's core functionalities.

## Security

### Overview

Ensuring the security of user data and the integrity of the application is a top priority. The following measures have been implemented to secure the Brendan Doyle Running Club website:

### 1. Environmental Variables

Sensitive information, such as API keys, database credentials, and secret keys, is stored in environment variables. This approach ensures that these details are not hard-coded into the codebase and are not exposed in the version control system (e.g., GitHub).

To manage environment variables, the project uses the `django-environ` package. Key configurations include:

- **SECRET_KEY**: This is the secret key used by Django for cryptographic signing. It is kept as an environment variable to prevent exposure.
- **DATABASE_URL**: Connection string for the PostgreSQL database.
- **EMAIL_HOST_PASSWORD**: Password for the email service used by the application.
- **STRIPE_PUBLIC_KEY**: Key for using the Stripe payment system.

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
- Future features will involve the generation of training plans based on the athletes needs. The plan will be generated for the athlete in their personal account, based on distance, skill level, elevation, tarining availability, and length of time until the event. This gives an extra edge over generic training plans that can be downloaded. This will expand on the current sorting system of finding a suitable training plan from the database. 

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
- Stripe

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

<img src="static/images/readme_images/lighthouse-desktop.jpg" alt="Lighthouse Testing Desktop" width="400"/>

**Mobile View Score**

<img src="static/images/readme_images/lighthouse-mobile.jpg" alt="Lighthouse Testing Mobile" width="400"/>



### Code Validation

### HTML Code Validation

### HTML Validation Notes

During the HTML validation process, certain errors were identified, primarily related to dynamically generated template tags in Django, such as `{% static %}`, `{% block %}`, and `{% include %}`. These tags are not valid HTML and can cause validation errors when checked directly through tools like the W3C HTML Validator. Additionally, issues like duplicate `id` attributes and invalid element nesting were flagged. While these issues would typically warrant correction, the project has reached a late stage of development, making structural changes impractical due to potential disruption of existing functionality.

Instead, the focus has been on ensuring that the rendered HTML follows semantic standards as much as possible. In future iterations or projects, these issues can be addressed earlier in the development process to improve maintainability and validation compliance.


### CSS Code Validation

The CSS code has been validated for compliance.

<img src="static/images/readme_images/css-validation.jpg" alt="CSS Code Validation" width="400"/>

### Python Code Validation

### runplanner_training app

The `urls.py` file in the  app has been validated for PEP8 compliance.

<img src="static/images/readme_images/rp-urls.py.jpg" alt="PEP8 Validation for urls.py in  App" width="400"/>

The `settings.py` file in the  app has been validated for PEP8 compliance.

<img src="static/images/readme_images/settings.py.jpg" alt="PEP8 Validation for settings.py in  App" width="400"/>

### account App

The `views.py` file in the profiles app has been validated for PEP8 compliance.

<img src="static/images/readme_images/acc-views.py.jpg" alt="PEP8 Validation for views.py in profiles App" width="400"/>

The `signals.py` file in the profiles app has been validated for PEP8 compliance.

<img src="static/images/readme_images/acc-signals.py.jpg" alt="PEP8 Validation for signals.py in profiles App" width="400"/>

The `urls.py` file in the profiles app has been validated for PEP8 compliance.

<img src="static/images/readme_images/acc-urls.py.jpg" alt="PEP8 Validation for urls.py in profiles App" width="400"/>

The `models.py` file in the profiles app has been validated for PEP8 compliance.

<img src="static/images/readme_images/acc-models.py.jpg" alt="PEP8 Validation for models.py in profiles App" width="400"/>

The `forms.py` file in the profiles app has been validated for PEP8 compliance.

<img src="static/images/readme_images/acc-forms.py.jpg" alt="PEP8 Validation for forms.py in profiles App" width="400"/>

The `apps.py` file in the profiles app has been validated for PEP8 compliance.

<img src="static/images/readme_images/acc-apps.py.jpg" alt="PEP8 Validation for apps.py in profiles App" width="400"/>


### basket App

The `views.py` file in the  app has been validated for PEP8 compliance.

<img src="static/images/readme_images/bask-views.py.jpg" alt="Views.py Code Validation" width="400"/>

The `signals.py` file in the  app has been validated for PEP8 compliance.

<img src="static/images/readme_images/bask-signals.py.jpg" alt="Signals.py Code Validation" width="400"/>

The `urls.py` file in the members app has been validated for PEP8 compliance.

<img src="static/images/readme_images/bask-urls.py.jpg" alt="Urls.py Code Validation" width="400"/>

The `models.py` file in the members app has been validated for PEP8 compliance.

<img src="static/images/readme_images/bask-models.py.jpg" alt="Models.py Code Validation" width="400"/>

The `contexts.py` file in the  app has been validated for PEP8 compliance.

<img src="static/images/readme_images/bask-contexts.py.jpg" alt="Middleware.py Code Validation" width="400"/>

The `apps.py` file in the  app has been validated for PEP8 compliance.

<img src="static/images/readme_images/bask-apps.py.jpg" alt="Apps.py Code Validation" width="400"/>


### blog App

The `urls.py` file in the home app has been validated for PEP8 compliance.

<img src="static/images/readme_images/blog-urls.py.jpg" alt="Urls.py Code Validation" width="400"/>

The `forms.py` file in the home app has been validated for PEP8 compliance.

<img src="static/images/readme_images/blog-forms.py.jpg" alt="Forms.py Code Validation" width="400"/>

The `apps.py` file in the home app has been validated for PEP8 compliance.

<img src="static/images/readme_images/blog-apps.py.jpg" alt="Apps.py Code Validation" width="400"/>

The `views.py` file in the home app has been validated for PEP8 compliance.

<img src="static/images/readme_images/blog-views.py.jpg" alt="Views.py Code Validation" width="400"/>

The `utils.py` file in the home app has been validated for PEP8 compliance.

<img src="static/images/readme_images/blog-utils.py.jpg" alt="Utils.py Code Validation" width="400"/>

### checkout App

The `urls.py` file in the home app has been validated for PEP8 compliance.

<img src="static/images/readme_images/check-urls.py.jpg" alt="Urls.py Code Validation" width="400"/>

The `forms.py` file in the home app has been validated for PEP8 compliance.

<img src="static/images/readme_images/check-forms.py.jpg" alt="Forms.py Code Validation" width="400"/>

The `apps.py` file in the home app has been validated for PEP8 compliance.

<img src="static/images/readme_images/check-apps.py.jpg" alt="Apps.py Code Validation" width="400"/>

The `views.py` file in the home app has been validated for PEP8 compliance.

<img src="static/images/readme_images/check-views.py.jpg" alt="Views.py Code Validation" width="400"/>

### contact App

The `urls.py` file in the home app has been validated for PEP8 compliance.

<img src="static/images/readme_images/con-urls.py.jpg" alt="Urls.py Code Validation" width="400"/>

The `forms.py` file in the home app has been validated for PEP8 compliance.

<img src="static/images/readme_images/con-forms.py.jpg" alt="Forms.py Code Validation" width="400"/>

The `apps.py` file in the home app has been validated for PEP8 compliance.

<img src="static/images/readme_images/con-apps.py.jpg" alt="Apps.py Code Validation" width="400"/>

The `views.py` file in the home app has been validated for PEP8 compliance.

<img src="static/images/readme_images/con-views.py.jpg" alt="Views.py Code Validation" width="400"/>

### pages App

The `urls.py` file in the home app has been validated for PEP8 compliance.

<img src="static/images/readme_images/pages-urls.py.jpg" alt="Urls.py Code Validation" width="400"/>

The `sitemaps.py` file in the home app has been validated for PEP8 compliance.

<img src="static/images/readme_images/pages-sitemaps.py.jpg" alt="Sitemaps.py Code Validation" width="400"/>

The `apps.py` file in the home app has been validated for PEP8 compliance.

<img src="static/images/readme_images/pages-apps.py.jpg" alt="Apps.py Code Validation" width="400"/>

The `views.py` file in the home app has been validated for PEP8 compliance.

<img src="static/images/readme_images/pages-views.py.jpg" alt="Views.py Code Validation" width="400"/>

### products App

The `urls.py` file in the home app has been validated for PEP8 compliance.

<img src="static/images/readme_images/prod-urls.py.jpg" alt="Urls.py Code Validation" width="400"/>

The `forms.py` file in the home app has been validated for PEP8 compliance.

<img src="static/images/readme_images/prod-forms.py.jpg" alt="Forms.py Code Validation" width="400"/>

The `apps.py` file in the home app has been validated for PEP8 compliance.

<img src="static/images/readme_images/prod-apps.py.jpg" alt="Apps.py Code Validation" width="400"/>

The `views.py` file in the home app has been validated for PEP8 compliance.

<img src="static/images/readme_images/prod-views.py.jpg" alt="Views.py Code Validation" width="400"/>

### Home App

The `urls.py` file in the home app has been validated for PEP8 compliance.

<img src="static/images/readme_images/prod-urls.py.jpg" alt="Urls.py Code Validation" width="400"/>

The `forms.py` file in the home app has been validated for PEP8 compliance.

<img src="static/images/readme_images/prod-forms.py.jpg" alt="Forms.py Code Validation" width="400"/>

The `apps.py` file in the home app has been validated for PEP8 compliance.

<img src="static/images/readme_images/prod-apps.py.jpg" alt="Apps.py Code Validation" width="400"/>

The `views.py` file in the home app has been validated for PEP8 compliance.

<img src="static/images/readme_images/prod-views.py.jpg" alt="Views.py Code Validation" width="400"/>


### Javascript Validation

<img src="static/images/readme_images/js-hint.jpg" alt="Javascript Code Validation" width="400"/>

### Manual Testing

Manual testing was conducted extensively to ensure the application's responsiveness and usability across different devices and browsers. This testing involved using various tools and techniques to verify that the application renders correctly on mobile devices, tablets, and desktops. 

Testing on physical devices included smartphones with different screen sizes and resolutions to check for any layout issues or touch interactions. Additionally, the application was tested on various browsers such as Chrome, Firefox, Safari, and Edge to ensure cross-browser compatibility and consistent user experience. 

Tools like Google Chrome DevTools were used to simulate different screen sizes and devices, allowing for quick checks of responsive design elements. The application's layout, typography, and interactive elements were adjusted based on feedback from these tests to ensure a seamless experience across all platforms. 

Overall, this rigorous manual testing process ensured that the application is fully responsive, accessible, and performs optimally on a wide range of devices and browsers.

### Manual Testing for E-Commerce Website

Below is a list of manual testing cases to ensure the functionality and user experience of the e-commerce website are working as expected.

---

#### **1. User Authentication**
- **Test Case 1.1**: **User Registration**
  - Navigate to the registration page.
  - Enter valid details (username, email, password) and submit.
  - Verify that the user is registered successfully and redirected to the appropriate page.

- **Test Case 1.2**: **Login**
  - Enter valid credentials and log in.
  - Confirm that the user is redirected to the homepage and their account information is accessible.

- **Test Case 1.3**: **Password Reset**
  - Request a password reset using a registered email.
  - Verify that the email contains a reset link.
  - Reset the password and log in with the new credentials.

---

#### **2. Product Pages**
- **Test Case 2.1**: **Product Listing**
  - Visit the product listing page.
  - Confirm that all products are displayed with correct titles, images, prices, and descriptions.

- **Test Case 2.2**: **Product Details**
  - Click on a product to view its details.
  - Verify that the product page displays accurate information, including name, price, images, and availability.

- **Test Case 2.3**: **Search Functionality**
  - Search for a product using the search bar.
  - Verify that relevant results are displayed.

---

#### **3. Shopping Cart**
- **Test Case 3.1**: **Add to Cart**
  - Add a product to the shopping cart.
  - Confirm that the cart updates with the correct product, quantity, and price.

- **Test Case 3.2**: **Update Cart**
  - Increase or decrease the quantity of a product in the cart.
  - Verify that the cart updates the total price accordingly.

- **Test Case 3.3**: **Remove Item**
  - Remove a product from the cart.
  - Confirm that the product is no longer listed in the cart.

---

#### **4. Checkout Process**
- **Test Case 4.1**: **Payment Integration**
  - Proceed to checkout and fill in billing and shipping details.
  - Use test credit card details to simulate a payment.
  - Verify that the payment is successful and the order is created.

- **Test Case 4.2**: **Error Handling**
  - Enter invalid payment details.
  - Confirm that an appropriate error message is displayed.

- **Test Case 4.3**: **Order Confirmation**
  - Complete a payment and verify that the user is redirected to the order confirmation page with the correct details.

---

#### **5. Webhooks and Payment Status**
- **Test Case 5.1**: **Successful Payment Webhook**
  - Simulate a successful payment webhook.
  - Verify that the order status is updated to "Paid" in the database.

- **Test Case 5.2**: **Failed Payment Webhook**
  - Simulate a failed payment webhook.
  - Verify that the order status remains "Pending" and the user is notified.

---

#### **6. User Account**
- **Test Case 6.1**: **View Order History**
  - Log in as a user with past orders.
  - Verify that the order history displays correct details, including product names, quantities, and statuses.

- **Test Case 6.2**: **Update Profile**
  - Update the user's profile information (e.g., name, email, address).
  - Confirm that the changes are saved and reflected immediately.

---


### Authentication Features

To ensure the authentication features of the RunPlanner Training website are functioning correctly, I performed thorough manual testing on the following key areas:


### Login Page

- **Login Page**: Confirmed that registered users can log in with valid credentials and that appropriate error messages are shown when incorrect details are entered.

Login Form View

<img src="static/images/readme_images/login-form.jpg" alt="Login Form View" width="400"/>

Login Incorrect Details Warning

<img src="static/images/readme_images/login-incorrect.jpg" alt="Login Incorrect Details Warning" width="400"/>


### Password Reset Request

- **Password Reset Request**: Checked the functionality of the "Forgot Password" link by requesting a password reset. Ensured that users receive a password reset email and that the link directs them to the correct reset page.

Forgotten Password Reset Form

<img src="static/images/readme_images/password-reset.jpg" alt="Forgotten Password Reset Form" width="400"/>

Password Reset Link Sent by Email

<img src="static/images/readme_images/password-link-sent.jpg" alt="Password Reset Link Sent by Email" width="400"/>

Set New Password Form

<img src="static/images/readme_images/new-password.jpg" alt="Set New Password Form" width="400"/>

Password Successfully Reset Notification

<img src="static/images/readme_images/password-changed.jpg" alt="Password Successfully Reset Notification" width="400"/>


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

### Stripe Integration

#### **Overview**
Stripe is integrated into the project to handle payment processing, including card payments, checkout sessions, and webhook notifications. This section documents the key steps involved in setting up Stripe within the project.

---

#### **Key Steps in Integration**

1. **Install Stripe SDK**:
   - The project uses the official Stripe Python library to interact with Stripe's API.
   - Installation:
     ```bash
     pip install stripe
     ```

2. **Configure Stripe API Keys**:
   - The following API keys were configured in the `.env` file for secure storage:
     - **Publishable Key**: Used on the client side for Stripe Checkout.
     - **Secret Key**: Used on the server side for Stripe API calls.
     - **Webhook Secret**: Used to verify the authenticity of incoming webhooks.
   - Example `.env` configuration:
     ```env
     STRIPE_PUBLISHABLE_KEY=your_publishable_key
     STRIPE_SECRET_KEY=your_secret_key
     STRIPE_WEBHOOK_SECRET=your_webhook_secret
     ```

3. **Checkout Session Creation**:
   - A Django view was created to handle checkout session creation using Stripe's API.
   - This view specifies:
     - Payment methods (e.g., card).
     - Product details (name, description, price, quantity).
     - Success and cancel URLs to handle user redirection after payment.
   - Example configuration in `urls.py`:
     ```python
     path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create_checkout_session'),
     ```

4. **Frontend Integration**:
   - The Stripe JavaScript library (`https://js.stripe.com/v3/`) was integrated into the project to redirect users to the Stripe-hosted Checkout page.
   - A "Checkout" button triggers the process, fetching a session ID from the backend and initiating the checkout flow.
   - Example JavaScript snippet:
     ```javascript
     const stripe = Stripe("your_publishable_key");

     document.getElementById("checkout-button").addEventListener("click", () => {
         fetch("/create-checkout-session/", {
             method: "POST",
         })
         .then(response => response.json())
         .then(data => stripe.redirectToCheckout({ sessionId: data.id }));
     });
     ```

5. **Webhook Integration**:
   - Webhooks were set up to handle events from Stripe, such as `checkout.session.completed`.
   - A webhook endpoint was added to listen for Stripe events and update order status in the database.
   - Example webhook flow:
     - Verify the webhook signature using the `STRIPE_WEBHOOK_SECRET`.
     - Parse the payload to identify the event type.
     - Fulfill the purchase (e.g., mark an order as paid) based on the event.

6. **Testing Integration**:
   - Stripe's test mode and test card numbers were used to simulate different payment scenarios.
   - Stripe CLI was used to forward webhook events to the local development server:
     ```bash
     stripe listen --forward-to localhost:8000/webhook/
     ```

7. **Deployment**:
   - The Stripe webhook endpoint was updated in the Stripe Dashboard to point to the live server after deployment.
   - Environment variables were configured on the live server to secure the API keys.

---

#### **Key Endpoints**
- **Checkout Session**: `/create-checkout-session/`
- **Stripe Webhook**: `/webhook/`

---

### Heroku Deployment

To deploy your Django project on Heroku, follow these steps:

1. **Install Required Packages**:
   - Install `gunicorn` (WSGI HTTP Server for Python), `whitenoise` (to serve static files), and `psycopg2` (PostgreSQL database adapter for Python).

2. **Create a Heroku App**:
   - Log in to Heroku and navigate to **Create New App**.
   - Enter your app name and click on **Create App**.

3. **Set Config Vars**:
   - In the **Deploy** section, navigate to **Config Vars** and reveal them.
   - Enter the necessary configuration values. For this project, they were `SECRET_KEY`, `DATABASE_URL`, `DEFAULT_FROM_EMAIL`, `GOOGLE_MAPS_API_KEY`,. Additionally, `PORT:8000` and `DISABLE_COLLECTSTATIC` (with a value of 1) were added during deployment.

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
- [How to use Stripe for payment in Django](https://www.youtube.com/watch?v=hZYWtK2k1P8&t=15s)

#### **References**
- [Stripe API Documentation](https://stripe.com/docs/api)
- [Stripe Webhooks](https://stripe.com/docs/webhooks)
- [Stripe Testing](https://stripe.com/docs/testing)
- [Stack Overflow](https://stackoverflow.com/)
- [Django documentation](https://docs.djangoproject.com/en/5.1/)
- [OpenAI's ChatGPT](https://chatgpt.com/)
- [Perplexity](https://www.perplexity.ai/)


### Acknowledgements

Thank you to my Facilitator, Mentor, Tutor support, Family and Friends that helped me with this difficult project, and course overall!!!
