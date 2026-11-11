# 🚀 Support-Pilot – Intelligent Email Support Automation System

Support-Pilot is an email support automation system designed to simplify customer support operations by automatically processing incoming emails, classifying support requests, retrieving relevant information, and generating context-aware responses.

The system combines a React frontend, FastAPI backend, PostgreSQL database, Pinecone vector database, and Google Gemini to streamline email-based support workflows.

---

## ✨ Key Features

- **Automated Email Monitoring:** Monitors incoming emails and processes new support requests.
- **Email Classification:** Identifies the category and intent of incoming emails.
- **Priority Detection:** Analyzes email content to identify urgency and severity.
- **Sentiment Analysis:** Understands the sentiment and tone of customer messages.
- **Context-Aware Response Generation:** Generates relevant responses using Google Gemini.
- **Retrieval-Augmented Generation (RAG):** Retrieves relevant information from the knowledge base using Pinecone.
- **Automated Email Replies:** Sends generated responses through email.
- **Human Review:** Supports review of responses when automatic resolution is not appropriate.
- **Support Dashboard:** Provides an interface to monitor and manage support requests.

---

## 🏗️ System Architecture

The application consists of three main components:

### 1. Frontend
- Built using React and Vite.
- Provides a dashboard for viewing and managing support requests.
- Communicates with the backend through REST APIs.

### 2. Backend
- Developed using Python and FastAPI.
- Handles email processing, classification, response generation, and API requests.
- Uses PostgreSQL for structured data storage.
- Integrates Gemini and Pinecone for intelligent processing and information retrieval.

### 3. Email Poller
- Connects to the email inbox using IMAP.
- Periodically checks for new incoming emails.
- Sends email content to the backend for processing.
- Uses SMTP to send generated email replies.

### Workflow

1. The poller periodically checks the support inbox.
2. New emails are retrieved using IMAP.
3. Email content is sent to the FastAPI backend.
4. The backend processes and classifies the support request.
5. Relevant knowledge is retrieved from Pinecone.
6. Gemini generates a context-aware response.
7. The response is sent through SMTP or routed for human review.
8. Support information is stored in PostgreSQL and displayed on the dashboard.

---

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Frontend | React, Vite, JavaScript |
| Backend | Python, FastAPI |
| Database | PostgreSQL, SQLAlchemy |
| Vector Database | Pinecone |
| Generative AI | Google Gemini 2.5 Flash |
| RAG Framework | LangChain |
| Email Integration | IMAP, SMTP |
| API Communication | REST APIs |
| Package Management | uv, npm |
| Version Control | Git, GitHub |

---

## 📂 Project Structure

```text
Support-Pilot/
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
├── server.py
├── main.py
├── config.py
├── .env.example
├── pyproject.toml
├── uv.lock
├── README.md
└── .gitignore
```

*The structure above highlights the main application components. Additional files and folders may be present in the repository.*

---

## ⚙️ Installation and Setup

### Prerequisites

Make sure the following tools are installed:

- Python
- uv
- Node.js and npm
- PostgreSQL
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/Manjiswari/Support-Pilot-Email-Automation-System.git
```

### 2. Navigate to the Project Directory

```bash
cd Support-Pilot-Email-Automation-System
```

### 3. Configure Environment Variables

Create a `.env` file in the project root using `.env.example` as a reference.

```env
EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-gmail-app-password

GEMINI_API_KEY=your-gemini-api-key

PINECONE_API_KEY=your-pinecone-api-key
PINECONE_INDEX_NAME=your-pinecone-index-name

SIMILARITY_THRESHOLD=0.40

DATABASE_URL=your-postgresql-connection-string

SERVER_URL=http://localhost:8000
```

Replace the placeholder values with your actual credentials.

**Important:** Never commit your `.env` file, API keys, passwords, or other sensitive credentials to GitHub.

### 4. Install Backend Dependencies

```bash
uv sync
```

### 5. Install Frontend Dependencies

```bash
cd frontend
npm install
```

---

## ▶️ Running the Application

Run the frontend, backend, and email poller in separate terminals.

### 1. Start the Backend

From the project root:

```bash
uv run uvicorn server:app --reload --port 8000
```

Backend URL:

```text
http://localhost:8000
```

### 2. Start the Email Poller

From the project root, open another terminal:

```bash
uv run main.py
```

The poller periodically checks the configured inbox for new emails.

### 3. Start the Frontend

Open another terminal:

```bash
cd frontend
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

---

## 🔐 Security

- API keys and credentials are maintained through environment variables.
- Sensitive configuration files should not be committed to version control.
- Email credentials should be protected.
- Database credentials should be stored securely.

---

## 🎯 Project Objective

The objective of Support-Pilot is to reduce repetitive manual work in email-based customer support by combining automated email processing, information retrieval, and response generation.

It provides a structured workflow for handling support requests while allowing human review when necessary.

---

## 👩‍💻 Developer

**Manjiswari Jajula**  
B.Tech – Computer Science and Engineering (AI & ML)  
VIT-AP University

GitHub: [Manjiswari](https://github.com/Manjiswari)

---

## 📄 License

This project is developed for educational and portfolio purposes.
