from typing import Tuple
from django.db import models
from django.db.models.base import Model
from .utils import *
from paranoid_model.models import Paranoid
from django.core.validators import MaxValueValidator, MinValueValidator 
import uuid


# Create your models here.
class BaseModel(models.Model):
	uuid = models.UUIDField(default=uuid.uuid4, unique=True)

	class Meta:
		abstract = True


class Vat(BaseModel):
	description = models.CharField(max_length=10, blank=True, null=True)
	amount = models.FloatField(default=0)


class Cost(BaseModel):
	description = models.CharField(max_length=50)
	amount = models.FloatField(null=False)
	priority = models.IntegerField(default=0)
	# active = models.BooleanField(default=False, blank=False)
	vat = models.ForeignKey(Vat, on_delete=models.CASCADE, null=True,blank=True)
	
	def __str__(self):
		return self.description


class CostQuantity(BaseModel):
	cost = models.ForeignKey(Cost, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
	amount = models.FloatField(blank=True, null=False,default=0)

	def __str__(self):
		return self.cost.description
	


class Validation(BaseModel):
	calculation_type = models.IntegerField(choices=CALCULATION_TYPES)
	reference = models.CharField(max_length=15)
	make = models.CharField(max_length=25, choices=VEHICLE_MAKES, blank=True, null=True)
	model = models.CharField(max_length=50)
	amount_purchase = models.FloatField()
	purchase_vat = models.BooleanField(default=False)
	amount_sale = models.FloatField()
	sale_vat = models.BooleanField(default=False)
	margin = models.FloatField(blank=True, null=True)
	type = models.IntegerField(choices=((0,0),(1,1),(2,2)))
	risk = models.IntegerField(choices=((1,1),(2,2)), null=True, blank=True)
	costs = models.ManyToManyField(CostQuantity,null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)


class Profitability(models.Model):
	min_purchase_range = models.IntegerField()
	max_purchase_range = models.IntegerField()
	typeA = models.IntegerField()
	typeB = models.IntegerField()
	typeC = models.IntegerField()