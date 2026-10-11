
from rest_framework import viewsets
from .models import LeaveRequest
from .serializers import LeaveRequestSerializer


class LeaveRequestViewSet(viewsets.ModelViewSet):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer
