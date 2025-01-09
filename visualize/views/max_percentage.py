import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from django.http import HttpResponse
import os

def max_percentage_movement(request):
    if request.method == 'POST' and 'csv_file' in request.FILES:
        csv_file = request.FILES['csv_file']
        df = pd.read_csv(csv_file)

        df['Percentage Change'] = (df['High'] - df['Low']) / df['Low'] * 100
        df['7 Day Max Change'] = df['Percentage Change'].rolling(window=7).max()

        plt.figure(figsize=(12, 6))
        sns.lineplot(data=df, x='Date', y='7 Day Max Change')
        plt.title('Max Percentage Movement in 7 Days')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()

        image_path = 'static/images/max_percentage_movement.png'
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        plt.savefig(image_path)
        plt.close()

        with open(image_path, 'rb') as f:
            return HttpResponse(f.read(), content_type='image/png')

    return render(request, 'visualize/max_percentage_movement.html')
