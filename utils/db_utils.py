from dataclasses import dataclass
from datetime import datetime, date


DATE_FORMAT_STR = "%Y-%m-%d"

DEFAULT_TO_DATE = "9999-01-01"
DEFAULT_TO_DATE_STR_FORMAT = "%Y-%m-%d"


class SameDeptExp(Exception):
    pass


class SameStartDate(Exception):
    pass


def _return_default_to_date():
    return datetime.strptime(DEFAULT_TO_DATE, DEFAULT_TO_DATE_STR_FORMAT)


@dataclass
class EmployeeDetail:
    emp_no: int
    first_name: str
    last_name: str
    title: str
    gender: str
    hire_date: date
    birth_date: date
    dept_name: str
    salary: int


@dataclass
class AllDeptEmpCount:
    dept_no: str
    dept_name: str
    no_of_employees: int
    avg_salary: float


@dataclass
class GenderBreakdown:
    dept_no: str
    dept_name: str
    male_count: int
    female_count: int


def return_employee_details(id, db_connection):
    sql = """SELECT DISTINCT emp.emp_no
                    ,emp.first_name
                    ,emp.last_name
                    ,tl.title
                    ,emp.gender
                    ,emp.hire_date
                    ,emp.birth_date
                    ,dept.dept_name
                    ,sal.salary
                FROM employee emp
                JOIN emp_dept ON (emp.emp_no = emp_dept.emp_no)
                JOIN department dept ON (dept.dept_no = emp_dept.dept_no)
                JOIN salary sal ON (emp.emp_no = sal.emp_no)
                JOIN title tl ON (emp.emp_no = tl.emp_no)
                WHERE emp.emp_no = %s
                    AND emp_dept.from_date = (
                        SELECT max(from_date)
                        FROM emp_dept
                        WHERE emp_no = %s
                        )
                    AND sal.from_date = (
                        SELECT max(from_date)
                        FROM salary
                        WHERE emp_no = %s
                        )
                    AND tl.from_date = (
                        SELECT MAX(from_date)
                        FROM title
                        WHERE emp_no = %s
                        )"""
    bind = [id, id, id, id]
    cursor = db_connection.cursor()
    cursor.execute(sql, bind)
    records = list()
    for record in cursor.fetchall():
        records.append(
            EmployeeDetail(
                record[0],
                record[1],
                record[2],
                record[3],
                record[4],
                record[5],
                record[6],
                record[7],
                record[8],
            )
        )
    return records


def update_employee_dept(emp_no, dept_no, from_date, db_connection):
    cursor = db_connection.cursor()

    sql = "select count(*) from emp_dept WHERE emp_no = %s and dept_no = %s"
    bind = [emp_no, dept_no]
    cursor.execute(sql, bind)

    emp_count = cursor.fetchone()[0]

    if emp_count > 0:
        print("Cant assign same dept, doing nothing")
    else:
        sql = """SELECT MAX(from_date) from_date FROM emp_dept WHERE emp_no = %s"""
        bind = [emp_no]
        cursor.execute(sql, bind)
        last_from_date = cursor.fetchone()[0]

        if last_from_date != from_date:
            sql = """UPDATE emp_dept
                        SET to_date = %s
                    WHERE from_date = %s
                        AND emp_no = %s"""
            bind = [from_date, last_from_date, emp_no]
            cursor.execute(sql, bind)
        else:
            raise SameStartDate("Can't have same start date")

        sql = """INSERT INTO emp_dept (emp_no, dept_no, from_date, to_date)
                VALUES (%s, %s, %s, %s)"""
        to_date = _return_default_to_date()
        bind = [emp_no, dept_no, from_date, to_date]
        cursor.execute(sql, bind)


def return_departments(db_connection):
    sql = "SELECT dept_no, dept_name FROM department"
    cursor = db_connection.cursor()
    cursor.execute(sql)
    departments = list()
    departments.append((None, ""))
    for record in cursor.fetchall():
        departments.append((record[0], record[1]))
    return departments


def add_dept_manager(db_connection, dept_no, emp_no, from_date):
    cursor = db_connection.cursor()

    sql = "SELECT MAX(from_date) from_date from manager_deptartment where dept_no = %s"
    bind = [dept_no]
    cursor.execute(sql, bind)
    last_from_date = cursor.fetchone()[0]

    if last_from_date:
        sql = "UPDATE manager_deptartment SET to_date = %s WHERE dept_no = %s AND from_date = %s"
        bind = [from_date, dept_no, last_from_date]
        cursor.execute(sql, bind)

    sql = """INSERT INTO manager_deptartment (emp_no, dept_no, from_date, to_date)
                VALUES (%s, %s, %s, %s)"""
    bind = [emp_no, dept_no, from_date, _return_default_to_date()]
    cursor.execute(sql, bind)
    print("executing 2...")
    db_connection.commit()


