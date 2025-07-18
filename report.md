# 🗂️ Internship Project Report

## 📌 Project Title: Indian Recipe Vault

*A culturally inclusive, AI-powered application that collects and preserves traditional Indian recipes in regional languages.*

---

## 👥 Team Information

| Name              | Role                                       |
|-------------------|--------------------------------------------|
| Naguboyina Dheeraj| Full Stack Developer, AI Integration       |
| Phani  Shashidhar | UI/UX Design & Frontend                    |
| phani Shashidhar  | Data Engineering & Processing              |
| Sai Kiran         | Whisper/NLLB Model Integration             |
| Charan            | NLP Tagging & Recipe Categorization        |
| Mohit             | Backend Scripting & File Management        |
| Naguboyina Dheeraj| Testing & QA, Feedback Collection          |

---

## 1.2 Application Overview

**Indian Recipe Vault** is a lightweight, AI-powered platform designed to digitally preserve Indian regional recipes shared in various languages and dialects. The app accepts both text and audio inputs, automatically transcribes them (if audio), translates regional languages, tags key entities (like ingredients, region, and cuisine), and stores the recipes in structured, accessible formats.

### ✅ MVP Core Features:

- Input recipes via **text or voice**
- **Speech-to-text** for regional audio input using Whisper
- **Language detection** and **translation** using NLLB
- Tagging of **ingredients**, **cuisine**, and **region**
- Store and display recipes in **CSV/JSON**

---

## 1.3 AI Integration Details

| AI Model           | Purpose                                      |
|--------------------|----------------------------------------------|
| Whisper (OpenAI)   | Transcribe regional audio inputs              |
| NLLB (Meta AI)     | Translate from Indian languages to English    |
| IndicBERT/FastText | Detect and classify language of the input     |
| SpaCy (rule-based) | Extract ingredients, cooking terms, region    |

### 🔁 Flow:

1. User submits text or audio
2. Whisper transcribes (if audio)
3. Language is detected with IndicBERT
4. NLLB translates if needed
5. NLP engine tags and categorizes data
6. Recipe saved in structured format (CSV/JSON)

---

## 1.4 Technical Architecture & Development

### 🧱 Tech Stack

| Layer        | Tools / Libraries                        |
|--------------|-------------------------------------------|
| Frontend     | Streamlit                                 |
| Backend      | Python, NumPy, Pandas                     |
| AI           | Whisper, NLLB, SpaCy, IndicBERT           |
| Storage      | CSV, JSON (File-based)                    |
| Deployment   | Hugging Face Spaces (Streamlit container) |

### 📁 File-based Storage

- Recipes saved in `.csv` and `.json`
- Easy to backup, share, and analyze
- No external database required

---

## 1.5 User Testing & Feedback (Week 2)

### 👨‍👩‍👧‍👦 Test Group

- Total users: 10
- Age group: 30–70 years
- Languages tested: Telugu, Hindi, Marathi, Kannada, English
- Device: Mobile and Desktop

### 🧪 Testing Methodology

- Manual testing of form inputs and speech transcription
- Google Forms for structured feedback
- Verbal feedback from family and local testers

### 📝 Key Scenarios Tested

| Test Case                      | Result                          |
|--------------------------------|----------------------------------|
| Voice input in Telugu          | Whisper worked well              |
| Mixed Hindi-English recipe     | Minor issues, mostly accurate    |
| Marathi text input             | Translated correctly via NLLB    |
| Unclear elderly audio          | Some errors; feedback noted      |

### 💬 Feedback Summary

- "Easy to use even for elders"
- "Loved the ability to speak recipes"
- "Would like to upload photos or see dishes"
- "Add filters for regions like Telangana or Punjab"

### 🔧 Improvements Made

- Trimmed silence in audio before Whisper
- Added dropdowns for selecting region/language
- Better UI hints for older users

---

## 🔮 Future Roadmap

- 📱 Mobile PWA support (offline usage)
- 📷 Add support for image uploads (dish photos)
- 🔈 Text-to-speech for read-aloud cooking steps
- 🧠 Recommend similar recipes via ingredients
- 🌍 Build community features (like ‘recipe by grandma’ wall)

---




> "A recipe is a story passed down. With AI, we’re making sure it’s never forgotten."  
> — **Team Indian Recipe Vault 🇮🇳**
