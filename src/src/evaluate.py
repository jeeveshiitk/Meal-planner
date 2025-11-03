import json
import argparse
import os

def load_json_file(filepath):
    """Helper to load a JSON file."""
    if not os.path.exists(filepath):
        print(f"Error: File not found at {filepath}")
        return None
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        return data
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {filepath}")
        return None

def evaluate_plan_validity(plan):
    """
    Performs the "Plan Validity" check.
    Checks for 7 days, and 3 meals (B, L, D) per day.
    """
    print("--- Running Evaluation: Plan Validity ---")
    
    if not isinstance(plan, dict):
        print("Fail: Plan is not a valid dictionary.")
        return False
        
    days = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7"]
    meals = ["Breakfast", "Lunch", "Dinner"]
    
    # Check 1: Are there 7 days?
    if len(plan.keys()) != 7 or not all(day in plan for day in days):
        print(f"Fail: Plan does not contain all 7 days. Found: {list(plan.keys())}")
        return False
    
    # Check 2: Does each day have 3 meals?
    for day in days:
        if not isinstance(plan[day], dict):
            print(f"Fail: {day} is not a valid dictionary.")
            return False
        if len(plan[day].keys()) != 3 or not all(meal in plan[day] for meal in meals):
            print(f"Fail: {day} does not contain all 3 meals. Found: {list(plan[day].keys())}")
            return False
            
    print("Pass: Plan structure is valid (7 days, 3 meals/day).")
    return True

def evaluate_ingredient_utilization(plan, provided_ingredients_str):
    """
    Performs the "Ingredient Utilization Rate" (IUR) check.
    """
    print("\n--- Running Evaluation: Ingredient Utilization Rate (IUR) ---")
    
    try:
        provided_set = set([ing.strip().lower() for ing in provided_ingredients_str.split(',')])
        if not provided_set:
            print("Warning: No provided ingredients to check against.")
            return 0.0
            
        used_set = set()
        
        # Iterate through the plan to find all used ingredients
        for day, meals in plan.items():
            for meal_type, meal_data in meals.items():
                if "ingredients_used" in meal_data and isinstance(meal_data["ingredients_used"], list):
                    for ing in meal_data["ingredients_used"]:
                        used_set.add(ing.strip().lower())
        
        # Find the intersection
        utilized_ingredients = provided_set.intersection(used_set)
        
        iur = len(utilized_ingredients) / len(provided_set)
        
        print(f"Provided: {len(provided_set)} ingredients {provided_set}")
        print(f"Used:     {len(utilized_ingredients)} ingredients {utilized_ingredients}")
        print(f"IUR:      {iur:.2%}")
        return iur
        
    except Exception as e:
        print(f"Error calculating IUR: {e}")
        return 0.0

def main():
    parser = argparse.ArgumentParser(description="Evaluation script for AI Meal Planner")
    
    parser.add_argument(
        "--plan_file",
        type=str,
        default="final_meal_plan.json",
        help="Path to the generated meal plan JSON file."
    )
    parser.add_argument(
        "--ingredients",
        type=str,
        required=True,
        help="The original comma-separated list of ingredients provided to the agent."
    )
    args = parser.parse_args()
    
    # 1. Load the plan
    plan_data = load_json_file(args.plan_file)
    if plan_data is None:
        print("Evaluation aborted.")
        return

    # 2. Run evaluations
    validity_passed = evaluate_plan_validity(plan_data)
    iur_score = evaluate_ingredient_utilization(plan_data, args.ingredients)
    
    print("\n--- Evaluation Summary ---")
    print(f"Plan Validity:   {'Pass' if validity_passed else 'Fail'}")
    print(f"Ingredient Use:  {iur_score:.2%}")

if __name__ == "__main__":
    main()