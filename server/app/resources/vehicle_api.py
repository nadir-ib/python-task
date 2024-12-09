from flask_restful import Resource
from flask import request, jsonify
import pandas as pd
from app.utils.auth import get_auth_header
from app.utils.data_merger import merge_and_filter
from config.config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, BAU_API_URL, BAU_COLOR_API_URL
import requests
from werkzeug.utils import secure_filename
import os


class VehicleAPI(Resource):
    def __init__(self):
        self.UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../uploads"))
        self.BAU_API_URL = BAU_API_URL
        self.BAU_COLOR_API_URL = BAU_COLOR_API_URL
        self.auth_header = ""


    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


    # Function to fetch color code for a given labelId
    def fetch_color_code(self, label_id):
        api_url = f"{self.BAU_COLOR_API_URL}{label_id}"
        try:
          response = requests.get(api_url, headers=self.auth_header)
          response.raise_for_status()
          label_data = response.json()
          return label_data.get("colorCode", "No ColorCode Found")
        except requests.RequestException as e:
            print(f"Error fetching color code for labelId {label_id}: {e}")
            return "Error"

    # Filter and enrich data
    def process_data(self, data):
        filtered_data = [item for item in data if item.get("hu")]  # Filter items with non-empty 'hu'
        for item in filtered_data:
            label_ids = item.get("labelIds", [])
            if label_ids:
                item["labelColorCodes"] = [
                    {"labelId": label_id, "colorCode": self.fetch_color_code(label_id)}
                    for label_id in label_ids
                ]
            else:
                item["labelColorCodes"] = []
        return filtered_data



    def post(self):
        """
        Upload a CSV and process vehicle data
        ---
        tags:
          - Vehicles
        consumes:
          - multipart/form-data
        parameters:
          - in: formData
            name: file
            type: file
            required: true
            description: CSV file containing vehicle data
        responses:
          200:
            description: Processed vehicle data
            content:
              application/json:
                schema:
                  type: array
                  items:
                    type: object
                    properties:
                      rnr:
                        type: string
                        description: Vehicle unique identifier
                      gruppe:
                        type: string
                        description: Vehicle group
                      hu:
                        type: string
                        format: date
                        description: Last technical inspection date
                      labelIds:
                        type: array
                        items:
                          type: integer
                        description: Associated label IDs
          400:
            description: Bad request (e.g., missing file or invalid CSV format)
          500:
            description: Server error (e.g., external API failure)
        """
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        if file and self.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(self.UPLOAD_FOLDER, filename)
            file.save(file_path)

        try:
            csv_data = pd.read_csv(file_path, delimiter=';')
        except pd.errors.ParserError as e:
            return {"error": f"Failed to parse CSV file: {str(e)}"}, 400

        self.auth_header = get_auth_header()
 
        response = requests.get(self.BAU_API_URL, headers=self.auth_header)

        if response.status_code != 200:
            return {"error": "Failed to fetch vehicle data"}, 500

        vehicles_data = response.json()    
        vehicles_data = pd.DataFrame(vehicles_data)
 
        merged_data = merge_and_filter(csv_data, vehicles_data)
        final_result = self.process_data(merged_data)

        return jsonify(final_result)
