from django.shortcuts import render
from django.http import JsonResponse
import spacy
from .models import QueryHistory  # Импортируем модель

# Загрузка модели spaCy
nlp = spacy.load("en_core_web_sm")  # Для русского языка: "ru_core_news_sm"


def index(request):
    # Получаем историю запросов
    history = QueryHistory.objects.all().order_by('-created_at')[:10]  # Последние 10 запросов
    return render(request, 'index.html', {'history': history})


def extract_entities(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')
        doc = nlp(text)

        # Извлечение именованных сущностей
        entities = [{"label": ent.label_, "text": ent.text} for ent in doc.ents]

        # Сохранение запроса в базу данных
        QueryHistory.objects.create(text=text, entities=entities)

        # Получаем историю запросов
        history = QueryHistory.objects.all().order_by('-created_at')[:10]

        return render(request, 'index.html', {'entities': entities, 'history': history})

    return render(request, 'index.html')