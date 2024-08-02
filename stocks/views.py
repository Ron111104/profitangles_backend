from rest_framework.views import APIView
from rest_framework.response import Response
import yfinance as yf

class StockDataView(APIView):
    def get(self, request, symbol):
        try:
            stock = yf.Ticker(symbol)
            stock_info = stock.info
            # print(stock_info)
            response_data = {
                "symbol": stock_info.get('symbol'),
                "price": stock_info.get('currentPrice'),
                "prev_close": stock_info.get('previousClose'),
                "sector":stock_info.get('sector'),
                "index": stock_info.get('exchange')
            }
            return Response(response_data)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
