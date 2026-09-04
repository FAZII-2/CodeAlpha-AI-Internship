# AI Language Translator

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-Backend-black?logo=flask)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6-yellow?logo=javascript)

A modern, responsive, AI-powered language translator built as a capstone project for the **Code Alpha Academy AI Internship**. This application leverages the MyMemory Translation API to provide real-time translation across 60 global languages.

## Features
* **Real-Time Auto-Translation:** Translates seamlessly with an 800ms debounce delay—no "Translate" button required.
* **Voice-to-Text Recognition:** Integrated Web Speech API allows users to dictate text via an animated microphone interface.
* **Smart Typography:** Automatically applies the elegant *Noto Nastaliq* web font when Urdu or Arabic is selected.
* **Local History Storage:** Automatically saves and displays recent translations using browser `localStorage`.
* **Dark/Light Mode:** Professional toggle with rotating SVG icon animations and persistent theme memory.
* **Copy to Clipboard:** One-click copy functionality for translated text.
* **Clear the text:** Clear both user input and translated output.

## Tech Stack
* **Frontend:** HTML5, CSS3 (Custom Variables, Flexbox/Grid), Vanilla JavaScript
* **Backend:** Python, Flask
* **API:** MyMemory Translation API

## Project Structure
```text
language-translator/
├── app.py              # Flask backend routing and API logic
├── requirements.txt    # Python dependencies
├── .env                # Environment variables (API Keys - Not included in repo)
├── .gitignore          # Git ignore rules
├── templates/
│   └── index.html      # Frontend user interface
└── static/
    ├── style.css       # Custom CSS styling and animations
    └── script.js       # Frontend logic, API calls, and local storage