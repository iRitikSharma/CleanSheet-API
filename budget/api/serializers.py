from rest_framework import serializers
from .models import Budget


class BudgetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Budget
        fields = "__all__"
        # exclude = ['About']

class ImportSerializer(serializers.Serializer):
    file = serializers.FileField(label="Upload Excel File",help_text="Please upload a .xlsx file with budget data")