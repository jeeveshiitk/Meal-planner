# AI Agent Prototype: The Auto-Planner

* **Name:** Jeevesh Narayan
* **University:** IIT Kanpur
* **Department:** Civil Engineering

## Project Overview

This project is an AI agent that automates the task of weekly meal planning. The user provides a list of available ingredients, and the agent **reasons**, **plans**, and **executes** to generate a complete 7-day meal plan (breakfast, lunch, and dinner).

The core of this agent uses a mandatory **fine-tuned model** as a specialized "Recipe Generation Tool" to ensure all generated meals are structured, reliable, and relevant to the user's ingredients.

## Architecture

The agent uses a "Planner + Tool" design pattern.

* **Planner (Main Agent):** A general-purpose LLM that manages the overall task. It breaks down the "7-day plan" request into 21 smaller "generate meal" steps. It tracks which ingredients have been used and tries to distribute them logically.
* **Recipe Tool (Fine-Tuned Model):** A `microsoft/Phi-3-mini` model fine-tuned with LoRA on a custom dataset of recipes. This tool's specific task is to receive a list of ingredients (e.g., `["chicken", "rice"]`) and return a single, valid JSON object for a meal.

For a complete breakdown, please see the `AI_Agent_Architecture.md` document.

## Data Science & Evaluation

The fine-tuning and evaluation process is detailed in the `Data_Science_Report.md`.
* **Fine-Tuning:** A LoRA fine-tune was performed to specialize a small model for reliable JSON output for recipes.
* **Evaluation:** The agent is evaluated on two primary metrics:
    1.  **Ingredient Utilization Rate (IUR):** The percentage of provided ingredients used in the final plan.
    2.  **Plan Validity:** A script that validates the structural integrity of the 7-day plan (e.g., correct JSON format, 7 days, 3 meals per day).

## How to Run

1.  **Clone the repository:**
    ```bash
    git clone [Your_Repo_URL]
    cd [Your_Repo_Name]
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r src/requirements.txt
    ```
3.  **Run the agent:**
    *(Note: This requires a working Python environment and API keys for an LLM service, which you must set as environment variables.)*
    ```bash
    python src/agent.py --ingredients "chicken, rice, broccoli, eggs, milk, bread, spinach, tomatoes, onion"
    ```
4.  **Run the evaluation:**
    ```bash
    python src/evaluate.py
    ```
