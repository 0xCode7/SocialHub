
# 🧑‍💻 SocialHub - Django Social Media Platform

![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg?logo=python&logoColor=white)  ![Django](https://img.shields.io/badge/Django-4.2%2B-green.svg?logo=django&logoColor=white)  ![License](https://img.shields.io/badge/License-MIT-yellow.svg)  ![Status](https://img.shields.io/badge/Status-Completed-brightgreen.svg)

A mini Facebook-like web app where users can post updates, customize settings, and interact socially — all built with **Django**.  

---

## 📌 Core Features

### 🔐 User Authentication
- Register with email verification  
- Login / Logout  
- Password reset via email  
- User profile with bio and profile picture  

### 📧 Email Integration
- Welcome email on registration  
- Password reset emails  
- Email notifications for key user actions  

### 🗨 Social Features
- Create posts with text + images  
- Like / Unlike functionality  
- Basic commenting system  
- Home feed with all user posts  

### ⚙ User Settings
- Post privacy (Public / Friend / Private)  
- Notification preferences  
- Profile visibility controls  

---

## 🧱 Project Structure

### 🔨 Backend
- **Framework**: Django 4.2+  
- **Database**: SQLite (development)  
- **Image Handling**: Pillow

### 🎨 Frontend
- Django Templates (Jinja-like)  
- Custom styling  

### 🧬 Data Models
- **User**: Django’s built-in user model  
- **Profile**: Extends User (bio, avatar, etc.)  
- **Post**: Contains text, image, author, timestamp  
- **Comment**: Linked to Post + User  
- **Like**: Tracks user likes per post  
- **Settings**: Privacy & notification options  

---

# 🌍 URL Paths

## 🔐 Accounts
- `/register` → Register a new user with email verification  
- `/login` → Login to your account  
- `/logout` → Logout from the app  
- `/profile/<id>` → View a user’s profile  
- `/accounts/activate/<uidb64>/<token>` → Activate account via email  
- `/account/settings` → Manage privacy, notifications, and profile settings  

## 📝 Posts
- `/` → Home feed with all posts  
- `/post/new` → Create a new post  
- `/post/<post_id>` → View details of a single post  
- `/post/<post_id>/like` → Like or unlike a post  
- `/post/<pk>/delete` → Delete a post  

## 💬 Comments
- `/post/<post_id>/comment` → Add a comment on a post  
- `/comment/<comment_id>/delete` → Delete a comment  

---

## 🛠 Setup & Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/0xCode7/SocialHub.git
   cd SocialHub
   ```

2. Create & activate virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate   # on Windows
   source venv/bin/activate   # on Linux/Mac
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Create superuser (for admin panel):
   ```bash
   python manage.py createsuperuser
   ```

6. Start the development server:
   ```bash
   python manage.py runserver
   ```

7. Visit the app in your browser:
   ```
   http://127.0.0.1:8000
   ```


---

## 📜 License
This project is for educational purposes only (ITI Graduation Project).  
Licensed under the [MIT License](LICENSE).

---

Made with ❤️ by 
- [@MahmoudSaid](https://github.com/0xCode7)  
- [@MahmoudNasr](https://github.com/nasrmahmoud538-cmd)  
- [@Fares](https://github.com/FAr-Es)  
- [@Fady]()
