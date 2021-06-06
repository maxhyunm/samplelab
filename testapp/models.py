from django.db import models
# from picklefield.fields import PickledObjectField

class Data(models.Model) :
    idx = models.AutoField(primary_key=True)
    datafile = models.JSONField()
    detailfile = models.JSONField(null=True)
    fixedfile = models.JSONField(null=True)
    fixednumfile = models.JSONField(null=True)
    up_date = models.DateTimeField(auto_now_add=True)

class Temp(models.Model) :
    idx = models.AutoField(primary_key=True)
    xcols = models.CharField(max_length=500, null=True)
    ycol = models.CharField(max_length=200, null=True)
    testsize = models.DecimalField(decimal_places=1, max_digits=3, null=True)
    dataid = models.IntegerField(null=True)