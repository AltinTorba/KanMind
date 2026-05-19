from django.db import models
from django.contrib.auth.models import User
from kanban_app.models import Board


class Task(models.Model):
    # 🧠 Basic info
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    # 📊 Status (MATCHES MENTOR SPEC)
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

    # 🔥 Priority (MENTOR REQUIRED)
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

    # 🧩 Relations
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

    # 🕒 timestamps (optional but BEST PRACTICE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 🧠 readable representation
    def __str__(self):
        return self.title