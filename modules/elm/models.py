
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


class Employee(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class LeaveRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("canceled", "Canceled"),
        ("extended", "Extended"),
        ("resumed", "Resumed"),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="leave_requests",
    )
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )
    reason = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        permissions = [
            ("can_submit_leave", "Can submit leave"),
            ("can_approve_leave", "Can approve leave"),
            ("can_reject_leave", "Can reject leave"),
            ("can_withdraw_leave", "Can withdraw leave"),
            ("can_cancel_leave", "Can cancel leave"),
            ("can_extend_leave", "Can extend leave"),
            ("can_resume_leave", "Can resume leave"),
            ("can_view_leave_history", "Can view leave history"),
        ]

    def clean(self):
        super().clean()
        if (
            self.start_date
            and self.end_date
            and self.end_date < self.start_date
        ):
            raise ValidationError(
                {"end_date": "End date cannot be earlier than start date."}
            )
