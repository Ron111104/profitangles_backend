import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from django.http import HttpResponse
import os

def rsi_graph(request):
    if request.method == 'POST' and 'csv_file' in request.FILES:
        csv_file = request.FILES['csv_file']
        df = pd.read_csv(csv_file)

        plt.figure(figsize=(12, 6))
        sns.lineplot(data=df.head(30), x='Date', y='RSI')
        plt.title('RSI Graph (First 30 Days)')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()

        image_path = 'static/images/rsi_graph.png'
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        plt.savefig(image_path)
        plt.close()

        with open(image_path, 'rb') as f:
            return HttpResponse(f.read(), content_type='image/png')

    return render(request, 'visualize/rsi_graph.html')
