# ✨ TopicLens AI

TopicLens AI is a premium NLP micro-service designed to classify tweets into six distinct categories with high precision. Built using the **CRISP-DM methodology**, this application leverages a tuned Linear Support Vector Machine (SVM) model to provide real-time linguistic analysis.

## 🚀 Features

- **Real-time Classification:** Instant topic prediction for any input tweet.
- **Premium UI/UX:** A modern, two-column interface built with Streamlit and custom CSS.
- **Interactive Examples:** One-click example selection to test model capabilities.
- **NLP Pipeline:** Integrated preprocessing including NLTK-based tokenization, stop-word removal, and WordNet lemmatization.

## 🧪 Methodology

This project follows the CRISP-DM (Cross-Industry Standard Process for Data Mining) framework:
1. Business Understanding: Identifying the need for automated tweet categorization.
2. Data Understanding: Ensuring the collected initial data, exploring it to detect insights, and identifying data quality issues.
3. Data Preparation: Cleaning, tokenizing, and lemmatizing raw text.
4. Modeling: Comparing Linear SVM, Logistic Regression, and Random Forest.
5. Evaluation: Hyperparameter tuning via GridSearchCV for optimal accuracy.
6. Deployment: Building the Streamlit app to classify the tweet topic.
    
## 📊 Model Overview

The underlying model was developed through extensive experimentation:
- **Architecture:** Linear Support Vector Machine (SVM).
- **Feature Engineering:** TF-IDF Vectorization with Bigram support.
- **Categories:**
  - 🎨 Arts & Culture
  - 💼 Business & Entrepreneurs
  - 🍿 Pop Culture
  - ☕ Daily Life
  - ⚽ Sports & Gaming
  - 🔬 Science & Technology

## 📂 Project Structure


## ⚙️ Installation & Local Setup

### 1. Clone Repo
```sh
git clone https://github.com/htutmyatoo/topic-lens-ai.git
cd topic-lens-ai
```

### 2. Create Environment
#### Windows (PowerShell)
```sh
python -m venv venv
venv\Scripts\activate
```
#### macOS / Linux
```sh
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```sh
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Launch App
```sh
streamlit run app.py
```

Open in your browser:
```sh
http://localhost:8501
```

## 🍥 Support
<a href="https://ko-fi.com/J3J21UINNT" target="_blank">
  <img src="https://storage.ko-fi.com/cdn/brandasset/v2/support_me_on_kofi_dark.png?_gl=1*mz6i7q*_gcl_au*MTE3MDY3MDM4NC4xNzcxNDUyMzcx*_ga*MTY2NTkxNjMxNy4xNzcxNDUyMzcy*_ga_M13FZ7VQ2C*czE3NzI0NTgwOTQkbzEyJGcxJHQxNzcyNDU4NDc4JGo1MSRsMCRoMA.." width = 200 alt="Ko-fi.com"/>
</a>
