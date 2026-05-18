from django.db import models

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=[
            ("todo", "To Do"),
            ("doing", "Doing"),
            ("done", "Done")
        ],
        default="todo"
    )

    board = models.ForeignKey(
        "kanban_app.Board",
        on_delete=models.CASCADE,
        related_name="tasks"
    )

    assignee = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )