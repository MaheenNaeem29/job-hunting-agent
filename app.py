"""
CareerPrep Job-Hunting Agent
============================
A file-driven agent that reads job posters, resumes, and knowledge base
notes to generate skill-gap reports, resume suggestions, interview
questions, and application reminders.

Usage:
    python app.py
"""

import os
import csv
from datetime import datetime, date

import pdfplumber

# ─────────────────────────────────────────────
#  CONFIGURATION
# ─────────────────────────────────────────────

JOB_DIR     = "input_jobs"
RESUME_DIR  = "input_resumes"
KB_DIR      = "input_kb"
OUTPUT_DIR  = "outputs"
TRACKER_DIR = "tracker"

DIVIDER  = "=" * 55
DIVIDER2 = "-" * 55

KEYWORDS = [
    "python", "machine learning", "data preprocessing", "github", "git",
    "sql", "communication", "problem solving", "oop", "database",
    "pandas", "numpy", "deep learning", "html", "css", "flask",
    "streamlit", "jupyter", "api", "prompt engineering", "nlp",
    "tensorflow", "scikit-learn", "data analysis", "excel", "power bi",
    "leadership", "teamwork", "time management", "critical thinking",
]


# ─────────────────────────────────────────────
#  UTILITY FUNCTIONS
# ─────────────────────────────────────────────

def ensure_folders():
    """Create required directories if they don't exist."""
    for folder in [JOB_DIR, RESUME_DIR, KB_DIR, OUTPUT_DIR, TRACKER_DIR]:
        os.makedirs(folder, exist_ok=True)


def read_text_files(folder: str) -> tuple[str, int]:
    """
    Read all .txt and .pdf files from a folder and return combined text + count.
    """
    combined = ""
    count = 0
    for filename in sorted(os.listdir(folder)):
        filepath = os.path.join(folder, filename)
        if filename.lower().endswith(".txt"):
            with open(filepath, "r", encoding="utf-8") as f:
                combined += f"\n\n{'─'*40}\n FILE: {filename}\n{'─'*40}\n"
                combined += f.read()
            count += 1
        elif filename.lower().endswith(".pdf"):
            try:
                with pdfplumber.open(filepath) as pdf:
                    combined += f"\n\n{'─'*40}\n FILE: {filename}\n{'─'*40}\n"
                    for page in pdf.pages:
                        text = page.extract_text() or ""
                        combined += text + "\n"
                count += 1
            except Exception as e:
                print(f"  [WARNING] Could not read PDF file: {filename} ({e})")
    return combined, count


