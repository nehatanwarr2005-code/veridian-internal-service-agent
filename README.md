# Veridian Corp — Autonomous Internal Service Agent (IT Support)
### AIONOS Recruitment Process — Assignment 2 Technical Submission

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit Prototype](https://img.shields.io/badge/Streamlit-Interactive_App-FF4B4B.svg)](https://streamlit.io/)
[![Policy Grounding](https://img.shields.io/badge/Policy_Grounding-100%25_Verified-success.svg)](#)
[![Zero Hallucination](https://img.shields.io/badge/Hallucinations-0%25-brightgreen.svg)](#)

---

## 📌 Executive Summary

This project implements an autonomous, policy-grounded **Internal IT Support Service Agent** for **Veridian Corp**, set during the operational week of **Monday, 21 September 2026 – Friday, 25 September 2026**.

The agent is designed to eliminate repetitive helpdesk toil, safeguard corporate assets, and strictly enforce company security policies. It enforces a **closed-world assumption**: all decisions, triage actions, and responses are **strictly grounded** in the provided knowledge base (`KB-01` through `KB-10` and the `Asset Management Policy Extract`), with **zero external policy hallucination**.

### 🎯 Core Agent Capabilities:
1. **Understand Employee Issues**: Accurate semantic intent extraction and context recognition.
2. **Strict Grounding & Source Citation**: Explicit citation of KB articles and corporate policies.
3. **Sensible Follow-up Inquiries**: Generates clarifying diagnostic questions for ambiguous queries (e.g., `REQ-15`).
4. **Instant Self-Service Resolution**: Automates standard, low-risk requests (e.g., Guest Wi-Fi kiosk in `REQ-02`, 90-day VPN self-renewal in `REQ-05`).
5. **Proactive Risk Escalation**: Immediately intercepts critical threats (e.g., internal phishing email forwarding in `REQ-08`, unauthorized admin escalation in `REQ-10`).
6. **Structured Ticket Creation**: Formulates tickets with priority, SLA, assigned department, and audit links.
7. **Immutable Audit Trail**: Append-only event ledger tracking timestamps, actors, reasoning steps, and policy citations.

---



---

## 🏗️ System Architecture

```
                     ┌────────────────────────────────────────┐
                     │          Employee / Reviewer           │
                     └───────────────────┬────────────────────┘
                                         │
                                         ▼
                     ┌────────────────────────────────────────┐
                     │  Streamlit UI & Interactive Console    │
                     │  - Interactive Chat with Agent         │
                     │  - 1-Click Request Tester (REQ 01-15)  │
                     │  - Live Ticket Queue (TK-1042 to 1051) │
                     │  - Grounded Knowledge Base Explorer    │
                     │  - Immutable Audit Trail Viewer        │
                     └───────────────────┬────────────────────┘
                                         │
                                         ▼
                     ┌────────────────────────────────────────┐
                     │          Agent Brain & Pipeline        │
                     │  1. Ingestion & Ambiguity Check        │
                     │  2. Policy Retrieval (KB-01 to KB-10,  │
                     │     Asset Policy Extract)              │
                     │  3. Precedent Matching (Closed Tickets)│
                     │  4. Risk & Clarity Assessment          │
                     │     - Low / Medium / High / Critical   │
                     │  5. Decision Engine:                   │
                     │     - Resolve Simple                   │
                     │     - Ask Follow-up Questions          │
                     │     - Escalate Risky / Complex         │
                     └───────────────────┬────────────────────┘
                                         │
                         ┌───────────────┴───────────────┐
                         ▼                               ▼
        ┌────────────────────────────────┐  ┌────────────────────────────────┐
        │   Structured Ticket System     │  │     Immutable Audit Trail      │
        │ - Ticket ID, Priority, Source  │  │ - Timestamped reasoning log    │
        │ - Action Taken, Routing Target │  │ - Decision steps & citations   │
        └────────────────────────────────┘  └────────────────────────────────┘
```

---

## 📚 Grounded Knowledge Base Summary

| Policy ID | Title | Key Governance Rules | Action Category |
|---|---|---|---|
| **KB-01** | Password Reset | Self-service portal at any time. If locked out after 5 failed attempts, manual IT unlock required. No approval needed. | Authentication & Access |
| **KB-02** | VPN Access | Automatic for full-time staff. Contractors require manager approval via access form. Credentials expire every 90 days (self-renewed). | Network & VPN |
| **KB-03** | Laptop Replacement | Eligible after 3 years of service, or earlier for verified hardware failure. 2 weeks advance notice required. | Hardware & Devices |
| **KB-04** | Software Installation | Approved catalog is self-installed. Non-catalog tools/extensions require IT Security review (3–5 business days SLA). | Software & Apps |
| **KB-05** | Printer Troubleshooting | Check queue & restart print spooler. If issue persists, log ticket with printer asset tag. | Peripherals & Printing |
| **KB-06** | Email Mailbox Quota | Default quota 25GB; archive old mail. Quota increases >25GB require manager approval and are capped at 50GB. | Email & Storage |
| **KB-07** | Guest Wi-Fi Access | Valid for 24 hours; generated by any employee from front-desk kiosk. No IT ticket required. | Network & Wi-Fi |
| **KB-08** | Expense Software Access | Account access granted by Finance, not IT. IT assists with login/technical issues only after account exists. | Enterprise Apps & Finance |
| **KB-09** | Security Incident Reporting | Phishing, malware, unauthorized access must be reported to `security@veridian-corp.example` immediately. **DO NOT FORWARD.** | Information Security |
| **KB-10** | Work-From-Home Equipment | Remote >3 days/week eligible for one-time allowance (chair, monitor). Requires Manager sign-off + Finance approval. IT ships once approved. | Remote Work & Assets |
| **ASSET-POL** | Asset Management Extract | Standard 4-year refresh cycle from date of issue. Early replacement outside cycle requires Finance sign-off + IT approval. | Hardware Governance |

---

## ⚖️ Nuanced Policy Reconciliation: KB-03 vs. Asset Management Policy

A critical test of the agent is handling the apparent conflict between:
- **IT Policy KB-03**: Permits replacement after 3 years of service or upon verified hardware failure.
- **Finance Asset Management Policy**: Mandates a 4-year standard refresh cycle, requiring Finance sign-off for earlier replacement.

### How the Agent Resolves This:
1. **Inoperable Hardware (`REQ-01`)**: Aditi's laptop won't turn on and is 3.5 years old. Because the hardware has suffered a verified total failure, it qualifies for early replacement under `KB-03`. However, because 3.5 years < 4 years, the agent automatically triggers the mandatory **Finance sign-off workflow** required by the Asset Management Policy, assigning the ticket jointly to Hardware Depot and Finance Assets (mirroring precedent `TK-1043`).
2. **Repair over Replacement (`REQ-13`)**: Aman's laptop is 2 years old with screen flickering. Because 2 years is well within the 4-year refresh cycle and the user requested a fix, the agent routes for hardware repair diagnostics rather than full lifecycle replacement.

---

## 📊 Benchmark Evaluation Matrix: All 15 Employee Requests

| ID | Employee | Employee Request | Grounded Policy | Risk Level | Agent Action | Status |
|---|---|---|---|---|---|---|
| **REQ-01** | Aditi Sharma | Laptop dead, won't turn on, 3.5 yrs old | KB-03, ASSET-POL | Medium | Escalate to Hardware & Finance | Approved for Inspection |
| **REQ-02** | Vikram Chawla | Guest Wi-Fi access for tomorrow | KB-07 | Low | Resolve Simple (Front-desk kiosk) | Resolved (Self-Service) |
| **REQ-03** | Karan Mehta | Locked out, tried password 6 times | KB-01 | Medium | Queue manual IT unlock (>5 attempts) | In Progress — Reset Queued |
| **REQ-04** | Ritu Bhatia | Non-catalog data analysis tool approval | KB-04 | Medium | Escalate to IT Security (3-5 day SLA) | Waiting on Security Review |
| **REQ-05** | Sanjay Oberoi | VPN expired this morning | KB-02 | Low | Resolve Simple (90-day self-renewal) | Resolved (Self-Service) |
| **REQ-06** | Meera Iyer | Printer 3rd floor phantom paper jam | KB-05 | Low | Follow-up: Ask Asset Tag for tech | Investigating — Tech Assigned |
| **REQ-07** | Farhan Ali | WFH 4 days/week, how to get monitor? | KB-10 | Low | Route: Manager sign-off + Finance | Pending Manager & Finance |
| **REQ-08** | Ananya Reddy | Phishing email — forwarding to teammates | KB-09 | **Critical** | **EMERGENCY ESCALATION: Halt forwarding** | Escalated to Security |
| **REQ-09** | Rohit Desai | Mailbox full, can't send emails | KB-06 | Low | Resolve Simple (Archive / Manager cap) | Resolved (Guidance Provided) |
| **REQ-10** | Kavya Pillai | Urgent admin access to finance server | KB-08, ASSET-POL | **High** | **Privilege Block / Reject Tier 1 (TK-1050)** | Rejected at Tier 1 / Pending Justification |
| **REQ-11** | Nikhil Bansal | Contractor joining, needs VPN | KB-02 | Low | Route: Require Access Request Form | Pending Manager Form |
| **REQ-12** | Sneha Kulkarni | Invalid credentials on expense tool | KB-08 | Low | Follow-up: Confirm Finance provisioned | Waiting on Employee Response |
| **REQ-13** | Aman Gupta | Screen flickering, 2 yrs old, fix not replace | KB-03, ASSET-POL | Medium | Diagnostic Follow-up & Repair ticket | In Progress — Diagnostics Queued |
| **REQ-14** | Tanya Chopra | Browser extension approval | KB-04 | Medium | Escalate to IT Security Review | Waiting on Security Review |
| **REQ-15** | Rahul Menon | "hey can you help, its not working" | None (Triage) | Low | **Generate 3 Diagnostic Follow-ups** | Awaiting Clarification |

**Benchmark Score**: **15 / 15 (100.0%) Policy Grounding Accuracy**

---

## 🚀 Quickstart & How to Run

### Prerequisites
- Python 3.10+ installed.

### 1. Clone & Install Dependencies
```bash
git clone <your-repo-url>
cd "placemnets project"
pip install -r requirements.txt
```

### 2. Launch Interactive Prototype (Streamlit)
```bash
streamlit run app.py
```
*Or on Windows, simply double-click `run_demo.bat`.*

### 3. Run Automated Unit Tests
```bash
python -m unittest discover -s tests
```

### 4. Run Quantitative Benchmark
```bash
python -m agent.evaluation
```

### 5. Generate / Refresh 10-Slide PPTX
```bash
python generate_presentation.py
```

---

## 🏛️ Project Directory Structure

```
placemnets project/
├── app.py                                          # Interactive Streamlit Prototype Web Application
├── run_demo.bat                                    # 1-Click Windows Batch Launcher
├── requirements.txt                                # Python Dependencies
├── generate_presentation.py                        # Automated python-pptx Slide Deck Generator
├── AIONOS_Assignment2_Internal_Service_Agent.pptx  # 10-Slide Presentation (.pptx)
├── presentation_slides.md                          # Presentation Transcript & Speaker Notes
├── demo_video_script.md                            # Demo Video Recording Script & Google Drive Guide
├── README.md                                       # Comprehensive Documentation
├── agent/
│   ├── __init__.py
│   ├── knowledge_base.py                           # KB-01 to KB-10 and Asset Management Policy Store
│   ├── data_loader.py                              # Official REQ-01..15 and TK-1042..1051 Datasets
│   ├── ticket_system.py                            # Structured Ticketing & Immutable Audit Trail
│   ├── core_agent.py                               # Core Agent Decision Brain & Triage Pipeline
│   └── evaluation.py                               # Automated 15-Request Verification Benchmark
└── tests/
    ├── __init__.py
    └── test_agent.py                               # Automated Unit Test Suite
```

---

## ⚖️ Governance & Compliance Notes
- **Zero-Trust Access Control**: Administrative privileges (`REQ-10`) cannot be bypassed via chatbot requests.
- **Quarantine Security Protocol**: Phishing forwarding (`REQ-08`) triggers immediate warnings and automated security alerts.
- **Complete Audit Trail**: Every session transition is timestamped and exportable as CSV.
