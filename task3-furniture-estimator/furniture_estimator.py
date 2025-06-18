from fpdf import FPDF
from datetime import datetime
import re

# --- Validation Functions ---

def get_valid_name(prompt):
    while True:
        name = input(prompt).strip()
        if not name:
            print("❌ Name cannot be empty.")
        elif not re.match("^[A-Za-z ]+$", name):
            print("❌ Enter letters and spaces only.")
        else:
            return name

def get_valid_phone(prompt):
    while True:
        phone = input(prompt).strip()
        if not phone.isdigit() or len(phone) != 10:
            print("❌ Enter a valid 10-digit phone number.")
        else:
            return phone

def get_valid_location(prompt):
    while True:
        location = input(prompt).strip()
        if not location:
            print("❌ Location cannot be empty.")
        elif not re.match("^[A-Za-z ]+$", location):
            print("❌ Location should contain only letters and spaces.")
        else:
            return location

def get_valid_dimension(label, min_val=1, max_val=15):
    while True:
        try:
            value = float(input(f"Enter {label} (in feet, {min_val}-{max_val}): "))
            if value < min_val or value > max_val:
                print(f"❌ Please enter a value between {min_val} and {max_val}.")
            else:
                return value
        except ValueError:
            print(f"❌ Please enter a valid number for {label}.")

def confirm_yes(prompt):
    while True:
        response = input(prompt).strip().lower()
        if response == "yes":
            return True
        elif response == "no":
            return False
        else:
            print("❌ Please enter 'yes' or 'no' only.")

# --- Main Estimator Function ---

def calculate_furniture_price():
    print("=== Interior Furniture Price Estimator ===")

    # Customer Information
    customer_name = get_valid_name("Enter your name: ")
    phone = get_valid_phone("Enter your phone number: ")
    location = get_valid_location("Enter project location/site: ")
    invoice_date = datetime.now().strftime("%d %B %Y")
    invoice_number = f"INV{datetime.now().strftime('%Y%m%d%H%M%S')}"

    furniture_items = [
        "Bed", "Wardrobe", "Crockery Unit",
        "Storage Unit", "Chest of Drawers"
    ]

    wood_types = {
        "Plywood": 1500,
        "MDF": 1200,
        "Teak Wood": 2500,
        "Particle Board": 1000,
        "Solid Wood": 3000
    }

    estimates = []

    while True:
        try:
            # Furniture Type
            print("\nSelect furniture type:")
            for i, item in enumerate(furniture_items, 1):
                print(f"{i}. {item}")
            choice = int(input("Enter your choice (1-5): "))
            if choice < 1 or choice > len(furniture_items):
                print("❌ Invalid furniture choice.")
                continue
            furniture_type = furniture_items[choice - 1]

            # Wood Type
            print("\nSelect wood type:")
            wood_keys = list(wood_types.keys())
            for i, wood in enumerate(wood_keys, 1):
                print(f"{i}. {wood} (Rs.{wood_types[wood]} per sq.ft)")
            wood_choice = int(input("Enter your choice (1-5): "))
            if wood_choice < 1 or wood_choice > len(wood_keys):
                print("❌ Invalid wood choice.")
                continue
            selected_wood = wood_keys[wood_choice - 1]
            price_per_sqft = wood_types[selected_wood]

            # Dimensions
            length = get_valid_dimension("length", 1, 15)
            breadth = get_valid_dimension("breadth", 1, 10)
            height = get_valid_dimension("height", 1, 10)

            dimensions = [length, breadth, height]
            dimensions.sort(reverse=True)
            used_dims = dimensions[:2]
            area = used_dims[0] * used_dims[1]
            total_price = area * price_per_sqft

            # Save item
            estimates.append({
                "furniture": furniture_type,
                "wood": selected_wood,
                "used_dims": used_dims,
                "area": area,
                "rate": price_per_sqft,
                "price": total_price
            })

            print(f"\n✅ Estimate Added:")
            print(f"Furniture: {furniture_type}")
            print(f"Wood Type: {selected_wood}")
            print(f"Used Area: {used_dims[0]} ft × {used_dims[1]} ft = {area:.2f} sq.ft")
            print(f"Rate: Rs.{price_per_sqft}/sq.ft")
            print(f"Estimated Price: Rs.{total_price:.2f}")

            more = input("\nDo you want to add another furniture item? (yes/no): ").strip().lower()
            if more != "yes":
                break

        except ValueError:
            print("❌ Please enter valid numeric inputs.")
            continue

    if not estimates:
        print("❌ No estimates were added.")
        return

    # Ask to generate PDF
    if not confirm_yes("\nDo you want to generate the PDF invoice? (yes/no): "):
        print("📁 PDF not generated. Exiting.")
        return

    # --- PDF Generation ---
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Interior Furniture Estimate Invoice", ln=True, align='C')

    pdf.set_font("Arial", '', 12)
    pdf.ln(10)
    pdf.cell(0, 10, f"Invoice No: {invoice_number}", ln=True)
    pdf.cell(0, 10, f"Date: {invoice_date}", ln=True)
    pdf.cell(0, 10, f"Customer Name: {customer_name}", ln=True)
    pdf.cell(0, 10, f"Phone: {phone}", ln=True)
    pdf.cell(0, 10, f"Project Location: {location}", ln=True)

    grand_total = 0
    for idx, estimate in enumerate(estimates, 1):
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, f"Item {idx}:", ln=True)

        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 10, f"Furniture Type: {estimate['furniture']}", ln=True)
        pdf.cell(0, 10, f"Wood Type: {estimate['wood']}", ln=True)
        dims = estimate["used_dims"]
        pdf.cell(0, 10, f"Used Area: {dims[0]} ft × {dims[1]} ft = {estimate['area']:.2f} sq.ft", ln=True)
        pdf.cell(0, 10, f"Rate: Rs.{estimate['rate']}/sq.ft", ln=True)
        pdf.cell(0, 10, f"Estimated Price: Rs.{estimate['price']:.2f}", ln=True)

        grand_total += estimate['price']

    # Total
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, f"Total Estimate: Rs.{grand_total:,.2f}", ln=True)

    # Save file
    date_str = datetime.now().strftime("%Y%m%d")
    safe_name = re.sub(r'[^A-Za-z0-9_]', '', customer_name.replace(" ", "_"))
    filename = f"{safe_name}_invoice_{date_str}.pdf"
    pdf.output(filename)

    print(f"\n✅ PDF invoice saved as: {filename}")

# Run it
calculate_furniture_price()
