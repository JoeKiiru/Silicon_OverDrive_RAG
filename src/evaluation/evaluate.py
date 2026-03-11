import json
import csv
from sentence_transformers import CrossEncoder
from src.generation import llm_rag_generation_documents

# Load a model trained for NLI (Natural Language Inference)
# Scores for Contradiction, Neutral, and Entailment
print("Loading Faithfulness evaluator...")
nli_model = CrossEncoder('cross-encoder/nli-deberta-v3-small')

def main():
    with open('src/evaluation/sample_queries.json', 'r') as f:
        qa_pairs = json.load(f)

    results = []
    
    for item in qa_pairs:
        query = item['query']
        context = item['ground_truth'] 
        
        generated_answer = str(llm_rag_generation_documents(query))

        # Evaluating Faithfulness (Does the context entail the answer?)
        # Labels: 0: contradiction, 1: neutral, 2: entailment
        # The higher the entailment score, the more confident 
        # that the context generated from RAG is faithful based on the ground truth
        scores = nli_model.predict([(context, generated_answer)])
        faithfulness_score = scores[0][2] # The 'Entailment' probability

        results.append({
            "Query": query,
            "Context": context,
            "Generated Answer": generated_answer,
            "Faithfulness Score": round(float(faithfulness_score), 4)
        })

    # Save to CSV
    with open('src/evaluation/evaluation_results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["Query", "Context", "Generated Answer", "Faithfulness Score"])
        writer.writeheader()
        writer.writerows(results)

    print("Evaluation saved to evaluation_results.csv")

if __name__ == "__main__":
    main()
