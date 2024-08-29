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

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_past_due_ledger_data(request):
    try:
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('pageSize', 10))
        
        # Ordering to avoid warnings
        past_due_list = past_due_model.objects.order_by('account_id').only(
            'account_id', 'pd_first_name', 'pd_middle_name', 'pd_last_name', 'branch_name'
        )
        
        paginator = Paginator(past_due_list, page_size)
        page_obj = paginator.get_page(page)
        
        combined_data_admin = []
        for due in page_obj:
            ledgers = past_due_ledger_model.objects.filter(account_id=due.account_id).only(
                'pdl_date', 'pdl_refno', 'pdl_debit', 'pdl_credit'
            )
            for ledger in ledgers:
                data = {
                    'account_id': due.account_id,
                    'full_name': f"{due.pd_first_name} {due.pd_middle_name} {due.pd_last_name}",
                    'pdl_date': ledger.pdl_date.strftime('%Y-%m-%d') if ledger.pdl_date else '',
                    'pdl_refno': ledger.pdl_refno,
                    'pdl_debit': ledger.pdl_debit,
                    'pdl_credit': ledger.pdl_credit,
                    'branch_name': due.branch_name,
                    'action': '<button>Action</button>'
                }
                combined_data_admin.append(data)

        return JsonResponse({
            'data': combined_data_admin,
            'recordsTotal': paginator.count,
            'recordsFiltered': paginator.count
        }, safe=False)
    
    except Exception as e:
        return JsonResponse({'error': 'Internal Server Error'}, status=500)