from django.db import models


class Function(models.Model):
    name = models.CharField(max_length=120)
    params = models.TextField()
    code = models.TextField()

    def __str__(self):
        return self.name
