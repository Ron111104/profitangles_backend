from django.conf import settings
from django.shortcuts import render
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib

matplotlib.use('Agg')  # Use non-GUI backend

def stock_open_price(request):
    image_path = None  # Initialize image_path
    try:
        # Check if the file is available in the session
        if 'csv_file_path' not in request.session:
            return HttpResponse("No file uploaded. Please upload a CSV first.", status=400)

        # Retrieve the full file path from the session
        file_path = request.session['csv_file_path']

        # Ensure the file exists before proceeding
        if not os.path.exists(file_path):
            return HttpResponse(f"File not found: {file_path}", status=404)

        # Read the CSV file
        df = pd.read_csv(file_path)

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

        # Save the plot to the media/images directory
        image_path = 'images/stock_open_price.png'  # Relative path to save in the media folder
        full_image_path = os.path.join(settings.MEDIA_ROOT, image_path)  # Full path in media directory
        os.makedirs(os.path.dirname(full_image_path), exist_ok=True)
        plt.savefig(full_image_path)
        plt.close()
        print(f"Saving image at: {full_image_path}")  # Debugging the full path

    except Exception as e:
        return HttpResponse(f"Error processing the file: {str(e)}", status=500)

    # Pass MEDIA_URL into the template context
    return render(request, 'visualize/stock_open_price.html', {'image_path': image_path, 'MEDIA_URL': settings.MEDIA_URL})
