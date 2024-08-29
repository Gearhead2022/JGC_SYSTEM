from django.urls import path
from . import views
from .app_views import checkwriter, nah_event, employee, or_printing, past_due, ssp

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('home/', views.home, name='index'),
    path('', views.login_form, name='login'),
    path('logout/', views.logout_form, name='logout_form'),
    path('register/', views.register, name='register'),
    path('checkwriter/', checkwriter.show_all_bnkchck_list, name='checkwriter'),

    path('crudevents/', nah_event.crudevents, name='crudevents'),
    path('get_events/', nah_event.get_events, name='get_events'),
    path('get_next_event_id/', nah_event.get_next_event_id, name='get_next_event_id'),
    path('nah/', nah_event.nah, name='nah'),

    path('employee/', employee.employee, name='employee'),
    path('get_next_emp_code/', employee.get_next_emp_code, name='get_next_emp_code'),
    path('crudemployee/', employee.crudemployee, name='crudemployee'),

    path('or_printing/', or_printing.read_dbf_file, name='or_printing'),
    path('upload_or_file/', or_printing.upload_or_file, name='upload_or_file'),

    path('past_due/', past_due.past_due_view, name='past_due'),
    path('get_past_due_data/', past_due.get_past_due_data, name='get_past_due_data'),

    path('past_due_ledger/<str:account_id>/', past_due.past_due_ledger_view, name='past_due_ledger'),
    path('edit_ledger/', past_due.edit_ledger_view, name='edit_ledger'),
    path('add_ledger/', past_due.add_ledger_view, name='add_ledger'),
    path('delete_ledger_view/', past_due.delete_ledger_view, name='delete_ledger_view'),

    path('past_due_pdf/', past_due.past_due_pdf, name='past_due_pdf'),
    path('past_due_ledger_pdf/', past_due.past_due_ledger_pdf, name='past_due_ledger_pdf'),
    path('get_next_olr_id_series/', past_due.get_next_olr_id_series, name='get_next_olr_id_series'),

    path('view_edit_past_due/', past_due.view_edit_past_due, name='view_edit_past_due'),
    path('get_next_past_due_code/', past_due.get_next_past_due_code, name='get_next_past_due_code'),
    path('add_past_due/', past_due.add_past_due_view, name='add_past_due'),
    path('update_past_due/', past_due.update_past_due_view, name='update_past_due'),
    path('delete_past_due/', past_due.delete_past_due_view, name='delete_past_due'),

    path('past_due_ledger_admin/', past_due.past_due_ledger_view_admin, name='past_due_ledger_admin'),
    path('get_past_due_ledger_data/', past_due.get_past_due_ledger_data, name='get_past_due_ledger_data'),

    path('ssp_ledger/', ssp.ssp_ledger_view, name='ssp_ledger'),
    path('upload_ssp_ledger_file/', ssp.upload_ssp_ledger_file, name='upload_ssp_ledger_file'),
    path('get_ssp_ledger_data/', ssp.get_ssp_ledger_data, name='get_ssp_ledger_data'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
