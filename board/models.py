# Create your models here.
from django.db import models
# Create your models here.
from django.db import models

from django.core import validators
from django.db.models import Avg
class NaverMovie(models.Model):
    column1 = models.IntegerField(blank=True, null=True)  # Field name made lowercase.
    moviecode = models.IntegerField(primary_key=True)
    moviename = models.CharField(max_length=50, blank=True, null=True)
    genre = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    timeline = models.CharField(max_length=50, blank=True, null=True)
    openingdate = models.DateField(blank=True, null=True)
    valuation = models.FloatField(blank=True, null=True)
    director = models.CharField(max_length=50, blank=True, null=True)
    grade = models.CharField(max_length=50, blank=True, null=True)
    actors = models.CharField(max_length=50, blank=True, null=True)
    heartcount = models.IntegerField(blank=True, null=True)
    story = models.TextField(blank=True, null=True)
    image = models.CharField(max_length=128, blank=True, null=True)
    wc = models.TextField(blank=True, null=True)


    @property
    def avg_score(self):
        return self.starcomments_set.aggregate(avg_score=Avg('starscore'))['avg_score']


class StarComments(models.Model):
    column1 = models.IntegerField(blank=True, null=True)
    moviecode = models.ForeignKey(NaverMovie, on_delete=models.DO_NOTHING, db_column='moviecode', blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    sctime = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    starscore = models.IntegerField(blank=True, null=True)
    recomm = models.IntegerField(blank=True, null=True, default=0)
    unrecomm = models.IntegerField(blank=True, null=True, default=0)
    nicknid = models.TextField(blank=True, null=True)
    userid = models.CharField(max_length=50, blank=True, null=True)
    nickname = models.TextField(blank=True, null=True)
