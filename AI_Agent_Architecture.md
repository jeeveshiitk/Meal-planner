# AI Agent Architecture Document

## 1. Components

This agent is built using a "Planner + Tool" architecture, a common AI agent design pattern.

1.  **Planner (Main Agent):**
    * **Model:** A general-purpose, reasoning-capable LLM (e.g., `Gemini-Pro`, `GPT-4o-mini`).
    * **Role:** This is the "brain" of the operation. It receives the user's high-level goal (e.g., "plan my meals from these ingredients"). Its job is to **reason** about the task, **plan** the steps, and **execute** by calling tools. It maintains the state of the 7-day plan and the list of remaining ingredients.

2.  **Recipe Tool (Specialized, Fine-Tuned Model):**
    * **Model:** `microsoft/Phi-3-mini` fine-tuned with LoRA adapters.
    * **Role:** This is a specialized "tool" that the Planner can call. It performs one task reliably: given a small list of ingredients, it returns a single meal idea in a strict JSON format.

## 2. Interaction Flow

The agent follows a ReAct (Reason + Act) style loop.

1.  **User Input:** `python agent.py --ingredients "chicken, rice, broccoli, eggs, ..."`
2.  **Planner (Reasoning):** "My goal is to create a 7-day plan (B, L, D). I have a list of ingredients. I will iterate from Day 1 to Day 7. For each meal, I will select 2-3 ingredients from the available list and call my `RecipeTool` to get a meal idea. I will then add this idea to my plan and update the ingredient list."
3.  **Planner (Act):** `call_recipe_tool(["eggs", "bread", "milk"])`
4.  **Tool (Observation):** The fine-tuned LoRA model executes and returns a clean JSON string:
    `{ "meal_name": "French Toast", "meal_type": "Breakfast", "ingredients_used": ["eggs", "bread", "milk"], "instructions": "1. Whisk eggs and milk. 2. Soak bread. 3. Fry until golden." }`
5.  **Planner (Reasoning):** "Excellent. I have the meal for Day 1, Breakfast. I will add this to my final plan. Now for Day 1, Lunch. I will pick from the remaining ingredients, maybe 'chicken' and 'rice'."
6.  **Planner (Act):** `call_recipe_tool(["chicken", "rice"])`
7.  **Tool (Observation):** `...`
8.  **(Loop):** This process repeats 21 times (7 days * 3 meals) until the plan is complete.
9.  **Planner (Execute):** The agent formats the complete 21-meal plan into a final JSON or Markdown file and presents it to the user.

## 3. Models Used & Justification

* **Planner (General LLM):**
    * **Why:** A powerful reasoning engine is required to manage the complex, multi-step task of building a 7-day plan, tracking state (available ingredients), and iterating. This task is too complex for a small, specialized model.

* **Recipe Tool (`Phi-3-mini` + LoRA):**
    * **Why:** This is the **mandatory fine-tuned model**.
    * **1. Task Specialization:** The base `Phi-3-mini` model is good, but it might return a recipe in plain text, or miss ingredients, or add extra conversational text. Fine-tuning on a dataset of `(prompt) -> (JSON recipe)` examples makes it an expert at *this one specific task*.
    * **2. Improved Reliability:** The most critical reason. For an agent to work, its tools *must* be reliable. By fine-tuning for **structured output (JSON)**, we guarantee that the Planner always receives machine-readable data. This prevents parsing errors and makes the entire system robust.
    * **3. Efficiency:** Using a small, fine-tuned model for the "tool" part is much faster and cheaper than calling a large model (like GPT-4) 21 times in a row.
