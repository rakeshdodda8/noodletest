from django.db import models

# Create your models here.
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    category = models.CharField(max_length=50, blank=True)

    def as_json(self):
        return dict(
            id=self.id,
            name=self.name, 
            price=self.price,
            category=self.category)
    
    def __unicode__(self):
        return u'%s' % (self.name)