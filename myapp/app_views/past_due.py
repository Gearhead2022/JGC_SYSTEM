from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from myapp.models import past_due as past_due_model, past_due_ledger as past_due_ledger_model
from datetime import date
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import F
from django.db.models import Prefetch
import logging

# Set up logging
# logger = logging.getLogger(__name__)

# @login_required(login_url='login')
# def past_due_view(request):

#     user = request.user
#     branch_name = user.username.replace('_', ' ')

#     past_due_list = past_due_model.objects.filter(branch_name=branch_name)
#     return render(request, 'myapp/modules/past_due.html', {'past_due_list': past_due_list})

def past_due_view(request):
    return render(request, 'myapp/modules/past_due.html')

def get_past_due_data(request):
    try:
        user = request.user
        branch_name = user.username.replace('_', ' ')

        # Extract parameters from the request
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('pageSize', 10))
        search_value = request.GET.get('searchValue', '')
        sort_column_index = int(request.GET.get('sortColumnIndex', 0))
        sort_direction = request.GET.get('sortDirection', 'asc')

        # Define the column mapping to your model fields for sorting
        column_mapping = {
            0: 'account_id',
            1: 'pd_first_name',  # Assuming you want to sort by full name which includes first name
            2: 'pd_type',
            3: 'pd_class',
            4: 'pd_bank',
            5: 'pd_refdate'
        }

        # Handle sorting
        sort_column = column_mapping.get(sort_column_index, 'account_id')
        if sort_direction == 'desc':
            sort_column = f'-{sort_column}'

        # Fetch all records
        due = past_due_model.objects.filter(branch_name=branch_name)

        # Apply search filter if there's a search term
        if search_value:
            due = due.filter(
                Q(account_id__icontains=search_value) |
                Q(pd_first_name__icontains=search_value) |  # Include name fields if needed
                Q(pd_middle_name__icontains=search_value) |
                Q(pd_last_name__icontains=search_value) |
                Q(pd_type__icontains=search_value) |
                Q(pd_class__icontains=search_value) |
                Q(pd_bank__icontains=search_value) |
                Q(pd_refdate__icontains=search_value)
            )

        # Apply sorting
        due = due.order_by(sort_column)

        # Pagination
        paginator = Paginator(due, page_size)
        page_obj = paginator.get_page(page)

        # Initialize a list to store combined data
        combined_data_admin = []
        for pd in page_obj:
            data = {
                "action": f'<span class="material-symbols-outlined btn btn-info btn_view_past_due" data-past-due-id="{pd.id}"> preview </span>'
                          f'<span class="material-symbols-outlined btn btn-primary btn_edit_past_due" data-past-due-id="{pd.id}"> edit </span>'
                          f'<span class="material-symbols-outlined btn btn-danger btn_delete_past_due" data-past-due-id="{pd.id}"> delete </span>',
                "account_id": pd.account_id,
                "full_name": f"{pd.pd_first_name} {pd.pd_middle_name} {pd.pd_last_name}",
                "pd_type": pd.pd_type,
                "pd_class": pd.pd_class,
                "pd_bank": pd.pd_bank,
                "pd_refdate": pd.pd_refdate,
                "branch_name": pd.branch_name
            }
            combined_data_admin.append(data)

        # Return a proper JSON response
        return JsonResponse({
            'data': combined_data_admin,
            'recordsTotal': paginator.count,
            'recordsFiltered': paginator.count  # Change this if using server-side search
        }, safe=False)

    except Exception as e:
        return JsonResponse({'error': 'Internal Server Error', 'details': str(e)}, status=500)

def past_due_ledger_view(request, account_id):
    x = date.today().strftime('%Y-%m-%d')
    user = request.user
    branch_name = user.username.replace('_', ' ')

    combined_data = get_combined_data(request, account_id, branch_name)  # Assume this is a helper function

    if combined_data:
        return render(request, 'myapp/modules/past_due_ledger.html', {'combined_data': combined_data, 'x':x})
    else:
        messages.info(request, 'No records found')
        return render(request, 'myapp/modules/past_due_ledger.html', {'x':x})
    
