from django.db import models


class Employees(models.Model):
    class Meta:
        db_table = "employee"

    emp_no = models.AutoField(primary_key=True)
    birth_date = models.DateField()
    first_name = models.CharField(max_length=14)
    last_name = models.CharField(max_length=16)
    gender = models.CharField(max_length=1)
    hire_date = models.DateField()


class Departments(models.Model):
    class Meta:
        db_table = "department"

    dept_no = models.CharField(primary_key=True, max_length=4)
    dept_name = models.CharField(unique=True, max_length=40)


class DeptEmp(models.Model):
    class Meta:
        db_table = "emp_dept"
        unique_together = ("emp_no", "dept_no")

    emp_no = models.IntegerField()
    dept_no = models.CharField(max_length=4)
    from_date = models.DateField()
    to_date = models.DateField()


class DeptManager(models.Model):
    class Meta:
        db_table = "manager_deptartment"

    emp_no = models.IntegerField()
    dept_no = models.CharField(max_length=4)
    from_date = models.DateField()
    to_date = models.DateField()


class Salaries(models.Model):
    class Meta:
        db_table = "salary"

    emp_no = models.IntegerField()
    salary = models.IntegerField()
    from_date = models.DateField()
    to_date = models.DateField()


class Titles(models.Model):
    class Meta:
        db_table = "title"

    emp_no = models.IntegerField()
    title = models.CharField(max_length=50)
    from_date = models.DateField()
    to_date = models.DateField()
