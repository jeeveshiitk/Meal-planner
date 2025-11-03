import os
import json
import argparse
from dotenv import load_dotenv

# --- Mock LLM Call Functions ---
# In a real app, these would make API calls to a service like
# Google (Gemini), Anthropic (Claude), or a local/Hugging Face model.

def call_finetuned_recipe_llm(ingredients_list):
    """
    MOCK FUNCTION: Simulates calling our fine-tuned LoRA model.
    This model is specialized to return ONLY a valid JSON object
    for a single meal based on the input ingredients.
    """
    print(f"--- [Tool Call: RecipeTool] ---")
    print(f"--- Input: {ingredients_list} ---")
    
    # Mocked JSON output, as if from the fine-tuned model
    # We'll just pick a meal idea based on the first ingredient
    
    first_ingredient = ingredients_list[0].lower()
    if "chicken" in first_ingredient:
        meal = {
            "meal_name": "Simple Chicken and Rice",
            "meal_type": "Lunch",
            "ingredients_used": ["chicken", "rice"],
            "instructions": "1. Cook chicken. 2. Cook rice. 3. Combine."
        }
    elif "eggs" in first_ingredient:
        meal = {
            "meal_name": "Scrambled Eggs",
            "meal_type": "Breakfast",
            "ingredients_used": ["eggs", "milk"],
            "instructions": "1. Whisk eggs and milk. 2. Cook in a pan."
        }
    elif "spinach" in first_ingredient:
         meal = {
            "meal_name": "Spinach Salad",
            "meal_type": "Lunch",
            "ingredients_used": ["spinach", "tomatoes", "onion"],
            "instructions": "1. Combine all ingredients in a bowl."
        }
    else:
        meal = {
            "meal_name": "Default Meal (e.g., Pasta)",
            "meal_type": "Dinner",
            "ingredients_used": ingredients_list,
            "instructions": "1. Boil water. 2. Cook pasta."
        }
        
    # The real fine-tuned model would return this JSON structure
    return json.dumps(meal)

def call_main_planner_llm(prompt):
    """
    MOCK FUNCTION: Simulates the "Planner" (the main reasoning LLM).
    This function takes a high-level goal and breaks it down.
    
    In this agent, the *real* logic is in the `run_agent_flow` function.
    This mock function just prints the "thoughts" of the agent.
    """
    print(f"\n[Planner Thought]: {prompt}\n")
    # In a real ReAct loop, this function would return a plan
    # or a tool call. We are simplifying that loop here.
    return True

# --- Main Agent Logic ---

def run_agent_flow(ingredients_str):
    """
    This function orchestrates the entire agent flow.
    It plays the role of the "Planner" LLM.
    """
    
    # 1. Parse input
    available_ingredients = [ing.strip().lower() for ing in ingredients_str.split(',')]
    full_plan = {}
    
    call_main_planner_llm(f"Goal: Create a 7-day meal plan. Available ingredients: {available_ingredients}. I will iterate day by day, for 3 meals each.")
    
    # 2. Iterate and plan
    days = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7"]
    meals = ["Breakfast", "Lunch", "Dinner"]
    
    ing_index = 0
    for day in days:
        full_plan[day] = {}
        for meal_type in meals:
            
            # 3. Select ingredients for the tool
            # (Simple logic: just pick 2 ingredients from the list)
            # A more complex agent would track used ingredients
            if ing_index + 1 >= len(available_ingredients):
                ing_index = 0 # Reset index if we run out
                
            ing1 = available_ingredients[ing_index]
            ing2 = available_ingredients[ing_index + 1]
            ing_index += 1 # Move to the next ingredient for the next meal
            
            call_main_planner_llm(f"Planning {day}, {meal_type}. I will use '{ing1}' and '{ing2}'. Calling RecipeTool.")
            
            # 4. Call the fine-tuned tool (Act)
            try:
                recipe_json_str = call_finetuned_recipe_llm([ing1, ing2])
                
                # 5. Parse the tool's observation
                meal_data = json.loads(recipe_json_str)
                
                # 6. Update the plan (Execute)
                full_plan[day][meal_type] = meal_data
                call_main_planner_llm(f"Successfully added '{meal_data['meal_name']}' to the plan.")
                
            except json.JSONDecodeError:
                call_main_planner_llm(f"Error: The tool returned invalid JSON. Skipping this meal.")
                full_plan[day][meal_type] = {"error": "Failed to generate meal"}
            except Exception as e:
                call_main_planner_llm(f"An unexpected error occurred: {e}")
                
    call_main_planner_llm("Plan complete. Formatting final output.")
    
    # 7. Return final output
    return full_plan

def main():
    # Load API keys (even if mock, good practice)
    load_dotenv()
    
    # Setup command-line argument parsing
    parser = argparse.ArgumentParser(description="AI Meal Planner Agent")
    parser.add_argument(
        "--ingredients",
        type=str,
        required=True,
        help="A comma-separated list of ingredients."
    )
    args = parser.parse_args()
    
    print("--- 🤖 AI Meal Planner Agent Initialized ---")
    
    # Run the agent
    final_plan = run_agent_flow(args.ingredients)
    
    # Print the final result
    print("\n--- ✅ Your 7-Day Meal Plan ---")
    print(json.dumps(final_plan, indent=2))
    
    # Save to a file
    with open("final_meal_plan.json", "w") as f:
        json.dump(final_plan, f, indent=2)
    print("\n[Saved plan to final_meal_plan.json]")

if __name__ == "__main__":
    main()
    