def return_all_titles_dropdown(db_connection):
    cursor = db_connection.cursor()
    sql = "select distinct title from title"
    cursor.execute(sql)
    records = list()
    records.append((None, None))
    for title in cursor.fetchall():
        records.append((title[0], title[0]))
    return records


def update_emp_title(db_connection, emp_no, title, from_date):
    cursor = db_connection.cursor()

    sql = "SELECT MAX(from_date) from_date from title where emp_no = %s"
    bind = [emp_no]
    cursor.execute(sql, bind)
    last_from_date = cursor.fetchone()[0]

    if last_from_date == from_date:
        raise SameDeptExp("Cant have same date as previous title")

    sql = "UPDATE title set to_date = %s WHERE emp_no = %s AND from_date = %s"
    bind = [from_date, emp_no, last_from_date]
    cursor.execute(sql, bind)

    sql = """INSERT INTO title(emp_no, title, from_date, to_date)
             VALUES (%s, %s, %s, %s)"""
    bind = [emp_no, title, from_date, _return_default_to_date()]
    cursor.execute(sql, bind)
    db_connection.commit()


def update_emp_salary(db_connection, emp_no, salary, from_date):
    cursor = db_connection.cursor()

    sql = "SELECT MAX(from_date) from_date from salary where emp_no = %s"
    bind = [emp_no]
    cursor.execute(sql, bind)
    last_from_date = cursor.fetchone()[0]

    if last_from_date == from_date:
        raise SameStartDate("Cant have same start date as previous salary")

    sql = "UPDATE salary SET to_date = %s WHERE emp_no = %s AND from_date = %s"
    bind = [from_date, emp_no, last_from_date]
    cursor.execute(sql, bind)

    sql = """INSERT INTO salary (emp_no, salary, from_date, to_date)
            VALUES (%s, %s, %s, %s)"""
    bind = [emp_no, salary, from_date, _return_default_to_date()]
    cursor.execute(sql, bind)


def add_employee_record(
    db_connection, first_name, last_name, hire_date, gender, birth_date
):
    cursor = db_connection.cursor()

    sql = """INSERT INTO employee (birth_date, first_name, last_name, gender, hire_date)
            VALUES (%s, %s, %s, %s, %s)"""
    bind = [birth_date, first_name, last_name, gender, hire_date]
    cursor.execute(sql, bind)

    sql = """SELECT MAX(emp_no) emp_no FROM employee
            WHERE first_name = %s
              AND last_name = %s
              AND birth_date = %s 
              AND hire_date = %s 
              AND gender = %s"""
    bind = [first_name, last_name, birth_date, hire_date, gender]
    cursor.execute(sql, bind)
    emp_no = cursor.fetchone()[0]
    db_connection.commit()
    return emp_no


def add_department(db_connection, dept_name):
    cursor = db_connection.cursor()
    sql = "select concat('d0',cast(cast(replace(max(dept_no),'d','') as signed)+1 as char)) from department"
    cursor.execute(sql)
    dept_no = cursor.fetchone()[0]

    sql = "INSERT INTO department (dept_no, dept_name) VALUES (%s, %s)"
    bind = [dept_no, dept_name]
    cursor.execute(sql, bind)
    db_connection.commit()


def return_all_dept_emp_count(db_connection):
    cursor = db_connection.cursor()
    sql = """SELECT dept.dept_no
                    ,dept.dept_name
                    ,count(ed.emp_no) no_of_employees
                    ,avg(sal.salary) avg_salary
                FROM department dept
                JOIN emp_dept ed ON (dept.dept_no = ed.dept_no)
                JOIN (
                    SELECT emp_no
                        ,salary
                    FROM salary
                    WHERE EXISTS (
                            SELECT NULL
                            FROM (
                                SELECT emp_no
                                    ,max(from_date) from_date
                                FROM salary
                                GROUP BY emp_no
                                ) e_max
                            WHERE salary.emp_no = e_max.emp_no
                                AND salary.from_date = e_max.from_date
                            )
                    ) sal ON (ed.emp_no = sal.emp_no)
                WHERE EXISTS (
                        SELECT NULL
                        FROM (
                            SELECT emp_no
                                ,max(from_date) from_date
                            FROM emp_dept e
                            GROUP BY emp_no
                            ) vw
                        WHERE ed.emp_no = vw.emp_no
                            AND ed.from_date = vw.from_date
                        )
                GROUP BY dept.dept_no
                    ,dept.dept_name"""
    cursor.execute(sql)

    dept_employees = [
        AllDeptEmpCount(record[0], record[1], record[2], record[3])
        for record in cursor.fetchall()
    ]
    return dept_employees


