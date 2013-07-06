from django.db import models

class Source(models.Model):
    text = models.TextField('source text')
    created_date = models.DateTimeField('date published')
    title = models.CharField('source title', max_length=200)
    address = models.CharField('source web address', max_length=255)
    #kraut = models.BinaryField
    def __unicode__(self):
      return self.title

class Poem(models.Model):
    source = models.ForeignKey(Source, blank=True, null=True)
    text = models.TextField('poem text')
    format_name = models.CharField('poem type', max_length=30)
    up_votes = models.IntegerField(default=0)
    down_votes = models.IntegerField(default=0)
    gen_date = models.DateTimeField('generation date')
    def __unicode__(self):
      return self.text
    def short_title(self):
      return self.source().title()