"""
Veridian Corp - Internal Service Agent (IT Support)
AIONOS Assignment 2 - Clickable Working Prototype
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from agent.core_agent import InternalServiceAgent
from agent.ticket_system import TicketManager
from agent.knowledge_base import list_all_policies, get_policy
from agent.data_loader import EMPLOYEE_REQUESTS, TICKET_QUEUE_RECORDS
from agent.evaluation import run_benchmark_evaluation

# Streamlit Page Configuration
st.set_page_config(
    page_title="Veridian Corp - IT Support Agent",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling for sleek, modern corporate appearance
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        color: white;
        padding: 24px;
        border-radius: 12px;
        margin-bottom: 24px;
        border-left: 6px solid #06B6D4;
    }
    .badge-critical {
        background-color: #EF4444;
        color: white;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 12px;
    }
    .badge-high {
        background-color: #F59E0B;
        color: white;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 12px;
    }
    .badge-medium {
        background-color: #3B82F6;
        color: white;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 12px;
    }
    .badge-low {
        background-color: #10B981;
        color: white;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 12px;
    }
    .policy-tag {
        background-color: #334155;
        color: #38BDF8;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: bold;
        margin-right: 5px;
    }
    .card-box {
        background-color: #1E293B;
        color: #F8FAFC;
        padding: 16px;
        border-radius: 8px;
        border: 1px solid #334155;
        margin-bottom: 16px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "ticket_manager" not in st.session_state:
    st.session_state.ticket_manager = TicketManager()

if "agent" not in st.session_state:
    st.session_state.agent = InternalServiceAgent(ticket_manager=st.session_state.ticket_manager)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

agent = st.session_state.agent
tm = st.session_state.ticket_manager

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/support.png", width=90)
    st.title("Veridian Corp IT")
    st.caption("Internal Service Desk Intelligence")
    st.markdown("**Context Window**: 21–25 Sep 2026")
    st.markdown("**Version**: 1.0.0 (AIONOS Prototype)")
    st.divider()
    
    st.markdown("### 📌 Quick Navigation")
    menu = st.radio(
        "Select View:",
        [
            "💬 Interactive Agent Chat",
            "📊 Batch Requests (REQ 01-15)",
            "🎫 Ticket Queue & Precedents",
            "📜 Immutable Audit Trail",
            "📚 Knowledge Base Explorer",
            "📑 Presentation & Deliverables"
        ]
    )
    
    st.divider()
    st.markdown("### ⚙️ System Controls")
    if st.button("🔄 Reset Agent State & Logs"):
        tm.reset()
        st.session_state.chat_history = []
        st.success("Agent state reset successfully!")
        st.rerun()

# Main Header Banner
st.markdown("""
<div class="main-header">
    <h2 style="margin:0; padding:0; color:#FFFFFF;">🛡️ Veridian Corp — Autonomous IT Service Agent</h2>
    <p style="margin:4px 0 0 0; color:#94A3B8; font-size:14px;">
        Strictly Grounded IT Support Intelligence | Zero Hallucination | Automated Triage, Escalation & Ticketing
    </p>
