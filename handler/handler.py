import json
from .s3_utils import fetch_file_from_s3, upload_to_s3
from .converters.csv_converter import convert_csv_to_json, convert_csv_to_pdf, convert_csv_to_xml
from .converters.pdf_converter import convert_pdf_to_word

def file_conversion(event, context):
    try:
        body = json.loads(event['body'])
        file_name = body.get("file_name")
        conversion_type = body.get("conversion_type")

        if not file_name or not conversion_type:
            return {"statusCode": 400, "body": json.dumps({"error": "file_name and conversion_type are required"})}

        file_content, error = fetch_file_from_s3(file_name)
        if error:
            return {"statusCode": 404, "body": json.dumps({"error": error})}

        if conversion_type == "csv_to_json":
            converted_data, error = convert_csv_to_json(file_content.decode('utf-8'))
            content_type = "application/json"
        elif conversion_type == "csv_to_pdf":
            converted_data, error = convert_csv_to_pdf(file_content.decode('utf-8'))
            content_type = "application/pdf"
        elif conversion_type == "csv_to_xml":
            converted_data, error = convert_csv_to_xml(file_content.decode('utf-8'))
            content_type = "application/xml"
        elif conversion_type == "pdf_to_word":
            converted_data, error = convert_pdf_to_word(file_content)
            content_type = "application/docx"
        else:
            return {"statusCode": 400, "body": json.dumps({"error": "Invalid conversion type"})}

        if error:
            return {"statusCode": 500, "body": json.dumps({"error": error})}

        new_file_name, error = upload_to_s3(file_name, converted_data, content_type)
        if error:
            return {"statusCode": 500, "body": json.dumps({"error": error})}

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "File converted and uploaded successfully",
                "s3_file": new_file_name
            })
        }

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
