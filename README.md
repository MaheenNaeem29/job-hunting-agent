# CareerPrep Job-Hunting Agent

A file-driven AI agent that reads job posters, resumes, and knowledge-base
notes to generate skill-gap reports, resume tailoring suggestions, interview
questions, and application reminders.

---

## Project Structure

```
job-hunting-agent/
├── app.py                    ← Main agent (run this)
├── requirements.txt          ← Python dependencies
├── README.md                 ← This file
├── reflection.md             ← Reflection on what was built
│
├── input_jobs/               ← Paste job posters here (.txt)
│   └── job_poster_01.txt
│
├── input_resumes/            ← Paste your resume here (.txt)
│   └── my_resume.txt
│
├── input_kb/                 ← Paste course/interview notes here (.txt)
│   └── interview_notes.txt
│
├── outputs/                  ← Agent saves all reports here
│   ├── job_analysis_report.txt
│   ├── skill_gap_report.txt
│   ├── tailored_resume_suggestions.txt
│   ├── interview_questions.txt
│   ├── preparation_plan.txt
│   └── final_agent_report.txt
│
├── tracker/                  ← Application tracker files
│   ├── applications.csv
│   └── reminders.txt
│
└── samples/                  ← Sample input files for testing
    ├── sample_job_poster.txt
    ├── sample_resume.txt
    └── sample_kb.txt
```

---

## Setup & Run

### Step 1 — Install Python
Make sure Python 3.10 or higher is installed.

```bash
python --version
```

### Step 2 — Install dependencies

```bash
pip install -r requirements.txt
```

> **Note:** The basic version uses only Python standard library — no extra
> packages are needed unless you enable PDF reading.

### Step 3 — Add your input files

| Folder | What to put there |
|---|---|
| `input_jobs/` | Copy job posters from LinkedIn / Rozee as `.txt` files |
| `input_resumes/` | Paste your resume as `my_resume.txt` |
| `input_kb/` | Paste course slides or interview notes as `.txt` files |

### Step 4 — Run the agent

```bash
python app.py
```

---

## Output Files

| File | Description |
|---|---|
| `outputs/job_analysis_report.txt` | Skills found in job posters |
| `outputs/skill_gap_report.txt` | Match score + missing skills |
| `outputs/tailored_resume_suggestions.txt` | How to improve your resume |
| `outputs/interview_questions.txt` | Technical + HR questions |
| `outputs/preparation_plan.txt` | 3-week study plan |
| `outputs/final_agent_report.txt` | Complete combined report |
| `tracker/applications.csv` | Application status tracker |
| `tracker/reminders.txt` | Interview and follow-up reminders |

---

## Application Tracker Fields

Edit `tracker/applications.csv` directly to update your application statuses.

| Field | Example |
|---|---|
| application_id | APP-001 |
| company | ABC Tech |
| role | Junior AI Engineer Intern |
| source | LinkedIn / Rozee / Website |
| status | Not Applied / Applied / Interview Scheduled / Offered |
| applied_date | 2026-04-28 |
| interview_date | 2026-05-03 |
| follow_up_date | 2026-05-06 |
| next_action | Revise Python and ML basics |
| notes | Resume tailored for this role |

---

## Features

- Reads all `.txt` files from three input folders automatically
- Extracts and matches 30+ skill keywords
- Generates match score with a visual progress bar
- Creates tailored resume bullet points per job
- Generates technical, HR, and KB-based interview questions
- Builds a 3-week preparation plan
- Tracks application status with urgency-based reminders
- Saves all outputs as clean text reports

---

## Author

Student Name: ___________________
Roll Number: ___________________
Course: Agentic AI Lab
