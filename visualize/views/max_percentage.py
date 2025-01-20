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
matplotlib.use('Agg') 

@csrf_exempt
def max_percentage_movement(request):
    try:
        if request.method != 'POST':
            return JsonResponse({'status': 'error', 'error': 'only post requests are allowed'}, status=405)

        # parse the incoming json data
        body = json.loads(request.body)
        data = body.get('data')

        if not data:
            return JsonResponse({'status': 'error', 'error': 'no data provided'}, status=400)

        # convert data to dataframe
        df = pd.DataFrame(data)

        # ensure date column is in datetime format
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

        # drop rows with nat in the 'date' column
        df = df.dropna(subset=['date'])

        # calculate percentage change and rolling max change
        df['percentage change'] = (df['high'] - df['low']) / df['low'] * 100
        df['7 day max change'] = df['percentage change'].rolling(window=7).max()

        # plot the graph
        plt.style.use('seaborn-v0_8-whitegrid')
        sns.set_palette("deep")
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(df['date'], df['7 day max change'], label='7 day max change', color='#2962ff', linewidth=2)

        # titles and labels
        ax.set_title('max percentage movement in 7 days', fontsize=16, pad=20, fontweight='bold', color='#1a237e')
        ax.set_xlabel('date', fontsize=12, labelpad=10, color='#424242')
        ax.set_ylabel('max percentage change (%)', fontsize=12, labelpad=10, color='#424242')

        # date formatting on x-axis
        date_locator = AutoDateLocator()
        ax.xaxis.set_major_locator(date_locator)
        ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45)

        # add grid and legend
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.legend(loc='upper left', fontsize=10)

        # save the plot as a base64 string
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()
        plt.close()

        # return the base64 image as json response
        return JsonResponse({'image': image_base64})

    except Exception as e:
        return JsonResponse({'status': 'error', 'error': str(e)}, status=500)
