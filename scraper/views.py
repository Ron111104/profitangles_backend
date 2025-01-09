from django.http import JsonResponse
from scraper.scraper import scrape_trending_data  # Import your scraping function

def scrape_view(request):
    try:
        # Attempt to scrape data
        data = scrape_trending_data()  # Updated function name
        
        # Return the scraped data as a JSON response
        return JsonResponse({'data': data}, status=200)
    
    except Exception as e:
        # If an error occurs, return the error message as a JSON response
        return JsonResponse({'error': str(e)}, status=500)
