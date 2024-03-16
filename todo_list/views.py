from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import TodoItem
from .serializers import TodoItemSerializer
from rest_framework import authentication,permissions
from datetime import date
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

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
    
    def get_overdue_items(self, request):
        # Get today's date
        today = date.today()

        # Filter todos by the authenticated user and due dates that have passed
        overdue_items = TodoItem.objects.filter(user=self.request.user, due_date__lt=today)

        # Serialize the queryset
        serializer = self.get_serializer(overdue_items, many=True)
        
        # Return the serialized data as a response
        return Response(serializer.data)

    
    def get_overdue_item(self, request, pk=None):
        # Get today's date
        today = date.today()

        # Retrieve the specific todo item by pk
        todo_item = get_object_or_404(TodoItem, pk=pk, user=request.user)

        # Check if the todo item is overdue
        if todo_item.due_date < today:
            # Serialize the todo item
            serializer = self.get_serializer(todo_item)
            return Response(serializer.data)
        else:
            return Response({"message": "Todo item is not overdue."}, status=status.HTTP_200_OK)
        
        return Response(serializer.data)

    def update_due_date(self, request, pk):
        try:
            # Retrieve the todo item
            todo_item = TodoItem.objects.get(pk=pk, user=request.user)
        except TodoItem.DoesNotExist:
            # Return 404 if todo item not found
            return Response({"error": "Todo item not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if new_due_date exists in the request data
        new_due_date = request.data.get('new_due_date')
        if not new_due_date:
            return Response({"error": "New due date is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Update the due date
        todo_item.due_date = new_due_date
        todo_item.save()

        # Serialize the updated todo item
        serializer = self.get_serializer(todo_item)
        return Response(serializer.data)

    def destroy(self, request,pk):
        try:
            todo_item = TodoItem.objects.get(pk=pk, user=request.user)
            self.perform_destroy(todo_item)
            return Response({"success": "Todo item deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response({"error": "Todo item does not exist."}, status=status.HTTP_404_NOT_FOUND)
    
    def update(self, request, pk):
        try:
            # Retrieve the todo item
            todo_item = TodoItem.objects.get(pk=pk, user=request.user)
            # Deserialize the request data
            serializer = self.get_serializer(todo_item, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            # Save the updated todo item
            serializer.save()
            # Respond with success message and updated data
            return Response({"success": "Todo item updated successfully.", "data": serializer.data}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            # Handle case where todo item does not exist
            return Response({"error": "Todo item does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Handle any other unexpected errors
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
