from django.db import models
from django.core.files import File


class Source(models.Model):
    text = models.TextField('source text')
    created_date = models.DateTimeField('date published')
    title = models.CharField('source title', max_length=200)
    address = models.CharField('source web address', max_length=255)
    #kraut = models.BinaryField
    def __unicode__(self):
      return self.title
    #returns the filename for the pickled version
    def dillwithit

class Poem(models.Model):
    source = models.ForeignKey(Source, blank=True, null=True)
    text = models.TextField('poem text')
    format_name = models.CharField('poem type', max_length=30)
    author_name = models.CharField('author name', max_length=100)
    up_votes = models.IntegerField(default=0)
    down_votes = models.IntegerField(default=0)
    votes = models.IntegerField(default=0)
    count_votes = models.IntegerField(default=0)
    gen_date = models.DateTimeField('generation date')
    def __unicode__(self):
      return self.text
    def short_title(self):
      return self.source().title()
