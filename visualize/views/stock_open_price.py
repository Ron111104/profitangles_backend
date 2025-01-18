import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, AutoDateLocator
from io import BytesIO
import base64
import seaborn as sns
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def stock_open_price(request):
    try:
        # Ensure you're accessing the data from the request body correctly
        body = json.loads(request.body)  # Assuming the data is being passed as JSON
        df = pd.DataFrame(body['data'])  # Construct the DataFrame from the 'data' field

        # Ensure date column is in datetime format
        df['date'] = pd.to_datetime(df['date'], errors='coerce')  # 'coerce' will convert invalid parsing to NaT

        # Drop rows with NaT in the 'date' column
        df = df.dropna(subset=['date'])

        # Plotting style and configuration
        plt.style.use('seaborn-v0_8-whitegrid')
        sns.set_palette("deep")

        # Create the plot
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(df['date'], df['open'], label='Open Price', color='#2962ff', linewidth=2)

        # Titles and labels
        ax.set_title('Stock Open Prices', fontsize=16, pad=20, fontweight='bold', color='#1a237e')
        ax.set_xlabel('Date', fontsize=12, labelpad=10, color='#424242')
        ax.set_ylabel('Open Price ($)', fontsize=12, labelpad=10, color='#424242')

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
        plt.close()

        # Return the base64 image as JSON response
        return JsonResponse({'image': image_base64})

    except Exception as e:
        return JsonResponse({'status': 'error', 'error': str(e)}, status=500)
