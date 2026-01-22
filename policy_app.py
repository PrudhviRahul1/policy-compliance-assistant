import streamlit as st
import json
from streamlit_lottie import st_lottie
from full_pipeline import run_full_pipeline

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="Policy Compliance Assistant",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===============================
# CSS
# ===============================
st.markdown("""
<style>

.stButton>button {
    background-color: #00D4FF !important;
    color: #0F172A !important;
    border-radius: 999px !important;
    padding: 14px 34px !important;
    font-weight: 600 !important;
    border: none !important;
    box-shadow: 0 0 18px rgba(0,212,255,0.6) !important;
}
.stButton>button:hover {
    background-color: #4F46E5 !important;
    color: white !important;
}

.glass-card {
    background: rgba(255,255,255,0.06);
    backdrop-filter: blur(14px);
    border-radius: 18px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.35);
    box-shadow:
        0 0 30px rgba(255,255,255,0.35),
        0 0 60px rgba(255,255,255,0.18);
    margin-bottom: 20px;
}

[data-testid="stHorizontalBlock"] > div:nth-child(2) {
    box-shadow: -4px 0 18px rgba(255,255,255,0.35);
}

[data-testid="column"]:nth-child(2) {
    max-height: 80vh;
    overflow-y: auto;
}

.risk-scale {
    display: flex;
    justify-content: space-between;
    margin-top: 12px;
}
.risk {
    flex: 1;
    text-align: center;
    padding: 10px;
    border-radius: 12px;
    margin: 0 6px;
    opacity: 0.3;
    font-weight: 600;
}
.risk.low { background: #10B981; }
.risk.medium { background: #FACC15; }
.risk.high { background: #F43F5E; }
.risk.active {
    opacity: 1;
    box-shadow: 0 0 18px rgba(255,255,255,0.4);
}

</style>
""", unsafe_allow_html=True)

# ===============================
# LOTTIE
# ===============================
def load_lottie(path):
    with open(path, "r") as f:
        return json.load(f)

lottie_scan = load_lottie("assets/scan.json")

# ===============================
# HEADER
# ===============================
st.markdown("""
<h1 style="text-align:center;">POLICY COMPLIANCE ASSISTANT</h1>
<p style="text-align:center; color:#CBD5E1;">
Analyze employee actions against organizational policy
</p>
""", unsafe_allow_html=True)

# ===============================
# PARSER (CORRECT + STABLE)
# ===============================
def parse_llm_output(text):
    parsed = {
        "prediction": "",
        "risk": "",
        "explanation": "",
        "decision": "",
        "policies": {}
    }

    lines = text.split("\n")
    mode = None
    current_policy = None

    for line in lines:
        line = line.strip()

        if line.startswith("Compliance:"):
            parsed["prediction"] = line.split(":", 1)[1].strip()

        elif line.startswith("Risk:"):
            parsed["risk"] = line.split(":", 1)[1].strip()

        elif line.startswith("Explanation:"):
            parsed["explanation"] = line.split(":", 1)[1].strip()
            mode = "explanation"

        elif line.startswith("Decision:"):
            parsed["decision"] = line.split(":", 1)[1].strip()
            mode = "decision"

        elif line.startswith("Policies:"):
            mode = "policies"

        elif mode == "explanation" and line:
            parsed["explanation"] += " " + line

        elif mode == "decision" and line:
            parsed["decision"] += " " + line

        elif mode == "policies":
            if line.startswith("-") and line.endswith(":"):
                current_policy = line.replace("-", "").replace(":", "").strip()
                parsed["policies"][current_policy] = {
                    "definition": "",
                    "clauses": []
                }

            elif line.startswith("Definition:") and current_policy:
                parsed["policies"][current_policy]["definition"] = (
                    line.split(":", 1)[1].strip()
                )

            elif line.startswith("•") and current_policy:
                parsed["policies"][current_policy]["clauses"].append(
                    line.replace("•", "").strip()
                )

    return parsed

# ===============================
# LAYOUT
# ===============================
left, right = st.columns([1, 1])

# ===============================
# LEFT PANEL
# ===============================
with left:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    scenario_text = st.text_area(
        "Enter Employee Scenario",
        height=300,
        placeholder="Example: Employee left without informing anybody"
    )

    analyze_btn = st.button("ANALYZE SCENARIO")

    st.markdown('</div>', unsafe_allow_html=True)

# ===============================
# RIGHT PANEL
# ===============================
with right:
    st.markdown(
        "<h2 style='margin-left:10px;'>Compliance Analysis</h2>",
        unsafe_allow_html=True
    )

    if analyze_btn:
        if not scenario_text.strip():
            st.error("Please enter a scenario before analysis.")
        else:
            with st.spinner("Analyzing scenario against policy..."):
                st_lottie(lottie_scan, height=180)
                result = run_full_pipeline(scenario_text)

            parsed = parse_llm_output(result["llm_output"])

            prediction = parsed["prediction"]
            risk = parsed["risk"]
            explanation = parsed["explanation"]
            decision = parsed["decision"]

            # STATUS
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown(
                f"<h3>{'❌ VIOLATION' if prediction=='Violation' else '✅ COMPLIANT'}</h3>",
                unsafe_allow_html=True
            )

            risk_lower = risk.lower()
            st.markdown(f"""
            <div class="risk-scale">
                <div class="risk low {'active' if risk_lower=='low' else ''}">Low</div>
                <div class="risk medium {'active' if risk_lower=='medium' else ''}">Medium</div>
                <div class="risk high {'active' if risk_lower=='high' else ''}">High</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # EXPLANATION
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("<h2 style='margin-left:10px;'>Explanation</h2>", unsafe_allow_html=True)
            st.write(explanation)
            st.markdown('</div>', unsafe_allow_html=True)

            # DECISION
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("<h2 style='margin-left:10px;'>Decision</h2>", unsafe_allow_html=True)
            st.write(decision)
            st.markdown('</div>', unsafe_allow_html=True)

            # POLICY CLAUSES
            with st.expander("View Relevant Policy Clauses"):
                for policy, details in parsed["policies"].items():
                    st.markdown(f"### {policy}")
                    st.markdown(f"**Definition:** {details['definition']}")
                    for clause in details["clauses"]:
                        st.markdown(f"- {clause}")
