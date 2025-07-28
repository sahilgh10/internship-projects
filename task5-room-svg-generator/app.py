from flask import Flask, render_template, request, send_file
import os
import csv
import random

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('csvfile')
        if not file or file.filename == '':
            return "No file selected"
        if not file.filename.endswith('.csv'):
            return "Please upload a CSV file"

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        svg_path = generate_svg(filepath)
        return send_file(svg_path, as_attachment=True)

    return render_template('index.html')

def generate_svg(csv_path):
    # Read CSV but skip comment lines (starting with #)
    with open(csv_path, newline='') as f:
        lines = f.readlines()
        lines = [line for line in lines if not line.strip().startswith('#')]
        reader = csv.DictReader(lines)
        all_rooms = list(reader)

    layout_count = 3
    max_width = 1000
    vertical_gap = 50
    svg_parts = []
    total_height = 0

    for layout_num in range(layout_count):
        rooms = all_rooms.copy()
        random.shuffle(rooms)

        x = 0
        y = total_height + 50
        row_height = 0

        # Header with unit note
        svg_parts.append(f'<text x="10" y="{y - 30}" font-size="16" fill="black">Layout {layout_num + 1} (Dimensions in mm)</text>')

        for room in rooms:
            name = room['Room Name']
            width = int(room['Width'])
            height = int(room['Height'])

            if x + width > max_width:
                x = 0
                y += row_height
                row_height = 0

            # Draw room rectangle
            svg_parts.append(
                f'<rect x="{x}" y="{y}" width="{width}" height="{height}" fill="#d9f9d9" stroke="black" stroke-width="2"/>'
            )

            # Room name
            svg_parts.append(
                f'<text x="{x + 10}" y="{y + 20}" font-size="14" fill="black">{name}</text>'
            )

            # Room dimensions in mm (1 unit = 10mm → display * 10)
            mm_width = width * 10
            mm_height = height * 10
            svg_parts.append(
                f'<text x="{x + 10}" y="{y + 40}" font-size="12" fill="#333">{mm_width}mm x {mm_height}mm</text>'
            )

            x += width
            row_height = max(row_height, height)

        total_height = y + row_height + vertical_gap

    svg_code = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="{max_width}" height="{total_height}" xmlns="http://www.w3.org/2000/svg">
{chr(10).join(svg_parts)}
</svg>"""

    output_file = os.path.join(OUTPUT_FOLDER, "zone_style_layout.svg")
    with open(output_file, 'w') as f:
        f.write(svg_code)

    return output_file

if __name__ == '__main__':
    app.run(debug=True)