from django.forms import formset_factory
from django.shortcuts import render, redirect
from rest_framework import generics

from .forms import NameForm
from .models import Name
from .serializers import NameSerializer


def index(request):
    formset = formset_factory(NameForm)
    return render(request, 'index.html', {'formset': formset})


def save_data(request):
    NameFormSet = formset_factory(NameForm)
    if request.method == 'POST':
        formset = NameFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                Name.objects.create(name=form.cleaned_data.get('name'))
        return redirect('index')


class NameView(generics.ListAPIView):
    queryset = Name.objects.all()
    serializer_class = NameSerializer
