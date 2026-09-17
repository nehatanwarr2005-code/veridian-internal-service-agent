"""
Unit Tests for Veridian Corp IT Support Agent.
Tests policy grounding, risk classification, sensible follow-ups, and ticket/audit integrity.
"""

import unittest
from agent.knowledge_base import KNOWLEDGE_BASE, get_policy, search_knowledge_base
from agent.ticket_system import TicketManager
from agent.core_agent import InternalServiceAgent
from agent.data_loader import EMPLOYEE_REQUESTS, TICKET_QUEUE_RECORDS


class TestInternalServiceAgent(unittest.TestCase):

    def setUp(self):
        self.tm = TicketManager()
        self.agent = InternalServiceAgent(ticket_manager=self.tm)

    def test_knowledge_base_integrity(self):
        """Ensure all 10 policies and Asset Management Policy extract are present."""
        expected_ids = ["KB-01", "KB-02", "KB-03", "KB-04", "KB-05", "KB-06", "KB-07", "KB-08", "KB-09", "KB-10", "ASSET-POL"]
        for pid in expected_ids:
            policy = get_policy(pid)
            self.assertIsNotNone(policy, f"Policy {pid} missing from Knowledge Base")
            self.assertTrue(len(policy["text"]) > 20)
            self.assertTrue(len(policy["rules"]) > 0)

    def test_critical_security_phishing_escalation(self):
        """Test REQ-08: Phishing forwarding must trigger Critical alert and KB-09 citation."""
        req = next(r for r in EMPLOYEE_REQUESTS if r["id"] == "REQ-08")
        resp = self.agent.process_request(
            query=req["request"],
            employee_name=req["employee"],
            employee_email=req["email"],
            request_id=req["id"]
        )
        self.assertEqual(resp.risk_level, "Critical")
        self.assertEqual(resp.action_type, "ESCALATE")
        self.assertIn("KB-09", resp.cited_policies)
        self.assertIn("DO NOT forward", resp.response_message)
        self.assertIsNotNone(resp.ticket)
        self.assertEqual(resp.ticket.priority, "Critical")

    def test_admin_privilege_escalation(self):
        """Test REQ-10: Unauthorized admin access to finance reporting server."""
        req = next(r for r in EMPLOYEE_REQUESTS if r["id"] == "REQ-10")
        resp = self.agent.process_request(
            query=req["request"],
            employee_name=req["employee"],
            employee_email=req["email"],
            request_id=req["id"]
        )
        self.assertEqual(resp.risk_level, "High")
        self.assertEqual(resp.action_type, "ESCALATE")
        self.assertIn("KB-08", resp.cited_policies)
        self.assertEqual(resp.precedent_cited, "TK-1050")

    def test_ambiguous_request_sensible_follow_up(self):
        """Test REQ-15: Underspecified request triggers diagnostic questions."""
        req = next(r for r in EMPLOYEE_REQUESTS if r["id"] == "REQ-15")
        resp = self.agent.process_request(
            query=req["request"],
            employee_name=req["employee"],
            employee_email=req["email"],
            request_id=req["id"]
        )
        self.assertEqual(resp.action_type, "FOLLOW_UP")
        self.assertTrue(len(resp.follow_up_questions) >= 2)
        self.assertEqual(len(resp.cited_policies), 0)  # No premature policy citation

    def test_simple_self_service_wifi(self):
        """Test REQ-02: Guest Wi-Fi access resolved immediately without ticket required."""
        req = next(r for r in EMPLOYEE_REQUESTS if r["id"] == "REQ-02")
        resp = self.agent.process_request(
            query=req["request"],
            employee_name=req["employee"],
            employee_email=req["email"],
            request_id=req["id"]
        )
        self.assertEqual(resp.action_type, "RESOLVE_SIMPLE")
        self.assertIn("KB-07", resp.cited_policies)
        self.assertIn("front-desk kiosk", resp.response_message)

    def test_ticket_and_audit_trail_consistency(self):
        """Verify that every processed request records an immutable audit log."""
        initial_log_count = len(self.tm.audit_log)
        resp = self.agent.process_request(
            query="Can I get Wi-Fi access for a guest?",
            employee_name="Test User",
            employee_email="test.user@veridian-corp.example"
        )
        self.assertIsNotNone(resp.ticket)
        self.assertGreater(len(self.tm.audit_log), initial_log_count)
        
        ticket_events = self.tm.get_audit_trail(resp.ticket.ticket_id)
        self.assertTrue(any(e.event_type == "TICKET_CREATED" for e in ticket_events))
        self.assertTrue(any(e.event_type == "RESOLVED_SELF_SERVICE" for e in ticket_events))


if __name__ == "__main__":
    unittest.main()
