from django.db import models
from django.core.files import File
from django.core.files.storage import FileSystemStorage

fs = FileSystemStorage()

class Source(models.Model):
    text = models.TextField('source text')
    created_date = models.DateTimeField('date published')
    title = models.CharField('source title', max_length=200)
    address = models.CharField('source web address', max_length=255)

    #halfsour = models.FileField(upload_to='thefridge')
    #a pickle is uniquely IDed by a format [haiku], whether partial lines are allowed [true/false] and a source

    def __unicode__(self):
      return self.title

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
    includes_partial_lines = models.BooleanField('includes partial lines')
    def __unicode__(self):
      return self.text
    def short_title(self):
      return self.source().title()

class Fridge(models.Model):
    source = models.ForeignKey(Source, blank=True, null=True)
    format_name = models.CharField('poem type', max_length=30)
    halfsour_nopartials = models.FileField(storage=fs, upload_to="%Y%m%d%H%M%S.nopartials.pickle")
    halfsour_partials = models.FileField(storage=fs, upload_to="%Y%m%d%H%M%S.partials.pickle")
    #a pickle is uniquely IDed by a format [haiku], whether partial lines are allowed [true/false] and a source
