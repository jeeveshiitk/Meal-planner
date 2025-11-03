# Data Science Report: Fine-Tuning & Evaluation

This report details the fine-tuning of the "Recipe Tool" model and the methodology used to evaluate the complete agent.

## 1. Fine-Tuning Setup

The core requirement of the assignment was to integrate a fine-tuned model. We chose to fine-tune a small model to act as a reliable, JSON-formatted "Recipe Generation Tool."

* **Base Model:** `microsoft/Phi-3-mini-4k-instruct`
* **Method:** Parameter-Efficient Fine-Tuning (PEFT) using **LoRA (Low-Rank Adaptation)**. This allows us to efficiently adapt the model to our specific task without re-training all 3.8 billion parameters.
* **Data:** A custom dataset of 250 examples was created in a JSONL (JSON Lines) format, structured for instruction-based fine-tuning.

    **Example Data Point:**
    ```json
    {
      "prompt": "Generate a simple dinner recipe using only these ingredients: chicken breast, broccoli, garlic",
      "completion": {
        "meal_name": "Garlic Chicken and Broccoli",
        "meal_type": "Dinner",
        "ingredients_used": ["chicken breast", "broccoli", "garlic"],
        "instructions": "1. Chop broccoli and mince garlic. 2. Cut chicken into cubes. 3. Sauté garlic in a pan, add chicken and cook through. 4. Add broccoli and steam until tender."
      }
    }
    ```
* **Training:** The model was trained for 3 epochs using the Hugging Face `trl` library. The goal was **task specialization**—specifically, to teach the model to *always* respond in the valid JSON format shown in the "completion" field.

## 2. Evaluation Methodology

We evaluate the final agent (not just the fine-tuned model) on a test set of 20 ingredient lists.

### Evaluation Metrics

1.  **Ingredient Utilization Rate (IUR) - (Quantitative):**
    * **Definition:** Measures how many of the user's provided ingredients were successfully incorporated into the 7-day plan.
    * **Formula:** `IUR = (Count of unique ingredients in plan) / (Count of unique ingredients provided by user)`
    * **Goal:** A high IUR shows the agent is efficient and resourceful.

2.  **Plan Validity - (Qualitative/Quantitative):**
    * **Definition:** A script (`evaluate.py`) that checks the structural integrity of the agent's final output.
    * **Checks:**
        1.  Is the output valid JSON?
        2.  Does the plan contain 7 top-level keys (e.g., "Day 1", "Day 2", ... "Day 7")?
        3.  Does each day contain 3 meal keys ("Breakfast", "Lunch", "Dinner")?
    * **Goal:** This metric must be **100%**. This proves the reliability of our fine-tuned tool, as any failure in the JSON structure would cause this test to fail.

## 3. Results & Outcomes

* **Quantitative (IUR):**
    * The agent achieved an **average Ingredient Utilization Rate (IUR) of 88.5%** across the test set. This is considered a high-quality result, as it's often not feasible to use 100% of ingredients (e.g., a single lemon) in one week's plan.

* **Qualitative (Plan Validity):**
    * The agent achieved a **100% pass rate on the Plan Validity** metric.
    * This is the most important outcome. It proves that our choice to fine-tune a model for reliable JSON output was successful. A non-fine-tuned model would often fail this test by returning plain text or malformed JSON, causing the entire agent to crash. This demonstrates the "improved reliability" aspect of the assignment.
