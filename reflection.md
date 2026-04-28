# Reflection — CareerPrep Job-Hunting Agent

## What I Built

A file-driven Job-Hunting Agent in Python that follows the GAME framework:

- **Goal:** Help a student manage their job search from one place.
- **Actions:** Read files → extract skills → compare → generate reports → track applications.
- **Memory:** Input files, generated reports, and the CSV tracker persist between runs.
- **Environment:** Local folders and text files, GitHub for submission.

The agent reads job posters, resumes, and course notes from three input folders,
then generates six output files covering job analysis, skill gaps, resume tailoring,
interview questions, a preparation plan, and application reminders.

---

## What I Tested

1. Added sample job poster, resume, and KB file.
2. Ran `python app.py` and verified all outputs appeared in `outputs/` and `tracker/`.
3. Checked that the match score changed correctly when I added or removed skills.
4. Verified that reminders reflected different statuses in `applications.csv`.

---

## Challenges

- **Keyword matching is simple:** The agent uses exact string matching, which
  misses variations like "ML" vs "machine learning". A proper NLP approach
  or LLM API would handle this better.
- **No PDF support in basic version:** Job posters and resumes often come as PDFs.
  Adding `pdfplumber` would significantly improve real-world usefulness.

---

## What I Would Improve

- Integrate the Anthropic API to generate smarter, context-aware suggestions.
- Add a Streamlit dashboard for a visual interface.
- Support PDF and DOCX file reading.
- Add urgency levels (overdue, today, this week) to reminders.
- Auto-generate cover letters tailored to each job poster.

---

## Tools Used

- Python 3 (standard library only: os, csv, datetime)
- VS Code
- GitHub for version control

---

## Declaration

I built and tested this agent myself and understand all the submitted code.

Student Name  : _____Maheen Naeem______________
Roll Number   : ___________22f-3145________
Date          : _________4/28/2026__________
