"""
Structured Ticket System and Immutable Audit Trail for Veridian Corp IT Support.
Fulfills requirements:
- Create a structured ticket
- Show the source used for its answer
- Maintain an audit trail
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Any


class AuditEvent:
    """Represents a single immutable audit event in the support lifecycle."""
    def __init__(
        self,
        event_id: str,
        timestamp: str,
        ticket_id: Optional[str],
        request_id: Optional[str],
        event_type: str,
        actor: str,
        details: str,
        source_used: Optional[str] = None
    ):
        self.event_id = event_id
        self.timestamp = timestamp
        self.ticket_id = ticket_id
        self.request_id = request_id
        self.event_type = event_type
        self.actor = actor
        self.details = details
        self.source_used = source_used

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "timestamp": self.timestamp,
            "ticket_id": self.ticket_id,
            "request_id": self.request_id,
            "event_type": self.event_type,
            "actor": self.actor,
            "details": self.details,
            "source_used": self.source_used
        }


class StructuredTicket:
    """Represents a formal IT Support Ticket with policy grounding and audit linkage."""
    def __init__(
        self,
        ticket_id: str,
        request_id: Optional[str],
        employee_name: str,
        employee_email: str,
        category: str,
        issue_summary: str,
        priority: str,
        risk_level: str,
        status: str,
        assigned_to: str,
        source_policies: List[str],
        resolution_or_action: str,
        follow_up_questions: Optional[List[str]] = None,
        created_at: Optional[str] = None
    ):
        self.ticket_id = ticket_id
        self.request_id = request_id
        self.employee_name = employee_name
        self.employee_email = employee_email
        self.category = category
        self.issue_summary = issue_summary
        self.priority = priority
        self.risk_level = risk_level
        self.status = status
        self.assigned_to = assigned_to
        self.source_policies = source_policies
        self.resolution_or_action = resolution_or_action
        self.follow_up_questions = follow_up_questions or []
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated_at = self.created_at

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ticket_id": self.ticket_id,
            "request_id": self.request_id,
            "employee_name": self.employee_name,
            "employee_email": self.employee_email,
            "category": self.category,
            "issue_summary": self.issue_summary,
            "priority": self.priority,
            "risk_level": self.risk_level,
            "status": self.status,
            "assigned_to": self.assigned_to,
            "source_policies": self.source_policies,
            "resolution_or_action": self.resolution_or_action,
            "follow_up_questions": self.follow_up_questions,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


class TicketManager:
    """Manages active tickets and appends to an immutable audit trail."""
    def __init__(self):
        self.tickets: Dict[str, StructuredTicket] = {}
        self.audit_log: List[AuditEvent] = []
        self._next_ticket_num: int = 1052
        self._next_event_num: int = 1

    def generate_ticket_id(self) -> str:
        ticket_id = f"TK-{self._next_ticket_num}"
        self._next_ticket_num += 1
        return ticket_id

    def log_audit(
        self,
        event_type: str,
        details: str,
        ticket_id: Optional[str] = None,
        request_id: Optional[str] = None,
        actor: str = "Agent:Veridian-IT",
        source_used: Optional[str] = None
    ) -> AuditEvent:
        event_id = f"EVT-{self._next_event_num:05d}"
        self._next_event_num += 1
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        event = AuditEvent(
            event_id=event_id,
            timestamp=timestamp,
            ticket_id=ticket_id,
            request_id=request_id,
            event_type=event_type,
            actor=actor,
            details=details,
            source_used=source_used
        )
        self.audit_log.append(event)
        return event

    def create_ticket(
        self,
        employee_name: str,
        employee_email: str,
        category: str,
        issue_summary: str,
        priority: str,
        risk_level: str,
        status: str,
        assigned_to: str,
        source_policies: List[str],
        resolution_or_action: str,
        request_id: Optional[str] = None,
        follow_up_questions: Optional[List[str]] = None,
        custom_ticket_id: Optional[str] = None
    ) -> StructuredTicket:
        ticket_id = custom_ticket_id if custom_ticket_id else self.generate_ticket_id()
        
        ticket = StructuredTicket(
            ticket_id=ticket_id,
            request_id=request_id,
            employee_name=employee_name,
            employee_email=employee_email,
            category=category,
            issue_summary=issue_summary,
            priority=priority,
            risk_level=risk_level,
            status=status,
            assigned_to=assigned_to,
            source_policies=source_policies,
            resolution_or_action=resolution_or_action,
            follow_up_questions=follow_up_questions
        )
        self.tickets[ticket_id] = ticket

        # Create audit entry for ticket creation
        source_str = ", ".join(source_policies) if source_policies else "N/A"
        self.log_audit(
            event_type="TICKET_CREATED",
            details=f"Structured ticket {ticket_id} created with status '{status}' and risk '{risk_level}'. Assigned to {assigned_to}.",
            ticket_id=ticket_id,
            request_id=request_id,
            source_used=source_str
        )
        return ticket

    def get_ticket(self, ticket_id: str) -> Optional[StructuredTicket]:
        return self.tickets.get(ticket_id)

    def get_all_tickets(self) -> List[StructuredTicket]:
        return list(self.tickets.values())

    def get_audit_trail(self, ticket_id: Optional[str] = None) -> List[AuditEvent]:
        if ticket_id:
            return [evt for evt in self.audit_log if evt.ticket_id == ticket_id]
        return self.audit_log

    def reset(self):
        """Reset tickets and audit logs."""
        self.tickets.clear()
        self.audit_log.clear()
        self._next_ticket_num = 1052
        self._next_event_num = 1
