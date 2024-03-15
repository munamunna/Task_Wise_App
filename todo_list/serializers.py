from rest_framework import serializers
from .models import TodoItem

class TodoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoItem
        fields = ['id','title', 'description', 'due_date', 'priority', 'user']
        read_only_fields = ['user']  # Make user field read-only
