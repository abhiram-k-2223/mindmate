# MindMate - Your Mental Health Companion

MindMate is a web application designed to assist users in maintaining their mental well-being through journaling, data visualization, and conversational interaction. This README provides an overview of the application's functionalities, setup, and usage.

## Features

### 1. Authentication
- Users can log in or sign up using their email address and password.
- Firebase Authentication is used for user management.

### 2. Journaling
- Users can write journal entries to express their thoughts and feelings.
- Each entry includes a mood selection (positive, negative, or neutral) and content.
- Journal entries are stored in Firebase Realtime Database.

### 3. Dashboard
- Provides a visual representation of the user's journal entries.
- Displays the distribution of positive, negative, and neutral sentiments in the form of column and Nightingale (radar) charts.

### 4. Chatbot Interaction
- Users can engage in conversation with a chatbot.
- The chatbot generates responses using a generative AI model.

## Setup

### Prerequisites
- Python 3.6 or higher
- pip package manager

### Installation
1. Clone the repository:

    ```bash
    git clone https://github.com/abhiram-k-2223/mindmate.git
    ```

2. Navigate to the project directory:

    ```bash
    cd MindMate
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up Firebase:
    - Create a Firebase project and obtain the necessary credentials.
    - Create an API for your project through the firebase application and grab yourself a json file.

5. Set up Google GenerativeAI:
    - Obtain an API key for Google GenerativeAI and set it as an environment variable named `GOOGLE_API_KEY`.

6. Run the application:

    ```bash
    streamlit run app.py
    ```

## Usage

1. Launch the application by running the command mentioned in the setup.
2. Log in or sign up to access the features.
3. Choose from the available options: Journal, Dashboard, or Chatbot.
4. Write journal entries, view visualizations on the dashboard, or engage in conversation with the chatbot.
5. Explore different features to enhance your mental well-being.

## Contributors

- [[ABHIRAM](https://github.com/abhiram-k-2223)]

## License

This project is licensed under the [MIT License](LICENSE).
