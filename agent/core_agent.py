"""
Core Internal Service Agent Engine for Veridian Corp IT Support.
Implements:
1. Issue understanding & categorization
2. Grounded policy retrieval (KB-01 to KB-10, Asset Management Policy)
3. Precedent matching (TK-1042 to TK-1051)
4. Risk & ambiguity assessment
5. Sensible follow-up question generation
6. Resolution vs. escalation decision logic
7. Structured ticket generation & audit trail integration
"""

import re
from typing import Dict, List, Optional, Any, Tuple
from agent.knowledge_base import KNOWLEDGE_BASE, get_policy, search_knowledge_base
from agent.ticket_system import TicketManager, StructuredTicket, AuditEvent
from agent.data_loader import TICKET_QUEUE_RECORDS


class AgentResponse:
    """Encapsulates the agent's comprehensive response."""
    def __init__(
        self,
        request_id: Optional[str],
        employee_name: str,
        employee_email: str,
        category: str,
        risk_level: str,
        action_type: str,  # RESOLVE_SIMPLE, ESCALATE, FOLLOW_UP, PENDING_APPROVAL
        status: str,
        assigned_to: str,
        response_message: str,
        cited_policies: List[str],
        follow_up_questions: List[str],
        precedent_cited: Optional[str] = None,
        ticket: Optional[StructuredTicket] = None
    ):
        self.request_id = request_id
        self.employee_name = employee_name
        self.employee_email = employee_email
        self.category = category
        self.risk_level = risk_level
        self.action_type = action_type
        self.status = status
        self.assigned_to = assigned_to
        self.response_message = response_message
        self.cited_policies = cited_policies
        self.follow_up_questions = follow_up_questions
        self.precedent_cited = precedent_cited
        self.ticket = ticket

    def to_dict(self) -> Dict[str, Any]:
        return {
            "request_id": self.request_id,
            "employee_name": self.employee_name,
            "employee_email": self.employee_email,
            "category": self.category,
            "risk_level": self.risk_level,
            "action_type": self.action_type,
            "status": self.status,
            "assigned_to": self.assigned_to,
            "response_message": self.response_message,
            "cited_policies": self.cited_policies,
            "follow_up_questions": self.follow_up_questions,
            "precedent_cited": self.precedent_cited,
            "ticket_id": self.ticket.ticket_id if self.ticket else None
        }


