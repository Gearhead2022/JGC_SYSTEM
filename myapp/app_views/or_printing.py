from django.shortcuts import render, redirect
import os
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib import messages
from myapp.models import BIRREC

# from simpledbf import Dbf5
from dbfread import DBF

# from django.db.models.signals import pre_delete
# from django.dispatch import receiver

def or_printing(request):
    return render(request, 'myapp/modules/or_printing.html')

@csrf_exempt
def upload_or_file(request):
    if request.method == 'POST':
        or_branch_name = request.POST.get('or_branch_name', 'default_branch')
        uploaded_file = request.FILES.get('or_file')

        if uploaded_file:
            # Construct the file path within MEDIA_ROOT
            file_path = os.path.join('files/branch_or_files/', or_branch_name, uploaded_file.name)
            full_path = os.path.join(settings.MEDIA_ROOT, file_path)

            # Ensure the directory exists
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

               # Save the file, overwriting if it already exists
            with open(full_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # Save the file
            # path = default_storage.save(file_path, ContentFile(uploaded_file.read()))

            return JsonResponse({'success': True, 'file_path': file_path})
        else:
            return JsonResponse({'success': False, 'error_message': 'No file uploaded'})
    else:
        return JsonResponse({'success': False, 'error_message': 'Invalid request method'})
    

def read_dbf_file(request):
    if request.method == 'POST':
        coll_date = request.POST.get('collDate')
        branch_name = request.POST.get('c_branch_name', 'default_branch')

        # Construct the file path
        file_path = os.path.join(settings.MEDIA_ROOT, 'files/branch_or_files/', branch_name, 'UPDTOR.DBF')

        if os.path.exists(file_path):
            try:
                # Open the DBF file with the specified encoding
                dbf = DBF(file_path, encoding='latin-1')  # Adjust the encoding as needed

                # Initialize the array to store collection records
                collection_list = []

                # First loop to collect main records
                for record in dbf:
                    cdate = record['CDATE'].strftime('%Y-%m-%d') if record['CDATE'] else ''
                    if cdate == coll_date and cdate != "":
                        posted = 'TRUE' if record['POSTED'] is True else 'FALSE' if record['POSTED'] is False else str(record['POSTED']).upper()
                        data = {
                            "cdate": cdate,
                            "account_id": record['ID'],
                            "batch": record['BATCH'],
                            "mntheff": record['MNTHEFF'],
                            "amount": record['AMOUNT'],
                            "posted": posted,
                            "collstat": ''.join(e for e in record['COLLSTAT'] if e.isalnum() or e.isspace()),
                            "bankno": record['BANKNO'],
                            "balterm": record['BALTERM'],
                            "atmbal": record['ATMBAL'],
                            "branch_name": branch_name,
                            "name": '',
                            "bank": '',
                            "target": '',
                            "normal": '',
                            "actpnsn": '',
                            "effyr": '',
                            "effmnth": '',
                            "desc": ''
                        }
                        collection_list.append(data)

                # Second loop to update records with additional info
                for data in collection_list:
                    for record in dbf:
                        if data['account_id'] == record['ID'] and not record['CDATE'] and record['NAME']:
                            data['name'] = record['NAME']
                            data['bank'] = record['BANK']
                            data['target'] = record['COLLAMT']
                            data['normal'] = record['PENSION']
                            data['actpnsn'] = record['ACTPNSN']
                            data['bankno'] = record['BANKNO']

                        if BIRREC.objects.filter().exists():

                            birrec = BIRREC.objects.get(account_id=data['account_id'])
                            data['desc'] = birrec.desc

                    # If no record has 'effyr' and 'effmnth', assign them from the first occurrence
                    for record in dbf:
                        if record['PERIOD']:
                            effyr = record['PERIOD'].strftime('%Y')
                            effmnth = record['PERIOD'].strftime('%m')
                            for data in collection_list:
                                data['effyr'] = effyr
                                data['effmnth'] = effmnth
                            break
                
                if collection_list:
                    return render(request, 'myapp/modules/or_printing.html', {'collection_list': collection_list})
                else:
                    messages.info(request, 'No records found')
            except Exception as e:
                messages.error(request, f'Error reading DBF file: {str(e)}')
        else:
            messages.error(request, 'File not found')

    return render(request, 'myapp/modules/or_printing.html')






    
    
# def read_dbf_file(request):
#     if request.method == 'POST':
#         coll_date = request.POST.get('collDate')
#         branch_name = request.POST.get('C_branch_name', 'default_branch')

#         # Construct the file path
#         file_path = os.path.join(settings.MEDIA_ROOT, 'files/branch_or_files/EMB MAIN BRANCH/UPDTOR.DBF')

#         if os.path.exists(file_path):
#             dbf = Dbf5(file_path)
#             df = dbf.to_dataframe()

#             # Filter the dataframe based on the coll_date
#             filtered_df = df[df['CDATE'].apply(lambda x: x.strftime('%Y-%m-%d') == coll_date)]

#             # Initialize the array to store collection records
#             collection_list = []

#             for index, row in filtered_df.iterrows():
#                 data = {
#                     "cdate": row['CDATE'].strftime('%Y-%m-%d'),
#                     "account_id": row['ID'],
#                     "batch": row['BATCH'],
#                     "mntheff": row['MNTHEFF'],
#                     "amount": row['AMOUNT'],
#                     "posted": 'TRUE' if row['POSTED'].upper() == 'TRUE' else 'FALSE',
#                     "collstat": ''.join(e for e in row['COLLSTAT'] if e.isalnum() or e.isspace()),
#                     "bankno": row['BANKNO'],
#                     "balterm": row['BALTERM'],
#                     "atmbal": row['ATMBAL'],
#                     "branch_name": branch_name
#                 }
#                 collection_list.append(data)

#             if collection_list:
#                 return render(request, 'myapp/modules/or_printing.html', {'collection_list': collection_list})
#             else:
#                 return render(request, 'myapp/modules/or_printing.html', {'error_message': 'No records found'})
#         else:
#             return render(request, 'myapp/modules/or_printing.html', {'error_message': 'File not found'})
#     else:
#         return render(request, 'myapp/modules/or_printing.html', {'error_message': 'Invalid request method'})

