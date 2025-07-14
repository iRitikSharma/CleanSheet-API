from django.db import models

# Create your models here.
class Budget(models.Model):
    File_Name = models.CharField(max_length=100,default = False)
    title = models.CharField(max_length=100,default = False)
    About = models.TextField(default = False)


class ExcelFile(models.Model):

    description = models.CharField(max_length=100)
    wbs_category = models.FloatField(null=True, default=None)
    wbs_code = models.CharField(max_length=50, null=True, default=None)
    total_budget = models.FloatField(null=True, default=None)
    april = models.FloatField(null=True, default=None)
    may = models.FloatField(null=True, default=None)
    june = models.FloatField(null=True, default=None)
    july = models.FloatField(null=True, default=None)
    august = models.FloatField(null=True, default=None)
    september = models.FloatField(null=True, default=None)
    october = models.FloatField(null=True, default=None)
    november = models.FloatField(null=True, default=None)
    december = models.FloatField(null=True, default=None)
    january = models.FloatField(null=True, default=None)
    february = models.FloatField(null=True, default=None)
    march = models.FloatField(null=True, default=None)

    def __str__(self):
        return self.description
    