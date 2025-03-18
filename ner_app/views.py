from django.shortcuts import render
from django.http import JsonResponse
import spacy

# Загрузка модели spaCy
nlp = spacy.load("en_core_web_sm")  # Для русского языка: "ru_core_news_sm"

def index(request):
    return render(request, 'index.html')

def extract_entities(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')
        doc = nlp(text)

        # Извлечение именованных сущностей
        entities = [{"label": ent.label_, "text": ent.text} for ent in doc.ents]

        return render(request, 'index.html', {'entities': entities})

    return render(request, 'index.html')