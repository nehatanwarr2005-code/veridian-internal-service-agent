"""
Data Loader Module for Veridian Corp IT Support Agent.
Loads official employee requests (REQ-01 to REQ-15) and ticket queue (TK-1042 to TK-1051).
"""

from typing import List, Dict, Any, Optional

EMPLOYEE_REQUESTS: List[Dict[str, Any]] = [
    {
        "id": "REQ-01",
        "employee": "Aditi Sharma",
        "email": "aditi.sharma@veridian-corp.example",
        "date_opened": "Mon 21 Sep",
        "request": "My laptop won’t turn on at all, it’s completely dead, had it about 3.5 years now.",
        "initial_action": "Not started",
        "expected_kb": ["KB-03", "ASSET-POL"],
        "category": "Hardware & Devices",
        "expected_action": "Escalate to Hardware inspection and Finance sign-off (3.5 yrs < 4 yrs standard cycle, but verified failure qualifies)"
    },
    {
        "id": "REQ-02",
        "employee": "Vikram Chawla",
        "email": "vikram.chawla@veridian-corp.example",
        "date_opened": "Mon 21 Sep",
        "request": "Can I get Wi-Fi access for a guest visiting our office tomorrow?",
        "initial_action": "Not started",
        "expected_kb": ["KB-07"],
        "category": "Network & Wi-Fi",
        "expected_action": "Resolve directly with self-service kiosk guidance (24h valid, no IT ticket required)"
    },
    {
        "id": "REQ-03",
        "employee": "Karan Mehta",
        "email": "karan.mehta@veridian-corp.example",
        "date_opened": "Mon 21 Sep",
        "request": "I’m locked out of my account, tried my password 6 times.",
        "initial_action": "In progress — reset queued",
        "expected_kb": ["KB-01"],
        "category": "Authentication & Access",
        "expected_action": "Queue manual IT unlock (lockout > 5 failed attempts, no approval required)"
    },
    {
        "id": "REQ-04",
        "employee": "Ritu Bhatia",
        "email": "ritu.bhatia@veridian-corp.example",
        "date_opened": "Tue 22 Sep",
        "request": "Need approval to install a data-analysis tool that’s not in the software catalog.",
        "initial_action": "Waiting on Security review",
        "expected_kb": ["KB-04"],
        "category": "Software & Applications",
        "expected_action": "Route ticket to IT Security review (3-5 business days SLA)"
    },
    {
        "id": "REQ-05",
        "employee": "Sanjay Oberoi",
        "email": "sanjay.oberoi@veridian-corp.example",
        "date_opened": "Tue 22 Sep",
        "request": "My VPN stopped working this morning, says credentials expired.",
        "initial_action": "Not started",
        "expected_kb": ["KB-02"],
        "category": "Network & VPN",
        "expected_action": "Resolve with 90-day credential renewal instructions for full-time employee"
    },
    {
        "id": "REQ-06",
        "employee": "Meera Iyer",
        "email": "meera.iyer@veridian-corp.example",
        "date_opened": "Tue 22 Sep",
        "request": "Printer on the 3rd floor keeps showing “paper jam” even though there’s no jam.",
        "initial_action": "Investigating — technician assigned",
        "expected_kb": ["KB-05"],
        "category": "Peripherals & Printing",
        "expected_action": "Follow troubleshooting steps (queue/spooler restart) and ask for printer asset tag for technician dispatch"
    },
    {
        "id": "REQ-07",
        "employee": "Farhan Ali",
        "email": "farhan.ali@veridian-corp.example",
        "date_opened": "Wed 23 Sep",
        "request": "I’ve started working from home 4 days a week, how do I get a monitor?",
        "initial_action": "Not started",
        "expected_kb": ["KB-10"],
        "category": "Remote Work & Assets",
        "expected_action": "Explain WFH equipment policy (>3 days eligible), instruct to obtain manager sign-off & Finance processing before IT ships"
    },
    {
        "id": "REQ-08",
        "employee": "Ananya Reddy",
        "email": "ananya.reddy@veridian-corp.example",
        "date_opened": "Wed 23 Sep",
        "request": "I think I got a phishing email asking for my login — forwarding it to a few teammates to check.",
        "initial_action": "Escalated to Security (auto-flagged)",
        "expected_kb": ["KB-09"],
        "category": "Information Security",
        "expected_action": "CRITICAL ALERT: Instruct employee to STOP forwarding immediately; escalate directly to security@veridian-corp.example"
    },
    {
        "id": "REQ-09",
        "employee": "Rohit Desai",
        "email": "rohit.desai@veridian-corp.example",
        "date_opened": "Wed 23 Sep",
        "request": "My mailbox is full and I can’t send emails.",
        "initial_action": "Not started",
        "expected_kb": ["KB-06"],
        "category": "Email & Collaboration",
        "expected_action": "Advise archiving old mail (default 25GB quota); explain >25GB requires manager approval up to 50GB cap"
    },
    {
        "id": "REQ-10",
        "employee": "Kavya Pillai",
        "email": "kavya.pillai@veridian-corp.example",
        "date_opened": "Wed 23 Sep",
        "request": "Can someone give me admin access to the finance reporting server? Need it urgently for month-end.",
        "initial_action": "Not started",
        "expected_kb": ["KB-08"],
        "category": "Enterprise Software & Finance",
        "expected_action": "Escalate/Reject unauthorized admin access; access granted solely by Finance, requires formal business justification"
    },
    {
        "id": "REQ-11",
        "employee": "Nikhil Bansal",
        "email": "nikhil.bansal@veridian-corp.example",
        "date_opened": "Thu 24 Sep",
        "request": "New contractor joining my team next week, they’ll need VPN access.",
        "initial_action": "Not started",
        "expected_kb": ["KB-02"],
        "category": "Network & VPN",
        "expected_action": "Clarify contractor policy: requires manager approval submitted via access request form"
    },
    {
        "id": "REQ-12",
        "employee": "Sneha Kulkarni",
        "email": "sneha.kulkarni@veridian-corp.example",
        "date_opened": "Thu 24 Sep",
        "request": "I can’t log into the expense tool, keeps saying invalid credentials.",
        "initial_action": "Waiting on employee response (asked for a screenshot, no reply yet)",
        "expected_kb": ["KB-08"],
        "category": "Enterprise Software & Finance",
        "expected_action": "Ask follow-up to confirm account exists with Finance; if account exists, assist with technical login"
    },
    {
        "id": "REQ-13",
        "employee": "Aman Gupta",
        "email": "aman.gupta@veridian-corp.example",
        "date_opened": "Thu 24 Sep",
        "request": "Laptop screen is flickering on and off, had it 2 years, might just need a fix not a replacement.",
        "initial_action": "Not started",
        "expected_kb": ["KB-03", "ASSET-POL"],
        "category": "Hardware & Devices",
        "expected_action": "Route for hardware repair diagnostics (under 3-yr KB-03 / 4-yr Asset Policy, fix preferred over replacement)"
    },
    {
        "id": "REQ-14",
        "employee": "Tanya Chopra",
        "email": "tanya.chopra@veridian-corp.example",
        "date_opened": "Fri 25 Sep",
        "request": "Requesting approval to install a browser extension for productivity tracking.",
        "initial_action": "Not started",
        "expected_kb": ["KB-04"],
        "category": "Software & Applications",
        "expected_action": "Log ticket and route to IT Security review (browser extensions require 3-5 business days review)"
    },
    {
        "id": "REQ-15",
        "employee": "Rahul Menon",
        "email": "rahul.menon@veridian-corp.example",
        "date_opened": "Fri 25 Sep",
        "request": "hey can you help, its not working",
        "initial_action": "Not started",
        "expected_kb": [],
        "category": "Unclear / Triage",
        "expected_action": "Ask sensible diagnostic follow-up questions: identify affected device, application, error message, and scope"
    }
]

