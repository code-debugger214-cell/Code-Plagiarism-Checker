# Code Plagiarism Checker (Python & Flask)

## Project Description
The Code Plagiarism Checker is a web-based application developed using Python and Flask that detects plagiarism in source code. The system compares user-submitted code with a predefined local dataset and calculates similarity using multiple comparison techniques. It provides a clear plagiarism decision along with detailed similarity metrics.

This project is suitable for academic use, lab submissions, and mini-project demonstrations.

## Objectives
- Detect plagiarism in source code files
- Compare user code with multiple dataset programs
- Measure similarity using different algorithms
- Generate a plagiarism score and risk level
- Display results in a simple web interface
- Prevent server errors through proper validation

## Features
- Text-based similarity using difflib
- Token-based similarity analysis
- Line-by-line code comparison
- Variable renaming detection
- Control flow similarity detection
- Weighted match score calculation
- Plagiarism risk classification (LOW, MEDIUM, HIGH)
- User-friendly web interface
- Safe handling of empty datasets and invalid input

## Technologies Used
- Python 3
- Flask
- HTML, CSS, JavaScript

## Project Structure
plagiarism_checker_project/
├── plagiarism_api.py
├── dataset/
├── templates/
│   └── index.html
├── static/
│   └── style.css
└── README.md

## How to Run
1. Install Flask:
   pip install flask
2. Run the application:
   python3 plagiarism_api.py
3. Open browser:
   http://127.0.0.1:5000/

## How It Works
The user pastes code into the web interface. The frontend sends the code to the Flask backend using a POST request. The backend compares the code with dataset files, calculates similarity scores, and returns the plagiarism analysis, which is displayed on the webpage.


## Conclusion
This project demonstrates an effective approach to code plagiarism detection using Python and Flask with multiple similarity techniques and proper error handling.
"""

path = "/mnt/data/README.md"
with open(path, "w", encoding="utf-8") as f:
    f.write(readme_content)

path
