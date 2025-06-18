print("🏠 Interior Design Budget Estimator\n")

# Default values
default_area = 1000  # sq.ft
default_cost_per_sqft = 1500  # ₹
default_furniture = 200000  # ₹
default_decor = 100000  # ₹
default_labor = 50000  # ₹

# Input helper
def get_input(prompt, default):
    user_input = input(f"{prompt} [Default: {default}]: ")
    return float(user_input) if user_input.strip() != "" else default

# Get inputs
area = get_input("Enter total area (in sq.ft)", default_area)
cost_per_sqft = get_input("Enter cost per sq.ft (₹)", default_cost_per_sqft)
furniture = get_input("Enter furniture cost (₹)", default_furniture)
decor = get_input("Enter décor cost (₹)", default_decor)
labor = get_input("Enter labor cost (₹)", default_labor)

# Calculate
construction_cost = area * cost_per_sqft
total_budget = construction_cost + furniture + decor + labor

# Output
print("\n--- Budget Breakdown ---")
print(f"Construction Cost: ₹{construction_cost:,.2f}")
print(f"Furniture: ₹{furniture:,.2f}")
print(f"Décor: ₹{decor:,.2f}")
print(f"Labor: ₹{labor:,.2f}")
print("------------------------")
print(f"Total Estimated Budget: ₹{total_budget:,.2f}")