</div>
""", unsafe_allow_html=True)


# ==============================================================================
# VIEW 1: Interactive Agent Chat
# ==============================================================================
if menu == "💬 Interactive Agent Chat":
    st.subheader("💬 Live Support Assistant")
    st.write("Chat with the IT agent in real-time, or load any official request from the assignment data pack.")

    # Quick test selector
    col_sel, col_btn = st.columns([4, 1])
    with col_sel:
        preset_options = ["-- Select Official Benchmark Request --"] + [
            f"{r['id']}: {r['employee']} — {r['request'][:55]}..." for r in EMPLOYEE_REQUESTS
        ]
        selected_preset = st.selectbox("Quick Load Official Request:", preset_options)

    prefill_text = ""
    preset_employee = "Employee"
    preset_email = "employee@veridian-corp.example"
    preset_req_id = None

    if selected_preset and selected_preset != "-- Select Official Benchmark Request --":
        req_id = selected_preset.split(":")[0].strip()
        matched_req = next((r for r in EMPLOYEE_REQUESTS if r["id"] == req_id), None)
        if matched_req:
            prefill_text = matched_req["request"]
            preset_employee = matched_req["employee"]
            preset_email = matched_req["email"]
            preset_req_id = matched_req["id"]

    # Input Form
    with st.form("chat_form", clear_on_submit=False):
        c1, c2 = st.columns(2)
        with c1:
            emp_name = st.text_input("Employee Name:", value=preset_employee)
        with c2:
            emp_email = st.text_input("Employee Email:", value=preset_email)

        user_query = st.text_area(
            "Describe your IT issue or question:",
            value=prefill_text,
            height=90,
            placeholder="e.g. My laptop won't turn on, or Can I get guest Wi-Fi access tomorrow?"
        )
        submitted = st.form_submit_button("🚀 Submit Request to Agent")

    if submitted and user_query.strip():
        with st.spinner("Processing through grounded policy engine..."):
            response = agent.process_request(
                query=user_query,
                employee_name=emp_name,
                employee_email=emp_email,
                request_id=preset_req_id
            )
            st.session_state.chat_history.append((user_query, response))

    # Display Chat Interaction History
    if st.session_state.chat_history:
        st.divider()
        st.markdown("### Conversation History & Structured Decisions")

        for query, resp in reversed(st.session_state.chat_history):
            with st.container():
                # Risk badge formatting
                risk_badge = f"<span class='badge-{resp.risk_level.lower()}'>{resp.risk_level.upper()} RISK</span>"
                
                # Header card
                st.markdown(f"""
                <div style="background-color:#1E293B; padding:12px; border-radius:8px; border:1px solid #334155; margin-bottom:8px;">
                    <strong>👤 {resp.employee_name}</strong> ({resp.employee_email}) &nbsp;|&nbsp; 
                    <strong>Category:</strong> {resp.category} &nbsp;|&nbsp; 
                    {risk_badge} &nbsp;|&nbsp;
                    <strong>Action:</strong> <code>{resp.action_type}</code>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"**Query:** *\"{query}\"*")

                # Response message
                st.markdown(resp.response_message)

                # Follow up questions
                if resp.follow_up_questions:
                    st.warning("⚠️ **Diagnostic Follow-up Questions Required:**")
                    for i, q in enumerate(resp.follow_up_questions, 1):
                        st.markdown(f"- **Q{i}**: {q}")

                # Policy and ticket info cards
                cols = st.columns([2, 2, 2])
                with cols[0]:
                    if resp.cited_policies:
                        st.markdown("**Grounded Policies Cited:**")
                        tags = " ".join([f"<span class='policy-tag'>{p}</span>" for p in resp.cited_policies])
                        st.markdown(tags, unsafe_allow_html=True)
                    else:
                        st.info("No policy cited yet (Awaiting clarification)")

                with cols[1]:
                    if resp.precedent_cited:
                        st.markdown(f"**Precedent Matched:** <code>{resp.precedent_cited}</code>")
                    else:
                        st.markdown("**Precedent:** Standard Policy Execution")

                with cols[2]:
                    if resp.ticket:
                        st.success(f"🎫 **Ticket Logged:** `{resp.ticket.ticket_id}` ({resp.ticket.status})")

                st.divider()


# ==============================================================================
# VIEW 2: Batch Requests (REQ 01 - 15)
# ==============================================================================
elif menu == "📊 Batch Requests (REQ 01-15)":
    st.subheader("📊 Official Employee Requests Benchmark (REQ-01 to REQ-15)")
    st.write("Execute all 15 official test cases from Section 2 of the assignment data pack to verify policy grounding, risk scoring, and ticket generation.")

    if st.button("⚡ Run Full Benchmark Across All 15 Requests"):
        with st.spinner("Evaluating all 15 requests..."):
            benchmark_data = run_benchmark_evaluation()
            st.session_state["benchmark_data"] = benchmark_data
            st.success("Benchmark completed successfully!")

    # Display benchmark results if available
    bdata = st.session_state.get("benchmark_data", None)
    if bdata:
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Requests Tested", bdata["total_requests_tested"])
        m2.metric("Policy Grounding Accuracy", f"{bdata['policy_grounding_accuracy']}%")
        m3.metric("Tickets Created", bdata["tickets_created"])
        m4.metric("Audit Trail Events", bdata["total_audit_events"])

        st.markdown("### Benchmark Results Matrix")
        table_rows = []
        for r in bdata["results"]:
            table_rows.append({
                "ID": r["request_id"],
                "Employee": r["employee"],
                "Request Snippet": r["request_text"][:45] + "...",
                "Category": r["category"],
                "Risk": r["risk_level"],
                "Action": r["action_type"],
                "Policies Cited": ", ".join(r["cited_policies"]) if r["cited_policies"] else "None (Follow-up)",
                "Expected Policies": ", ".join(r["expected_policies"]) if r["expected_policies"] else "None",
                "Match": "✅ PASS" if r["policy_match"] else "❌ FAIL",
                "Ticket ID": r["ticket_id"]
            })
        st.dataframe(pd.DataFrame(table_rows), use_container_width=True)

        st.markdown("### Active Ticket Queue Re-evaluations")
        st.dataframe(pd.DataFrame(bdata["active_queue_evaluations"]), use_container_width=True)
    else:
        st.info("Click the button above to run the 15-request benchmark suite.")
        # Show raw requests
        st.markdown("#### Official Requests in Data Pack:")
        df_raw = pd.DataFrame(EMPLOYEE_REQUESTS)[["id", "employee", "date_opened", "request", "initial_action"]]
        st.dataframe(df_raw, use_container_width=True)


