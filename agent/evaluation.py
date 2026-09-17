"""
Evaluation and Benchmark Module for Veridian Corp IT Support Agent.
Tests the agent across all 15 benchmark employee requests (REQ-01 to REQ-15)
and active tickets in the ticket queue (TK-1042 to TK-1051).
"""

from typing import Dict, List, Any
from agent.core_agent import InternalServiceAgent
from agent.ticket_system import TicketManager
from agent.data_loader import EMPLOYEE_REQUESTS, TICKET_QUEUE_RECORDS


def run_benchmark_evaluation() -> Dict[str, Any]:
    """
    Executes all 15 employee requests and active queue items.
    Returns quantitative metrics and detailed evaluation logs.
    """
    tm = TicketManager()
    agent = InternalServiceAgent(ticket_manager=tm)
    
    results = []
    total = len(EMPLOYEE_REQUESTS)
    passed_policy = 0
    passed_risk = 0
    passed_action = 0

    for req in EMPLOYEE_REQUESTS:
        response = agent.process_request(
            query=req["request"],
            employee_name=req["employee"],
            employee_email=req["email"],
            request_id=req["id"]
        )

        # Policy citation check
        expected_kbs = req.get("expected_kb", [])
        if not expected_kbs:
            # For ambiguous requests like REQ-15, no KB is expected until clarified
            policy_match = (len(response.cited_policies) == 0)
        else:
            policy_match = any(kb in response.cited_policies for kb in expected_kbs)

        if policy_match:
            passed_policy += 1

        # Check sensible follow-up questions
        has_follow_ups = len(response.follow_up_questions) > 0

        # Check ticket and audit trail
        has_ticket = response.ticket is not None
        audit_events = tm.get_audit_trail(response.ticket.ticket_id if response.ticket else None)

        record = {
            "request_id": req["id"],
            "employee": req["employee"],
            "request_text": req["request"],
            "category": response.category,
            "risk_level": response.risk_level,
            "action_type": response.action_type,
            "status": response.status,
            "assigned_to": response.assigned_to,
            "cited_policies": response.cited_policies,
            "expected_policies": expected_kbs,
            "policy_match": policy_match,
            "follow_up_questions": response.follow_up_questions,
            "ticket_id": response.ticket.ticket_id if response.ticket else None,
            "audit_count": len(audit_events),
            "response_snippet": response.response_message[:140] + "..."
        }
        results.append(record)

    # Evaluate Active Tickets from Section 3
    active_tickets = [t for t in TICKET_QUEUE_RECORDS if t.get("is_active")]
    active_evaluations = []
    for at in active_tickets:
        # Evaluate how the agent reasons about these active cases
        sample_response = agent.process_request(
            query=at["issue_summary"],
            employee_name=at["employee"],
            employee_email=f"{at['employee'].lower().replace(' ', '.')}@veridian-corp.example",
            request_id=f"QUEUE-{at['ticket_id']}"
        )
        active_evaluations.append({
            "original_ticket_id": at["ticket_id"],
            "employee": at["employee"],
            "issue_summary": at["issue_summary"],
            "original_status": at["status"],
            "agent_recommended_action": sample_response.action_type,
            "agent_assigned_to": sample_response.assigned_to,
            "cited_policies": sample_response.cited_policies,
            "precedent_matched": at["precedent_note"]
        })

    summary = {
        "total_requests_tested": total,
        "policy_grounding_accuracy": round((passed_policy / total) * 100, 1),
        "tickets_created": len(tm.get_all_tickets()),
        "total_audit_events": len(tm.audit_log),
        "results": results,
        "active_queue_evaluations": active_evaluations
    }
    return summary


if __name__ == "__main__":
    print("=" * 80)
    print("VERIDIAN CORP IT SERVICE AGENT - BENCHMARK EVALUATION")
    print("=" * 80)
    eval_summary = run_benchmark_evaluation()
    print(f"Total Requests Evaluated: {eval_summary['total_requests_tested']}")
    print(f"Policy Grounding Accuracy: {eval_summary['policy_grounding_accuracy']}%")
    print(f"Structured Tickets Created: {eval_summary['tickets_created']}")
    print(f"Total Audit Trail Entries: {eval_summary['total_audit_events']}")
    print("-" * 80)
    for r in eval_summary["results"]:
        status_symbol = "PASS" if r["policy_match"] else "FAIL"
        print(f"[{status_symbol}] {r['request_id']} | {r['employee']} | Risk: {r['risk_level']:<8} | Action: {r['action_type']:<15} | Policies: {r['cited_policies']} (Expected: {r['expected_policies']})")
    print("=" * 80)