def get_combined_data(request, account_id, branch_name):

    combined_data = []
    current_date = timezone.now().date()

    past_due_list = past_due_model.objects.filter(account_id=account_id, branch_name=branch_name)
    for due in past_due_list:
        pd_id = due.pd_id
        pd_first_name = due.pd_first_name
        pd_middle_name = due.pd_middle_name
        pd_last_name = due.pd_last_name
        pd_class = due.pd_class
        pd_address = due.pd_address
        pd_age = due.pd_age
        pd_balance = due.pd_balance
        pd_refdate = due.pd_refdate

    past_due_ledger_list = past_due_ledger_model.objects.filter(account_id=account_id, branch_name=branch_name).order_by('-pdl_date')

    for ledger in past_due_ledger_list:
        data = {
            "pd_id": pd_id,
            "pdl_id": ledger.id if ledger else '',
            "account_id": ledger.account_id if ledger else '',
            "pd_first_name": pd_first_name,
            "pd_middle_name": pd_middle_name,
            "pd_last_name": pd_last_name,
            "pd_class": pd_class,
            "pd_address": pd_address,
            "pd_age": pd_age,
            "pd_balance": pd_balance,
            "pd_refdate": pd_refdate,
            "branch_name": ledger.branch_name if ledger else '',
            "pdl_date": ledger.pdl_date if ledger else '',
            "pdl_refno": ledger.pdl_refno if ledger else '',
            "pdl_debit": ledger.pdl_debit if ledger else '',
            "pdl_credit": ledger.pdl_credit if ledger else '',
            "pay_mis": ledger.pay_mis if ledger else '',
            "include_week": ledger.include_week if ledger else '',
            "current_date": current_date,
        }
        combined_data.append(data)

    return combined_data

def add_ledger_view(request):
    if request.method == "POST":
        branch_name = request.POST.get("branch_name")
        account_id = request.POST.get("account_id")
        pdl_date = request.POST.get("pdl_date")
        pdl_refno = request.POST.get("pdl_refno")
        pdl_amount = request.POST.get("pdl_amount")

        pay_mis = 1 if request.POST.get("pay_mis") == "on" else 0
        include_week = 1 if request.POST.get("include_week") == "on" else 0

        if float(pdl_amount) > 0:
            pdl_credit = pdl_amount
            pdl_debit = 0
        else:
            pdl_credit = 0 
            pdl_debit = pdl_amount

        try:
            if past_due_ledger_model.objects.filter(account_id=account_id, pdl_refno=pdl_refno).exists():
                return JsonResponse({'success': False, 'error_message': f"Past due ledger with account_id '{account_id}' with ref no '{pdl_refno}' already exist."})

            past_due_ledger_model.objects.create(
                account_id=account_id,
                branch_name=branch_name,
                pdl_date=pdl_date,
                pdl_refno=pdl_refno,
                pdl_credit=pdl_credit,
                pdl_debit=pdl_debit,
                pay_mis=pay_mis,
                include_week=include_week
            )
            return JsonResponse({'success': True})
        except IntegrityError as e:
           return JsonResponse({'success': False, 'error_message': str(e)})
    return JsonResponse({'success': False, 'error_message': 'Invalid request method'})

def edit_ledger_view(request):
    if request.method == "POST":
        pdl_id = request.POST.get("pdl_id")
        account_id = request.POST.get("account_no")
        pdl_date = request.POST.get("pdl_date")
        pdl_refno = request.POST.get("pdl_refno")
        pdl_amount = request.POST.get("pdl_amount")

        pay_mis = 1 if request.POST.get("pay_mis") == "on" else 0
        include_week = 1 if request.POST.get("include_week") == "on" else 0

        if float(pdl_amount) > 0:
            pdl_credit = pdl_amount
            pdl_debit = 0
        else:
            pdl_credit = 0 
            pdl_debit = pdl_amount

        try:
            ledger = past_due_ledger_model.objects.get(id=pdl_id, account_id=account_id)
            ledger.account_id = account_id
            ledger.pdl_date = pdl_date
            ledger.pdl_refno = pdl_refno
            ledger.pdl_credit = pdl_credit
            ledger.pdl_debit = pdl_debit
            ledger.pay_mis = pay_mis
            ledger.include_week = include_week

            ledger.save()
            return JsonResponse({'success': True})
        except past_due_ledger_model.DoesNotExist:
            return JsonResponse({'success': False, 'error_message': f"Past due ledger with ID '{pdl_id}' and account ID '{account_id}' does not exist."})
    return JsonResponse({'success': False, 'error_message': 'Invalid request method'})

def delete_ledger_view(request):
    ledger_id = request.POST.get("ledger_id")
    
    if not ledger_id:
        return JsonResponse({'success': False, 'error_message': 'No ledger ID provided.'})

    try:
        ledger = past_due_ledger_model.objects.get(id=ledger_id)

        ledger.delete()
        return JsonResponse({'success': True})
    except ObjectDoesNotExist:
        return JsonResponse({'success': False, 'error_message': 'Employee not found.'})
    

