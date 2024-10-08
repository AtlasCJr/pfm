# Personal Finance Manager

**Personal Finance Manager (PFM)** is a tool designed to help individuals manage their finances effectively. With features for tracking income, expenses, and budgeting. 

## Features

1. **Multiple Accounts**: Track various accounts in one place.
2. **Embedded Database System**: Includes an internal database (cloud-based aswell) to store financial data.
3. **Budgeting Tools**: Set up custom budgets and track spending by category (groceries, entertainment, etc.).
4. **Income & Expense Tracking**: Log all transactions and categorize them easily.
5. **Data Visualization**: Charts and graphs to visualize financial trends and spending patterns.
6. **Internal Chatbot**: Use a chatbot to assist in interacting with PFM and get quick tips or insights.

## Technologies Used

This project is built using the following technologies:

<p align="center">
    <a href="https://github.com/search?q=user%3ADenverCoder1+language%3Acss">
        <img alt="CSS" src="https://img.shields.io/badge/CSS-1572B6.svg?logo=css3&logoColor=white"></a>
    <a href="https://github.com/search?q=user%3ADenverCoder1+language%3Ahtml">
        <img alt="HTML" src="https://img.shields.io/badge/HTML-E34F26.svg?logo=html5&logoColor=white"></a>
    <a href="https://github.com/search?q=user%3ADenverCoder1+language%3Amarkdown">
        <img alt="Markdown" src="https://img.shields.io/badge/Markdown-000000.svg?logo=markdown&logoColor=white"></a>
    <a href="https://github.com/search?q=user%3ADenverCoder1+language%3Apython">
        <img alt="Python" src="https://img.shields.io/badge/Python-14354C.svg?logo=python&logoColor=white"></a>
    <a href="https://github.com/search?q=user%3ADenverCoder1+language%3Asql">
        <img alt="SQL" src="https://custom-icon-badges.demolab.com/badge/SQL-025E8C.svg?logo=database&logoColor=white"></a>
</p>

1. **HTML/CSS**: for TOS and PP.
2. **Python** for backend logic, data processing, and frontend (PyQt5).
3. **SQL** for database management to store financial data.
4. **Markdown** for easy documentation and support.

## Installation & Setup

To get started with the project, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/AtlasCJr/pfm.git
    ```
2. Navigate to the project directory:
    ```bash
    cd pfm
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Start the application:
    ```bash
    python main.py
    ```
    ```bash
    PFM.exe
    ```

## Notes

1. Files in the **other** folder are not executable unless they are moved out of the folder, to the same hierarchy level as the folder (root).
2. The application includes two pre-configured user accounts with the following credentials and security question answers:
    1. Username: "user1", Password: "user1_template", Security Answer: "depok"
    2. Username: "user2", Password: "user2_template", Security Answer: "jakarta"
3. A Gemini API key is required to use the application. The key should be placed in **other/API.key**. However, an API key has already been added for now.
4. For the app:
    1. 'Login' page wouldn't show if you are already logged in.
    2. 'Visualize', 'Analyze', 'Profile', and 'Edit' pages will not be available unless the user is logged in.
    3. 'Visualize' and 'Edit' pages will only be accessible if the user's account has a minimum of two transactions.
    4. The 'Analyze' page will be unavailable unless the user's account contains transactions with a minimum time gap of one year (e.g., from 31st December 2023 to 1st January 2024).
    
## Contributors

<h4>
1. <a href="https://github.com/AtlasCJr">Jonathan Edward Charles</a><br/>
2. <a href="https://github.com/PinZapPin">Davin Nazhif Wilviadli</a><br/>
3. <a href="https://github.com/farhanhanafi">Muhammad Farhan Hanafi</a><br/>
</h4>