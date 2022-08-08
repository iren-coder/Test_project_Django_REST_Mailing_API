from django.db import models
from django.contrib.auth.models import User  
import pytz
from django.core.validators import RegexValidator

# Create your models here.

# User
class UserProfile(models.Model):  
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

# Mobile operator code
class Code(models.Model):
    error_message = "Mobile operator code format XXX. Please, check the input"
    code_validator = RegexValidator(
        regex=r"^\d{3}$",
        message=error_message,
    )
    code = models.CharField(
        max_length=3,
        validators=[code_validator],
        primary_key=True,
        verbose_name="mobile operator code",
    )

    def __str__(self):
        return str(self.code)

# Tag
class Tag(models.Model):
    name = models.CharField(
        max_length=30,
        primary_key=True,
        verbose_name="tag",
    )

    def __str__(self):
        return self.name

# Client
class Client(models.Model):
    error_message = "Phone number format 7XXXXXXXXXX. Please, check the input"
    phone_validator = RegexValidator(
        regex=r"^7\d{10}$",
        message=error_message,
    )
    phone_number = models.CharField(
        max_length=11,
        validators=[phone_validator],
        null=False,
        verbose_name="Mobile number",
    )

    operator_code = models.ForeignKey(
        Code,
        null=False,
        on_delete=models.CASCADE,
        verbose_name="Mobile number code",
    )
    tag = models.ForeignKey(
        Tag,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="tag",
    )

    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

    timezone = models.CharField(
        max_length=32,
        choices=TIMEZONES,
        default="Europe/Moscow",
        verbose_name="time zone",
    )

    def __str__(self):
        return f"{self.phone_number} - {self.tag}"


# Mailing
class Mailing(models.Model):
    start_at = models.DateTimeField(
        null=False,
        verbose_name="mailing start",
    )
    text = models.TextField(
        null=False,
        verbose_name="message",
    )
    operator_code = models.ForeignKey(
        Code,
        null=False,
        on_delete=models.CASCADE,
        verbose_name="Mobile number code",
    )
    tag = models.ForeignKey(
        Tag,
        null=False,
        on_delete=models.CASCADE,
        verbose_name="tag",
    )
    finish_at = models.DateTimeField(
        null=False,
        verbose_name="mailing end",
    )

    def __str__(self):
        return f"{self.start_at} - {self.operator_code} - {self.tag}"

# Message
class Message(models.Model):
    created_at = models.DateTimeField(
        null=False,
        auto_now_add=True,
        verbose_name="sending time",
    )
    status = models.CharField(
        max_length=20,
        null=False,
        verbose_name="status",
    )
    maillist = models.ForeignKey(
        Mailing,
        null=False,
        on_delete=models.CASCADE,
        verbose_name="mailing",
        related_name="messages",
    )
    customer = models.ForeignKey(
        Client,
        null=False,
        on_delete=models.CASCADE,
        verbose_name="client",
    )

    def __str__(self):
        return f"{self.id} - {self.created_at} - {self.status}"
