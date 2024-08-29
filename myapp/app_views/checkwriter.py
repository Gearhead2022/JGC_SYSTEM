from django.shortcuts import render

from django.http import JsonResponse
from datetime import datetime
from django.contrib import messages
import pyodbc

def show_all_bnkchck_list(request):
    if request.method == 'POST':
        coll_date = request.POST.get('bnkchck_date')

        try:
            datenew = datetime.strptime(coll_date, '%Y-%m-%d').strftime('%m/%d/%Y')

            dsn = "Database"  # ODBC DSN name
            user = ''  # Leave blank if not required
            password = ''  # Leave blank if not required

            # Open the ODBC connection without setting autocommit attribute
            connection = pyodbc.connect(f'DSN={dsn};UID={user};PWD={password}', autocommit=True)
            cursor = connection.cursor()

            # Prepare and execute a query to select records from the DBF file
            sql = "SELECT * FROM BNKCHCK WHERE CDATE = ? AND CHKSTAT = 'P'"
            cursor.execute(sql, datenew)

            # Fetch all records
            records = cursor.fetchall()

            # Convert records to list of dictionaries
            records_list = [dict(zip([column[0] for column in cursor.description], row)) for row in records]

            if records_list:
                return render(request, 'myapp/modules/checkwriter.html', {'records': records_list})
            else:
                messages.info(request, 'No records found')

        except pyodbc.Error as e:
            # return JsonResponse({'success': False, 'error_message': f'Failed to connect to ODBC data source: {e}'})
            messages.error(request, f'Failed to connect to ODBC data source: {str(e)}')
        except ValueError as ve:
            # return JsonResponse({'success': False, 'error_message': f'Invalid date format: {ve}'})
            messages.error(request, f'Invalid date format: {str(ve)}')

    return render(request, 'myapp/modules/checkwriter.html')
