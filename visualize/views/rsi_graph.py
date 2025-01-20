import os
import pandas as pd
import seaborn as sns
from io import BytesIO
import base64
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def rsi_graph(request):
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

        # Replace NaN values in 'rsi' column with 0
        df['rsi'] = df['rsi'].fillna(0)

        # Create reference lines data
        date_range = pd.date_range(start=df['date'].min(), end=df['date'].max(), freq='D')
        overbought_df = pd.DataFrame({'date': date_range, 'value': 70, 'level': 'Overbought'})
        oversold_df = pd.DataFrame({'date': date_range, 'value': 30, 'level': 'Oversold'})
        reference_df = pd.concat([overbought_df, oversold_df])

        # Set up the seaborn style without grid lines
        sns.set_theme(style="ticks")
        
        # Create the figure with specific size
        g = sns.FacetGrid(df, height=6, aspect=2)

        # Plot RSI line
        rsi_line, = g.ax.plot(df['date'], df['rsi'], color='#d32f2f', linewidth=2, label='RSI')

        # Add reference lines
        overbought_line, = g.ax.plot(
            overbought_df['date'], overbought_df['value'], color='red', linestyle=':', linewidth=1.5, label='Overbought (70)'
        )
        oversold_line, = g.ax.plot(
            oversold_df['date'], oversold_df['value'], color='green', linestyle=':', linewidth=1.5, label='Oversold (30)'
        )

        # Customize the plot
        g.fig.suptitle('RSI Graph with Key Levels', fontsize=16, y=1.02, color='#1a237e', fontweight='bold')
        g.set_axis_labels('Date', 'RSI')
        
        # Rotate x-axis labels
        g.ax.tick_params(axis='x', rotation=45)

        # Adjust the legend
        g.ax.legend(
            handles=[rsi_line, overbought_line, oversold_line],
            labels=['RSI', 'Overbought (70)', 'Oversold (30)'],
            loc='upper left', 
            fontsize=10,
            frameon=False
        )

        # Remove grid lines
        g.ax.grid(False)

        # Adjust layout
        g.fig.tight_layout()

        # Save the plot as a base64 string
        buffer = BytesIO()
        g.fig.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()
        
        # Close the figure to free memory
        g.fig.clear()
        
        # Return the base64 image as JSON response
        return JsonResponse({'image': image_base64})

    except Exception as e:
        return JsonResponse({'status': 'error', 'error': str(e)}, status=500)
