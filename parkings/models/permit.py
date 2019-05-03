from django.db import models

from .mixins import TimestampedModelMixin, UUIDPrimaryKeyMixin


# class PermitArea(models.Model):
#     identifier = models.CharField(max_length=50, primary_key=True)

#     def __str__(self):
#         return self.identifier


# class PermitSubject(models.Model):
#     registration_number = models.CharField(max_length=20, primary_key=True)

#     def __str__(self):
#         return self.registration_number


# class Permit(TimestampedModelMixin, UUIDPrimaryKeyMixin):
#     start_time = models.DateTimeField()
#     end_time = models.DateTimeField()
#     subjects = models.ManyToManyField(PermitSubject, related_name='permits')
#     areas = models.ManyToManyField(PermitArea, related_name='permits')

#     def __str__(self):
#         return (
#             '{start_time:%Y-%m-%d %H:%M} -- {end_time:%Y-%m-%d %H:%M} / '
#             '{subjects} / {areas}'
#         ).format(
#             start_time=self.start_time,
#             end_time=self.end_time,
#             subjects=' '.join(sorted(str(x) for x in self.subjects.all())),
#             areas=' '.join(sorted(str(x) for x in self.areas.all())))


class PermitSeries(TimestampedModelMixin, models.Model):
    active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class PermitQuerySet(models.QuerySet):
    sep = ';'

    def active(self):
        return self.filter(series__active=True)

    def by_time(self, timestamp):
        return self.filter(start_time__lte=timestamp, end_time__gte=timestamp)

    def by_subject(self, subject_identifier):
        return self.filter(_subjects__contains='{sep}{key}{sep}'.format(
            sep=self.sep, key=subject_identifier))

    def by_area(self, area_identifier):
        return self.filter(_areas__contains='{sep}{key}{sep}'.format(
            sep=self.sep, key=area_identifier))


class Permit(TimestampedModelMixin, UUIDPrimaryKeyMixin, models.Model):
    series = models.ForeignKey(PermitSeries, on_delete=models.PROTECT)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    _subjects = models.CharField(max_length=1000)
    _areas = models.CharField(max_length=100)

    objects = PermitQuerySet.as_manager()

    def __init__(self, *args, **kwargs):
        subjects = kwargs.pop('subjects', None)
        if subjects is not None:
            kwargs['_subjects'] = _values_to_string(subjects)
        areas = kwargs.pop('areas', None)
        if areas is not None:
            kwargs['_areas'] = _values_to_string(areas)
        super().__init__(*args, **kwargs)

    @property
    def subjects(self):
        return _string_to_values(self._subjects)

    @subjects.setter
    def subjects(self, values):
        self._subjects = _values_to_string(values)

    @property
    def areas(self):
        return _string_to_values(self._areas)

    @areas.setter
    def areas(self, values):
        self._areas = _values_to_string(values)

    def __str__(self):
        return (
            '{start_time:%Y-%m-%d %H:%M} -- {end_time:%Y-%m-%d %H:%M} / '
            '{subjects} / {areas}'
        ).format(
            start_time=self.start_time, end_time=self.end_time,
            subjects=' '.join(sorted(self.subjects)),
            areas=' '.join(sorted(self.areas)))


def _values_to_string(values, sep=PermitQuerySet.sep):
    return '{sep}{vals}{sep}'.format(sep=sep, vals=';'.join(sorted(values)))


def _string_to_values(string, sep=PermitQuerySet.sep):
    stripped = string.strip(sep)
    return stripped.split(sep) if stripped else []