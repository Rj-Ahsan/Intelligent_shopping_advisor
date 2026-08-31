# 🛍️ Intelligent Shopping Advisor

An **AI-powered multi-agent shopping advisor** that helps users find and compare products based on their **budget, preferences, and natural-language requirements**.

The system uses **LangGraph and LangChain** to orchestrate multiple AI agents that understand user requirements, retrieve relevant products, compare available options, and generate personalized recommendations.

For example, a user can ask:

> **"Best smartphone under 100,000 PKR with a good camera and battery?"**

The system processes the request, identifies the user's requirements, evaluates available products, and provides an intelligent recommendation.

---

## 🚀 Features

* 🤖 **Multi-Agent AI Architecture**
* 🧠 Natural-language understanding of shopping requirements
* 💰 Budget-aware product recommendations
* 🔎 Product retrieval and information processing
* ⚖️ Product comparison
* ⭐ Personalized recommendations
* 🔄 Agent workflow orchestration using LangGraph
* 🔗 LangChain-based AI integration
* 🗃️ Structured product/data management
* 🧪 Evaluation and testing utilities
* 🐳 Docker support

---

## 🧠 How It Works

The system follows a multi-stage AI workflow:

```text
                User Query
                    │
                    ▼
        ┌──────────────────────┐
        │ Requirement Analysis │
        │      / Agent         │
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │  Product Retrieval   │
        │       Agent          │
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │ Product Comparison   │
        │       Agent          │
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │ Recommendation Agent │
        └──────────┬───────────┘
                   │
                   ▼
          Smart Recommendation
```

The multi-agent approach separates different responsibilities instead of relying on a single AI component to perform the entire shopping workflow.

---

## 🏗️ Project Architecture

The repository is organized into several components:

```text
Intelligent_shopping_advisor/
│
├── agents/
│   └── AI agent implementations
│
├── app/
│   └── Application components
│
├── data/
│   └── Product/data resources
│
├── database/
│   └── Database-related components
│
├── models/
│   └── Data/model definitions
│
├── utils/
│   └── Utility functions
│
├── app.py
│   └── Application entry point
│
├── evaluate.py
│   └── Evaluation utilities
│
├── simple_test.py
│   └── Basic testing
│
├── test.py
│   └── Testing utilities
│
├── requirements.txt
│   └── Python dependencies
│
├── Dockerfile
│   └── Container configuration
│
└── README.md
```

The repository currently contains dedicated modules for agents, application logic, data, database functionality, models, and utilities.

---

## 🔄 Multi-Agent Workflow

### 1. User Requirement Extraction

The user provides a natural-language shopping request.

Example:

```text
"Recommend a laptop under 150,000 PKR for AI development."
```

The system identifies important requirements such as:

* Product category
* Maximum budget
* Intended usage
* Desired specifications
* User preferences

---

### 2. Product Retrieval

The relevant agent searches or retrieves product information based on the extracted requirements.

The retrieved information can then be used for further analysis and comparison.

---

### 3. Product Comparison

Candidate products are analyzed according to factors such as:

* Price
* Features
* Specifications
* User requirements
* Relative value

---

### 4. Recommendation Generation

The final recommendation agent uses the processed information to generate a user-friendly response.

Instead of simply returning a list of products, the system aims to explain **which product is most suitable and why**.

---

## 🧩 Technology Stack

### AI / LLM

* **LangChain**
* **LangGraph**
* Large Language Model integration
* Multi-agent AI workflows

### Backend / Application

* Python
* Application modules
* Database integration

### Data

* Product data
* Structured data processing

### Testing & Evaluation

* Python testing scripts
* Model/agent evaluation utilities

### Deployment

* Docker
* `requirements.txt`

---

## 📊 Evaluation

The repository includes an `evaluate.py` module along with testing scripts such as:

```text
evaluate.py
simple_test.py
test.py
```

These components can be used to evaluate and test different parts of the shopping advisor workflow.

---

## 🐳 Docker

The project includes a `Dockerfile`, allowing the application to be packaged into a container for more consistent deployment environments.

Build the Docker image:

```bash
docker build -t intelligent-shopping-advisor .
```

Run the container:

```bash
docker run -p 8000:8000 intelligent-shopping-advisor
```

> Update the exposed port/command if the application configuration uses a different port.

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Rj-Ahsan/Intelligent_shopping_advisor.git
```

```bash
cd Intelligent_shopping_advisor
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

On Linux/macOS:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file if your configured LLM/provider integrations require API credentials.

Example:

```env
OPENAI_API_KEY=your_api_key_here
```

> Add only the environment variables required by your implementation. Never commit API keys or other secrets to GitHub.

---

## ▶️ Running the Application

Run the main application:

```bash
python app.py
```

If the project is configured as a web/API application, access the corresponding local URL shown by the application.

---

## 💡 Example Queries

The advisor can process natural-language shopping requests such as:

```text
Best smartphone under 100,000 PKR
```

```text
Suggest a laptop under 150,000 PKR for programming
```

```text
Which phone is better for photography?
```

```text
I need a budget laptop with good performance and battery life
```

The system extracts the important requirements and uses its multi-agent workflow to produce recommendations.

---

## 🎯 Project Objectives

The main objectives of this project are:

* Build a practical **AI agent system**.
* Understand multi-agent architecture.
* Learn how to orchestrate AI agents using **LangGraph**.
* Use **LangChain** for LLM-based application development.
* Process natural-language user requirements.
* Build intelligent product recommendation workflows.
* Implement product comparison logic.
* Work with structured product data.
* Develop evaluation and testing workflows.
* Containerize the application using Docker.

---

## 🧠 Key Concepts Demonstrated

This project demonstrates practical experience with:

* Generative AI
* Large Language Models
* AI Agents
* Multi-Agent Systems
* LangChain
* LangGraph
* Prompt Engineering
* Natural Language Processing
* Product Recommendation
* Information Retrieval
* Agent Orchestration
* Python Application Development
* Database Integration
* Testing & Evaluation
* Docker

---

## 📈 Future Improvements

Potential improvements include:

* 🔍 Real-time product search APIs
* 💵 Real-time price comparison
* 📉 Price-history analysis
* ⭐ Review sentiment analysis
* 🧠 User preference memory
* 🔎 Semantic product search
* 📊 Product ranking algorithms
* 🛒 Shopping-cart integration
* 💬 Conversational memory
* 📱 Web-based user interface
* 🚀 Cloud deployment
* 📈 Agent observability and monitoring
* 🧪 More comprehensive evaluation benchmarks

---

## 👨‍💻 Author

### Ahsan Tanveer

**BS Artificial Intelligence**

Interested in:

* Machine Learning
* Deep Learning
* Generative AI
* LLM Applications
* AI Agents
* NLP
* Computer Vision
* MLOps

---

## ⭐ Project Purpose

This project was developed as a practical implementation of **Generative AI and Agentic AI concepts**, focusing on how multiple specialized AI agents can work together to solve a real-world problem.

The project represents my continued learning in **LLM applications, LangChain, LangGraph, AI agents, and intelligent recommendation systems**.

---

## 📜 License

This project is intended for educational and portfolio purposes.
