from django.shortcuts import render
from django import forms
import spacy

# Загрузка модели SpaCy
nlp = spacy.load("en_core_web_sm")


class TextForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, label="Введите текст")


def extract_entities(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities


def home(request):
    form = TextForm()
    entities = None

    if request.method == "POST":
        form = TextForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data["text"]
            entities = extract_entities(text)

    return render(request, "index.html", {"form": form, "entities": entities})