def save_text(path: str, content: str):
    """Save string content to a text file."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  [SAVED] {path}")


def extract_keywords(text: str) -> list[str]:
    """Extract matching keywords from text (case-insensitive)."""
    text_lower = text.lower()
    return [kw for kw in KEYWORDS if kw in text_lower]


def compare_skills(job_skills: list, resume_skills: list) -> tuple:
    """Return matched skills, missing skills, and match percentage."""
    matched = [s for s in job_skills if s in resume_skills]
    missing = [s for s in job_skills if s not in resume_skills]
    score   = round((len(matched) / len(job_skills)) * 100, 1) if job_skills else 0.0
    return matched, missing, score


def header(title: str) -> str:
    """Return a formatted section header string."""
    return f"\n{DIVIDER}\n  {title.upper()}\n{DIVIDER}\n"


# ─────────────────────────────────────────────
#  REPORT GENERATORS
# ─────────────────────────────────────────────

def generate_job_analysis(job_text: str, job_skills: list) -> str:
    report  = header("Job Analysis Report")
    report += f"Generated : {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
    report += f"Total skills/keywords found in job posters: {len(job_skills)}\n\n"
    report += "Detected Skills & Keywords:\n"
    for i, skill in enumerate(job_skills, 1):
        report += f"  {i:>2}. {skill}\n"
    return report


def generate_skill_gap_report(
    job_skills: list, resume_skills: list,
    matched: list, missing: list, score: float
) -> str:
    report  = header("Skill Gap Report")
    report += f"Generated : {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"

    filled = int(score / 5)
    bar    = "█" * filled + "░" * (20 - filled)
    report += f"Match Score : {score}%\n"
    report += f"Progress    : [{bar}]\n\n"

    report += f"{'─'*30}\n"
    report += f"  Matched Skills ({len(matched)}) ✔\n"
    report += f"{'─'*30}\n"
    for s in matched:
        report += f"  + {s}\n"

    report += f"\n{'─'*30}\n"
    report += f"  Missing Skills ({len(missing)}) ✘\n"
    report += f"{'─'*30}\n"
    for s in missing:
        report += f"  - {s}\n"

    report += f"\n{'━'*55}\n"
    report += "SUMMARY\n"
    report += f"{'━'*55}\n"
    report += f"  Total Job Skills Required : {len(job_skills)}\n"
    report += f"  Skills You Already Have   : {len(matched)}\n"
    report += f"  Skills You Are Missing    : {len(missing)}\n"
    report += f"  Your Match Score          : {score}%\n"
    if score >= 70:
        recommendation = "Apply"
    elif score >= 40:
        recommendation = "Improve first"
    else:
        recommendation = "More prep needed"
    report += f"  Recommendation            : {recommendation}\n"

    return report


def generate_resume_suggestions(job_skills: list, missing: list) -> str:
    output  = header("Tailored Resume Suggestions")
    output += f"Generated : {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"

    output += "Recommended Resume Improvements:\n"
    output += f"{'─'*40}\n"
    for skill in job_skills:
        output += f"  • Add strong evidence of '{skill}' in your resume.\n"

    output += "\nSuggested Resume Bullet Points:\n"
    output += f"{'─'*40}\n"
    output += "  • Developed Python-based projects with clean, documented code.\n"
    output += "  • Managed source code using Git and GitHub with regular commits.\n"
    output += "  • Applied data analysis techniques using pandas and NumPy.\n"
    output += "  • Solved real-world problems through structured thinking.\n"
    output += "  • Collaborated in team environments and delivered on deadlines.\n"

    if missing:
        output += f"\nPriority Skills to Learn Before Applying:\n"
        output += f"{'─'*40}\n"
        for skill in missing:
            output += f"  ⚠  {skill}\n"

    return output


def generate_interview_questions(job_skills: list, kb_text: str) -> str:
    questions  = header("Interview Preparation Questions")
    questions += f"Generated : {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"

    questions += "Technical Questions (based on job requirements):\n"
    questions += f"{'─'*40}\n"
    for skill in job_skills:
        questions += f"  Q: What is {skill}? Describe how you have used it.\n"
        questions += f"  Q: Give an example project where you applied {skill}.\n\n"

    questions += "HR & Behavioural Questions:\n"
    questions += f"{'─'*40}\n"
    hr_qs = [
        "Tell me about yourself.",
        "Why are you interested in this role?",
        "What is your greatest strength and weakness?",
        "Describe a challenge you faced and how you resolved it.",
        "Where do you see yourself in 3 years?",
        "Why should we select you over other candidates?",
    ]
    for q in hr_qs:
        questions += f"  Q: {q}\n"

    questions += "\nQuestions from Knowledge Base / Course Notes:\n"
    questions += f"{'─'*40}\n"
    kb_lines = [l.strip() for l in kb_text.splitlines() if l.strip() and not l.startswith("─") and not l.startswith("FILE")]
    for line in kb_lines[:8]:
        questions += f"  Q: How would you explain this concept in an interview?\n"
        questions += f"     → \"{line[:90]}\"\n\n"

    return questions


def generate_preparation_plan(matched: list, missing: list, score: float) -> str:
    plan  = header("Interview Preparation Plan")
    plan += f"Generated : {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"

    plan += "Week 1 — Foundation Review:\n"
    plan += f"{'─'*40}\n"
    for skill in matched[:5]:
        plan += f"  • Revise and strengthen: {skill}\n"

    plan += "\nWeek 2 — Gap Filling:\n"
    plan += f"{'─'*40}\n"
    for skill in missing[:5]:
        plan += f"  • Learn / improve: {skill}\n"

    plan += "\nWeek 3 — Practice:\n"
    plan += f"{'─'*40}\n"
    plan += "  • Practice mock interviews with a friend.\n"
    plan += "  • Prepare 2-minute project explanations.\n"
    plan += "  • Review your resume line-by-line.\n"
    plan += "  • Prepare questions to ask the interviewer.\n"

    plan += f"\nCurrent Readiness Score: {score}%\n"
    plan += "Target Score Before Applying: 70%+\n"

    return plan


# ─────────────────────────────────────────────
#  TRACKER & REMINDERS
# ─────────────────────────────────────────────

def create_or_update_tracker():
    """Create applications.csv with sample data if it doesn't exist."""
    path = os.path.join(TRACKER_DIR, "applications.csv")
    if not os.path.exists(path):
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "application_id", "company", "role", "source", "status",
                "applied_date", "interview_date", "follow_up_date",
                "next_action", "notes"
            ])
            writer.writerow([
                "APP-001", "ABC Tech", "Junior AI Engineer Intern",
                "LinkedIn", "Interview Scheduled",
                "2026-04-28", "2026-05-03", "2026-05-06",
                "Revise Python, ML basics, explain projects",
                "Resume tailored and submitted"
            ])
            writer.writerow([
                "APP-002", "XYZ Solutions", "Data Analyst Intern",
                "Rozee.pk", "Applied",
                "2026-04-27", "", "2026-05-04",
                "Follow up if no response by May 4",
                "Cover letter included"
            ])
            writer.writerow([
                "APP-003", "DataVision", "ML Research Intern",
                "Company Website", "Not Applied",
                "", "", "",
                "Tailor resume and apply this week",
                "Strong ML focus — good fit"
            ])
    return path


