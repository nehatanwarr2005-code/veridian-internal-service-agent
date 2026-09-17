"""
Knowledge Base and Policy Module for Veridian Corp IT Support Agent.
Strictly grounded in Veridian Corp Data Pack - Assignment 2.
No ungrounded or invented policies.
"""

from typing import Dict, List, Optional, Any

KNOWLEDGE_BASE: Dict[str, Dict[str, Any]] = {
    "KB-01": {
        "id": "KB-01",
        "title": "Password Reset",
        "category": "Authentication & Access",
        "summary": "Self-service password reset; manual IT unlock if locked out after 5 failed attempts.",
        "text": (
            "Employees can reset their own password via the self-service portal at any time. "
            "If locked out after 5 failed attempts, contact IT to unlock the account manually. "
            "No approval required."
        ),
        "rules": [
            "Self-service portal is available at any time for normal password resets.",
            "Lockout occurs after 5 failed attempts.",
            "Lockouts require manual IT unlock.",
            "No approval required for account unlock."
        ],
        "keywords": ["password", "reset", "locked out", "unlock", "failed attempts", "login password", "credentials"],
        "self_service": True,
        "requires_approval": False,
        "escalate_if": "Lockout (>5 attempts) requires manual IT admin intervention."
    },
    "KB-02": {
        "id": "KB-02",
        "title": "VPN Access",
        "category": "Network & VPN",
        "summary": "Automatic for full-time employees; manager approval required for contractors; 90-day expiration.",
        "text": (
            "VPN access is granted automatically to all full-time employees. "
            "Contractors require manager approval submitted via the access request form. "
            "VPN credentials expire every 90 days and must be renewed by the employee."
        ),
        "rules": [
            "Full-time employees receive VPN access automatically.",
            "Contractors require manager approval submitted via the access request form.",
            "VPN credentials expire every 90 days.",
            "Renewal must be performed by the employee."
        ],
        "keywords": ["vpn", "remote access", "vpn credentials", "contractor vpn", "renew vpn", "expired credentials", "cisco", "tunnel"],
        "self_service": True,
        "requires_approval": "Only for contractors (manager approval required via access request form)",
        "escalate_if": "Contractor requesting access without manager approval form."
    },
    "KB-03": {
        "id": "KB-03",
        "title": "Laptop Replacement",
        "category": "Hardware & Devices",
        "summary": "Eligible after 3 years of service or verified hardware failure; 2 weeks advance notice.",
        "text": (
            "Laptops are eligible for replacement after 3 years of service, or earlier in case of verified hardware failure. "
            "Requests must be raised at least 2 weeks in advance of intended replacement."
        ),
        "rules": [
            "Eligibility threshold is 3 years of service under IT policy KB-03.",
            "Earlier replacement is permitted only upon verified hardware failure.",
            "Must be requested at least 2 weeks in advance of intended replacement.",
            "Subject to reconciliation with Finance & Assets 4-year standard refresh cycle policy."
        ],
        "keywords": ["laptop", "replacement", "laptop replacement", "dead laptop", "broken screen", "won't turn on", "hardware failure", "new laptop", "pc upgrade"],
        "self_service": False,
        "requires_approval": True,
        "escalate_if": "Requires IT hardware inspection/verification and Finance sign-off if under 4-year Finance refresh cycle."
    },
    "KB-04": {
        "id": "KB-04",
        "title": "Software Installation Requests",
        "category": "Software & Applications",
        "summary": "Catalog software is self-installed; non-catalog software requires IT Security review (3-5 days).",
        "text": (
            "Standard software (listed in the approved catalog) can be self-installed. "
            "Non-catalog software requires IT Security review, which takes 3–5 business days."
        ),
        "rules": [
            "Standard approved catalog software can be self-installed directly by the employee.",
            "Non-catalog software requires formal IT Security review.",
            "Security review turnaround SLA is 3 to 5 business days.",
            "Browser extensions and third-party tools not in catalog require security approval."
        ],
        "keywords": ["software", "install", "installation", "catalog", "non-catalog", "security review", "application", "extension", "plugin", "browser extension", "tool"],
        "self_service": "Only for approved catalog software",
        "requires_approval": True,
        "escalate_if": "Non-catalog tool or extension requires routing to IT Security review."
    },
    "KB-05": {
        "id": "KB-05",
        "title": "Printer Troubleshooting",
        "category": "Peripherals & Printing",
        "summary": "Check queue and restart print spooler; if unresolved, log ticket with printer asset tag.",
        "text": (
            "For printer issues, first check the printer queue and restart the print spooler. "
            "If the issue persists after restart, log a ticket with the printer’s asset tag."
        ),
        "rules": [
            "Step 1: Check the printer queue for stuck print jobs.",
            "Step 2: Restart the local/network print spooler service.",
            "Step 3: If issue persists after spooler restart, log ticket with the printer asset tag."
        ],
        "keywords": ["printer", "print", "paper jam", "spooler", "print queue", "asset tag", "printing", "scanner", "copier"],
        "self_service": True,
        "requires_approval": False,
        "escalate_if": "Hardware jam or hardware fault persists after restart; technician dispatch required."
    },
    "KB-06": {
        "id": "KB-06",
        "title": "Email Mailbox Quota",
        "category": "Email & Collaboration",
        "summary": "Default quota 25GB; archive old mail; increases >25GB require manager approval (cap 50GB).",
        "text": (
            "Default mailbox quota is 25GB. Employees nearing quota should archive old mail. "
            "Quota increases beyond 25GB require manager approval and are capped at 50GB."
        ),
        "rules": [
            "Default mailbox quota is 25GB for all employees.",
            "Employees nearing or at quota must first archive old mail.",
            "Quota increases beyond 25GB require formal manager approval.",
            "Absolute maximum mailbox quota cap is 50GB."
        ],
        "keywords": ["mailbox", "email", "quota", "full", "archive", "storage", "outlook", "exchange", "inbox full", "cant send email", "can't send"],
        "self_service": "Archiving is self-service; quota increase requires manager approval",
        "requires_approval": "Manager approval required for quota above 25GB",
        "escalate_if": "Employee requests increase beyond 25GB without manager approval, or requests >50GB."
    },
    "KB-07": {
        "id": "KB-07",
        "title": "Guest Wi-Fi Access",
        "category": "Network & Wi-Fi",
        "summary": "Valid for 24 hours; generated by any employee from front-desk kiosk; no ticket required.",
        "text": (
            "Guest Wi-Fi credentials are valid for 24 hours and can be generated by any employee from the front-desk kiosk. "
            "No IT ticket required."
        ),
        "rules": [
            "Credentials are valid for 24 hours from generation.",
            "Any employee can generate guest Wi-Fi passes directly at the front-desk kiosk.",
            "No IT support ticket is required for guest Wi-Fi access."
        ],
        "keywords": ["wifi", "wi-fi", "guest", "visitor", "guest access", "front desk", "kiosk", "internet access"],
        "self_service": True,
        "requires_approval": False,
        "escalate_if": "Kiosk hardware failure or special prolonged visitor event."
    },
    "KB-08": {
        "id": "KB-08",
        "title": "Expense Software Access",
        "category": "Enterprise Software & Finance",
        "summary": "Account provisioning is granted by Finance, not IT. IT assists with login/technical issues only.",
        "text": (
            "Access to the expense management tool is granted by Finance, not IT. "
            "IT can only assist with login/technical issues once an account already exists."
        ),
        "rules": [
            "Finance department is solely responsible for granting and provisioning expense tool accounts.",
            "IT does not have authority to create or grant new expense tool accounts.",
            "IT can assist with login/password/technical issues only if an account already exists."
        ],
        "keywords": ["expense", "expense tool", "concur", "expensify", "finance access", "reporting server", "admin access", "accounting", "invalid credentials"],
        "self_service": False,
        "requires_approval": True,
        "escalate_if": "Employee lacks an account (route to Finance) or requests unauthorized admin/elevated privileges."
    },
    "KB-09": {
        "id": "KB-09",
        "title": "Security Incident Reporting",
        "category": "Information Security",
        "summary": "Report phishing/malware to security@veridian-corp.example immediately; NEVER forward to teammates.",
        "text": (
            "Any suspected phishing email, malware, or unauthorized access attempt must be reported to "
            "security@veridian-corp.example immediately and should not be forwarded to other employees."
        ),
        "rules": [
            "Suspected phishing, malware, or unauthorized access must be reported to security@veridian-corp.example immediately.",
            "CRITICAL PROTOCOL: Suspected phishing emails must NEVER be forwarded to colleagues or teammates.",
            "Forwarding phishing internally spreads security risk across the corporate perimeter."
        ],
        "keywords": ["phishing", "phish", "malware", "virus", "suspicious", "hack", "compromised", "unauthorized", "security incident", "forwarding", "forward"],
        "self_service": False,
        "requires_approval": False,
        "escalate_if": "Any suspected phishing, especially if forwarded to other teammates (Immediate Security Escalation)."
    },
    "KB-10": {
        "id": "KB-10",
        "title": "Work-From-Home Equipment",
        "category": "Remote Work & Assets",
        "summary": "WFH >3 days/week eligible for one-time allowance (chair, monitor). Manager sign-off + Finance processing required.",
        "text": (
            "Employees working remotely more than 3 days/week are eligible for a one-time home office equipment allowance (chair, monitor). "
            "Requires manager sign-off and Finance processing — IT only handles the equipment shipping request once approved."
        ),
        "rules": [
            "Eligibility criteria: Employee must work remotely more than 3 days/week.",
            "Covers one-time home office allowance for chair and/or monitor.",
            "Prerequisites: Manager sign-off AND Finance processing approval.",
            "IT responsibility boundary: IT only handles equipment shipping once both approvals are recorded."
        ],
        "keywords": ["work from home", "wfh", "remote", "monitor", "chair", "home office", "allowance", "shipping", "remote work"],
        "self_service": False,
        "requires_approval": "Requires Manager sign-off and Finance processing before IT shipping",
        "escalate_if": "Direct shipping request without verified Manager sign-off and Finance approval."
    },
    "ASSET-POL": {
        "id": "ASSET-POL",
        "title": "Asset Management Policy (Extract)",
        "category": "Hardware & Asset Governance",
        "summary": "Standard 4-year refresh cycle for laptops/monitors. Early replacement requires Finance sign-off + IT approval.",
        "text": (
            "Asset Management Policy (Extract) — issued by Finance & Assets, last updated Q2 2026: "
            "All company-issued hardware, including laptops and monitors, follows a standard 4-year refresh cycle from date of issue. "
            "Early replacement outside this cycle requires Finance sign-off in addition to IT approval."
        ),
        "rules": [
            "Issued by Finance & Assets department, updated Q2 2026.",
            "Standard hardware refresh cycle is 4 years from date of issue for laptops and monitors.",
            "Early replacement prior to 4 years requires dual approval: Finance sign-off AND IT approval.",
            "Cross-reference KB-03: KB-03 allows eligibility at 3 years or upon verified hardware failure, but Finance approval is required if under 4-year cycle."
        ],
        "keywords": ["refresh cycle", "4-year", "4 years", "finance sign-off", "asset management", "early replacement", "hardware refresh", "asset policy"],
        "self_service": False,
        "requires_approval": True,
        "escalate_if": "Any hardware replacement requested before 4 years requires Finance sign-off."
    }
}


def get_policy(policy_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve a policy by its identifier."""
    return KNOWLEDGE_BASE.get(policy_id)


def list_all_policies() -> List[Dict[str, Any]]:
    """Return all policies in the knowledge base."""
    return list(KNOWLEDGE_BASE.values())


def search_knowledge_base(query: str) -> List[Dict[str, Any]]:
    """
    Search knowledge base matching query terms strictly against verified policies.
    Returns ranked list of matching policy objects.
    """
    query_lower = query.lower()
    matches = []
    
    for policy in KNOWLEDGE_BASE.values():
        score = 0
        # Keyword matching
        for kw in policy["keywords"]:
            if kw in query_lower:
                score += 3
        # Title matching
        if policy["title"].lower() in query_lower:
            score += 5
        # Text matching
        for word in query_lower.split():
            if len(word) > 3 and word in policy["text"].lower():
                score += 1
                
        if score > 0:
            matches.append((score, policy))
            
    matches.sort(key=lambda x: x[0], reverse=True)
    return [item[1] for item in matches]
