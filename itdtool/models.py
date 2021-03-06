from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.db.models import signals
from django.dispatch import dispatcher
# Create your models here.


# class UserAction(models.Model):
#     username = models.CharField(max_length=30)
#     routeradmin = models.CharField(max_length=30)
#     lsname = models.CharField(max_length=30)
#     date_modified = models.DateTimeField(auto_now=True)
#     router_task = models.TextField()
#     script_commited = models.TextField()
#
#     def __str__(self):
#         output = self.username+" "+self.script_commited
#         return output


class QueryParameters(models.Model):
    description = models.TextField()
    keywords = models.TextField()#snowden
    location = models.CharField(max_length=30) # ["Athens", "Rome", "Madrid"]
    start_date = models.DateField() # starting time period to search
    end_date = models.DateField()  # ending time period to search
    inference = models.BooleanField()
    questions = models.BooleanField()
    twitter = models.BooleanField()
    google = models.BooleanField()
    youtube = models.BooleanField()
    date_param_added = models.DateTimeField(auto_now=True)
    category = models.IntegerField()
    topic = models.TextField()

    def __str__(self):
        output = self.description + " " + self.keywords
        return output


# keyword	language	year	month	count	location
class AdwordsResults(models.Model):
    keyword = models.TextField() #snowden
    language = models.CharField(max_length=30) #["en", "el"]
    location = models.CharField(max_length=30) # ["Athens", "Rome", "Madrid"]
    year = models.IntegerField() # 2016
    month = models.IntegerField()  # 5
    date_param_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        output = self.keyword + " " + self.location+" "+self.month+" "+self.year
        return output


class HistoryModel (models.Model):
    query_id = models.IntegerField()
    query_desc = models.TextField()
    user_name = models.CharField(max_length=30)
    results = models.TextField()
    execution_date = models.DateTimeField(auto_now=True)
    keyword = models.TextField()
