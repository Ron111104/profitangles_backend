import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend

def max_percentage_movement(request):
    image_path = None  # Initialize image_path
    if request.method == 'POST' and 'csv_file' in request.FILES:
        try:
            csv_file = request.FILES['csv_file']
            df = pd.read_csv(csv_file)

            # Check required columns
            if not {'Date', 'High', 'Low'}.issubset(df.columns):
                return HttpResponse(
                    "Error: CSV must contain 'Date', 'High', and 'Low' columns.",
                    status=400
                )

            # Calculate percentage change and rolling max change
            df['Percentage Change'] = (df['High'] - df['Low']) / df['Low'] * 100
            df['7 Day Max Change'] = df['Percentage Change'].rolling(window=7).max()

            # Plot the graph
            plt.figure(figsize=(12, 6))
            sns.lineplot(data=df, x='Date', y='7 Day Max Change')
            plt.title('Max Percentage Movement in 7 Days')
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.tight_layout()

            # Save the plot to the static directory
            image_path = 'images/max_percentage_movement.png'
            full_image_path = os.path.join(settings.STATICFILES_DIRS[0], image_path)
            os.makedirs(os.path.dirname(full_image_path), exist_ok=True)
            plt.savefig(full_image_path)
            plt.close()
        except Exception as e:
            return HttpResponse(f"Error processing the file: {str(e)}", status=500)

    return render(request, 'visualize/max_percentage_movement.html', {'image_path': image_path})
