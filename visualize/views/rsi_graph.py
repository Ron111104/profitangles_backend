import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend

def rsi_graph(request):
    image_path = None  # Initialize image_path
    if request.method == 'POST' and 'csv_file' in request.FILES:
        try:
            csv_file = request.FILES['csv_file']
            df = pd.read_csv(csv_file)

            # Check if the required columns are in the CSV file
            if not {'Date', 'RSI_14'}.issubset(df.columns):
                return HttpResponse(
                    "Error: CSV must contain 'Date' and 'RSI_14' columns.",
                    status=400
                )

            # Ensure 'Date' column is parsed as datetime
            df['Date'] = pd.to_datetime(df['Date'])

            # Plot the RSI graph
            plt.figure(figsize=(12, 6))
            sns.lineplot(data=df.head(30), x='Date', y='RSI_14')  # First 30 entries
            plt.title('RSI Graph (First 30 Days)')
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.tight_layout()

            # Save the plot to the static directory
            image_path = 'images/rsi_graph.png'
            full_image_path = os.path.join(settings.STATICFILES_DIRS[0], image_path)
            os.makedirs(os.path.dirname(full_image_path), exist_ok=True)
            plt.savefig(full_image_path)
            plt.close()
        except Exception as e:
            return HttpResponse(f"Error processing the file: {str(e)}", status=500)

    return render(request, 'visualize/rsi_graph.html', {'image_path': image_path})
