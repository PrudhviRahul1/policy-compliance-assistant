import os
print(os.getenv("OPENAI_API_KEY"))


# testing code ------------ for LLM explanation.

#if __name__ == "__main__":
#    test_scenario = "Employee took 10 days leave without prior approval"
#    test_prediction = "Violation"
#    test_risk = "High"
#    test_clauses = [
#        "Casual Leave is limited to a maximum of 10 days in a calendar year.",
#        "Leave without approval may result in disciplinary action."
#    ]
#
#    explanation = generate_explanation(
#        test_scenario,
#        test_prediction,
#        test_risk,
#        test_clauses
#    )
#
#    print("Generated Explanation:\n")
#    print(explanation)
#