print("🧾 Interior Design Service Quotation Generator\n")

# Define available services and their prices
services = {
    "Flooring": 30000,
    "Lighting": 15000,
    "Painting": 25000,
    "Furniture Setup": 40000,
    "Wall Décor": 12000
}

selected_services = {}

# Ask user which services they want
for service, price in services.items():
    response = input(f"Do you want {service} service? (yes/no): ").strip().lower()
    if response == "yes":
        selected_services[service] = price

# Print quotation summary
print("\n--- Quotation Summary ---")
total = 0
if selected_services:
    for service, price in selected_services.items():
        print(f"✔ {service}: ₹{price:,}")
        total += price
else:
    print("No services selected.")

print("\n---------------------------")
print(f"Total Estimated Quote: ₹{total:,}")
