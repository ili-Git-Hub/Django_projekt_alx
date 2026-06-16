from django.http import HttpResponse
from django.shortcuts import render

# funkcja indeksowa ktora zwraca w przegladarce odpowiedz (indeksowa jest tylko zaslepka na szybko
# bo generalnie w html bedziemy pozniej to pisac)
# def index(request):
#     return HttpResponse("<h1>DevBoard - etap 1: scaffold!</h1>")

# funkcja renderowa
def index(request):
    return render(request, 'index.html')
