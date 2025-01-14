from django.http import JsonResponse
from visualize.models import StockAnalysis

def fetch_stock_data(request):
    try:
        latest_record = StockAnalysis.objects.latest('created_at')  # Fetch the latest entry
        response_data = {
            'status': latest_record.status,
            'message': latest_record.message,
            'image': latest_record.image,
            'image_url': latest_record.image_url,
            'metrics': {
                'start_price': latest_record.start_price,
                'end_price': latest_record.end_price,
                'price_change_percent': latest_record.price_change_percent,
            }
        }
        return JsonResponse(response_data)
    except StockAnalysis.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'No records found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'error': str(e)}, status=500)
