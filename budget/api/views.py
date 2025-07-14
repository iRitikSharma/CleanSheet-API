from io import BytesIO
from rest_framework.response import Response    
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser , FormParser
from rest_framework import status
import pandas as pd
import os                                            
from django.core.files.storage import default_storage
from django.conf import settings

from .models import ExcelFile
from .serializers import ImportSerializer

from .budget_changes import main



class ImportView(APIView):
    serializer_class  = ImportSerializer
    parser_classes = [MultiPartParser, FormParser]
    
    def get_view_name(self):
        return "Upload Budget Excel File"

    def post(self,request):
        try:
            data = request.FILES
            # request.data
            serializer = self.serializer_class(data=data)
            if not serializer.is_valid():
                return Response({
                    "Status" : False , 
                    "message" : "Provide a valid file"
                },status = status.HTTP_400_BAD_REQUEST)
            
            excel_file = data.get('file')
            if not excel_file:
                return Response({
                    "Status": False,
                    "message": "No file found in the request"
                }, status=status.HTTP_400_BAD_REQUEST)

            file_bytes = BytesIO(excel_file.read())
            df = pd.read_excel(file_bytes, engine='openpyxl')
            
            file_bytes.seek(0)  # Reset stream position before re-reading
            output_path = main(file_bytes)
            if not output_path:
                return Response({
                    'Status': False,
                    'message': 'EXPORT FAILED! Reason: WBS validation errors.'
                }, status=status.HTTP_400_BAD_REQUEST)
    
            return Response({
                'Status': True,
                'message': f'Excel File imported and exported successfully to {output_path}'
            }, status=status.HTTP_201_CREATED)


        except ValueError as ve:
            error_details = ve.args[0]
            if not isinstance(error_details, list):
                error_details = [str(error_details)]
                
            return Response({
                'Status': False,
                'message': "Validation Error: One or more issues found in the Excel file.",
                'details': error_details
            }, status=status.HTTP_400_BAD_REQUEST)
        
