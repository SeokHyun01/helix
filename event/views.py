from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from ultralytics import YOLO
from PIL import Image
from event.serializers import EventSerializer
from rest_framework import status
from rest_framework.exceptions import ValidationError


class EventViewSet(ViewSet):
    serializer_class = EventSerializer
    model = YOLO("yolov8l.pt")

    def create(self, request, *args, **kwargs):
        try:
            event_header = request.data['EventHeader']
        except KeyError:
            return Response({'Error': 'EventHeader key not found.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_id = event_header['UserId']
            camera_id = event_header['CameraId']
            created = event_header['Created']
            path = event_header['Path']
        except KeyError:
            return Response({'Error': 'UserId, CameraId, Created, or Path key not found in EventHeader.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            image = Image.open(path)
        except FileNotFoundError:
            return Response({'Error': 'File not found.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            results = self.model.predict(source=image)
        except Exception as e:
            return Response({'Error': 'Failed to get model predictions.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        event_bodies = []
        for result in results:
            for bbox, cls in zip(result.boxes.xyxy, result.boxes.cls):
                left, top, right, bottom = bbox.tolist()
                event_bodies.append({
                    'Label': cls.item(),
                    'Left': left,
                    'Top': top,
                    'Right': right,
                    'Bottom': bottom
                })

        event = {
            'EventHeader': {
                'UserId': user_id,
                'CameraId': camera_id,
                'Created': created,
                'Path': path,
                'IsRequiredObjectDetection': False,
            },
            'EventBodies': event_bodies,
        }

        image.close()

        try:
            serializer = self.serializer_class(data=event)
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            return Response({'Error': 'Failed to serialize data.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.data, status=status.HTTP_200_OK)
