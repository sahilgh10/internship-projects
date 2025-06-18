# 🧾 Week 3 - Interior Furniture Price Estimator with PDF Invoice

This project is a console-based tool built in Python that helps interior design businesses estimate furniture costs for clients based on custom dimensions and materials. It generates a professional **PDF invoice** at the end.

---

## 📌 Overview

This tool allows interior designers or sales executives to input customer details and furniture selections to generate a detailed cost estimate. The output includes a structured **quotation invoice in PDF format**.

---

## ⚙️ Features

- 📇 Takes customer name, phone number, and project location
- 🪑 Allows multiple furniture item selections (e.g., bed, wardrobe, storage)
- 🧱 Offers choice of wood materials with per-square-foot pricing
- 📏 Accepts 3D measurements (length, breadth, height)
- 🧮 Calculates price based on 2 largest dimensions × wood rate
- 🧾 Generates a **PDF invoice** with breakdown, invoice number & date
- 🚫 Handles invalid inputs: names, numbers, dimensions, etc.

---

## ▶️ How to Run

1. Make sure `fpdf` is installed:

```bash
pip install fpdf


### 💻 Sample Output & 🧠 What I Learned
```
=== Interior Furniture Price Estimator ===

Enter your name: Sahil Gholap
Enter your phone number: 9876543210
Enter project location/site: Pune

Select furniture type:
1. Bed
2. Wardrobe
3. Crockery Unit
4. Storage Unit
5. Chest of Drawers
Enter your choice (1-5): 1

Select wood type:
1. Plywood (Rs.1500 per sq.ft)
2. MDF (Rs.1200 per sq.ft)
3. Teak Wood (Rs.2500 per sq.ft)
4. Particle Board (Rs.1000 per sq.ft)
5. Solid Wood (Rs.3000 per sq.ft)
Enter your choice (1-5): 3

Enter length (in feet, 1-15): 6
Enter breadth (in feet, 1-10): 3
Enter height (in feet, 1-10): 5

✅ Estimate Added:
Furniture: Bed
Wood Type: Teak Wood
Used Area: 6.0 ft × 5.0 ft = 30.00 sq.ft
Rate: Rs.2500/sq.ft
Estimated Price: Rs.75000.00

Do you want to add another furniture item? (yes/no): no
Do you want to generate the PDF invoice? (yes/no): yes

✅ PDF invoice saved as: Sahil_Gholap_invoice_20250610.pdf

-------------------------------
🧠 What I Learned:
- Validating name, phone number, and location inputs properly
- Using `re` for text-only input validation
- Handling user input with default error messages
- Calculating area from 2 largest dimensions (not volume)
- Storing multiple entries using lists and dictionaries
- Formatting currency values cleanly
- Generating structured PDF invoices using the `fpdf` library
- Dynamic file naming using date and customer name
```
