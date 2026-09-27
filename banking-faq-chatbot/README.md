# Banking FAQ Chatbot

BankID is an AI-powered banking FAQ assistant that helps users get quick answers to common banking questions. It supports natural-language questions about accounts, cards, transfers, loans, fees, online banking, security, fraud, and general banking terms.

The project includes a FastAPI backend with NLP-based FAQ matching and a React/Vite frontend with voice input, animated responses, suggestions, and banking calculators.

## Features

- Natural-language banking FAQ matching
- TF-IDF and cosine similarity search
- spaCy text preprocessing and lemmatization
- Confidence-based answers and fallback suggestions
- Support for informal conversation:
  - Greetings
  - Thanks
  - Goodbye
  - Help requests
  - Assistant identity questions
- BankID assistant branding
- EMI calculator
- Savings and compound-interest calculator
- Follow-up questions using recent conversation context
- Voice input through the browser Web Speech API
- Manual text input when voice input is unavailable
- Animated thinking indicator before responses
- Animated user and assistant chat bubbles
- Animated black and orange background
- Interactive voice-recording animation
- Responsive design for desktop and mobile browsers
- CORS configuration for frontend-backend communication
- API validation using Pydantic
- Automated backend and API tests

## Technology Stack

## Backend

- Python
- FastAPI
- Uvicorn
- spaCy
- scikit-learn
- TF-IDF vectorization
- Cosine similarity
- Pydantic
- Pytest

## Frontend

- React
- Vite
- Tailwind CSS
- Framer Motion
- JavaScript
- Web Speech API

## Project Structure

```text
banking-faq-chatbot/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── `routes.py`
│   │   ├── data/
│   │   │   └── faqs/
│   │   │       ├── `accounts.json`
│   │   │       ├── `assistant.json`
│   │   │       ├── `banking_basics.json`
│   │   │       ├── `cards.json`
│   │   │       ├── `fees.json`
│   │   │       ├── `loans.json`
│   │   │       ├── `online_banking.json`
│   │   │       ├── `security_fraud.json`
│   │   │       └── `transfers.json`
│   │   ├── nlp/
│   │   │   ├── `calculators.py`
│   │   │   ├── `matcher.py`
│   │   │   └── `preprocessing.py`
│   │   ├── `config.py`
│   │   ├── `main.py`
│   │   └── `schemas.py`
│   ├── tests/
│   │   ├── `test_api.py`
│   │   └── `test_matcher.py`
│   └── `requirements.txt`
├── frontend/
│   ├── public/
│   │   └── `favicon.svg`
│   ├── src/
│   │   ├── api/
│   │   │   └── `chatApi.js`
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── screens/
│   │   ├── `App.jsx`
│   │   ├── `index.css`
│   │   └── `main.jsx`
│   ├── `.env.example`
│   ├── `eslint.config.js`
│   ├── `index.html`
│   ├── `package.json`
│   └── `vite.config.js`
├── .gitignore
└── README.md
```

## Requirements

Install the following before running the project:

- Python 3.11 or newer
- Node.js 20 or newer
- npm
- Git


## FAQ Categories

The chatbot currently supports:

- Accounts
- Cards
- Transfers and payments
- Loans and credit
- Fees and charges
- Online and mobile banking
- Security and fraud
- Banking basics
- Assistant conversations

## Calculator Support

The chatbot can calculate:

### EMI

Example:

```text
EMI on 300000 at 10 percent for 2 years
```

### Savings Growth

Example:

```text
If I save 10000 at 6% for 5 years how much will I have?
```

Calculator results are estimates. Actual bank calculations may differ because of compounding frequency, fees, taxes, changing rates, and lender-specific rules.



## Security and Privacy

BankID is a general-information assistant. It does not access or control personal banking accounts.

Users should never share:

- Passwords
- PINs
- One-time passwords
- Full card numbers
- CVV/security codes
- Account login details
- Private financial information

For urgent or account-specific issues, users should contact their bank through an official website, application, branch, or the phone number printed on their card.

Before production deployment, the project should add:

- Authentication
- Rate limiting
- Request logging and monitoring
- HTTPS
- Stronger production CORS configuration
- Secure secret management
- Database-backed conversation storage if required


## License

This project was created by me [faizan ali] as part of an AI internship project for educational purposes.
