from django.db import models


	
class College(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    average_cost = models.IntegerField()
    website = models.CharField(max_length = 1000)

    def __str__(self):
        return self.name
	
	