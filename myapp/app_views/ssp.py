from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dbfread import DBF
from myapp.models import ssp_ledger as ssp_ledger_model  # Import your model correctly
import os
import tempfile
from django.db.models import Q
from django.core.paginator import Paginator

def ssp_ledger_view(request):  # Renamed the function to avoid conflict
    return render(request, 'myapp/modules/ssp_ledger.html')

@csrf_exempt
def upload_ssp_ledger_file(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('ssp_ledger_file')

        if uploaded_file:
            try:
                # Save uploaded file to a temporary location
                with tempfile.NamedTemporaryFile(delete=False, suffix='.dbf') as temp_file:
                    temp_file.write(uploaded_file.read())
                    temp_file_path = temp_file.name

                # Load the DBF file using dbfread from the temporary location
                dbf = DBF(temp_file_path, encoding='latin-1')  # Adjust the encoding if necessary

                # Loop through records and save to the database
                for record in dbf:
                    # Ensure the fields exist in the record to avoid KeyError
                    data = {
                        "ssp_ref": record.get('REF', ''),
                        "ssp_folio": record.get('FOLIO', ''),
                        "ssp_tcode": record.get('TCODE', ''),
                        "ssp_tdate": record.get('TDATE', None),  # Convert to date if needed
                        "ssp_desc": record.get('DESC', ''),
                        "ssp_amount": record.get('AMOUNT', 0.0),
                        "ssp_old_ref": record.get('OLDREF', ''),
                        "ssp_atm_bal": record.get('ATMBAL', 0.0)
                    }

                    # Save each record to the database
                    ssp_ledger_model.objects.create(
                        ssp_ref=data['ssp_ref'], 
                        ssp_folio=data['ssp_folio'], 
                        ssp_tcode=data['ssp_tcode'], 
                        ssp_tdate=data['ssp_tdate'], 
                        ssp_desc=data['ssp_desc'],
                        ssp_amount=data['ssp_amount'],
                        ssp_old_ref=data['ssp_old_ref'],
                        ssp_atm_bal=data['ssp_atm_bal']
                    )

                # Clean up the temporary file
                os.remove(temp_file_path)

                return JsonResponse({'success': True})
            
            except Exception as e:
                # Handle exceptions and provide feedback
                return JsonResponse({'success': False, 'error_message': str(e)})
        
        else:
            return JsonResponse({'success': False, 'error_message': 'No file uploaded'})
    
    return JsonResponse({'success': False, 'error_message': 'Invalid request method'})

def get_ssp_ledger_data(request):
    try:
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('pageSize', 1))
        search_value = request.GET.get('searchValue', '')
        sort_column_index = request.GET.get('sortColumnIndex', 0)
        sort_direction = request.GET.get('sortDirection', 'asc')

        # Define the column mapping to your model fields for sorting
        column_mapping = {
            0: 'ssp_ref',
            1: 'ssp_folio',
            2: 'ssp_tcode',
            3: 'ssp_tdate',
            4: 'ssp_desc',
            5: 'ssp_amount',
            6: 'ssp_old_ref',
            7: 'ssp_atm_bal'
        }

        # Handle sorting
        sort_column = column_mapping.get(int(sort_column_index), 'ssp_tdate')
        if sort_direction == 'desc':
            sort_column = f'-{sort_column}'
        
        # Initial queryset
        ledgers = ssp_ledger_model.objects.all()
    
        # Apply search filter if there's a search term
        if search_value:
            ledgers = ledgers.filter(
                Q(ssp_ref__icontains=search_value) |
                Q(ssp_folio__icontains=search_value) |
                Q(ssp_tcode__icontains=search_value) |
                Q(ssp_tdate__icontains=search_value) |
                Q(ssp_desc__icontains=search_value) |
                Q(ssp_amount__icontains=search_value) |
                Q(ssp_old_ref__icontains=search_value) |
                Q(ssp_atm_bal__icontains=search_value)
            )

        # Apply sorting
        ledgers = ledgers.order_by(sort_column)

        # Pagination
        paginator = Paginator(ledgers, page_size)
        page_obj = paginator.get_page(page)

        combined_data_admin = []
        count = 0
        for ledger in page_obj:

            data = {
                'ssp_ref': ledger.ssp_ref,
                'ssp_folio': ledger.ssp_folio,
                'ssp_tcode': ledger.ssp_tcode,
                'ssp_tdate': ledger.ssp_tdate,
                'ssp_desc': ledger.ssp_desc,
                'ssp_amount': ledger.ssp_amount,
                'ssp_old_ref': ledger.ssp_old_ref,
                'ssp_atm_bal': ledger.ssp_atm_bal
            }
            combined_data_admin.append(data)

        return JsonResponse({
            'data': combined_data_admin,
            'recordsTotal': paginator.count,
            'recordsFiltered': paginator.count  # Change this if using server-side search
        }, safe=False)

    except Exception as e:
        return JsonResponse({'error': 'Internal Server Error', 'details': str(e)}, status=500)
