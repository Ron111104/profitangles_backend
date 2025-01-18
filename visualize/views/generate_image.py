import os
import mysql.connector
import requests
import pandas as pd
import json
from django.db import models
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

# Model for saving the image in the 'test' database
class StockVisualization(models.Model):
    image = models.TextField()  # For storing base64 encoded image
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'stock_visualization'

# Function to ensure the table exists in the 'test' database
def ensure_table_exists(connection):
    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS stock_visualization (
        id INT AUTO_INCREMENT PRIMARY KEY,
        image LONGTEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    cursor.execute(create_table_query)
    connection.commit()
    cursor.close()

# Connection to fetch data from the 'trial' database
def get_trial_db_connection():
    connection = mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_STORAGE', 'trial'),
        port=os.getenv('DB_PORT', 3306)
    )
    return connection

# Connection to store data in the 'test' database
def get_test_db_connection():
    connection = mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'test'),  # Store the image in the 'test' database
        port=os.getenv('DB_PORT', 3306)
    )
    ensure_table_exists(connection)  # Ensure the table exists in the 'test' database
    return connection

# Function to detect if the request is local or hosted (production)
def get_base_url(request):
    host = request.get_host().lower()
    if 'localhost' in host or '127.0.0.1' in host:
        # If it's local, use the development URL
        return os.getenv('BACKEND_URL_DEV')
    else:
        # Otherwise, use the production URL
        return os.getenv('BACKEND_URL')

# View for generating and storing the stock visualization image
@csrf_exempt
def generate_image(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'error': 'Only POST requests are allowed'}, status=405)

    try:
        # Get base URL dynamically based on whether it's local or hosted
        BASE_URL = get_base_url(request)

        # Parse MySQL query from the JSON request body
        body = json.loads(request.body)
        query = body.get('query')
        if not query:
            return JsonResponse({'status': 'error', 'error': 'No query provided'}, status=400)

        # Get trial database connection to fetch data
        trial_connection = get_trial_db_connection()

        # Execute the query for stock data
        cursor = trial_connection.cursor()
        cursor.execute(query)
        columns = [col[0].lower() for col in cursor.description]  # Make columns lowercase for consistency
        results = cursor.fetchall()

        # Convert results to DataFrame
        df = pd.DataFrame(results, columns=columns)

        # Initialize a list to store visualization IDs
        visualization_ids = []

        # Check and process data for stock_open_price
        if 'open' in df.columns and 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')  # Ensure date format
            df = df.dropna(subset=['date'])  # Drop invalid dates
            df['date'] = df['date'].dt.strftime('%Y-%m-%d')
            stock_data = df[['date', 'open']].copy()

            # Convert data to JSON-compatible format and send to stock_open_price endpoint
            payload = {'data': stock_data.to_dict(orient='records')}
            response = requests.post(
                f"{BASE_URL}/visualize/stock_open_price/",
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )

            if response.status_code == 200:
                response_data = response.json()
                if 'image' in response_data:
                    # Save the image to the database
                    image_base64 = response_data['image']
                    test_connection = get_test_db_connection()
                    cursor_test = test_connection.cursor()
                    cursor_test.execute("INSERT INTO stock_visualization (image) VALUES (%s)", (image_base64,))
                    visualization_ids.append(cursor_test.lastrowid)
                    test_connection.commit()
                    cursor_test.close()
                    test_connection.close()

        # Check and process data for max_percentage_movement
        if 'high' in df.columns and 'low' in df.columns and 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')  # Ensure date format
            df = df.dropna(subset=['date'])  # Drop invalid dates
            df['date'] = df['date'].dt.strftime('%Y-%m-%d')
            max_percentage_data = df[['date', 'high', 'low']].copy()

            # Convert data to JSON-compatible format and send to max_percentage_movement endpoint
            payload = {'data': max_percentage_data.to_dict(orient='records')}
            response = requests.post(
                f"{BASE_URL}/visualize/max_percentage_movement/",
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )

            if response.status_code == 200:
                response_data = response.json()
                if 'image' in response_data:
                    # Save the image to the database
                    image_base64 = response_data['image']
                    test_connection = get_test_db_connection()
                    cursor_test = test_connection.cursor()
                    cursor_test.execute("INSERT INTO stock_visualization (image) VALUES (%s)", (image_base64,))
                    visualization_ids.append(cursor_test.lastrowid)
                    test_connection.commit()
                    cursor_test.close()
                    test_connection.close()

        # Clean up the trial database connection
        cursor.close()
        trial_connection.close()

        # Return the list of visualization IDs
        if visualization_ids:
            return JsonResponse({'status': 'success', 'ids': visualization_ids})
        else:
            return JsonResponse({'status': 'error', 'error': 'No relevant columns found to generate visualizations'}, status=400)

    except Exception as e:
        # Clean up connections if they exist
        if 'cursor' in locals():
            cursor.close()
        if 'trial_connection' in locals():
            trial_connection.close()
        if 'test_connection' in locals():
            test_connection.close()
        return JsonResponse({'status': 'error', 'error': str(e)}, status=500)
