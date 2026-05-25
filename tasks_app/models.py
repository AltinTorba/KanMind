# 1. Django
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

# 3. Local imports
from kanban_app.models import Board


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    STATUS_CHOICES = [
        ("to-do", "To Do"),
        ("in-progress", "In Progress"),
        ("review", "Review"),
        ("done", "Done"),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="to-do"
    )

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default="medium"
    )

    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        related_name="tasks"
    )

    assignee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tasks"
    )

    reviewer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="review_tasks"
    )

    due_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_tasks"
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self):
        return self.title


class Comment(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return f"{self.author.username} - {self.task.title}"