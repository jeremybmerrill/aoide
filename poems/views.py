# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
#from django.contrib.auth.decorators import login_required
from django.core.files.base import File as DjangoFile

from django.db.models import Count
from django.views.generic import ListView, DetailView

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from django.template import RequestContext

from poems.models import Poem, Source, Fridge
import showemapoem.poemformat
from showemapoem.poemifier import Poemifier
from showemapoem.line import Line


import BeautifulSoup
import urllib2
import urlparse
from boilerpipe.extract import Extractor

import datetime
import nltk.tokenize.punkt

def index(request):
    latest_poems_list = Poem.objects.order_by('-gen_date')[:5]
    popular_sources_list = Source.objects.annotate(num_poems=Count('poem')).order_by('-num_poems')[:5]
    #TODO display source titles
    context = RequestContext(request, {
        'latest_poems_list': latest_poems_list,
        'popular_sources_list': popular_sources_list,
        'format_names': [c.__name__ for c in showemapoem.poemformat.PoemFormat.__subclasses__()]
    })
    return render(request, 'poems/index.html', context)

def detail(request, poem_id):
    poem = get_object_or_404(Poem, pk=poem_id)
    return render(request, 'poems/detail.html', {'poem': poem,})

# def new(request):
#     return render(request, 'poems/new.html', {'format_names': [c.__name__ for c in showemapoem.poemformat.PoemFormat.__subclasses__()]} )

# #@login_required
# def snap(request, poem_id): #or roll eyes / sigh loudly
#     poem = get_object_or_404(Poem, pk=poem_id)
#     vote_polarity = pk=request.POST['polarity']
#     if vote_polarity == "snap":
#       poem.up_votes += 1
#     elif vote_polarity == "sigh":
#       poem.down_votes += 1
#     else:
#       #TODO: make this not happen
#       raise Http404
#     poem.votes = poem.up_votes - poem.down_votes
#     poem.count_votes = poem.up_votes + poem.down_votes
#     selected_choice.save()
#     # Always return an HttpResponseRedirect after successfully dealing
#     # with POST data. This prevents data from being posted twice if a
#     # user hits the Back button.
#     return HttpResponseRedirect(reverse('poems:detail', args=(poem.id,)))

