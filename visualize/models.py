from django.db import models
import json

class StockAnalysis(models.Model):
    status = models.CharField(max_length=20)
    message = models.TextField()
    image = models.TextField()
    image_url = models.TextField()
    start_price = models.FloatField()
    end_price = models.FloatField()
    price_change_percent = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def metrics_as_json(self):
        return json.dumps({
            "start_price": self.start_price,
            "end_price": self.end_price,
            "price_change_percent": self.price_change_percent
        })
