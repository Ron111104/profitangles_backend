import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from django.http import HttpResponse
from django.shortcuts import render
import os

def visualize_stock_data(request):
    if request.method == 'POST' and 'csv_file' in request.FILES:
        csv_file = request.FILES['csv_file']
        df = pd.read_csv(csv_file)

        # Create the plot
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=df.head(30), x='Date', y='Open')
        plt.title('Apple Stock Opening Prices (First 30 Days)')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()

        # Save the plot as an image
        image_path = 'static/images/stock_visualization.png'
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        plt.savefig(image_path)
        plt.close()

        # Serve the image
        with open(image_path, 'rb') as f:
            return HttpResponse(f.read(), content_type='image/png')

    return render(request, 'upload.html')
