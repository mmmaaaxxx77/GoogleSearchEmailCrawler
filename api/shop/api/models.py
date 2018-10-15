import datetime
import traceback
import uuid
from django.utils import timezone

from django.db import models, transaction
from enum import Enum

from django.contrib.auth.models import AbstractUser


class StatusType(Enum):
    DONE = "DONE"
    INPROGRESS = "INPROGRESS"
    INSCHEDULED = "INSCHEDULED"
    FAIL = "FAIL"


class Job(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    title = models.CharField(
        max_length=255,
        blank=False
    )

    query_url = models.CharField(
        max_length=500,
        blank=False
    )

    skip_url = models.CharField(
        max_length=500,
        blank=True
    )

    total_count = models.IntegerField(
        default=0
    )

    skip_count = models.IntegerField(
        default=0
    )

    status = models.CharField(
        max_length=50,
        default=StatusType.INSCHEDULED.value
    )

    filename = models.CharField(
        max_length=50,
        default=""
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return (f'{self.title} {self.query_url}')
