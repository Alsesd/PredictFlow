# 🌊 PredictFlow: Customer Churn Prediction Service

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange.svg)](https://www.tensorflow.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red.svg)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![Poetry](https://img.shields.io/badge/Dependency%20Management-Poetry-blueviolet.svg)](https://python-poetry.org/)

**PredictFlow** is a containerized machine learning application designed to predict customer churn probability. This project demonstrates a complete, end-to-end machine learning pipeline, seamlessly bridging the gap between data exploration, model training, and production-ready deployment.

---

## 📑 Table of Contents
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started & Deployment](#-getting-started--deployment)
- [Usage](#-usage)
- [Future Improvements](#-future-improvements)

---

## ✨ Features

- 🧠 **Predictive Modeling:** Utilizes a custom TensorFlow neural network to accurately classify customer churn risk.
- 🔄 **Robust Data Pipeline:** Includes automated data cleaning, feature engineering, and preprocessing workflows.
- 📊 **Interactive UI:** A Streamlit dashboard enables real-time inference and intuitive visualization of prediction results.
- 🗄️ **Persistent Logging:** Stores prediction history in a local SQLite database for easy auditing and tracking.
- 🐳 **Containerization:** Fully Dockerized to guarantee consistent, reproducible execution across any environment.

---

## 🛠️ Tech Stack

- **Language:** Python
- **ML Frameworks:** TensorFlow, Keras, Scikit-Learn
- **Frontend:** Streamlit
- **Dependency Management:** Poetry (`pyproject.toml`)
- **Database:** SQLite
- **Deployment:** Docker

---

## 📂 Project Structure

The repository is organized to maintain a clear separation between research, model artifacts, and application logic:

```text
.
├── data/               # Raw and processed datasets
├── models/             # Trained .keras models and .pkl scalers
├── notebooks/          # Jupyter notebooks for EDA and model experimentation
├── Dockerfile          # Production-ready container definition
├── main.py             # Streamlit application entry point
├── utils.py            # Preprocessing and inference logic helpers
├── pyproject.toml      # Dependency management (Poetry)
└── README.md           # Project documentation
```
## 🚀 Launch Instructions

The fastest way to run PredictFlow is by using the pre-built Docker image hosted on Docker Hub. No local Python environment setup is required!

### Step 1: Pull the Docker Image
Pull the latest pre-built image directly from Docker Hub:
```bash
docker pull alsesd/churn-service:latest
```

### Step 2: Run the Container
Start the application and map the necessary ports and volumes:
```bash
docker run -d -p 8501:8501 -v $(pwd)/data:/app/data --name predictflow alsesd/churn-service:latest
```
*(Note: The `-d` flag runs the container in the background, and `-v` ensures your local `data` folder is mounted so the SQLite database persists between restarts).*

### Step 3: Verify the Launch
Open your web browser and navigate to:
👉 **[http://localhost:8501](http://localhost:8501)**

> **💡 Local Build Alternative:**
> If you have made code changes and want to build the image yourself instead of pulling from Docker Hub, run:
> `docker build -t alsesd/churn-service:latest .`
> Then run the `docker run` command from Step 2.
