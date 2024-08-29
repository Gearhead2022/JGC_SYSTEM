from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db import IntegrityError
from myapp.models import Employee
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.decorators import login_required

from django.conf import settings
import os

from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseForbidden

# from django.db.models.signals import pre_delete
# from django.dispatch import receiver

def employee(request):
    employees = Employee.objects.all()
    return render(request, 'myapp/modules/employee.html', {'employees': employees})


def crudemployee(request):
    employees = Employee.objects.all()
    if request.method == "POST":

        action = request.POST.get("action")

        if action == "addEmp":
            EmpCode = request.POST.get("EmpCode")
            Firstname = request.POST.get("Firstname")
            Middlename = request.POST.get("Middlename")
            Lastname = request.POST.get("Lastname")
            EmpImg = request.FILES.get("EmpImg")
            DateofBirth = request.POST.get("Birthdate")
            Gender = request.POST.get("Gender")
            CivilStatus = request.POST.get("Status")
            Address = request.POST.get("Address")
            Position = request.POST.get("Position")
            Department = request.POST.get("Department")

            if EmpImg:
                img_path = f"employee_images/{EmpImg.name}"
                img_full_path = os.path.join(settings.MEDIA_ROOT, img_path)
                with open(img_full_path, 'wb+') as destination:
                    for chunk in EmpImg.chunks():
                        destination.write(chunk)
            else:
                img_path = None

            try:
                if Employee.objects.filter(EmpCode=EmpCode, Firstname=Firstname).exists():
                    return JsonResponse({'success': False, 'error_message': f"Employee with EmpCode '{EmpCode}' already exists."})

                Employee.objects.create(
                    EmpCode=EmpCode, 
                    Firstname=Firstname, 
                    Middlename=Middlename, 
                    Lastname=Lastname, 
                    EmpImg=img_path,
                    DateofBirth=DateofBirth,
                    Gender=Gender,
                    CivilStatus=CivilStatus,
                    Address=Address,
                    Position=Position,
                    Department=Department
                )
                return JsonResponse({'success': True})

            except IntegrityError as e:
                return JsonResponse({'success': False, 'error_message': str(e)})


        elif action == "updateEmp":
            
               # Update existing employee
            EmpCode = request.POST.get("EmpCode")
            Firstname = request.POST.get("Firstname")
            Middlename = request.POST.get("Middlename")
            Lastname = request.POST.get("Lastname")
            EmpImg = request.FILES.get("EmpImg")
            DateofBirth = request.POST.get("Birthdate")
            Gender = request.POST.get("Gender")
            CivilStatus = request.POST.get("Status")
            Address = request.POST.get("Address")
            Position = request.POST.get("Position")
            Department = request.POST.get("Department")

            try:
                employee = Employee.objects.get(EmpCode=EmpCode)
                employee.Firstname = Firstname
                employee.Middlename = Middlename
                employee.Lastname = Lastname
                employee.DateofBirth = DateofBirth
                employee.Gender = Gender
                employee.CivilStatus = CivilStatus
                employee.Address = Address
                employee.Position = Position
                employee.Department = Department

                if EmpImg:
                    # Check if the employee already has an image
                    if employee.EmpImg:
                        # Delete the previous image file
                        if os.path.exists(employee.EmpImg.path):
                            os.remove(employee.EmpImg.path)

                    # Save the uploaded file to the media directory
                    employee.EmpImg.save(EmpImg.name, EmpImg, save=True)
                else:
                    img_path = None

                employee.save()
                return JsonResponse({'success': True})
            except Employee.DoesNotExist:
                return JsonResponse({'success': False, 'error_message': f"Employee with EmpCode '{EmpCode}' does not exist."})

      
        elif action == "deleteEmp":
            EmpCode = request.POST.get("EmpCode")
            try:
                employee = Employee.objects.get(EmpCode=EmpCode)
               # Check if the employee has an image and if it exists
                if employee.EmpImg and os.path.exists(employee.EmpImg.path):
                    os.remove(employee.EmpImg.path)

                employee.delete()
                return JsonResponse({'success': True})
            except ObjectDoesNotExist:
                return JsonResponse({'success': False, 'error_message': 'Employee not found.'})

    return render(request, 'myapp/modules/employee.html', {'employees': employees})

@csrf_exempt
def get_next_emp_code(request):
    if request.method == 'GET':
        try:
            last_employee = Employee.objects.latest('id')
            last_id = last_employee.id
        except Employee.DoesNotExist:
            last_id = 0
        next_emp_code = f'EMP{last_id + 1:04d}'
        return JsonResponse({'next_emp_code': next_emp_code})
    return JsonResponse({'error': 'Invalid request'}, status=400)


