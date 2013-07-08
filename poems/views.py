# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from django.template import RequestContext

from poems.models import Poem, Source
import showemapoem.poemformat
from showemapoem.poemifier import Poemifier
from showemapoem.line import Line

import urllib2
from boilerpipe.extract import Extractor

import datetime
import nltk.tokenize.punkt

def index(request):
    latest_poems_list = Poem.objects.order_by('-gen_date')[:5]
    best_poems_list = Poem.objects.order_by('-votes')[:5] #todo: denormalize database to keep track of sum of votes, or something
    #TODO display source titles
    context = RequestContext(request, {
        'latest_poems_list': latest_poems_list,
        'best_poems_list': best_poems_list,
    })
    return render(request, 'poems/index.html', context)

def detail(request, poem_id):
    poem = get_object_or_404(Poem, pk=poem_id)
    return render(request, 'poems/detail.html', {'poem': poem,})

def new(request):
    return render(request, 'poems/new.html', {'format_names': [c.__name__ for c in showemapoem.poemformat.PoemFormat.__subclasses__()]} )

def snap(request, poem_id): #or roll eyes / sigh loudly
    poem = get_object_or_404(Poem, pk=poem_id)
    vote_polarity = pk=request.POST['polarity']
    if vote_polarity == "snap":
      poem.up_votes += 1
    elif vote_polarity == "sigh":
      poem.down_votes += 1
    else:
      #TODO: make this not happen
      raise Http404
    poem.votes = poem.up_votes - poem.down_votes
    poem.count_votes = poem.up_votes + poem.down_votes
    selected_choice.save()
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('poems:detail', args=(poem.id,)))

def create(request):
    try:
        source_url = request.POST['sourceUrl']
        format_name = request.POST['formatName']
        source_text = request.POST['content']
        if len(source_text) < 100 and len(source_url) == 0:
            raise ValidationError, "Too short and no URL"
        elif len(source_text) >= 100:
            title = None
            pass
        elif len(source_url) > 0:
            val = URLValidator()
            val(source_url) #raises ValidationError if invalid url
            #TODO: create source object from URL
            #fail if we've made too many requests to that URL
            html = urllib2.urlopen(source_url).read()
            extractor = Extractor(extractor='DefaultExtractor', html=html)
            #TODO: get title from extractor.html
            source_text = extractor.getText()
    except ValidationError, e:
        # Redisplay the poll voting form.
        return render(request, 'poems/new.html', {
            'error_message': e,
            'format_names': [c.__name__ for c in showemapoem.poemformat.PoemFormat.__subclasses__()],
            'given_source_url': source_url, 
            'given_format_name': format_name, 
            "given_source_text": source_text,
        })
    else:
        # UI: 
        #  1. give boxes to choose source, format
        #  2. "approval page" with button to "show it, poet" or not
        #  3. share page
        sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
        linetexts = sent_detector.tokenize(source_text.replace("\r\n", ". "))

        poemFormatClass = getattr( showemapoem.poemformat, format_name )()
        for allow_partial_lines in [False, True]:
            p = Poemifier( poemFormatClass )
            p.allow_partial_lines = allow_partial_lines
            #this can't be a do... while, because we have to add all the lines, then do various processing steps.
            for linetext in linetexts:
              line = Line(linetext, p.rhyme_checker)
              if line.should_be_skipped():
                continue
              #p.try_line(line) #too slow
              p.add_line(line)
            djangoPoem = Poem()
            raw_poem =  p.create_poem(True)
            if raw_poem:
              break
        if raw_poem:
            poem_text = poemFormatClass.format_poem( raw_poem ).replace("\n", "<br />")
            djangoPoem.text = poem_text
            djangoPoem.format_name = format_name
            djangoPoem.gen_date = datetime.datetime.now()
            djangoPoem.save()
            #TODO

          # Always return an HttpResponseRedirect after successfully dealing
          # with POST data. This prevents data from being posted twice if a
          # user hits the Back button.
            return HttpResponseRedirect(reverse('poems:detail', args=(djangoPoem.id,)))
        else:




            return render(request, 'poems/new.html', {
            'format_names': [c.__name__ for c in showemapoem.poemformat.PoemFormat.__subclasses__()],
            'error_message': "Sorry, couldn't generate a {poemformat}. Try again?".format(poemformat=format_name.lower()),
            'given_source_url': source_url, 
            'given_format_name': format_name, 
            "given_source_text": source_text,
        })

