from rest_framework import serializers
from .models import Invoice, InvoiceDetail

class InvoiceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceDetail
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    details = InvoiceDetailSerializer(many=True, required=False)

    class Meta:
        model = Invoice
        fields = '__all__'

    def create(self, validated_data):
        details_data = validated_data.pop('details', [])  # Extract details data
        invoice = Invoice.objects.create(**validated_data)
        for detail_data in details_data:
            InvoiceDetail.objects.create(invoice=invoice, **detail_data)
        return invoice

    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', [])  # Extract details data
        instance.date = validated_data.get('date', instance.date)
        instance.customer_name = validated_data.get('customer_name', instance.customer_name)
        instance.save()
        existing_details = {detail.id: detail for detail in instance.details.all()}

        # Update existing details and create new ones
        for detail_data in details_data:
            detail_id = detail_data.get('id')
            if detail_id in existing_details:
                # If the detail exists, update it
                detail = existing_details.pop(detail_id)
                for attr, value in detail_data.items():
                    setattr(detail, attr, value)
                detail.save()
            else:
                # If the detail doesn't exist, create it
                InvoiceDetail.objects.create(invoice=instance, **detail_data)

        # Delete any remaining details (if any)
        for detail in existing_details.values():
            detail.delete()

        return instance  # Return the instance here, outside the loop