# ==============================================================================
# VIEW 3: Ticket Queue & Precedents
# ==============================================================================
elif menu == "🎫 Ticket Queue & Precedents":
    st.subheader("🎫 Veridian Corp Ticket Queue Management")
    st.write("Tracks historical precedent cases (TK-1042 to TK-1051) and newly generated tickets from the current session.")

    tab_active, tab_hist, tab_new = st.tabs(["Active Cases from Queue", "Historical Precedent Archive (Closed)", "Newly Generated Tickets"])

    with tab_active:
        st.markdown("#### Open Tickets Requiring SLA Action:")
        active_tickets = [t for t in TICKET_QUEUE_RECORDS if t["is_active"]]
        st.dataframe(pd.DataFrame(active_tickets), use_container_width=True)

    with tab_hist:
        st.markdown("#### Closed Tickets (Used for Precedent & Consistency Reasoning):")
        hist_tickets = [t for t in TICKET_QUEUE_RECORDS if not t["is_active"]]
        st.dataframe(pd.DataFrame(hist_tickets), use_container_width=True)

    with tab_new:
        st.markdown("#### Newly Created Tickets in Current Session:")
        created_tickets = tm.get_all_tickets()
        if created_tickets:
            t_data = [t.to_dict() for t in created_tickets]
            st.dataframe(pd.DataFrame(t_data), use_container_width=True)
        else:
            st.info("No new tickets created in this session yet. Interact with the chat or run the batch benchmark.")


# ==============================================================================
# VIEW 4: Immutable Audit Trail
# ==============================================================================
elif menu == "📜 Immutable Audit Trail":
    st.subheader("📜 Enterprise Immutable Audit Ledger")
    st.write("Chronological, tamper-evident log of all agent actions, policy citations, and routing transitions.")

    audit_logs = tm.get_audit_trail()
    if audit_logs:
        df_audit = pd.DataFrame([e.to_dict() for e in audit_logs])
        st.dataframe(df_audit, use_container_width=True)
        
        st.download_button(
            label="📥 Export Audit Trail (CSV)",
            data=df_audit.to_csv(index=False),
            file_name=f"veridian_audit_trail_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    else:
        st.info("No audit logs recorded yet. Send a request in the chat to see events logged in real-time.")


# ==============================================================================
# VIEW 5: Knowledge Base Explorer
# ==============================================================================
elif menu == "📚 Knowledge Base Explorer":
    st.subheader("📚 Grounded Knowledge Base & Governance Policies")
    st.write("All responses are strictly grounded in the following approved policies. No ungrounded policies exist in this system.")

    policies = list_all_policies()
    search_q = st.text_input("🔍 Search Knowledge Base:", "")

    for pol in policies:
        if not search_q or search_q.lower() in pol["title"].lower() or search_q.lower() in pol["text"].lower():
            with st.expander(f"📌 {pol['id']}: {pol['title']} ({pol['category']})"):
                st.markdown(f"**Policy Text:**\n\n> {pol['text']}")
                st.markdown("**Key Rules & Constraints:**")
                for r in pol["rules"]:
                    st.markdown(f"- {r}")
                st.markdown(f"• **Approval Requirement:** `{pol['requires_approval']}`")
                st.markdown(f"• **Self-Service Support:** `{pol['self_service']}`")
                st.markdown(f"• **Escalation Trigger:** `{pol['escalate_if']}`")


# ==============================================================================
# VIEW 6: Presentation & Deliverables
# ==============================================================================
elif menu == "📑 Presentation & Deliverables":
    st.subheader("📑 Submission Deliverables & 10-Slide Deck")
    st.markdown("""
    This project fulfills all mandatory submission criteria for AIONOS Assignment 2:
    1. **GitHub Repository Codebase** with modular architecture, unit tests, and runner.
    2. **Clickable Working Prototype** (this Streamlit application).
    3. **10-Slide PowerPoint Presentation** (`AIONOS_Assignment2_Internal_Service_Agent.pptx`).
    4. **Demo Video Recording Script** (`demo_video_script.md`) for Google Drive upload.
    """)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 📊 10-Slide Presentation (.pptx)")
        try:
            with open("AIONOS_Assignment2_Internal_Service_Agent.pptx", "rb") as f:
                st.download_button(
                    label="📥 Download 10-Slide PPTX Presentation",
                    data=f.read(),
                    file_name="AIONOS_Assignment2_Internal_Service_Agent.pptx",
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                )
        except Exception as e:
            st.warning("Run `python generate_presentation.py` to regenerate the presentation.")

    with c2:
        st.markdown("#### 🎬 Demo Video Guide")
        st.info("Follow `demo_video_script.md` for the exact 3-5 minute spoken narration and screen recording guide.")
