from django.forms import ValidationError
from django.utils import timezone
from rest_framework import serializers

from .models import Client, Mailing, Message, Code, Tag


class CodeSerializer(serializers.Serializer):
    code = serializers.RegexField(regex=r"^\d{3}$")

# Do an external check for mobile operator code and tag
# Create new code and new tag if don't exist
# Do mobile operator code validation
def get_or_create_code_and_tag(data):
    if "operator_code" in data:
        serializer = CodeSerializer(
            data={"code": data.get("operator_code", None)}
        )
        if serializer.is_valid():
            Code.objects.get_or_create(code=data["operator_code"])
        else:
            raise serializers.ValidationError(serializer.errors)
    if "tag" in data:
        if data["tag"] != "":
            Tag.objects.get_or_create(name=data["tag"])
    return data


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["name"]


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"

    def to_internal_value(self, data):
        data = get_or_create_code_and_tag(data)
        return super().to_internal_value(data)


class MailingSerializer(serializers.ModelSerializer):
    messages = serializers.StringRelatedField(many=True)

    class Meta:
        model = Mailing
        fields = (
            "id",
            "start_at",
            "text",
            "finish_at",
            "operator_code",
            "tag",
            "messages",
        )
# Additional validation of the start and end time of the mailing list
    def validate(self, attrs):
        if ("finish_at" in attrs) and ("start_at" in attrs):
            if attrs["finish_at"] <= attrs["start_at"]:
                raise ValidationError(
                    "Mailing finish time "
                    "must be longer than start time"
                )
        if "finish_at" in attrs:
            if attrs["finish_at"] <= timezone.now():
                raise ValidationError(
                    "Mailing finish time "
                    "must be longer than current time"
                )
        return super().validate(attrs)

    def to_internal_value(self, data):
        data = get_or_create_code_and_tag(data)
        return super().to_internal_value(data)


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


class MailingListSerializer(serializers.ModelSerializer):
    status_failed = serializers.ReadOnlyField()
    status_pending = serializers.ReadOnlyField()
    status_success = serializers.ReadOnlyField()
    class Meta:
        model = Mailing
        fields = (
            'id',
            'start_at',
            'finish_at',
            'operator_code',
            'tag',
            'status_failed',
            'status_pending',
            'status_success'
        )