TICKET_QUEUE_RECORDS: List[Dict[str, Any]] = [
    {
        "ticket_id": "TK-1042",
        "employee": "R. Verma",
        "issue_summary": "VPN credential expired",
        "status": "Resolved (closed)",
        "is_active": False,
        "precedent_note": "Self-renewed 90-day credentials per KB-02 policy."
    },
    {
        "ticket_id": "TK-1043",
        "employee": "S. Iyer",
        "issue_summary": "Laptop replacement (3.2 yrs old)",
        "status": "Approved — pending fulfillment (active)",
        "is_active": True,
        "precedent_note": "Hardware age > 3 yrs met KB-03 criteria; Finance approved exception to 4-yr refresh cycle."
    },
    {
        "ticket_id": "TK-1044",
        "employee": "A. Khan",
        "issue_summary": "Non-catalog software request",
        "status": "Pending Security review (active)",
        "is_active": True,
        "precedent_note": "Under IT Security review SLA (3-5 business days) per KB-04."
    },
    {
        "ticket_id": "TK-1045",
        "employee": "P. Joshi",
        "issue_summary": "Mailbox quota increase",
        "status": "Approved at 35GB (closed)",
        "is_active": False,
        "precedent_note": "Approved with manager sign-off below 50GB cap per KB-06."
    },
    {
        "ticket_id": "TK-1046",
        "employee": "M. Das",
        "issue_summary": "Printer paper jam, floor 2",
        "status": "Resolved (closed)",
        "is_active": False,
        "precedent_note": "Spooler restarted and physical feeder cleared per KB-05."
    },
    {
        "ticket_id": "TK-1047",
        "employee": "K. Singh",
        "issue_summary": "Home office equipment request",
        "status": "Pending Finance (active)",
        "is_active": True,
        "precedent_note": "Manager sign-off received, awaiting Finance processing per KB-10."
    },
    {
        "ticket_id": "TK-1048",
        "employee": "T. Rao",
        "issue_summary": "Phishing email reported",
        "status": "Escalated to Security — under investigation (active)",
        "is_active": True,
        "precedent_note": "Reported to security@veridian-corp.example per KB-09; sender domain blocked."
    },
    {
        "ticket_id": "TK-1049",
        "employee": "V. Nambiar",
        "issue_summary": "Password reset",
        "status": "Resolved (closed)",
        "is_active": False,
        "precedent_note": "Account unlocked manually by IT after 5 failed attempts per KB-01."
    },
    {
        "ticket_id": "TK-1050",
        "employee": "J. Fernandes",
        "issue_summary": "Admin access request",
        "status": "Rejected — no business justification provided (closed)",
        "is_active": False,
        "precedent_note": "Access denied due to lack of manager approval and business justification (relevant to REQ-10)."
    },
    {
        "ticket_id": "TK-1051",
        "employee": "L. Menon",
        "issue_summary": "Guest Wi-Fi issued",
        "status": "Resolved (closed)",
        "is_active": False,
        "precedent_note": "Generated at front-desk kiosk without IT ticket per KB-07."
    }
]


def get_all_requests() -> List[Dict[str, Any]]:
    """Return all 15 benchmark employee requests."""
    return EMPLOYEE_REQUESTS


def get_request_by_id(req_id: str) -> Optional[Dict[str, Any]]:
    """Get single employee request by its REQ id."""
    for req in EMPLOYEE_REQUESTS:
        if req["id"] == req_id:
            return req
    return None


def get_ticket_queue() -> List[Dict[str, Any]]:
    """Return all historical and active ticket queue records."""
    return TICKET_QUEUE_RECORDS
