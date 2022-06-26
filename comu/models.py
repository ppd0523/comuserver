from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


def upload_file(filter_instance, filename):
	return f'filters/{filter_instance.create_date.strftime("%y%m%d")}_{filter_instance.name}'


def validate_size(file):
	return file if file.size <= 4096 else ValidationError('The file size limit must not exceed 4KB.')


class Filter(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=30, null=False, blank=False)
	# owner = models.ForeignKey(User, to_field='username', null=True, blank=True, on_delete=models.SET_NULL)
	description = models.TextField()
	create_date = models.DateTimeField(default=timezone.localdate, null=False, blank=False, editable=False)
	delete_date = models.DateTimeField(default=None, null=True, blank=True)
	permission = models.PositiveSmallIntegerField(default=1, null=False, blank=False)
	filename = models.FileField(upload_to=upload_file, validators=[validate_size], )

	def __str__(self):
		return f'{self.id} {self.name}'


class Report(models.Model):
	id = models.AutoField(primary_key=True)
	filter = models.ForeignKey(Filter, to_field='id', on_delete=models.CASCADE)
	stock_code = models.CharField(max_length=6, null=False, blank=False)
	create_date = models.DateField(auto_now=True)

	class Meta:
		constraints = [
			models.UniqueConstraint(fields=['filter_id', 'stock_code', 'create_date'], name='unique_reporting'),
		]

	def __str__(self):
		return f'{self.filter} {self.create_date} {self.stock_code}'
