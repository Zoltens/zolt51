from django.db import models


class Name(models.Model):
    name = models.JSONField(null=True, blank=True)


