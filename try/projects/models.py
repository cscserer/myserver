from django.db import models

# Create your models here.


class Feature(models.Model):
    agd = models.CharField(max_length=200, help_text="average geodesic distance")
    cf = models.CharField(max_length=200, help_text="conformal factors")
    mytanhgaussian = models.CharField(max_length=200, help_text="Gaussian curvature")
    geobase = models.CharField(max_length=200, help_text="geodesic distance to bottom")
    normalsangle = models.CharField(max_length=200, help_text="angle of normal vector")
    sdfval = models.CharField(max_length=200, help_text="shape diameter function")
    area = models.CharField(max_length=200, help_text="face area")
    version = models.IntegerField(default=0)


class Statistics(models.Model):
    total_vertices = models.IntegerField(default=0)
    total_faces = models.IntegerField(default=0)
    total_area = models.FloatField(default=0)
    min_area = models.FloatField(default=0)
    max_area = models.FloatField(default=0)
    mean_area = models.FloatField(default=0)
    std_area = models.FloatField(default=0)
    var_area = models.FloatField(default=0)
    version = models.IntegerField(default=0)


class Mesh(models.Model):
    feature = models.ForeignKey(Feature, on_delete=models.SET_NULL, null=True)
    statistics = models.OneToOneField(Statistics, on_delete=models.SET_NULL, null=True)
    path = models.CharField(max_length=200, unique=True)
    dir = models.CharField(max_length=200, default="")
    kind = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    suffix = models.CharField(max_length=10)
    version = models.IntegerField(default=0)


class Scatter(models.Model):
    name = models.CharField(max_length=200)
    path = models.CharField(max_length=200)
    version = models.IntegerField(default=0)
    dict = models.CharField(max_length=1000)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'path', 'version'], name='unique_together')
        ]