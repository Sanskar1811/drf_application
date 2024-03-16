from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Invoice, InvoiceDetail

class InvoiceAPITestCase(TestCase):
    def setUp(self):
        """
        Set up the test environment.
        """
        self.client = APIClient()
        self.invoice = Invoice.objects.create(date='2024-03-15', customer_name='Test Customer')

    def test_get_invoice_list(self):
        """
        Test retrieving a list of invoices.
        """
        response = self.client.get('/invoices/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invoice_detail(self):
        """
        Test retrieving details of a specific invoice.
        """
        response = self.client.get(f'/invoices/{self.invoice.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['customer_name'], self.invoice.customer_name)

    def test_create_invoice(self):
        """
        Test creating a new invoice.
        """
        data = {'date': '2024-03-20', 'customer_name': 'New Customer'}
        response = self.client.post('/invoices/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Invoice.objects.count(), 2)

    def test_update_invoice(self):
        """
        Test updating an existing invoice.
        """
        data = {'date': '2024-03-20', 'customer_name': 'Updated Customer'}
        response = self.client.put(f'/invoices/{self.invoice.pk}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.customer_name, 'Updated Customer')

    def test_delete_invoice(self):
        """
        Test deleting an existing invoice.
        """
        response = self.client.delete(f'/invoices/{self.invoice.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Invoice.objects.filter(pk=self.invoice.pk).exists())

class InvoiceDetailAPITestCase(TestCase):
    def setUp(self):
        """
        Set up the test environment.
        """
        self.client = APIClient()
        self.invoice = Invoice.objects.create(date='2024-03-15', customer_name='Test Customer')
        self.invoice_detail = InvoiceDetail.objects.create(invoice=self.invoice, description='Test Description', quantity=1, unit_price=10.00, price=10.00)

    def test_get_invoice_detail_list(self):
        """
        Test retrieving a list of details for a specific invoice.
        """
        response = self.client.get(f'/invoices/{self.invoice.pk}/details/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_invoice_detail(self):
        """
        Test creating a new detail for a specific invoice.
        """
        data = {'invoice': self.invoice.pk, 'description': 'New Description', 'quantity': 2, 'unit_price': 20.00, 'price': 40.00}
        response = self.client.post(f'/invoices/{self.invoice.pk}/details/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(InvoiceDetail.objects.count(), 2)

    def test_update_invoice_detail(self):
        """
        Test updating an existing detail for a specific invoice.
        """
        data = {
            'invoice': self.invoice.pk,  # Include the required 'invoice' field
            'description': 'Updated Description', 
            'quantity': 2, 
            'unit_price': 20.00, 
            'price': 40.00
        }
        response = self.client.put(f'/invoices/{self.invoice.pk}/details/{self.invoice_detail.pk}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.invoice_detail.refresh_from_db()
        self.assertEqual(self.invoice_detail.description, 'Updated Description')

    def test_delete_invoice_detail(self):
        """
        Test deleting an existing detail for a specific invoice.
        """
        response = self.client.delete(f'/invoices/{self.invoice.pk}/details/{self.invoice_detail.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(InvoiceDetail.objects.filter(pk=self.invoice_detail.pk).exists())
