from datetime import timezone

from django.db.models import Value, CharField, IntegerField, DateTimeField, F, UUIDField
from django.db.models.functions import Cast
from rest_framework import serializers, viewsets
from rest_framework.response import Response

from parkings.api.enforcement.valid_parking import ValidParkingViewSet
from parkings.models import Parking, PermitLookupItem


class ValidParkingAndPermitSerializer(serializers.Serializer):
    id = serializers.CharField(source="identifier")
    created_at = serializers.DateTimeField(default=None)
    modified_at = serializers.DateTimeField(default=None)
    registration_number = serializers.CharField(default=None)
    time_start = serializers.DateTimeField(default=None)
    time_end = serializers.DateTimeField(default=None)
    zone = serializers.CharField(source="temp_zone")
    area = serializers.CharField(source="area_identifier")
    operator = serializers.CharField(default=None)
    operator_name = serializers.CharField(source="operator.name", default=None)


class ValidParkingAndPermitViewSet(ValidParkingViewSet):
    serializer_class = ValidParkingAndPermitSerializer

    def get_queryset(self):
        parking_queryset = super().get_queryset()

        filter_params = self._get_filter_params(parking_queryset)

        # TODO: Where should filter the permits be?
        reg_num = filter_params['reg_num']
        time = filter_params.get('time') or timezone.now()
        permit_queryset = PermitLookupItem.objects.by_time(time).by_subject(reg_num)

        parking_queryset = parking_queryset.annotate(
            identifier=Cast("id", output_field=CharField())
        )
        parking_queryset = parking_queryset.annotate(
            area_identifier=Value(None, output_field=CharField())
        )
        parking_queryset = parking_queryset.annotate(
            temp_zone=Cast("zone", output_field=CharField())
        )
        parking = parking_queryset.values_list(
            "identifier",
            "created_at",
            "registration_number",
            "time_start",
            "time_end",
            "area_identifier",
            "temp_zone",
            named=True,
        )

        permit_queryset = permit_queryset.annotate(
            identifier=Cast("id", output_field=CharField())
        )
        # filtered_permit_queryset = filtered_permit_queryset.annotate(
        #     created_at=F("permit__created_at")
        # )
        permit_queryset = permit_queryset.annotate(
            temp_zone=Value(None, output_field=CharField())
        )
        permit_queryset = permit_queryset.annotate(
            area_identifier=Cast("area__identifier", output_field=CharField())
        )
        permits = permit_queryset.values_list(
            "identifier",
            "permit__created_at",
            "registration_number",
            "start_time",
            "end_time",
            "area_identifier",
            "temp_zone",
            named=True,
        )

        union = parking.union(permits)
        # print('UNION')
        # print(union.query)

        return union
