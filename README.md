# 🍛 Indian Recipe Vault

---

## Team

**Team Name:** TechInnovators

**Team Members:**

* Naguboyina Dheeraj
* Phani Shashindhar
* Charan
* Sai Kiran
* Mohit

---

## 📝 Overview

**Recipe Vault** is an intuitive Streamlit application designed to streamline the process of storing, organizing, and managing your favorite culinary creations. It provides a seamless experience for users to log in, submit detailed recipes—complete with ingredients, preparation steps, and optional multimedia instructions (images and audio)—and easily review past submissions.

---

## ✨ Features

* **Secure User Login:** Access the application using pre-defined credentials.
* **Comprehensive Recipe Submission Form:** Submit new recipes with the following details:
    * User's Full Name and Email
    * Geolocation
    * Recipe Category (e.g., Dessert, Main Course)
    * Recipe Title and Description
    * Ingredients (comma-separated)
    * Preparation Steps
    * Image Upload (JPG, JPEG, PNG)
    * Optional Audio Instruction Upload (MP3, WAV)
* **Previous Submissions View:** A clear sidebar provides a quick summary of all submitted recipes, including timestamp, username, title, geolocation, and category.
* **CSV Data Storage:** All recipe data is persistently stored in a `recipes.csv` file.
* **Automated File Handling:** Uploaded images and audio files are automatically saved to a dedicated `uploads` directory.

---

## 🚀 Getting Started

### 🔧 Prerequisites

To run this application, ensure you have the following installed:

* **Python:** Version 3.8 or higher (recommended).
* **pip:** Python package installer.
* **Git:** For cloning the repository.

### 🖥️ Local Setup

Follow these steps to get the application running on your local machine:

1.  **Clone the repository:**
    ```bash
    git clone [https://code.swecha.org/soai2025/soai-hackathon/recipevault/](https://code.swecha.org/soai2025/soai-hackathon/recipevault/)
    cd recipevault
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *If you don't have a `requirements.txt` file, create one in the `recipevault` directory and add `streamlit` and `pandas` to it.*
3.  **Create the uploads directory:**
    ```bash
    mkdir uploads
    ```
4.  **Run the application:**
    ```bash
    streamlit run your_app_file_name.py # Replace 'your_app_file_name.py' with the actual name of your main Python file (e.g., app.py or main.py)
    ```
5.  Open your web browser and navigate to the URL provided by Streamlit (typically `http://localhost:8501`).

---

## 🌐 Live Application & 🎥 Demo Video

Currently, there is no live deployment or demo video available for the "Indian Recipe Vault."

---

## 📁 Repository Link

You can access the project's source code on GitLab:

[Visit the GitLab Repository](https://code.swecha.org/soai2025/soai-hackathon/recipevault/)

---

## 🧠 Usage Guide

### Login

Upon opening the application, you'll be prompted to log in. Use the following default credentials:

* **Username:** `admin`
* **Password:** `password123`

### Submit a Recipe

After logging in, navigate to the "Submit a Recipe" section. Fill in all the required details:

* Your full name and email address.
* Your approximate geolocation (e.g., "Hyderabad, India" or "17.3850, 78.4867").
* The category of your recipe (e.g., "Dessert," "Main Course," "Snack").
* The recipe title, a brief description, ingredients (comma-separated), and preparation steps.
* Optionally, upload an image and/or an audio file for instructions.

Click the "Submit Recipe" button to save your entry.

### View Submissions

On the left sidebar, you can find a summary table displaying all previously submitted recipes, including their timestamp, username, title, geolocation, and category.

---

## ⚙️ Supported File Types

* **Images:** JPG, JPEG, PNG
* **Audio:** MP3, WAV

---

## 📈 Roadmap

The development roadmap for the "Indian Recipe Vault" includes the following:

* [x] Basic Recipe Submission Form
* [x] CSV Data Storage & Retrieval
* [x] Image & Audio File Upload Handling
* [x] User Login System
* [ ] Enhanced Search and Filtering for Recipes
* [ ] User Accounts (beyond single admin)
* [ ] Recipe Editing and Deletion
* [ ] Integration with a proper database (e.g., SQLite)
* [ ] Deployment to Streamlit Community Cloud
