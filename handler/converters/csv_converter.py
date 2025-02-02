import csv
import pandas as pd
import xml.etree.ElementTree as ET
from io import BytesIO, StringIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def convert_csv_to_json(csv_content):
    try:
        df = pd.read_csv(StringIO(csv_content))
        json_data = df.to_json(orient='records', lines=True)
        return json_data, None
    except Exception as e:
        return None, str(e)

def convert_csv_to_pdf(csv_content):
    try:
        reader = csv.reader(StringIO(csv_content))
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)

        y_position = 750
        for row in reader:
            pdf.drawString(40, y_position, ", ".join(row))
            y_position -= 20
            if y_position < 50:
                pdf.showPage()
                y_position = 750

        pdf.save()
        buffer.seek(0)
        return buffer, None
    except Exception as e:
        return None, str(e)

def convert_csv_to_xml(csv_content):
    try:
        reader = csv.DictReader(StringIO(csv_content))
        root = ET.Element("root")
        for row in reader:
            item = ET.SubElement(root, "row")
            for key, value in row.items():
                field = ET.SubElement(item, key)
                field.text = value

        xml_data = ET.tostring(root, encoding="utf-8", method="xml").decode()
        return xml_data, None
    except Exception as e:
        return None, str(e)
