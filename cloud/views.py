from sys import stdout
from django.shortcuts import render
from django.views import View
from django.core.management import call_command
from utils import parser
from utils import test
from scipy.interpolate import interp1d
from django.db import transaction

from cloud.models import MapWord, Myword



# from .models import Myword


class ShowCloud(View):
    def get(self, request):
        word = str(self.request.GET.get("query"))
       
        #out = StringIO()
        # with StringIO() as out:
        #     call_command("parsegoogle", word, stdout=out)
        #     x = out.getvalue()
        
        #     print(f"!{x}")
        # MapWord.objects.all().delete()
        if word != "None":
            parser.new_word(word)
            #parser.parse_links(word)
            words, minvalue, maxvalue = parser.show_cloud(word, 250)
            #parser.get_minus_words()

            lst = []
            
            m = interp1d([minvalue,maxvalue],[16,100]) #mapping word frequencies to fontsizes
            recent_searches = Myword.objects.all()

            for i in words:
                lst.append((i[0].lower(), int(m(i[1]))))
            # maxv = lst[0][1]
            # minv = lst[-1][1]
            lst = set(lst)
            context = {
                "lst" : lst,
                "word": word,
                "recent_searches": recent_searches
            }
        else:
            context = {

            }
        return render(request, "cloud/index.html", context)

    