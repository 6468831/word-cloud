from django.core.management.base import BaseCommand

def doublename(word):
    word = word+word
    print(word)
    return word




class Command(BaseCommand):
    
    def add_arguments(self, parser):
        parser.add_argument('word', type=str)

    
    def handle(self, *args, **kwargs):
        word = kwargs['word']
        doublename(word)
