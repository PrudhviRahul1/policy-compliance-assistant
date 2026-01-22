from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_decision(scenario, policy_clauses):
    formatted_clauses = "\n".join(
        [f"[{c['policy_type']}] {c['clause']}" for c in policy_clauses]
    )

    prompt = f"""
You are an HR Compliance Expert.

Scenario:
\"\"\"{scenario}\"\"\"

Relevant Policy Clauses (with policy type):
{formatted_clauses}

Tasks:
1. Decide Compliance: Compliant or Violation
2. Decide Risk Level: Low / Medium / High
3. Provide a short explanation (2–3 lines, plain English)
4. Provide an HR decision/action
5. Group the relevant clauses by policy type and:
   - Give a one-line definition for each policy
   - List only the clauses that apply to this scenario

Rules:
- Do NOT include unrelated policies
- If a policy does not apply, exclude it entirely
- Be precise and fair
- Consider negation and intent carefully

Return output STRICTLY in this format:

Compliance: ...
Risk: ...

Explanation: ...

Decision: ...

Policies:
- Policy Name:
  Definition: ...
  Clauses:
    • ...
    • ...
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content