def return_emp_count_for_dept(db_connection, dept_no):
    cursor = db_connection.cursor()

    sql = """SELECT dept.dept_no
                    ,dept.dept_name
                    ,count(ed.emp_no) no_of_employees
                    ,avg(sal.salary) avg_salary
                FROM department dept
                JOIN emp_dept ed ON (dept.dept_no = ed.dept_no)
                JOIN (
                    SELECT emp_no
                        ,salary
                    FROM salary
                    WHERE EXISTS (
                            SELECT NULL
                            FROM (
                                SELECT emp_no
                                    ,max(from_date) from_date
                                FROM salary
                                GROUP BY emp_no
                                ) e_max
                            WHERE salary.emp_no = e_max.emp_no
                                AND salary.from_date = e_max.from_date
                            )
                    ) sal ON (ed.emp_no = sal.emp_no)
                WHERE EXISTS (
                        SELECT NULL
                        FROM (
                            SELECT emp_no
                                ,max(from_date) from_date
                            FROM emp_dept e
                            GROUP BY emp_no
                            ) vw
                        WHERE ed.emp_no = vw.emp_no
                            AND ed.from_date = vw.from_date
                        )
                    AND dept.dept_no = %s
                GROUP BY dept.dept_no
                    ,dept.dept_name"""
    bind = [dept_no]
    cursor.execute(sql, bind)

    dept_cnt = [
        AllDeptEmpCount(record[0], record[1], record[2], record[3])
        for record in cursor.fetchall()
    ]
    return dept_cnt


def return_all_dept_gender_count(db_connection):
    cursor = db_connection.cursor()

    sql = """SELECT d.dept_no
                    ,d.dept_name
                    ,sum(CASE 
                            WHEN emp.gender = %s
                                THEN 1
                            ELSE 0
                            END) male_count
                    ,sum(CASE 
                            WHEN emp.gender = %s
                                THEN 1
                            ELSE 0
                            END) female_count
                FROM employee emp
                JOIN emp_dept ed ON (emp.emp_no = ed.emp_no)
                JOIN department d ON (d.dept_no = ed.dept_no)
                WHERE EXISTS (
                        SELECT NULL
                        FROM (
                            SELECT emp_no
                                ,max(from_date) from_date
                            FROM emp_dept e
                            GROUP BY emp_no
                            ) vw
                        WHERE ed.emp_no = vw.emp_no
                            AND ed.from_date = vw.from_date
                        )
                GROUP BY d.dept_no
                    ,d.dept_name"""
    bind = ["M", "F"]
    cursor.execute(sql, bind)
    return [
        GenderBreakdown(record[0], record[1], record[2], record[3])
        for record in cursor.fetchall()
    ]


def return_dept_gender_count(db_connection, dept_no):
    cursor = db_connection.cursor()

    sql = """SELECT d.dept_no
                    ,d.dept_name
                    ,sum(CASE 
                            WHEN emp.gender = %s
                                THEN 1
                            ELSE 0
                            END) male_count
                    ,sum(CASE 
                            WHEN emp.gender = %s
                                THEN 1
                            ELSE 0
                            END) female_count
                FROM employee emp
                JOIN emp_dept ed ON (emp.emp_no = ed.emp_no)
                JOIN department d ON (d.dept_no = ed.dept_no)
                WHERE EXISTS (
                        SELECT NULL
                        FROM (
                            SELECT emp_no
                                ,max(from_date) from_date
                            FROM emp_dept e
                            GROUP BY emp_no
                            ) vw
                        WHERE ed.emp_no = vw.emp_no
                            AND ed.from_date = vw.from_date
                        )
                  AND d.dept_no = %s
                GROUP BY d.dept_no
                    ,d.dept_name"""
    bind = ["M", "F", dept_no]
    cursor.execute(sql, bind)
    return [
        GenderBreakdown(record[0], record[1], record[2], record[3])
        for record in cursor.fetchall()
    ]