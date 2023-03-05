from rest_framework import serializers


class EventHeaderSerializer(serializers.Serializer):
    Id = serializers.IntegerField(read_only=True)
    UserId = serializers.CharField(max_length=255)
    CameraId = serializers.IntegerField()
    Created = serializers.CharField(max_length=255)
    Path = serializers.CharField(max_length=255)
    IsRequiredObjectDetection = serializers.BooleanField()
    EventVideoId = serializers.IntegerField(read_only=True)

class EventBodySerializer(serializers.Serializer):
    Id = serializers.IntegerField(read_only=True)
    EventHeaderId = serializers.IntegerField(read_only=True)
    Label = serializers.IntegerField()
    Left = serializers.IntegerField()
    Top = serializers.IntegerField()
    Right = serializers.IntegerField()
    Bottom = serializers.IntegerField()

class EventSerializer(serializers.Serializer):
    EventHeader = EventHeaderSerializer()
    EventBodies = EventBodySerializer(many=True)
    Error = serializers.CharField(read_only = True, max_length=255)
