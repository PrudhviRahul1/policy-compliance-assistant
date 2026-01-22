import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from llm_explanation import generate_decision

# Load policy clauses
policy_df = pd.read_excel("Data/policy_clauses_cleaned.xlsx")


policy_texts = policy_df["clause"].tolist()

policy_vectorizer = TfidfVectorizer(stop_words="english")
policy_vectors = policy_vectorizer.fit_transform(policy_texts)

def retrieve_policy_clauses(scenario_text, top_k=6):
    scenario_vec = policy_vectorizer.transform([scenario_text])
    similarity = cosine_similarity(scenario_vec, policy_vectors)[0]

    top_indices = similarity.argsort()[-top_k:][::-1]

    return policy_df.iloc[top_indices][["policy_type", "clause"]].to_dict(orient="records")

def run_full_pipeline(scenario_text):
    # 1. Retrieve relevant policies
    clauses = retrieve_policy_clauses(scenario_text)

    # 2. LLM decides everything
    llm_output = generate_decision(
        scenario=scenario_text,
        policy_clauses=clauses
    )

    return {
        "scenario": scenario_text,
        "policy_clauses": clauses,
        "llm_output": llm_output
    }
