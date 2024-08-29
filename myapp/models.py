from django.db import models
from datetime import date
from django.contrib.auth.models import User

class Events(models.Model):
    id = models.AutoField(primary_key=True)
    event_id = models.CharField(max_length=20,unique=True)
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    start_date = models.DateField(default=date(2000, 1, 1), null=True)
    end_date = models.DateField(default=date(2000, 1, 1), null=True)
    start_time = models.CharField(max_length=20, default="N/D")
    end_time = models.CharField(max_length=20, default="N/D")
    cottage = models.CharField(max_length=100, null=True)
    room = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.title
    
class Employee(models.Model):
    EmpCode = models.CharField(max_length=20,unique=True)
    Firstname = models.CharField(max_length=20)
    Middlename = models.CharField(max_length=20)
    Lastname = models.CharField(max_length=20)
    EmpImg = models.ImageField(upload_to='employee_images/', null=True, blank=True)
    DateofBirth = models.DateField(default=date(2000, 1, 1), null=True)
    Gender = models.CharField(max_length=8, default="Male")
    CivilStatus = models.CharField(max_length=10, default="N/A")
    Address = models.CharField(max_length=50, default="N/D")
    Position = models.CharField(max_length=50)
    Department = models.CharField(max_length=50, default="N/A", null=True, blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        permissions = [
            ("can_delete_employee", "Can delete employee"),
        ]
    
class BIRREC(models.Model):
    id = models.AutoField(primary_key=True, default=None)
    rdate = models.DateField(default=date(2000, 1, 1), null=True)
    name = models.CharField(max_length=50)
    amtwrd = models.CharField(max_length=100)
    amount = models.CharField(max_length=50)
    birsales = models.CharField(max_length=50, null=True, blank=True)
    biramt = models.CharField(max_length=50)
    birdue = models.CharField(max_length=50)
    tdate = models.DateField(default=date(2000, 1, 1), null=True)
    ttime = models.CharField(max_length=15)
    desc = models.CharField(max_length=255)
    account_id = models.CharField(max_length=10)
    month = models.CharField(max_length=5)
    day = models.CharField(max_length=5)
    yr = models.CharField(max_length=10)
    branch_name = models.CharField(max_length=20)
    status = models.CharField(max_length=2, default="NP")
    p_date =  models.CharField(max_length=2, null=True, blank=True)

    def __str__(self):
        return self.title
    
class past_due(models.Model):
    id = models.AutoField(primary_key=True, default=None)
    pd_id = models.CharField(max_length=20)
    user_id = models.CharField(max_length=20)
    branch_name = models.CharField(max_length=20)
    account_id = models.CharField(max_length=20)
    pd_first_name = models.CharField(max_length=20)
    pd_middle_name = models.CharField(max_length=20)
    pd_last_name = models.CharField(max_length=20)
    pd_balance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    pd_bank = models.CharField(max_length=15)
    pd_class = models.CharField(max_length=5)
    pd_status = models.CharField(max_length=5)
    pd_refdate = models.DateField(null=True, blank=True)
    pd_age = models.CharField(max_length=5)
    pd_address = models.CharField(max_length=200)
    pd_type = models.CharField(max_length=5)
    date_change = models.DateField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    old_account_no = models.CharField(max_length=20)

    class Meta:
        db_table = "past_due"

class past_due_ledger(models.Model):
    id = models.AutoField(primary_key=True, default=None)
    user_id = models.CharField(max_length=20)
    branch_name = models.CharField(max_length=20)
    account_id = models.CharField(max_length=20)
    pdl_date = models.DateField(null=True, blank=True)
    pdl_refno = models.CharField(max_length=50)
    pdl_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    pdl_credit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    pdl_debit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    pay_mis = models.IntegerField()
    include_week = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    old_account_no = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = "past_due_ledger"

class ssp_ledger(models.Model):
    id = models.AutoField(primary_key=True, default=None)
    ssp_ref = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True, default=0)
    ssp_folio = models.CharField(max_length=20)
    ssp_tcode = models.IntegerField()
    ssp_tdate = models.DateField(null=True, blank=True)
    ssp_desc = models.CharField(max_length=20)
    ssp_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    ssp_old_ref = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True, default=0)
    ssp_atm_bal = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)

    class Meta:
        db_table = "ssp_ledger"
    
