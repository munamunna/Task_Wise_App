from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import TodoItem
from .serializers import TodoItemSerializer
from rest_framework import authentication,permissions
from datetime import date

class TodoItemViewSet(viewsets.ModelViewSet):
    serializer_class = TodoItemSerializer
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]  # Restrict view to authenticated users only

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
            success_message = "Todo item added successfully."
            return Response({"success": success_message}, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"error": "You must be authenticated to perform this action."},
                status=status.HTTP_401_UNAUTHORIZED
            )
    def get_queryset(self):
        # Filter todos by the authenticated user
        return TodoItem.objects.filter(user=self.request.user)
    
    def get_overdue_items(self,request):
        # Get today's date
        today = date.today()

        # Filter todos by the authenticated user and due dates that have passed
        overdue_items = TodoItem.objects.filter(user=self.request.user, due_date__lt=today)
        
        # Serialize the queryset
        serializer = self.get_serializer(overdue_items, many=True)
        
        return Response(serializer.data)

    def update_due_date(self, request, pk=None):
        try:
            todo_item = TodoItem.objects.get(pk=pk)
        except TodoItem.DoesNotExist:
            return Response({"error": "Todo item not found."}, status=status.HTTP_404_NOT_FOUND)

        new_due_date = request.data.get('new_due_date')

        if not new_due_date:
            return Response({"error": "New due date is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Update the due date
        todo_item.due_date = new_due_date
        todo_item.save()

        serializer = self.get_serializer(todo_item)
        return Response(serializer.data)