@csrf_exempt
def get_next_olr_id_series(request):
    if request.method == 'GET':
        branch_name = request.GET.get('branch_name')
        if branch_name:
            try:
                olr_count = past_due_model.objects.filter(branch_name=branch_name, account_id__startswith='000').count()
        
                next_olr_id = f'{olr_count + 1:04d}'
                
                return JsonResponse({'next_olr_id': next_olr_id})
            except past_due_model.DoesNotExist:
                return JsonResponse({'error': 'No records found'}, status=404)
        
        return JsonResponse({'error': 'Branch name is required'}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def view_edit_past_due(request):

    if request.method == 'POST':
        user = request.user
        branch_name = user.username.replace('_', ' ')
        past_due_id = request.POST.get('past_due_id')  # Get the ID from POST request
        pd_account_data = past_due_model.objects.get(id=past_due_id, branch_name=branch_name)
        
        if pd_account_data:

            data = {
                "success": True,
                "id": pd_account_data.id,
                "pd_id": pd_account_data.pd_id,
                "account_id": pd_account_data.account_id,
                "pd_first_name": pd_account_data.pd_first_name,
                "pd_middle_name": pd_account_data.pd_middle_name,
                "pd_last_name": pd_account_data.pd_last_name,
                "pd_class": pd_account_data.pd_class,
                "pd_address": pd_account_data.pd_address,
                "pd_age": pd_account_data.pd_age,
                "pd_balance": pd_account_data.pd_balance,
                "pd_refdate": pd_account_data.pd_refdate,
                "pd_type": pd_account_data.pd_type,
                "branch_name": pd_account_data.branch_name,
                "pd_bank": pd_account_data.pd_bank,
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'success': False, 'message': 'No records found'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@csrf_exempt
def get_next_past_due_code(request):
    if request.method == 'GET':
        try:
            last_past_due = past_due_model.objects.latest('id')
            last_id = last_past_due.id
        except past_due_model.DoesNotExist:
            last_id = 0
        next_pd_code = f'PD{last_id + 1:04d}'
        return JsonResponse({'next_pd_code': next_pd_code})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def add_past_due_view(request):
    if request.method == "POST":
        pd_id = request.POST.get("pd_id")
        account_id = request.POST.get("account_id")
        branch_name = request.POST.get("branch_name")
        pd_first_name = request.POST.get("pd_first_name")
        pd_middle_name = request.POST.get("pd_middle_name")
        pd_last_name = request.POST.get("pd_last_name")
        pd_class = request.POST.get("pd_class")
        pd_address = request.POST.get("pd_address")
        pd_age = request.POST.get("pd_age")
        pd_balance = request.POST.get("pd_balance")
        pd_refdate = request.POST.get("pd_refdate")
        pd_type = request.POST.get("pd_type")
        pd_bank = request.POST.get("pd_bank")

        try:
            if past_due_model.objects.filter(account_id=account_id, pd_id=pd_id).exists():
                return JsonResponse({'success': False, 'error_message': f"Past due ledger with account_id '{account_id}' with Past Due no '{pd_id}' already exist."})

            past_due_model.objects.create(
                pd_id=pd_id,
                account_id=account_id,
                branch_name=branch_name,
                pd_first_name=pd_first_name,
                pd_middle_name=pd_middle_name,
                pd_last_name=pd_last_name,
                pd_class=pd_class,
                pd_address=pd_address,
                pd_age=pd_age,
                pd_balance=pd_balance,
                pd_refdate=pd_refdate,
                pd_type=pd_type,
                pd_bank=pd_bank
            )
            return JsonResponse({'success': True})
        except IntegrityError as e:
           return JsonResponse({'success': False, 'error_message': str(e)})
    return JsonResponse({'success': False, 'error_message': 'Invalid request method'})

def update_past_due_view(request):
    if request.method == "POST":
        id = request.POST.get("edit_id_pd")
        account_id = request.POST.get("edit_pd_account_id")
        branch_name = request.POST.get("branch_name")
        pd_first_name = request.POST.get("edit_pd_first_name")
        pd_middle_name = request.POST.get("edit_pd_middle_name")
        pd_last_name = request.POST.get("edit_pd_last_name")
        pd_class = request.POST.get("edit_pd_class")
        pd_address = request.POST.get("edit_pd_address")
        pd_age = request.POST.get("edit_pd_age")
        pd_balance = request.POST.get("edit_pd_balance")
        pd_refdate = request.POST.get("edit_pd_refdate")
        pd_type = request.POST.get("edit_pd_type")
        pd_bank = request.POST.get("edit_pd_bank")

        try:
            past_due = past_due_model.objects.get(id=id)
            past_due.account_id = account_id
            past_due.branch_name = branch_name
            past_due.pd_first_name = pd_first_name
            past_due.pd_middle_name = pd_middle_name
            past_due.pd_last_name = pd_last_name
            past_due.pd_class = pd_class
            past_due.pd_address = pd_address
            past_due.pd_age = pd_age
            past_due.pd_balance = pd_balance
            past_due.pd_refdate = pd_refdate
            past_due.pd_type = pd_type
            past_due.pd_bank = pd_bank

            past_due.save()
            return JsonResponse({'success': True})
        except past_due_ledger_model.DoesNotExist:
            return JsonResponse({'success': False, 'error_message': f"Past due ledger with ID '{id}' and account ID '{account_id}' does not exist."})
    return JsonResponse({'success': False, 'error_message': 'Invalid request method'})

def delete_past_due_view(request):
    past_due_id = request.POST.get("past_due_id")
    if not past_due_id:
        return JsonResponse({'success': False, 'error_message': 'No ledger ID provided.'})
    try:
        past_due = past_due_model.objects.get(id=past_due_id)
        past_due.delete()
        return JsonResponse({'success': True})
    except ObjectDoesNotExist:
        return JsonResponse({'success': False, 'error_message': 'Employee not found.'})
    

    
# For Pastdue PDF

def past_due_pdf(request):
    account_id = request.GET.get('account_id')
    branch_name = request.GET.get('branch_name')
    data = past_due_model.objects.filter(account_id=account_id, branch_name=branch_name).values()
    return JsonResponse(list(data), safe=False)

def past_due_ledger_pdf(request):
    account_id = request.GET.get('account_id')
    branch_name = request.GET.get('branch_name')
    data = past_due_ledger_model.objects.filter(account_id=account_id, branch_name=branch_name).values()
    return JsonResponse(list(data), safe=False)



# For Admin Side

def past_due_ledger_view_admin(request):
    
    return render(request, 'myapp/modules/past_due_ledger_admin.html')


from django.db.models import Q

def get_past_due_ledger_data(request):
    try:
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('pageSize', 11))
        search_value = request.GET.get('searchValue', '')
        sort_column_index = request.GET.get('sortColumnIndex', 0)
        sort_direction = request.GET.get('sortDirection', 'asc')

        # Define the column mapping to your model fields for sorting
        column_mapping = {
            1: 'account_id',
            2: 'full_name',
            3: 'pdl_date',
            4: 'pdl_refno',
            5: 'pdl_debit',
            6: 'pdl_credit',
            7: 'branch_name'
        }

        # Handle sorting
        sort_column = column_mapping.get(int(sort_column_index), 'branch_name')
        if sort_direction == 'desc':
            sort_column = f'-{sort_column}'
        
        # Initial queryset
        ledgers = past_due_ledger_model.objects.all()

        # Apply search filter if there's a search term
        if search_value:
            ledgers = ledgers.filter(
                Q(account_id__icontains=search_value) |
                Q(branch_name__icontains=search_value) |
                Q(pdl_refno__icontains=search_value)
            )

        # Apply sorting
        ledgers = ledgers.order_by(sort_column)

        # Pagination
        paginator = Paginator(ledgers, page_size)
        page_obj = paginator.get_page(page)

        combined_data_admin = []
        for ledger in page_obj:
            past_due_list = past_due_model.objects.filter(account_id=ledger.account_id, branch_name=ledger.branch_name).only(
                'pd_first_name', 'pd_middle_name', 'pd_last_name'
            )
            for due in past_due_list:
                data = {
                    'action': f'<span class="material-symbols-outlined btn btn-primary btn_edit_past_due_ledger" data-past-due-ledger-id="{ledger.id}"> edit </span>'
                              f'<span class="material-symbols-outlined btn btn-danger btn_delete_ledger" data-past-due-ledger-id="{ledger.id}"> delete </span>',
                    'account_id': ledger.account_id,
                    'full_name': f"{due.pd_first_name} {due.pd_middle_name} {due.pd_last_name}",
                    'pdl_date': ledger.pdl_date.strftime('%Y-%m-%d') if ledger.pdl_date else '',
                    'pdl_refno': ledger.pdl_refno,
                    'pdl_debit': ledger.pdl_debit,
                    'pdl_credit': ledger.pdl_credit,
                    'branch_name': ledger.branch_name
                }
                combined_data_admin.append(data)

        return JsonResponse({
            'data': combined_data_admin,
            'recordsTotal': paginator.count,
            'recordsFiltered': paginator.count  # Change this if using server-side search
        }, safe=False)

    except Exception as e:
        return JsonResponse({'error': 'Internal Server Error', 'details': str(e)}, status=500)


