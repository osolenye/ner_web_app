from django.db import models

class QueryHistory(models.Model):
    text = models.TextField()  # Текст запроса
    entities = models.JSONField(default=list)  # Извлеченные сущности (в формате JSON)
    created_at = models.DateTimeField(auto_now_add=True)  # Время создания записи

    def __str__(self):
        return f"Query: {self.text[:50]}..."