def generate_reminders() -> str:
    tracker_path = os.path.join(TRACKER_DIR, "applications.csv")
    if not os.path.exists(tracker_path):
        header_text = (
            "╔" + "═"*54 + "╗\n"
            "║         APPLICATION REMINDERS & ACTION PLAN          ║\n"
            "╚" + "═"*54 + "╝\n"
            f"Generated : {datetime.now().strftime('%Y-%m-%d')}\n\n"
        )
        return header_text + "No tracker file found. Run agent first.\n"

    today = date.today()
    urgent, applied_items, pending = [], [], []
    counts = {"interview scheduled": 0, "applied": 0, "not applied": 0}
    LINE = "━" * 55

    with open(tracker_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            aid      = row.get("application_id", "")
            company  = row.get("company", "")
            role     = row.get("role", "")
            status   = row.get("status", "").strip().lower()
            idate    = row.get("interview_date", "").strip()
            adate    = row.get("applied_date", "").strip()
            fdate    = row.get("follow_up_date", "").strip()
            action   = row.get("next_action", "").strip()

            if status == "interview scheduled":
                counts[status] += 1
                days_away = ""
                if idate:
                    try:
                        diff = (date.fromisoformat(idate) - today).days
                        days_away = f"  ({diff} days away)" if diff >= 0 else "  (Date passed)"
                    except ValueError:
                        days_away = ""
                if "explain projects" in action.lower() and "clearly" not in action.lower():
                    action = action.rstrip(". ") + " clearly"
                tips = f"Practice 2-minute project explanation. Research {company}."
                urgent.append(
                    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    "⚡ URGENT — INTERVIEW SCHEDULED\n"
                    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"  Application ID  : {aid}\n"
                    f"  Company         : {company}\n"
                    f"  Role            : {role}\n"
                    f"  Interview Date  : {idate}{days_away}\n"
                    f"  Follow-up Date  : {fdate}\n"
                    f"  Next Action     : {action}\n"
                    f"  Tips            : {tips}\n"
                )

            elif status == "applied":
                counts[status] += 1
                next_action = action
                if fdate:
                    next_action = f"Send a polite follow-up email if no response by {fdate}"
                applied_items.append(
                    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    "📋 APPLIED — AWAITING RESPONSE\n"
                    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"  Application ID  : {aid}\n"
                    f"  Company         : {company}\n"
                    f"  Role            : {role}\n"
                    f"  Applied Date    : {adate}\n"
                    f"  Follow-up Date  : {fdate}\n"
                    f"  Next Action     : {next_action}\n"
                )

            elif status == "not applied":
                counts[status] += 1
                action_text = action
                if "tailor resume" in action.lower():
                    if "ml" in role.lower():
                        action_text = "Tailor resume for ML role and apply this week"
                pending.append(
                    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    "📌 PENDING — NOT APPLIED YET\n"
                    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"  Application ID  : {aid}\n"
                    f"  Company         : {company}\n"
                    f"  Role            : {role}\n"
                    f"  Next Action     : {action_text}\n"
                )

    total_apps = sum(counts.values())
    reminders = (
        "╔" + "═"*54 + "╗\n"
        "║         APPLICATION REMINDERS & ACTION PLAN          ║\n"
        "╚" + "═"*54 + "╝\n"
        f"Generated : {datetime.now().strftime('%Y-%m-%d')}\n"
        f"Total Applications Tracked : {total_apps}\n\n"
    )

    reminders += "".join(urgent)
    reminders += "".join(applied_items)
    reminders += "".join(pending)
    reminders += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    reminders += "SUMMARY\n"
    reminders += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    reminders += f"  Interview Scheduled : {counts['interview scheduled']}\n"
    reminders += f"  Applied             : {counts['applied']}\n"
    reminders += f"  Not Applied         : {counts['not applied']}\n"
    reminders += f"  Total               : {total_apps}\n"

    return reminders


# ─────────────────────────────────────────────
#  MAIN AGENT
# ─────────────────────────────────────────────

def print_banner():
    print("\n" + "=" * 55)
    print("   CareerPrep Job-Hunting Agent")
    print("   Agentic AI Lab — File-Driven Workflow")
    print("=" * 55)


def run_agent():
    print_banner()
    ensure_folders()

    # ── Read all input files ──────────────────────────────
    print("\n[1/5] Reading input files...")
    job_text,    job_count    = read_text_files(JOB_DIR)
    resume_text, resume_count = read_text_files(RESUME_DIR)
    kb_text,     kb_count     = read_text_files(KB_DIR)

    print(f"  Job posters   : {job_count} file(s)")
    print(f"  Resume files  : {resume_count} file(s)")
    print(f"  KB files      : {kb_count} file(s)")

    if job_count == 0 or resume_count == 0 or kb_count == 0:
        print("\n[ERROR] Please add .txt files in all three input folders and re-run.")
        return

    # ── Analyse ───────────────────────────────────────────
    print("\n[2/5] Analysing skills and gaps...")
    job_skills    = extract_keywords(job_text)
    resume_skills = extract_keywords(resume_text)
    matched, missing, score = compare_skills(job_skills, resume_skills)
    print(f"  Job skills found   : {len(job_skills)}")
    print(f"  Matched skills     : {len(matched)}")
    print(f"  Missing skills     : {len(missing)}")
    print(f"  Match score        : {score}%")

    # ── Generate reports ──────────────────────────────────
    print("\n[3/5] Generating reports...")
    job_report   = generate_job_analysis(job_text, job_skills)
    gap_report   = generate_skill_gap_report(job_skills, resume_skills, matched, missing, score)
    suggestions  = generate_resume_suggestions(job_skills, missing)
    questions    = generate_interview_questions(job_skills, kb_text)
    plan         = generate_preparation_plan(matched, missing, score)

    # ── Tracker & reminders ───────────────────────────────
    print("\n[4/5] Updating tracker and reminders...")
    create_or_update_tracker()
    reminders = generate_reminders()
    # Inject skill summary into reminders output
    LINE = "━" * 55
    if score >= 70:
        recommendation = "Apply with confidence!"
    elif score >= 40:
        recommendation = "Improve missing skills first, then apply."
    else:
        recommendation = "More preparation needed before applying."
    skill_block  = f"\n{LINE}\n"
    skill_block += "SKILL MATCH SUMMARY\n"
    skill_block += f"{LINE}\n"
    skill_block += f"  Total Job Skills Required : {len(job_skills)}\n"
    skill_block += f"  Skills You Already Have   : {len(matched)}\n"
    skill_block += f"  Skills You Are Missing    : {len(missing)}\n"
    skill_block += f"  Your Match Score          : {score}%\n"
    skill_block += f"  Recommendation            : {recommendation}\n"
    reminders += skill_block

    # ── Save all outputs ──────────────────────────────────
    print("\n[5/5] Saving outputs...")
    save_text(os.path.join(OUTPUT_DIR, "job_analysis_report.txt"),        job_report)
    save_text(os.path.join(OUTPUT_DIR, "skill_gap_report.txt"),           gap_report)
    save_text(os.path.join(OUTPUT_DIR, "tailored_resume_suggestions.txt"),suggestions)
    save_text(os.path.join(OUTPUT_DIR, "interview_questions.txt"),        questions)
    save_text(os.path.join(OUTPUT_DIR, "preparation_plan.txt"),           plan)
    save_text(os.path.join(TRACKER_DIR, "reminders.txt"),                 reminders)

    # Final combined report
    final  = f"CAREEPREP JOB-HUNTING AGENT — FULL REPORT\n"
    final += f"Generated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    final += DIVIDER + "\n"
    final += job_report + gap_report + suggestions + questions + plan + reminders
    save_text(os.path.join(OUTPUT_DIR, "final_agent_report.txt"), final)

    # ── Summary ───────────────────────────────────────────
    print("\n" + DIVIDER)
    print("  AGENT COMPLETE")
    print(DIVIDER)
    print(gap_report)
    print(reminders)
    print(f"All files saved in '{OUTPUT_DIR}/' and '{TRACKER_DIR}/'")
    print(DIVIDER + "\n")


if __name__ == "__main__":
    run_agent()
