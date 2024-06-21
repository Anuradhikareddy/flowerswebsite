from django.db import models

# delivary_choices = ("free Delivary", "paid delivary")
class FlowerProducts(models.Model):
    name = models.CharField(max_length=160)
    price = models.IntegerField()
    image = models.ImageField(upload_to='images')
    
    def __str__(self):
        return self.name