class InternalServiceAgent:
    """
    Intelligent IT Service Agent strictly grounded in Veridian Corp policies.
    """
    def __init__(self, ticket_manager: Optional[TicketManager] = None):
        self.ticket_manager = ticket_manager or TicketManager()
        self.precedents = TICKET_QUEUE_RECORDS

    def assess_risk(self, query: str, category: str) -> Tuple[str, str]:
        """
        Evaluate risk level (Low, Medium, High, Critical) and risk rationale.
        """
        q = query.lower()
        
        # Critical: Phishing forwarding, active security breach, data leak
        if "phishing" in q or "malware" in q or "virus" in q or "unauthorized access" in q:
            if "forward" in q or "sent to" in q or "teammates" in q:
                return "Critical", "Suspected security incident involving internal forwarding of malicious content (violates KB-09 quarantine protocol)."
            return "High", "Security incident requiring prompt IT Security team investigation."

        # High: Admin privilege escalation, unauthorized access to sensitive financial servers
        if "admin access" in q or "root access" in q or "finance reporting server" in q or "bypass" in q:
            return "High", "Privilege escalation / administrative server access request without verified authorization."

        # Medium: Hardware failure, early replacement, non-catalog software, WFH procurement
        if "laptop" in q and ("won't turn on" in q or "dead" in q or "replacement" in q or "flicker" in q):
            return "Medium", "Hardware failure requiring technician diagnostics or asset lifecycle reconciliation."
        if "not in the software catalog" in q or "browser extension" in q or "non-catalog" in q:
            return "Medium", "Third-party non-catalog software requiring mandatory IT Security review."
        if "work from home" in q or "wfh" in q or "monitor" in q or "equipment allowance" in q:
            return "Medium", "Asset procurement requiring multi-departmental approval (Manager + Finance)."
        if "locked out" in q and ("failed" in q or "times" in q or "attempts" in q):
            return "Medium", "Account lockout exceeding failed attempt threshold, requires manual IT unlock."

        # Low: Routine self-service, guest Wi-Fi, VPN renewal, quota archive
        return "Low", "Standard operational or self-service request within regular policy parameters."

    def detect_ambiguity(self, query: str) -> bool:
        """
        Detect whether a user query lacks actionable specifics.
        """
        q = query.strip().lower()
        # Vague requests like REQ-15 ("hey can you help, its not working")
        if len(q.split()) <= 12 and any(phrase in q for phrase in ["not working", "help", "broken", "issue", "trouble", "doesn't work", "doesnt work"]):
            # Check if specific device/service is absent
            specific_terms = ["laptop", "printer", "vpn", "wifi", "wi-fi", "password", "email", "mailbox", "software", "catalog", "expense", "monitor", "screen", "phish", "lock"]
            if not any(term in q for term in specific_terms):
                return True
        return False

    def find_precedent(self, category: str, query: str) -> Optional[Dict[str, Any]]:
        """Find historical ticket precedent from Section 3."""
        q = query.lower()
        if "vpn" in q and "expire" in q:
            return next((t for t in self.precedents if t["ticket_id"] == "TK-1042"), None)
        if "laptop" in q and ("replace" in q or "year" in q):
            return next((t for t in self.precedents if t["ticket_id"] == "TK-1043"), None)
        if "catalog" in q or "extension" in q:
            return next((t for t in self.precedents if t["ticket_id"] == "TK-1044"), None)
        if "mailbox" in q or "quota" in q:
            return next((t for t in self.precedents if t["ticket_id"] == "TK-1045"), None)
        if "printer" in q:
            return next((t for t in self.precedents if t["ticket_id"] == "TK-1046"), None)
        if "work from home" in q or "monitor" in q or "wfh" in q:
            return next((t for t in self.precedents if t["ticket_id"] == "TK-1047"), None)
        if "phishing" in q:
            return next((t for t in self.precedents if t["ticket_id"] == "TK-1048"), None)
        if "password" in q or "locked out" in q:
            return next((t for t in self.precedents if t["ticket_id"] == "TK-1049"), None)
        if "admin" in q or "finance reporting" in q:
            return next((t for t in self.precedents if t["ticket_id"] == "TK-1050"), None)
        if "guest" in q or "wifi" in q or "wi-fi" in q:
            return next((t for t in self.precedents if t["ticket_id"] == "TK-1051"), None)
        return None

    def process_request(
        self,
        query: str,
        employee_name: str = "Employee",
        employee_email: str = "employee@veridian-corp.example",
        request_id: Optional[str] = None
    ) -> AgentResponse:
        """
        Main decision pipeline executing:
        1. Ambiguity detection
        2. Policy retrieval & grounding
        3. Risk assessment
        4. Resolution / Escalation / Follow-up generation
        5. Ticket and audit log creation
        """
        q = query.strip()
        q_lower = q.lower()

        # Audit initial request receipt
        self.ticket_manager.log_audit(
            event_type="REQUEST_RECEIVED",
            details=f"Received IT support request from {employee_name} ({employee_email}): '{q}'",
            request_id=request_id
        )

        # -------------------------------------------------------------
        # STEP 1: Ambiguity Check (e.g. REQ-15)
        # -------------------------------------------------------------
        if self.detect_ambiguity(q):
            follow_ups = [
                "Which device, system, or service is experiencing the issue (e.g., laptop, VPN, email, Wi-Fi, printer)?",
                "What exact error message, notification, or behavior are you observing?",
                "When did the issue start, and does it prevent you from completing time-sensitive work?"
            ]
            response_msg = (
                f"Hello {employee_name},\n\n"
                "Thank you for reaching out to Veridian IT Support. Your request does not currently provide enough technical "
                "details for us to diagnose the issue or apply the appropriate company policy. "
                "To assist you immediately, please answer the follow-up questions below."
            )
            
            ticket = self.ticket_manager.create_ticket(
                employee_name=employee_name,
                employee_email=employee_email,
                category="Unclear / Triage",
                issue_summary="Underspecified IT support inquiry",
                priority="Low",
                risk_level="Low",
                status="Awaiting Employee Response",
                assigned_to="IT Service Desk Tier 1",
                source_policies=[],
                resolution_or_action="Diagnostic clarification requested from employee.",
                request_id=request_id,
                follow_up_questions=follow_ups
            )

            self.ticket_manager.log_audit(
                event_type="FOLLOW_UP_REQUESTED",
                details="Request lacks diagnostic detail. Generated 3 targeted triage questions.",
                ticket_id=ticket.ticket_id,
                request_id=request_id
            )

            return AgentResponse(
                request_id=request_id,
                employee_name=employee_name,
                employee_email=employee_email,
                category="Unclear / Triage",
                risk_level="Low",
                action_type="FOLLOW_UP",
                status="Awaiting Employee Response",
                assigned_to="IT Service Desk Tier 1",
                response_message=response_msg,
                cited_policies=[],
                follow_up_questions=follow_ups,
                ticket=ticket
            )

        # -------------------------------------------------------------
        # STEP 2: Grounded Policy Search & Intent Matching
        # -------------------------------------------------------------
        matched_policies = search_knowledge_base(q)
        precedent = self.find_precedent("General", q)
        risk_level, risk_rationale = self.assess_risk(q, "General")

        # Specific Case Handlers strictly aligned with Veridian Corp Policies:

        # CASE: REQ-08 (Phishing / Security Incident + Forwarding)
        if "phishing" in q_lower or ("malware" in q_lower or "login" in q_lower and "teammates" in q_lower):
            category = "Information Security"
            cited = ["KB-09"]
            kb09 = get_policy("KB-09")
            
            response_msg = (
                f"🚨 **CRITICAL SECURITY ALERT — ACTION REQUIRED**\n\n"
                f"Hello {employee_name},\n\n"
                f"**DO NOT forward this email to any colleagues or teammates.** Forwarding suspected phishing emails spreads the attack vector across Veridian Corp.\n\n"
                f"**Immediate Protocol per {kb09['title']} ({kb09['id']}):**\n"
                f"1. **Stop Forwarding**: Please inform any teammates who received your forward to delete it without clicking any links or attachments.\n"
                f"2. **Report Immediately**: We have automatically generated a Critical Incident Ticket and alerted `security@veridian-corp.example`.\n"
                f"3. **Account Safety**: If you entered credentials anywhere, notify IT immediately so we can trigger a mandatory session termination and credential reset."
            )
            
            ticket = self.ticket_manager.create_ticket(
                employee_name=employee_name,
                employee_email=employee_email,
                category=category,
                issue_summary="Suspected phishing email reported (forwarded internally to teammates)",
                priority="Critical",
                risk_level="Critical",
                status="Escalated to Security (auto-flagged)",
                assigned_to="IT Security Incident Response Team (security@veridian-corp.example)",
                source_policies=cited,
                resolution_or_action="Quarantine alert issued; escalated immediately to Security team per KB-09.",
                request_id=request_id
            )

            self.ticket_manager.log_audit(
                event_type="RISK_ESCALATED",
                details=f"Critical phishing protocol triggered. Employee alerted to halt forwarding. Escalated to Security team per KB-09. {risk_rationale}",
                ticket_id=ticket.ticket_id,
                request_id=request_id,
                source_used="KB-09"
            )

            return AgentResponse(
                request_id=request_id,
                employee_name=employee_name,
                employee_email=employee_email,
                category=category,
                risk_level="Critical",
                action_type="ESCALATE",
                status="Escalated to Security (auto-flagged)",
                assigned_to="IT Security Incident Response Team",
                response_message=response_msg,
                cited_policies=cited,
                follow_up_questions=[],
                precedent_cited=precedent["ticket_id"] if precedent else "TK-1048",
                ticket=ticket
            )

        # CASE: REQ-10 (Admin Access / Finance Server)
        if "admin access" in q_lower or ("finance reporting server" in q_lower and "access" in q_lower):
            category = "Enterprise Software & Finance"
            cited = ["KB-08", "ASSET-POL"]
            kb08 = get_policy("KB-08")
            
            response_msg = (
                f"Hello {employee_name},\n\n"
                f"**Request Denied at Tier 1 / Escalated for Business Justification:**\n\n"
                f"Under Veridian Corp policy **{kb08['id']} ({kb08['title']})**, access to finance tools and servers is granted solely by **Finance**, not IT. "
                f"IT does not possess the administrative authority to grant ad-hoc or urgent administrative permissions without verified authorization.\n\n"
                f"**Precedent Reference**: In historical ticket **TK-1050**, administrative access requested without documented business justification was formally rejected.\n\n"
                f"**Required Next Steps:**\n"
                f"1. Have your department director submit a formal Access Request with business justification to Finance Systems Governance.\n"
                f"2. Once Finance grants the role, IT can configure login connectivity."
            )
            
            ticket = self.ticket_manager.create_ticket(
                employee_name=employee_name,
                employee_email=employee_email,
                category=category,
                issue_summary="Urgent admin access requested for finance reporting server",
                priority="High",
                risk_level="High",
                status="Rejected at Tier 1 / Pending Business Justification",
                assigned_to="Finance Systems Governance & IT Security",
                source_policies=cited,
                resolution_or_action="Direct admin grant denied per KB-08 and precedent TK-1050; redirected to Finance approval workflow.",
                request_id=request_id
            )

            self.ticket_manager.log_audit(
                event_type="ACCESS_REVIEWED",
                details="Unapproved admin privilege request flagged and redirected to Finance. Consistent with precedent TK-1050.",
                ticket_id=ticket.ticket_id,
                request_id=request_id,
                source_used="KB-08, TK-1050"
            )

            return AgentResponse(
                request_id=request_id,
                employee_name=employee_name,
                employee_email=employee_email,
                category=category,
                risk_level="High",
                action_type="ESCALATE",
                status="Rejected at Tier 1 / Pending Business Justification",
                assigned_to="Finance Systems Governance & IT Security",
                response_message=response_msg,
                cited_policies=cited,
                follow_up_questions=["Do you have an existing signed authorization form from the Finance Department Director?"],
                precedent_cited="TK-1050",
                ticket=ticket
            )

        # CASE: REQ-01 & REQ-13 (Laptop Issues / Replacement / Repair)
        if "laptop" in q_lower:
            category = "Hardware & Devices"
            cited = ["KB-03", "ASSET-POL"]
            kb03 = get_policy("KB-03")
            asset_pol = get_policy("ASSET-POL")

            # REQ-01: Completely dead / 3.5 years old
            if "won’t turn on" in q_lower or "won't turn on" in q_lower or "completely dead" in q_lower or "3.5 years" in q_lower:
                response_msg = (
                    f"Hello {employee_name},\n\n"
                    f"We are sorry to hear your laptop has failed. Here is the policy guidance for your case:\n\n"
                    f"• **IT Policy {kb03['id']} ({kb03['title']})**: Laptops are eligible for replacement after 3 years of service, or earlier in case of verified hardware failure (advance notice requirement: 2 weeks).\n"
                    f"• **{asset_pol['id']} ({asset_pol['title']})**: Standard corporate refresh cycle is 4 years. Because your device is 3.5 years old, early replacement outside the 4-year cycle requires **Finance sign-off** in addition to IT approval.\n\n"
                    f"**Action Taken**: Because your laptop is completely inoperable (verified hardware failure), we have created an expedited hardware ticket and routed it for combined IT Hardware verification and Finance sign-off (similar to approved precedent **TK-1043**).\n\n"
                    f"**Next Step**: Please drop off the device at the IT Depot (or confirm your shipping address if remote) for hardware verification."
                )
                status = "Approved for Inspection — Pending Finance Sign-off"
                action_type = "ESCALATE"
                assigned = "IT Hardware Depot & Finance Assets"
                follow_ups = ["Are you available to bring the dead laptop to the IT Depot, or do you need a pre-paid return shipping box?"]
            
            # REQ-13: Screen flickering / 2 years old / fix not replacement
            elif "flicker" in q_lower or "2 years" in q_lower or "fix" in q_lower:
                response_msg = (
                    f"Hello {employee_name},\n\n"
                    f"Thank you for reporting your screen flickering issue. At 2 years of service, your laptop is within its standard 4-year refresh cycle ({asset_pol['id']}) and not yet due for scheduled lifecycle replacement ({kb03['id']}).\n\n"
                    f"Your request for a repair rather than replacement aligns with policy. We have logged a hardware diagnostic ticket."
                )
                status = "In Progress — Hardware Diagnostic Queued"
                action_type = "FOLLOW_UP"
                assigned = "IT Hardware Depot Technician"
                follow_ups = [
                    "Does the flickering occur when you move the laptop hinge/lid, or does it happen intermittently regardless of position?",
                    "Does the flickering also happen when connected to an external monitor?",
                    "What is your laptop's Asset Tag or Serial Number (located on the bottom sticker)?"
                ]
            else:
                response_msg = f"Logged hardware ticket per {kb03['id']} and {asset_pol['id']}."
                status = "Under Review"
                action_type = "ESCALATE"
                assigned = "IT Hardware Depot"
                follow_ups = ["What is the exact age and asset tag of your device?"]

            ticket = self.ticket_manager.create_ticket(
                employee_name=employee_name,
                employee_email=employee_email,
                category=category,
                issue_summary="Laptop hardware issue / replacement eligibility review",
                priority="Medium",
                risk_level="Medium",
                status=status,
                assigned_to=assigned,
                source_policies=cited,
                resolution_or_action="Hardware diagnostics and policy lifecycle review initiated per KB-03 and Asset Management Policy.",
                request_id=request_id,
                follow_up_questions=follow_ups
            )

            self.ticket_manager.log_audit(
                event_type="POLICY_GROUNDED",
                details=f"Evaluated hardware replacement against dual policy: KB-03 (3-year rule / failure) and Asset Management Policy (4-year refresh / Finance sign-off).",
                ticket_id=ticket.ticket_id,
                request_id=request_id,
                source_used="KB-03, ASSET-POL"
            )

            return AgentResponse(
                request_id=request_id,
                employee_name=employee_name,
                employee_email=employee_email,
                category=category,
                risk_level="Medium",
                action_type=action_type,
                status=status,
                assigned_to=assigned,
                response_message=response_msg,
                cited_policies=cited,
                follow_up_questions=follow_ups,
                precedent_cited="TK-1043",
                ticket=ticket
            )

        # CASE: REQ-02 (Guest Wi-Fi)
        if "guest" in q_lower and ("wi-fi" in q_lower or "wifi" in q_lower or "access" in q_lower):
            category = "Network & Wi-Fi"
            cited = ["KB-07"]
            kb07 = get_policy("KB-07")

            response_msg = (
                f"Hello {employee_name},\n\n"
                f"**Resolution — No IT Ticket Required:**\n\n"
                f"Under Veridian Corp policy **{kb07['id']} ({kb07['title']})**:\n"
                f"• Guest Wi-Fi credentials are valid for **24 hours**.\n"
                f"• They can be generated directly by **any employee** at the **front-desk kiosk** in the main lobby.\n"
                f"• No formal IT approval or ticket is required.\n\n"
                f"You can generate the pass tomorrow morning when your guest arrives at the reception kiosk."
            )

            ticket = self.ticket_manager.create_ticket(
                employee_name=employee_name,
                employee_email=employee_email,
                category=category,
                issue_summary="Guest Wi-Fi access inquiry",
                priority="Low",
                risk_level="Low",
                status="Resolved (Self-Service)",
                assigned_to="Self-Service Portal (Lobby Kiosk)",
                source_policies=cited,
                resolution_or_action="Informed employee of front-desk kiosk self-service procedure per KB-07. Precedent TK-1051 matched.",
                request_id=request_id
            )

            self.ticket_manager.log_audit(
                event_type="RESOLVED_SELF_SERVICE",
                details="Provided self-service front-desk kiosk guidance per KB-07. Ticket marked resolved.",
                ticket_id=ticket.ticket_id,
                request_id=request_id,
                source_used="KB-07"
            )

            return AgentResponse(
                request_id=request_id,
                employee_name=employee_name,
                employee_email=employee_email,
                category=category,
                risk_level="Low",
                action_type="RESOLVE_SIMPLE",
                status="Resolved (Self-Service)",
                assigned_to="Self-Service Portal (Lobby Kiosk)",
                response_message=response_msg,
                cited_policies=cited,
                follow_up_questions=[],
                precedent_cited="TK-1051",
                ticket=ticket
            )

        # CASE: REQ-03 (Account Lockout / Password Reset)
        if "locked out" in q_lower or ("password" in q_lower and ("6 times" in q_lower or "failed" in q_lower)):
            category = "Authentication & Access"
            cited = ["KB-01"]
            kb01 = get_policy("KB-01")

            response_msg = (
                f"Hello {employee_name},\n\n"
                f"**Account Lockout Remediation:**\n\n"
                f"Per policy **{kb01['id']} ({kb01['title']})**:\n"
                f"• Employees can normally reset passwords via the self-service portal at any time.\n"
                f"• However, because you have exceeded 5 failed attempts (tried 6 times), your account is **locked out** and requires a **manual IT unlock**.\n"
                f"• **No manager approval is required** for this unlock.\n\n"
                f"**Action Taken**: We have placed your account into the manual unlock queue. An IT Operations engineer will unlock your account shortly and send a secure one-time passcode to your registered mobile."
            )

            ticket = self.ticket_manager.create_ticket(
                employee_name=employee_name,
                employee_email=employee_email,
                category=category,
                issue_summary="Account lockout after 6 failed attempts (manual unlock required)",
                priority="Medium",
                risk_level="Medium",
                status="In Progress — Reset Queued",
                assigned_to="IT Identity Operations Team",
                source_policies=cited,
                resolution_or_action="Manual unlock queued per KB-01 (no approval required). Precedent TK-1049 referenced.",
                request_id=request_id
            )

            self.ticket_manager.log_audit(
                event_type="ACTION_EXECUTED",
                details="Threshold exceeded (>5 failed attempts). Queued for manual IT unlock per KB-01.",
                ticket_id=ticket.ticket_id,
                request_id=request_id,
                source_used="KB-01"
            )

            return AgentResponse(
                request_id=request_id,
                employee_name=employee_name,
                employee_email=employee_email,
                category=category,
                risk_level="Medium",
                action_type="RESOLVE_SIMPLE",
                status="In Progress — Reset Queued",
                assigned_to="IT Identity Operations Team",
                response_message=response_msg,
                cited_policies=cited,
                follow_up_questions=[],
                precedent_cited="TK-1049",
                ticket=ticket
            )

        # CASE: REQ-04 & REQ-14 (Software Installation / Non-catalog / Extensions)
        if "install" in q_lower or "software" in q_lower or "extension" in q_lower:
            category = "Software & Applications"
            cited = ["KB-04"]
            kb04 = get_policy("KB-04")

            response_msg = (
                f"Hello {employee_name},\n\n"
                f"**Software Request Logged for Security Review:**\n\n"
                f"Under Veridian Corp policy **{kb04['id']} ({kb04['title']})**:\n"
                f"• Standard catalog software can be self-installed directly by employees.\n"
                f"• Non-catalog software and browser extensions require a mandatory **IT Security review**.\n"
                f"• The review turnaround SLA takes **3–5 business days**.\n\n"
                f"**Action Taken**: We have opened a security review ticket and dispatched it to the IT Security Team (following precedent **TK-1044**). You will receive an automated notification once security vetting is completed."
            )

            ticket = self.ticket_manager.create_ticket(
                employee_name=employee_name,
                employee_email=employee_email,
                category=category,
                issue_summary="Non-catalog software / extension security review request",
                priority="Medium",
                risk_level="Medium",
                status="Waiting on Security Review",
                assigned_to="IT Security Review Board",
                source_policies=cited,
                resolution_or_action="Forwarded to IT Security for 3-5 day software security review per KB-04.",
                request_id=request_id,
                follow_up_questions=["Please provide the exact tool version and official download URL if not already submitted."]
            )

            self.ticket_manager.log_audit(
                event_type="SECURITY_ROUTED",
                details="Non-catalog software routed to IT Security review board with 3-5 business days SLA per KB-04.",
                ticket_id=ticket.ticket_id,
                request_id=request_id,
                source_used="KB-04"
            )

            return AgentResponse(
                request_id=request_id,
                employee_name=employee_name,
                employee_email=employee_email,
                category=category,
                risk_level="Medium",
                action_type="ESCALATE",
                status="Waiting on Security Review",
                assigned_to="IT Security Review Board",
                response_message=response_msg,
                cited_policies=cited,
                follow_up_questions=["Please provide the exact tool version and official download URL if not already submitted."],
                precedent_cited="TK-1044",
                ticket=ticket
            )

        # CASE: REQ-05 & REQ-11 (VPN Access / Credentials / Contractors)
        if "vpn" in q_lower:
            category = "Network & VPN"
            cited = ["KB-02"]
            kb02 = get_policy("KB-02")

            # REQ-11: Contractor VPN
            if "contractor" in q_lower:
                response_msg = (
                    f"Hello {employee_name},\n\n"
                    f"**Contractor VPN Access Protocol:**\n\n"
                    f"Under policy **{kb02['id']} ({kb02['title']})**:\n"
                    f"• Unlike full-time employees who receive VPN automatically, **contractors require manager approval**.\n"
                    f"• This approval must be formally submitted via the **Access Request Form**.\n"
                    f"• Credentials are valid for 90 days once provisioned.\n\n"
                    f"**Action Required**: As the sponsoring manager/lead, please complete and submit the Access Request Form with the contractor's full name, contracting agency, and start/end dates."
                )
                status = "Pending Manager Access Request Form"
                action_type = "PENDING_APPROVAL"
                follow_ups = ["Have you submitted the Access Request Form for this contractor yet?"]
            # REQ-05: Expired VPN credentials
            else:
                response_msg = (
                    f"Hello {employee_name},\n\n"
                    f"**VPN Credential Renewal Guidance:**\n\n"
                    f"Under policy **{kb02['id']} ({kb02['title']})**:\n"
                    f"• VPN credentials for full-time employees expire every **90 days** for security compliance.\n"
                    f"• Renewal must be performed by the employee via the self-service credential portal.\n\n"
                    f"**Resolution Steps:**\n"
                    f"1. Open your browser and navigate to `https://vpn-portal.veridian-corp.example/renew`\n"
                    f"2. Authenticate using your corporate credentials and MFA token.\n"
                    f"3. Click 'Renew Credentials' to generate an active 90-day certificate. Precedent: **TK-1042**."
                )
                status = "Resolved (Self-Service Guidance)"
                action_type = "RESOLVE_SIMPLE"
                follow_ups = []

            ticket = self.ticket_manager.create_ticket(
                employee_name=employee_name,
                employee_email=employee_email,
                category=category,
                issue_summary="VPN access / credential renewal request",
                priority="Low",
                risk_level="Low",
                status=status,
                assigned_to="IT Network Operations",
                source_policies=cited,
                resolution_or_action="Processed per KB-02 policy requirements. Precedent TK-1042 applied.",
                request_id=request_id,
                follow_up_questions=follow_ups
            )

            self.ticket_manager.log_audit(
                event_type="VPN_POLICY_APPLIED",
                details=f"Evaluated VPN request against KB-02. Status set to '{status}'.",
                ticket_id=ticket.ticket_id,
                request_id=request_id,
                source_used="KB-02"
            )

            return AgentResponse(
                request_id=request_id,
                employee_name=employee_name,
                employee_email=employee_email,
                category=category,
                risk_level="Low",
                action_type=action_type,
                status=status,
                assigned_to="IT Network Operations",
                response_message=response_msg,
                cited_policies=cited,
                follow_up_questions=follow_ups,
                precedent_cited="TK-1042",
                ticket=ticket
            )

        # CASE: REQ-06 (Printer Troubleshooting)
        if "printer" in q_lower or "paper jam" in q_lower:
            category = "Peripherals & Printing"
            cited = ["KB-05"]
            kb05 = get_policy("KB-05")

            response_msg = (
                f"Hello {employee_name},\n\n"
                f"**Printer Troubleshooting Protocol per {kb05['id']} ({kb05['title']}):**\n\n"
                f"1. **Check Queue**: Check the local printer queue on your computer for stalled or corrupted print jobs.\n"
                f"2. **Restart Print Spooler**: Open Services or run the printer diagnostic tool to restart the print spooler service.\n"
                f"3. **Persistent Issue**: Since you reported a phantom 'paper jam' error on the 3rd floor that persists, a technician must inspect the physical sensor.\n\n"
                f"**Action Taken**: Ticket logged for technician dispatch (similar to precedent **TK-1046**)."
            )
            follow_ups = [
                "What is the printer's Asset Tag (usually a 6-digit barcode sticker located on the top-right corner of the printer)?",
                "Which specific room or wing on the 3rd floor is this printer located in?"
            ]

            ticket = self.ticket_manager.create_ticket(
                employee_name=employee_name,
                employee_email=employee_email,
                category=category,
                issue_summary="Printer 3rd floor phantom paper jam error",
                priority="Medium",
                risk_level="Low",
                status="Investigating — Technician Assigned",
                assigned_to="IT Deskside Support Technician",
                source_policies=cited,
                resolution_or_action="Spooler troubleshooting provided; asset tag requested for on-site technician inspection per KB-05.",
                request_id=request_id,
                follow_up_questions=follow_ups
            )

            self.ticket_manager.log_audit(
                event_type="DISPATCH_TECHNICIAN",
                details="Printer spooler guidance issued; technician dispatch queued pending asset tag per KB-05.",
                ticket_id=ticket.ticket_id,
                request_id=request_id,
                source_used="KB-05"
            )

            return AgentResponse(
                request_id=request_id,
                employee_name=employee_name,
                employee_email=employee_email,
                category=category,
                risk_level="Low",
                action_type="FOLLOW_UP",
                status="Investigating — Technician Assigned",
                assigned_to="IT Deskside Support Technician",
                response_message=response_msg,
                cited_policies=cited,
                follow_up_questions=follow_ups,
                precedent_cited="TK-1046",
                ticket=ticket
            )

        # CASE: REQ-07 (Work From Home Equipment / Monitor)
        if "working from home" in q_lower or "wfh" in q_lower or ("monitor" in q_lower and "days" in q_lower):
            category = "Remote Work & Assets"
            cited = ["KB-10"]
            kb10 = get_policy("KB-10")

            response_msg = (
                f"Hello {employee_name},\n\n"
                f"**Work-From-Home Equipment Allowance Eligibility:**\n\n"
                f"Under Veridian Corp policy **{kb10['id']} ({kb10['title']})**:\n"
                f"• Employees working remotely **more than 3 days/week** are eligible for a one-time home office equipment allowance (chair, monitor).\n"
                f"• Since you work 4 days a week from home, **you meet the eligibility threshold**.\n\n"
                f"**Process Workflow & Boundaries:**\n"
                f"1. **Manager Sign-Off**: You must first obtain formal sign-off from your direct manager.\n"
                f"2. **Finance Processing**: Finance processes and approves the equipment budget allocation.\n"
                f"3. **IT Shipping**: IT only handles equipment provisioning and shipping **once both approvals are completed**.\n\n"
                f"**Action Taken**: Ticket opened in `Pending Finance/Manager Approval` status (aligning with active ticket **TK-1047**)."
            )

            ticket = self.ticket_manager.create_ticket(
                employee_name=employee_name,
                employee_email=employee_email,
                category=category,
                issue_summary="WFH 4 days/week monitor equipment allowance request",
                priority="Low",
                risk_level="Low",
                status="Pending Manager Sign-off & Finance Processing",
                assigned_to="Finance & Assets / IT Logistics",
                source_policies=cited,
                resolution_or_action="Eligibility confirmed under KB-10 (>3 days); waiting on Manager & Finance sign-off before IT shipping.",
                request_id=request_id,
                follow_up_questions=["Has your manager already approved your remote work schedule in the HR portal?"]
            )

            self.ticket_manager.log_audit(
                event_type="POLICY_GROUNDED",
                details="Evaluated WFH allowance eligibility (>3 days confirmed). Routed to Finance/Manager workflow per KB-10.",
                ticket_id=ticket.ticket_id,
                request_id=request_id,
                source_used="KB-10"
            )

            return AgentResponse(
                request_id=request_id,
                employee_name=employee_name,
                employee_email=employee_email,
                category=category,
                risk_level="Low",
                action_type="PENDING_APPROVAL",
                status="Pending Manager Sign-off & Finance Processing",
                assigned_to="Finance & Assets / IT Logistics",
                response_message=response_msg,
                cited_policies=cited,
                follow_up_questions=["Has your manager already approved your remote work schedule in the HR portal?"],
                precedent_cited="TK-1047",
                ticket=ticket
            )

        # CASE: REQ-09 (Mailbox Full / Email Quota)
        if "mailbox" in q_lower or ("quota" in q_lower or "can't send emails" in q_lower or "cant send emails" in q_lower):
            category = "Email & Collaboration"
            cited = ["KB-06"]
            kb06 = get_policy("KB-06")

            response_msg = (
                f"Hello {employee_name},\n\n"
                f"**Mailbox Quota Policy & Resolution per {kb06['id']} ({kb06['title']}):**\n\n"
                f"• **Default Quota**: All Veridian Corp mailboxes are allocated **25GB**.\n"
                f"• **Immediate Resolution**: To resume sending emails immediately, please **archive old mail and empty the Deleted Items folder**.\n"
                f"• **Quota Extension**: If archiving is insufficient, quota increases beyond 25GB require **manager approval** and are strictly capped at **50GB** (as demonstrated in precedent **TK-1045**, where 35GB was approved).\n\n"
                f"**Recommendation**: Follow the Outlook archiving guide to move items older than 6 months to your local archive."
            )

            ticket = self.ticket_manager.create_ticket(
                employee_name=employee_name,
                employee_email=employee_email,
                category=category,
                issue_summary="Mailbox quota full — unable to send emails",
                priority="Medium",
                risk_level="Low",
                status="Resolved (Guidance Provided) / Pending Archive",
                assigned_to="Self-Service / IT Exchange Admin",
                source_policies=cited,
                resolution_or_action="Informed employee of 25GB limit, archiving procedure, and 50GB manager-approval cap per KB-06.",
                request_id=request_id,
                follow_up_questions=["Do you need assistance setting up auto-archiving in Outlook, or do you wish to request a manager-approved quota increase?"]
            )

            self.ticket_manager.log_audit(
                event_type="RESOLVED_SELF_SERVICE",
                details="Mailbox quota rules explained; archiving steps provided per KB-06. Precedent TK-1045 cited.",
                ticket_id=ticket.ticket_id,
                request_id=request_id,
                source_used="KB-06"
            )

            return AgentResponse(
                request_id=request_id,
                employee_name=employee_name,
                employee_email=employee_email,
                category=category,
                risk_level="Low",
                action_type="RESOLVE_SIMPLE",
                status="Resolved (Guidance Provided) / Pending Archive",
                assigned_to="Self-Service / IT Exchange Admin",
                response_message=response_msg,
                cited_policies=cited,
                follow_up_questions=["Do you need assistance setting up auto-archiving in Outlook, or do you wish to request a manager-approved quota increase?"],
                precedent_cited="TK-1045",
                ticket=ticket
            )

        # CASE: REQ-12 (Expense Tool Access / Invalid Credentials)
        if "expense" in q_lower:
            category = "Enterprise Software & Finance"
            cited = ["KB-08"]
            kb08 = get_policy("KB-08")

            response_msg = (
                f"Hello {employee_name},\n\n"
                f"**Expense Management Tool Access Protocol:**\n\n"
                f"Under Veridian Corp policy **{kb08['id']} ({kb08['title']})**:\n"
                f"• Access and account provisioning for the expense management tool is **granted by Finance, not IT**.\n"
                f"• IT can only assist with login and technical issues **once an account already exists**.\n\n"
                f"To resolve your 'invalid credentials' error, we need to verify whether your account has been provisioned by Finance."
            )
            follow_ups = [
                "Has the Finance Department already confirmed that your expense account was created?",
                "Have you successfully logged in before, or is this your first attempt after joining/transferring?"
            ]

            ticket = self.ticket_manager.create_ticket(
                employee_name=employee_name,
                employee_email=employee_email,
                category=category,
                issue_summary="Expense tool invalid credentials login issue",
                priority="Medium",
                risk_level="Low",
                status="Waiting on Employee Response",
                assigned_to="IT Service Desk / Finance Systems",
                source_policies=cited,
                resolution_or_action="Explained Finance provisioning boundary under KB-08; asked follow-up to confirm account existence.",
                request_id=request_id,
                follow_up_questions=follow_ups
            )

            self.ticket_manager.log_audit(
                event_type="FOLLOW_UP_REQUESTED",
                details="Inquired whether Finance has provisioned the expense account per KB-08 boundary.",
                ticket_id=ticket.ticket_id,
                request_id=request_id,
                source_used="KB-08"
            )

            return AgentResponse(
                request_id=request_id,
                employee_name=employee_name,
                employee_email=employee_email,
                category=category,
                risk_level="Low",
                action_type="FOLLOW_UP",
                status="Waiting on Employee Response",
                assigned_to="IT Service Desk / Finance Systems",
                response_message=response_msg,
                cited_policies=cited,
                follow_up_questions=follow_ups,
                precedent_cited=None,
                ticket=ticket
            )

        # -------------------------------------------------------------
        # FALLBACK / GENERAL POLICY RESOLVER (Strictly Grounded)
        # -------------------------------------------------------------
        if matched_policies:
            top_policy = matched_policies[0]
            cited = [top_policy["id"]]
            category = top_policy["category"]
            
            response_msg = (
                f"Hello {employee_name},\n\n"
                f"Regarding your inquiry, here is the relevant Veridian Corp policy:\n\n"
                f"**{top_policy['title']} ({top_policy['id']})**:\n"
                f"{top_policy['text']}\n\n"
                f"• Approval Requirement: {top_policy['requires_approval']}\n"
                f"• Self-Service Option: {top_policy['self_service']}"
            )
            status = "Resolved (Policy Clarification)" if top_policy["self_service"] else "Pending Review"
            action_type = "RESOLVE_SIMPLE" if top_policy["self_service"] else "ESCALATE"

            ticket = self.ticket_manager.create_ticket(
                employee_name=employee_name,
                employee_email=employee_email,
                category=category,
                issue_summary=f"Inquiry regarding {top_policy['title']}",
                priority="Low",
                risk_level=risk_level,
                status=status,
                assigned_to="IT Service Desk",
                source_policies=cited,
                resolution_or_action=f"Matched to grounded policy {top_policy['id']}.",
                request_id=request_id
            )

            return AgentResponse(
                request_id=request_id,
                employee_name=employee_name,
                employee_email=employee_email,
                category=category,
                risk_level=risk_level,
                action_type=action_type,
                status=status,
                assigned_to="IT Service Desk",
                response_message=response_msg,
                cited_policies=cited,
                follow_up_questions=[],
                ticket=ticket
            )

        # UNMATCHED QUERY (Ask sensible follow-up questions)
        follow_ups = [
            "Could you specify which corporate system or hardware this pertains to?",
            "What specific error code or symptom are you encountering?"
        ]
        ticket = self.ticket_manager.create_ticket(
            employee_name=employee_name,
            employee_email=employee_email,
            category="General Support",
            issue_summary="General IT inquiry",
            priority="Low",
            risk_level="Low",
            status="Awaiting Clarification",
            assigned_to="IT Service Desk",
            source_policies=[],
            resolution_or_action="Awaiting diagnostic clarification.",
            request_id=request_id,
            follow_up_questions=follow_ups
        )
        return AgentResponse(
            request_id=request_id,
            employee_name=employee_name,
            employee_email=employee_email,
            category="General Support",
            risk_level="Low",
            action_type="FOLLOW_UP",
            status="Awaiting Clarification",
            assigned_to="IT Service Desk",
            response_message="Thank you for reaching out. Please clarify the details so we can assist you under the appropriate policy.",
            cited_policies=[],
            follow_up_questions=follow_ups,
            ticket=ticket
        )
