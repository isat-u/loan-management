from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from django.db import IntegrityError
from rest_framework.exceptions import PermissionDenied

from payments.models.payment_history import PaymentHistory as Master

from .serializers import PaymentHistoryPublicSerializer as PublicSerializer
from .serializers import PaymentHistoryPrivateSerializer as PrivateSerializer
from .serializers import PaymentHistoryPrivateCreateSerializer as CreateSerializer
from .serializers import PaymentHistoryPrivateUpdateSerializer as UpdateSerializer


###############################################################################
# Public
###############################################################################
class ApiPublicPaymentHistoryListDetail(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PublicSerializer
    model = Master

    def get_queryset(self):
        filters = {
            'is_active': True
        }
        if 'id' in self.request.GET:
            filters['id'] = self.request.GET.get('id')

        return self.model.objects.filter(**filters)


###############################################################################
# Private
###############################################################################
class ApiPrivatePaymentHistoryViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = PrivateSerializer
    model = Master

    def get_queryset(self):
        filters = {
            'is_active': True
        }
        if 'id' in self.request.GET:
            filters['id'] = self.request.GET.get('id')

        return self.model.objects.filter(**filters)

    @swagger_auto_schema(operation_description="Create Payment History", request_body=CreateSerializer)

    def create(self, request, *args, **kwargs):
        serializer = CreateSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            data['created_by'] = request.user
            try:
                self.model.objects.create(**data)
            except IntegrityError as error:
                return Response(str(error), status=status.HTTP_400_BAD_REQUEST)
            except KeyError as error:
                return Response(str(error), status=status.HTTP_400_BAD_REQUEST)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_description="Update Payment History", request_body=UpdateSerializer)
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()  # override
        serializer = UpdateSerializer(instance, data=request.data, partial=partial)

        if instance.created_by != request.user:
            raise PermissionDenied()

        if serializer.is_valid():
            data = serializer.validated_data
            data['last_updated_by'] = request.user
            data.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_description="Delete Payment History")
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # override

        if instance.created_by != request.user:
            raise PermissionDenied()

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
