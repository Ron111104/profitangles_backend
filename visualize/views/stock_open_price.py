import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend

def stock_open_price(request):
    image_path = None  # Initialize image_path
    if request.method == 'POST' and 'csv_file' in request.FILES:
        try:
            csv_file = request.FILES['csv_file']
            df = pd.read_csv(csv_file)

            # Check required columns
            if 'Date' not in df.columns or 'Open' not in df.columns:
                return HttpResponse(
                    "Error: CSV must contain 'Date' and 'Open' columns.",
                    status=400
                )

            # Generate Stock Open Price graph
            plt.figure(figsize=(12, 6))
            sns.lineplot(data=df.head(30), x='Date', y='Open')
            plt.title('Stock Opening Prices (First 30 Days)')
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.tight_layout()

            # Save the plot to the static directory
            image_path = 'images/stock_open_price.png'
            full_image_path = os.path.join(settings.STATICFILES_DIRS[0], image_path)
            os.makedirs(os.path.dirname(full_image_path), exist_ok=True)
            plt.savefig(full_image_path)
            plt.close()
        except Exception as e:
            return HttpResponse(f"Error processing the file: {str(e)}", status=500)

    return render(request, 'visualize/stock_open_price.html', {'image_path': image_path})
