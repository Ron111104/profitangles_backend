from django.conf import settings
from django.http import JsonResponse
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
from io import BytesIO
import base64
from matplotlib.dates import DateFormatter, AutoDateLocator
from datetime import timedelta
import numpy as np
<<<<<<< Updated upstream
from visualize.models import StockAnalysis
=======
>>>>>>> Stashed changes

matplotlib.use('Agg')  # Use non-GUI backend

def stock_open_price(request):
    try:
        # File path handling
<<<<<<< Updated upstream
        file_path = os.path.join(settings.MEDIA_ROOT, "uploads", "AAPL.csv")
=======
        file_path = os.path.join(settings.MEDIA_ROOT, "uploads", "AAME.csv")
>>>>>>> Stashed changes
        if not os.path.exists(file_path):
            return JsonResponse({"error": f"File not found: {file_path}"}, status=404)

        # Data loading and validation
        df = pd.read_csv(file_path)
        if 'Date' not in df.columns or 'Open' not in df.columns:
            return JsonResponse({
                "error": "CSV must contain 'Date' and 'Open' columns."
            }, status=400)

        # Data preparation
        df['Date'] = pd.to_datetime(df['Date'])
        latest_date = df['Date'].max()
        one_year_ago = latest_date - timedelta(days=365)
        df_last_year = df[df['Date'] >= one_year_ago].copy()

        if df_last_year.empty:
            return JsonResponse({
                "error": "No data available for the last 1 year based on the latest available date."
            }, status=404)

        # Calculate additional metrics
        df_last_year['MA5'] = df_last_year['Open'].rolling(window=5).mean()
        df_last_year['MA20'] = df_last_year['Open'].rolling(window=20).mean()
        
        # Style configuration
        plt.style.use('seaborn-v0_8-whitegrid')
        sns.set_palette("deep")
        
        # Create figure with specific dimensions and DPI
        fig, ax = plt.subplots(figsize=(14, 8), dpi=100)
        
        # Set background colors
        fig.patch.set_facecolor('#f8f9fa')
        ax.set_facecolor('#ffffff')
        
        # Plot main elements
        # Main price line
        ax.plot(df_last_year['Date'], df_last_year['Open'],
                color='#2962ff', linewidth=2, label='Daily Open Price',
                alpha=0.8, zorder=3)
        
        # Moving averages
        ax.plot(df_last_year['Date'], df_last_year['MA5'],
                color='#00c853', linewidth=1.5, label='5-day MA',
                linestyle='--', alpha=0.8, zorder=4)
        
        ax.plot(df_last_year['Date'], df_last_year['MA20'],
                color='#ff6d00', linewidth=1.5, label='20-day MA',
                linestyle='--', alpha=0.8, zorder=4)
        
        # Add price markers at start and end
        start_price = df_last_year['Open'].iloc[0]
        end_price = df_last_year['Open'].iloc[-1]
        price_change = ((end_price - start_price) / start_price) * 100
        
        # Styling improvements
        # Title and labels
        plt.title('Stock Price Analysis - Last 12 Months', 
                 fontsize=16, pad=20, fontweight='bold',
                 color='#1a237e')
        
        ax.set_xlabel('Date', fontsize=12, labelpad=10, color='#424242')
        ax.set_ylabel('Price ($)', fontsize=12, labelpad=10, color='#424242')
        
        # Grid styling
        ax.grid(True, linestyle='--', alpha=0.2, color='#9e9e9e')
        
        # Axis styling
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#424242')
        ax.spines['bottom'].set_color('#424242')
        
        # Tick styling
        ax.tick_params(colors='#424242')
        
        # Date formatter
        date_locator = AutoDateLocator()
        ax.xaxis.set_major_locator(date_locator)
        ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45)
        
        # Add price annotations
        ax.annotate(f'${start_price:.2f}',
                   xy=(df_last_year['Date'].iloc[0], start_price),
                   xytext=(10, 10), textcoords='offset points',
                   color='#424242', fontweight='bold')
        
        ax.annotate(f'${end_price:.2f}\n({price_change:+.1f}%)',
                   xy=(df_last_year['Date'].iloc[-1], end_price),
                   xytext=(10, 10), textcoords='offset points',
                   color='#424242', fontweight='bold')
        
        # Legend styling
        legend = ax.legend(loc='upper left', frameon=True, fancybox=True,
                         shadow=True, fontsize=10)
        legend.get_frame().set_facecolor('#ffffff')
        legend.get_frame().set_alpha(0.9)
        
        # Add volume bars at bottom (scaled)
        if 'Volume' in df_last_year.columns:
            volume_ax = ax.twinx()
            volume_ax.set_ylim(0, df_last_year['Volume'].max() * 3)
            volume_ax.bar(df_last_year['Date'], df_last_year['Volume'],
                        color='#e3f2fd', alpha=0.3, zorder=1)
            volume_ax.set_ylabel('Volume', color='#90a4ae',
                               fontsize=10, labelpad=10)
            volume_ax.tick_params(colors='#90a4ae')
            volume_ax.spines['right'].set_color('#90a4ae')
        
        # Adjust layout
        plt.tight_layout()
        
        # Save the image
        image_path = 'images/stock_analysis.png'
        full_image_path = os.path.join(settings.MEDIA_ROOT, image_path)
        os.makedirs(os.path.dirname(full_image_path), exist_ok=True)
        plt.savefig(full_image_path, dpi=300, bbox_inches='tight',
                   facecolor=fig.get_facecolor(), edgecolor='none')
        
        # Generate base64 image
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight',
                   facecolor=fig.get_facecolor(), edgecolor='none')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()
        plt.close()
        
<<<<<<< Updated upstream
        response_data = {
=======
        return JsonResponse({
>>>>>>> Stashed changes
            'status': 'success',
            'message': 'Enhanced stock analysis graph generated successfully',
            'image': image_base64,
            'image_url': f"{settings.MEDIA_URL}{image_path}",
            'metrics': {
                'start_price': float(start_price),
                'end_price': float(end_price),
                'price_change_percent': float(price_change)
            }
<<<<<<< Updated upstream
        }

        # Save the data to MySQL
        StockAnalysis.objects.create(
            status=response_data['status'],
            message=response_data['message'],
            image=response_data['image'],
            image_url=response_data['image_url'],
            start_price=response_data['metrics']['start_price'],
            end_price=response_data['metrics']['end_price'],
            price_change_percent=response_data['metrics']['price_change_percent']
        )

        return JsonResponse(response_data)

    except Exception as e:
        return JsonResponse({'status': 'error', 'error': str(e)}, status=500)
=======
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error': str(e)
        }, status=500)
>>>>>>> Stashed changes
