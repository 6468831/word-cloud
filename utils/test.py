from cloud.models import Myword, MapWord, Link

def new(word):
    url = "https://microsoft.com"
    if Myword.objects.filter(word=word).exists():
        if Link.objects.filter(link = url): 
            Myword.objects.get(word=word).links.add(Link.objects.get(link=url))
        else:
            Link.objects.create(link=url)
            Myword.objects.get(word=word).links.add(Link.objects.get(link=url))
