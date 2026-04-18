# 🩺 醫師二階國考複習平台

A web-based review platform for Taiwan's Physician Licensing Examination (Stage 2), covering nearly 10 years of past exam questions across multiple subjects.

🔗 **[Open the website](https://fred901229.github.io/medical-exam-review_for_Taiwan_MedStudents/)**

---

## Features

- 📚 Nearly 10 years of past exam questions — 醫學(三)(四)(五)(六)，共 6720 題
- 🔍 Filter by year, session, and subject
- 🔎 Full-text keyword search
- 🎲 Quiz mode — select a number of questions, answer them, and get a summary report
- ✅ Click-to-answer with instant green / red feedback
- 🖼️ Image support for questions with figures
- 📊 Progress tracking — records correct / wrong answers across sessions (localStorage)
- 📕 Wrong answer book — filter to review only questions you got wrong
- 🌙 Dark mode
- 🔠 Adjustable font size
- 📱 Mobile-friendly responsive layout
- 🔄 Appeal-corrected answers clearly labeled (申覆更正)

---

## How to Use

1. Open the [website](https://fred901229.github.io/medical-exam-review_for_Taiwan_MedStudents/)
2. Use the sidebar to filter by year, session, subject, or answer status
3. Click a question card to expand it and select an answer
4. Enter a number and click **隨機出題** to start quiz mode
5. After finishing all quiz questions, a result summary appears automatically

---

## Tech Stack

- Python + pdfplumber (PDF parsing & image extraction)
- Vanilla HTML / CSS / JavaScript (no framework)
- GitHub Pages (static hosting)

---

*Created by Yu-Yuan Wu (KMU M109)*