#@login_required
def create(request):
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('poems:index',))
    else:
        format_name = request.POST['formatName']
        if 'sourceUrl' in request.POST:
          source_url = request.POST['sourceUrl']
        else:
          source_url = None
        if 'sourceText' in request.POST:
          source_text = request.POST['sourceText']
        else:
          source_text = None

        #TODO: abstract this out.
        given_context = {
            'given_source_url': source_url, 
            'given_format_name': format_name, 
            "given_source_text": source_text,
            'latest_poems_list': Poem.objects.order_by('-gen_date')[:5],
            "popular_sources_list": Source.objects.annotate(num_poems=Count('poem')).order_by('-num_poems')[:5],
            'format_names': [c.__name__ for c in showemapoem.poemformat.PoemFormat.__subclasses__()]
          }
        try:
            validator = URLValidator()
            #figure out whether to use source_text or source_url
            if source_text and len(source_url.strip()) == 0:
                if len(source_text) > 50:# and validator(source_url):
                    title = None
                    source = None
                else:
                    raise ValidationError("Too short and no URL")
            else:
                try:
                    source = Source.objects.get(address=source_url.split("#")[0])
                except ObjectDoesNotExist:
                    #fail if we've made too many requests to that URL or if we've already gotten that URL
                    try:
                      html = urllib2.urlopen(source_url).read()
                    except urllib2.HTTPError:
                        if "nytimes.com" in source_url:
                            given_context['error_message'] = "Sorry, NYT pages don't work. Copy/paste the text yourself, or try a different page.".format(poemformat=format_name.lower()),
                        else:
                            given_context['error_message'] = "Sorry, couldn't fetch that page. Copy/paste the text yourself, or try a different URL.".format(poemformat=format_name.lower()),
                        return render(request, 'poems/index.html', given_context)

                    extractor = Extractor(extractor='DefaultExtractor', html=html)
                    #TODO: get title from extractor.html
                    soup = BeautifulSoup.BeautifulSoup(html)
                    source_text = extractor.getText()
                    source = Source()
                    source.text = source_text.encode("utf8", "ignore")
                    source.created_date = datetime.datetime.now()
                    source.title = soup.title.string
                    source.address = source_url.split("#")[0]
                    source.save()

        except ValidationError as e:
            # Redisplay the poll voting form.
            given_context['error_message'] = e
            return render(request, 'poems/index.html', given_context)
        else:
            # UI: 
            #  1. give boxes to choose source, format
            #  2. "approval page" with button to "show it, poet" or not
            #  3. share page
            sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
            if source:
                source_text = source.text
            linetexts = sent_detector.tokenize(source_text.replace("\r\n", ". "))
            poemFormatClass = getattr( showemapoem.poemformat, format_name )()
            for allow_partial_lines in [False, True]:
                p = Poemifier( poemFormatClass )
                p.allow_partial_lines = allow_partial_lines
                if source:
                    try:
                        fridge = Fridge.objects.get(format_name=format_name, source__address=source.address)
                    except ObjectDoesNotExist:
                        fridge = None
                else:
                    fridge = None
                if fridge:   #if pickle exists, unpickle here
                    if not allow_partial_lines:
                        try:
                            p.take_out_of_fridge(open(str(fridge.halfsour_nopartials.file), 'rb'))
                            fridge.halfsour_nopartials.close()
                            print "getting nopartials poemifier from the fridge"
                        except ValueError:
                            continue
                    else:
                        p.take_out_of_fridge(open(str(fridge.halfsour_partials.file), 'rb'))
                        fridge.halfsour_partials.close()
                        print "getting partials poemifier from the fridge"
                else:
                    print "adding lines de novo"
                    #this can't be a do... while, because we have to add all the lines, then do various processing steps.
                    for linetext in linetexts:
                      line = Line(linetext.encode("utf8", "ignore"), p.rhyme_checker)
                      if line.should_be_skipped():
                        continue
                      #p.try_line(line) #too slow
                      p.add_line(line)
                    p.prep_for_creation()

                djangoPoem = Poem()
                djangoPoem.source = source
                djangoPoem.includes_partial_lines = allow_partial_lines
                raw_poem = p.create_poem(True)
                if raw_poem:
                  break

        
            if not raw_poem:
                given_context['error_message'] = "Sorry, couldn't generate a {poemformat}. Try again?".format(poemformat=format_name.lower()),
                return render(request, 'poems/index.html', given_context)
            else:
                #if pickled thing doesn't exist yet
                if source and not fridge:
                    with open('/tmp/pickle', 'r+b') as f: #TODO: will have threaded problems
                        fridge = Fridge()
                        if allow_partial_lines:
                            fridge.halfsour_partials = DjangoFile(f)
                            p.put_in_fridge(fridge.halfsour_partials.url)
                        else:
                            fridge.halfsour_nopartials = DjangoFile(f)
                            p.put_in_fridge(fridge.halfsour_nopartials.url)
                        fridge.source = source
                        fridge.format_name = format_name
                        fridge.save()
                    source.save()
                poem_text = poemFormatClass.format_poem( raw_poem )
                djangoPoem.text = poem_text
                djangoPoem.format_name = format_name
                djangoPoem.gen_date = datetime.datetime.now()
                djangoPoem.save()
                # Always return an HttpResponseRedirect after successfully dealing
                # with POST data. This prevents data from being posted twice if a
                # user hits the Back button.
                return HttpResponseRedirect(reverse('poems:detail', args=(djangoPoem.id,)))


class SourceListView(ListView):
    model = Source

class SourceDetailView(DetailView):
    model = Source
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SourceDetailView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['format_names'] = [c.__name__ for c in showemapoem.poemformat.PoemFormat.__subclasses__()]
        return context
