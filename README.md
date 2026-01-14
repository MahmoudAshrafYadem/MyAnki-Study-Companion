# MyAnki Study Companion

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-6.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A powerful PyQt6-based desktop study companion application designed to enhance your learning experience through three interactive modes: **Flashcards**, **Practice MCQs**, and **Exam Simulator**.

## 📋 Table of Contents
- [Features](#features)
- [Installation](#installation)
- [How to Use](#how-to-use)
- [File Format Requirements](#file-format-requirements)
- [Application Modes](#application-modes)
- [AI Prompt Template](#ai-prompt-template)
- [Screenshots](#screenshots)
- [Requirements](#requirements)
- [Contributing](#contributing)

## ✨ Features

### 🎴 Flashcard Mode
- Interactive flashcard review system
- Front/Back card flipping
- Navigation controls (Previous/Next)
- PDF export functionality
- Clean, distraction-free interface

### 📝 Practice MCQ Mode
- Multiple-choice question practice
- Instant visual feedback with correct answer highlighting
- Progress tracking through questions
- PDF export for offline review

### 🎯 Exam Simulator Mode
- Timed exam environment with countdown timer
- Comprehensive scoring system
- No answer feedback during exam (realistic testing)
- Final score report with statistics
- PDF export for exam review

### 🎨 Additional Features
- **Full-screen mode** for focused studying (Press ESC to toggle)
- **Beautiful UI** with custom styling and color-coded modes
- **PDF Export** for all modes to save your study sessions
- **Keyboard shortcuts** for efficient navigation

---

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Step 1: Clone the Repository
```bash
git clone https://github.com/MahmoudAshrafYadem/MyAnki-Study-Companion.git
cd MyAnki-Study-Companion
```

### Step 2: Install Dependencies
```bash
pip install PyQt6 reportlab
```

### Step 3: Run the Application
```bash
python MyAnki.py
```

---

## 📖 How to Use

### Starting the Application

1. **Launch MyAnki**:
   ```bash
   python MyAnki.py
   ```

2. **Full-Screen Mode**: The application starts in full-screen mode by default. Press `ESC` to toggle between full-screen and windowed mode.

3. **Select Your Study Mode**: On the home screen, you'll see three book-style buttons:
   - 🟢 **Flashcards Collection** (Green)
   - 🟠 **Practice MCQs Workbook** (Orange)
   - 🔴 **Final Exam Simulator** (Red)

### Using Flashcard Mode

1. Click **"Flashcards Collection"**
2. Select your `.txt` file containing flashcard data
3. **Navigation**:
   - Click **"Flip Card"** to reveal the answer
   - Use **"Next"** and **"Prev"** buttons to navigate
   - Click **"Save PDF"** to export your flashcards
   - Click **"Home"** to return to the main menu

### Using Practice MCQ Mode

1. Click **"Practice MCQs Workbook"**
2. Select your `.txt` file containing MCQ data
3. **How it works**:
   - Questions are displayed with 4 options (A, B, C, D)
   - **Correct answers are highlighted in green** for immediate feedback
   - Select your answer by clicking the radio button
   - Use **"Next"** and **"Prev"** to navigate through questions
   - Click **"Export PDF"** to save the question set
   - Click **"Home"** when finished

### Using Exam Simulator Mode

1. Click **"Final Exam Simulator"**
2. Select your `.txt` file containing exam questions
3. **Set Exam Duration**: Enter the time limit in minutes (default: 30 minutes)
4. **Taking the Exam**:
   - A countdown timer appears at the top (in red)
   - Select your answers for each question
   - Navigate using **"Next"** and **"Prev"** buttons
   - **No correct answers are shown** during the exam
   - Click **"Submit"** when finished or time runs out
5. **View Results**: Your score is displayed as a ratio (e.g., "Score: 15/20")

---

## 📄 File Format Requirements

### Flashcard File Format (`.txt`)

Your flashcard file must follow this exact format:

```
Card 1
Front: What is the capital of Egypt?
Back: Cairo

Card 2
Front: What does PyQt6 stand for?
Back: Python bindings for Qt version 6

Card 3
Front: What is the speed of light?
Back: 299,792,458 meters per second
```

**Important Rules**:
- Each card must start with `Front:` followed by the question
- Next line must have `Back:` followed by the answer
- Leave one blank line between cards
- Minimum 50 cards recommended for best experience

### MCQ/Exam File Format (`.txt`)

Your MCQ file must follow this format:

```
Answer Key:
1B2C3A4B5D6C7B8A9B10C

1. What is the standard chip rate for a 3G W-CDMA system?
A. 1.25 Mcps
B. 3.84 Mcps
C. 5.00 Mcps
D. 200 Kcps

2. Which interface is defined between the Node B and RNC?
A. Uu
B. Iur
C. Iub
D. Iu-PS

3. What is the carrier bandwidth for UMTS?
A. 5 MHz
B. 200 KHz
C. 1.25 MHz
D. 10 MHz
```

**Important Rules**:
- **First line** must be the answer key in format: `1B2C3A4B5D...` (no spaces)
- Questions numbered as `1.`, `2.`, `3.`, etc.
- Options must be `A.`, `B.`, `C.`, `D.` (uppercase with period)
- Leave one blank line between questions
- Minimum 50 questions recommended

---

## 🤖 AI Prompt Template

Included in this repository is **`MyAnki-Promptet.txt`** - a comprehensive AI prompt template that you can use with ChatGPT, Claude, or other AI assistants to generate properly formatted content files.

### How to Use the Prompt Template:

1. Open `MyAnki-Promptet.txt`
2. Copy the prompt for your desired mode:
   - **MODE 1**: Flashcard generation
   - **MODE 2**: Practice MCQ generation  
   - **MODE 3**: Exam question generation
3. Paste it into your AI chatbot
4. Provide your study content/topic
5. The AI will generate properly formatted output
6. Save the output as a `.txt` file
7. Use it with MyAnki!

**Example Usage**:
```
[Paste MODE 1 prompt]

CONTENT: Generate flashcards about 5G NR Physical Layer procedures
```

The AI will generate 50+ flashcards in the correct format automatically!

---

## 🎮 Application Modes Comparison

| Feature | Flashcards | Practice MCQs | Exam Simulator |
|---------|-----------|--------------|----------------|
| **Purpose** | Memorization | Practice with feedback | Realistic testing |
| **Answer Visibility** | On flip | Always visible | Only after submit |
| **Timer** | ❌ | ❌ | ✅ |
| **Scoring** | ❌ | ❌ | ✅ |
| **Navigation** | Prev/Next | Prev/Next | Prev/Next |
| **PDF Export** | ✅ | ✅ | ✅ |
| **Best For** | Learning new material | Self-assessment | Exam preparation |

---

## 💻 Requirements

```txt
Python >= 3.7
PyQt6 >= 6.0.0
reportlab >= 3.6.0
```

Install all requirements:
```bash
pip install -r requirements.txt
```

---

## 🎯 Tips for Best Experience

1. **Prepare your content files in advance** using the AI prompt template
2. **Start with Practice MCQ mode** before attempting Exam mode
3. **Use full-screen mode** (F11 or default) for distraction-free studying
4. **Export to PDF** to review your questions offline or on mobile devices
5. **Create topic-specific files** for focused study sessions
6. **Use realistic exam durations** in Exam mode (e.g., 60-90 minutes)

---

## 🐛 Troubleshooting

### File Upload Error (>25MB)
If your `.rar` file is too large for GitHub:
- **Solution 1**: Use [Git LFS](https://git-lfs.github.com/) for large files
- **Solution 2**: Upload to Google Drive/Dropbox and share the link
- **Solution 3**: Split the content into smaller topic-based files

### Application Won't Start
```bash
# Ensure PyQt6 is installed
pip install --upgrade PyQt6

# Check Python version
python --version  # Should be 3.7+
```

### File Format Errors
- Verify your file follows the exact format shown in [File Format Requirements](#file-format-requirements)
- Use the AI prompt template to auto-generate correctly formatted files
- Check for missing blank lines between questions/cards

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

---

## 📝 License

This project is open-source and available under the MIT License.

---

## 👨‍💻 Author

**Made by Mahmoud Yadem**

Telecommunications Engineering Student | ITI Telco Cloud Trainee

---

## ⭐ Support

If you find this project helpful, please give it a ⭐ on GitHub!

---

**Happy Studying! 📚✨**
