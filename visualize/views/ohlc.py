import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from matplotlib.dates import DateFormatter, AutoDateLocator
import matplotlib
import matplotlib.dates as mdates

matplotlib.use('Agg')  # Use non-GUI backend

@csrf_exempt
def ohlc_graph(request):
    try:
        if request.method != 'POST':
            return JsonResponse({'status': 'error', 'error': 'Only POST requests are allowed'}, status=405)

        # Parse the incoming JSON data
        body = json.loads(request.body)
        data = body.get('data')

        if not data:
            return JsonResponse({'status': 'error', 'error': 'No data provided'}, status=400)

        # Convert data to DataFrame
        df = pd.DataFrame(data)

        # Ensure 'date' column is in datetime format
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

        # Drop rows with NaT in the 'date' column
        df = df.dropna(subset=['date'])

        # Plot the OHLC graph
        plt.style.use('seaborn-v0_8-whitegrid')
        sns.set_palette("deep")
        fig, ax = plt.subplots(figsize=(12, 6))

        # Plot Open, High, Low, and Close
        ax.plot(df['date'], df['open'], label='Open', color='#4caf50', linewidth=2)
        ax.plot(df['date'], df['high'], label='High', color='#2196f3', linewidth=2)
        ax.plot(df['date'], df['low'], label='Low', color='#f44336', linewidth=2)
        ax.plot(df['date'], df['close'], label='Close', color='#ff9800', linewidth=2)

        # Titles and labels
        ax.set_title('OHLC Graph', fontsize=16, pad=20, fontweight='bold', color='#1a237e')
        ax.set_xlabel('Date', fontsize=12, labelpad=10, color='#424242')
        ax.set_ylabel('Price', fontsize=12, labelpad=10, color='#424242')

        # Date formatting on x-axis
        date_locator = AutoDateLocator()
        ax.xaxis.set_major_locator(date_locator)
        ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45)

        # Add grid and legend
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.legend(loc='upper left', fontsize=10)

        # Save the plot as a base64 string
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()
        plt.close(fig)

        # Return the base64 image as JSON response
        return JsonResponse({'image': image_base64})

    except Exception as e:
        return JsonResponse({'status': 'error', 'error': str(e)}, status=500)
