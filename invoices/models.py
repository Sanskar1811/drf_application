from django.db import models

# Model for Invoice
class Invoice(models.Model):
	date = models.DateField()
	customer_name = models.CharField(max_length=100)

	def __str__(self):
		return self.customer_name

# Model for Invoice Detail
class InvoiceDetail(models.Model):
	invoice = models.ForeignKey(Invoice, related_name='details', on_delete=models.CASCADE)
	description = models.CharField(max_length=255)
	quantity = models.IntegerField()
	unit_price = models.DecimalField(max_digits=10, decimal_places=2)
	price = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
        	return f"{self.invoice.customer_name} - {self.description}"



