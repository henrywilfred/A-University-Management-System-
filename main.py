"""
University Management System
OOP Practical Assessment Project

Demonstrates:
- Encapsulation (private attributes, properties)
- Inheritance (Student, Lecturer from Person)
- Polymorphism (overridden methods)
- Abstraction (ABC)
- Composition / Aggregation (relationships between objects)
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import uuid


class Person(ABC):
    """Abstract base class for all people in the university."""

    def __init__(self, name: str, email: str, phone: str):
        self._id = str(uuid.uuid4())[:8].upper()
        self._name = name
        self._email = email
        self._phone = phone

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not value.strip():
            raise ValueError("Name cannot be empty")
        self._name = value.strip()

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str):
        if "@" not in value:
            raise ValueError("Invalid email")
        self._email = value

    @property
    def phone(self) -> str:
        return self._phone

    @abstractmethod
    def get_role(self) -> str:
        """Return the role of the person. Must be implemented by subclasses."""
        pass

    def display_info(self) -> str:
        return f"[{self.get_role()}] ID: {self.id} | Name: {self.name} | Email: {self.email} | Phone: {self.phone}"

    def __str__(self) -> str:
        return self.display_info()


class Student(Person):
    """Student class inheriting from Person."""

    def __init__(self, name: str, email: str, phone: str, year: int = 1, department: Optional['Department'] = None):
        super().__init__(name, email, phone)
        self._year = year
        self._department = department
        self._enrolled_courses: List['Course'] = []
        self._results: List['Result'] = []

    def get_role(self) -> str:
        return "Student"

    @property
    def year(self) -> int:
        return self._year

    @year.setter
    def year(self, value: int):
        if value < 1 or value > 6:
            raise ValueError("Year must be between 1 and 6")
        self._year = value

    @property
    def department(self):
        return self._department

    @department.setter
    def department(self, dept):
        self._department = dept

    def enroll_course(self, course: 'Course'):
        if course not in self._enrolled_courses:
            self._enrolled_courses.append(course)
            course.add_student(self)
            print(f"✓ {self.name} enrolled in {course.code}")

    def drop_course(self, course: 'Course'):
        if course in self._enrolled_courses:
            self._enrolled_courses.remove(course)
            course.remove_student(self)
            print(f"✓ {self.name} dropped {course.code}")

    def add_result(self, result: 'Result'):
        self._results.append(result)

    def get_gpa(self) -> float:
        if not self._results:
            return 0.0
        total_points = sum(r.grade_points * r.course.credits for r in self._results)
        total_credits = sum(r.course.credits for r in self._results)
        return round(total_points / total_credits, 2) if total_credits else 0.0

    def display_info(self) -> str:
        base = super().display_info()
        dept_name = self._department.name if self._department else "None"
        courses = ", ".join(c.code for c in self._enrolled_courses) or "None"
        return f"{base}\n   Year: {self._year} | Department: {dept_name} | Courses: {courses} | GPA: {self.get_gpa()}"

    def get_results_summary(self) -> str:
        if not self._results:
            return "No results yet."
        lines = [f"Results for {self.name}:"]
        for r in self._results:
            lines.append(f"  {r.course.code}: {r.score}/100 → {r.grade} ({r.grade_points} pts)")
        lines.append(f"Overall GPA: {self.get_gpa()}")
        return "\n".join(lines)


class Lecturer(Person):
    """Lecturer class inheriting from Person."""

    def __init__(self, name: str, email: str, phone: str, specialization: str = "", department: Optional['Department'] = None):
        super().__init__(name, email, phone)
        self._specialization = specialization
        self._department = department
        self._courses_taught: List['Course'] = []

    def get_role(self) -> str:
        return "Lecturer"

    @property
    def specialization(self) -> str:
        return self._specialization

    @property
    def department(self):
        return self._department

    @department.setter
    def department(self, dept):
        self._department = dept

    def assign_course(self, course: 'Course'):
        if course not in self._courses_taught:
            self._courses_taught.append(course)
            course.lecturer = self
            print(f"✓ {self.name} assigned to teach {course.code}")

    def display_info(self) -> str:
        base = super().display_info()
        dept_name = self._department.name if self._department else "None"
        courses = ", ".join(c.code for c in self._courses_taught) or "None"
        return f"{base}\n   Specialization: {self._specialization} | Department: {dept_name} | Teaching: {courses}"


class Department:
    """Department class (Composition/Aggregation)."""

    def __init__(self, code: str, name: str):
        self.code = code.upper()
        self.name = name
        self.head: Optional[Lecturer] = None
        self.students: List[Student] = []
        self.lecturers: List[Lecturer] = []
        self.courses: List['Course'] = []

    def add_student(self, student: Student):
        if student not in self.students:
            self.students.append(student)
            student.department = self

    def add_lecturer(self, lecturer: Lecturer):
        if lecturer not in self.lecturers:
            self.lecturers.append(lecturer)
            lecturer.department = self

    def add_course(self, course: 'Course'):
        if course not in self.courses:
            self.courses.append(course)
            course.department = self

    def set_head(self, lecturer: Lecturer):
        self.head = lecturer
        print(f"✓ {lecturer.name} set as Head of {self.name}")

    def display_info(self) -> str:
        head_name = self.head.name if self.head else "Not assigned"
        return (f"Department: {self.name} ({self.code})\n"
                f"  Head: {head_name}\n"
                f"  Students: {len(self.students)} | Lecturers: {len(self.lecturers)} | Courses: {len(self.courses)}")

    def __str__(self):
        return self.display_info()


class Course:
    """Course class."""

    def __init__(self, code: str, title: str, credits: int = 3):
        self.code = code.upper()
        self.title = title
        self.credits = credits
        self.department: Optional[Department] = None
        self.lecturer: Optional[Lecturer] = None
        self.enrolled_students: List[Student] = []

    def add_student(self, student: Student):
        if student not in self.enrolled_students:
            self.enrolled_students.append(student)

    def remove_student(self, student: Student):
        if student in self.enrolled_students:
            self.enrolled_students.remove(student)

    def display_info(self) -> str:
        dept = self.department.name if self.department else "None"
        lect = self.lecturer.name if self.lecturer else "Not assigned"
        students = ", ".join(s.name for s in self.enrolled_students) or "None"
        return (f"Course: {self.code} - {self.title} ({self.credits} credits)\n"
                f"  Department: {dept} | Lecturer: {lect}\n"
                f"  Enrolled: {students}")

    def __str__(self):
        return self.display_info()


class Result:
    """Assessment / Result class."""

    GRADE_SCALE = [
        (70, "A", 5.0),
        (60, "B", 4.0),
        (50, "C", 3.0),
        (45, "D", 2.0),
        (40, "E", 1.0),
        (0, "F", 0.0),
    ]

    def __init__(self, student: Student, course: Course, score: float):
        if not 0 <= score <= 100:
            raise ValueError("Score must be between 0 and 100")
        self.student = student
        self.course = course
        self.score = score
        self.grade, self.grade_points = self._calculate_grade(score)

    def _calculate_grade(self, score: float):
        for threshold, grade, points in self.GRADE_SCALE:
            if score >= threshold:
                return grade, points
        return "F", 0.0

    def __str__(self):
        return f"{self.course.code}: {self.score} → {self.grade} ({self.grade_points})"


class UniversityManagementSystem:
    """Main system class that manages all entities (Facade pattern style)."""

    def __init__(self, name: str = "University"):
        self.name = name
        self.departments: Dict[str, Department] = {}
        self.students: Dict[str, Student] = {}
        self.lecturers: Dict[str, Lecturer] = {}
        self.courses: Dict[str, Course] = {}
        self.results: List[Result] = []

    # ---------- Department Management ----------
    def add_department(self, code: str, name: str) -> Department:
        if code.upper() in self.departments:
            raise ValueError("Department code already exists")
        dept = Department(code, name)
        self.departments[code.upper()] = dept
        print(f"✓ Department '{name}' added.")
        return dept

    def view_departments(self):
        if not self.departments:
            print("No departments found.")
            return
        print("\n=== DEPARTMENTS ===")
        for dept in self.departments.values():
            print(dept)
            print("-" * 40)

    # ---------- Student Management ----------
    def add_student(self, name: str, email: str, phone: str, year: int = 1, dept_code: Optional[str] = None) -> Student:
        student = Student(name, email, phone, year)
        self.students[student.id] = student
        if dept_code and dept_code.upper() in self.departments:
            self.departments[dept_code.upper()].add_student(student)
        print(f"✓ Student {name} added with ID: {student.id}")
        return student

    def view_students(self):
        if not self.students:
            print("No students found.")
            return
        print("\n=== STUDENTS ===")
        for s in self.students.values():
            print(s.display_info())
            print("-" * 40)

    def find_student(self, student_id: str) -> Optional[Student]:
        return self.students.get(student_id.upper())

    # ---------- Lecturer Management ----------
    def add_lecturer(self, name: str, email: str, phone: str, specialization: str = "", dept_code: Optional[str] = None) -> Lecturer:
        lecturer = Lecturer(name, email, phone, specialization)
        self.lecturers[lecturer.id] = lecturer
        if dept_code and dept_code.upper() in self.departments:
            self.departments[dept_code.upper()].add_lecturer(lecturer)
        print(f"✓ Lecturer {name} added with ID: {lecturer.id}")
        return lecturer

    def view_lecturers(self):
        if not self.lecturers:
            print("No lecturers found.")
            return
        print("\n=== LECTURERS ===")
        for l in self.lecturers.values():
            print(l.display_info())
            print("-" * 40)

    # ---------- Course Management ----------
    def add_course(self, code: str, title: str, credits: int = 3, dept_code: Optional[str] = None) -> Course:
        if code.upper() in self.courses:
            raise ValueError("Course code already exists")
        course = Course(code, title, credits)
        self.courses[code.upper()] = course
        if dept_code and dept_code.upper() in self.departments:
            self.departments[dept_code.upper()].add_course(course)
        print(f"✓ Course {code} - {title} added.")
        return course

    def view_courses(self):
        if not self.courses:
            print("No courses found.")
            return
        print("\n=== COURSES ===")
        for c in self.courses.values():
            print(c)
            print("-" * 40)

    def assign_lecturer_to_course(self, lecturer_id: str, course_code: str):
        lecturer = self.lecturers.get(lecturer_id.upper())
        course = self.courses.get(course_code.upper())
        if not lecturer or not course:
            print("Lecturer or Course not found.")
            return
        lecturer.assign_course(course)

    def enroll_student_in_course(self, student_id: str, course_code: str):
        student = self.students.get(student_id.upper())
        course = self.courses.get(course_code.upper())
        if not student or not course:
            print("Student or Course not found.")
            return
        student.enroll_course(course)

    # ---------- Results / Assessment ----------
    def record_result(self, student_id: str, course_code: str, score: float):
        student = self.students.get(student_id.upper())
        course = self.courses.get(course_code.upper())
        if not student or not course:
            print("Student or Course not found.")
            return
        if course not in student._enrolled_courses:
            print("Student is not enrolled in this course.")
            return
        result = Result(student, course, score)
        self.results.append(result)
        student.add_result(result)
        print(f"✓ Result recorded: {student.name} - {course.code}: {score} → {result.grade}")

    def view_student_results(self, student_id: str):
        student = self.students.get(student_id.upper())
        if not student:
            print("Student not found.")
            return
        print(student.get_results_summary())

    def view_all_results(self):
        if not self.results:
            print("No results recorded yet.")
            return
        print("\n=== ALL RESULTS ===")
        for r in self.results:
            print(f"{r.student.name} ({r.student.id}) | {r}")
            print("-" * 40)


def main():
    ums = UniversityManagementSystem("State University")

    # Optional: Preload sample data for demonstration
    print("=== University Management System ===")
    print("Loading sample data...\n")

    cs = ums.add_department("CS", "Computer Science")
    eng = ums.add_department("ENG", "Engineering")

    lect1 = ums.add_lecturer("Dr. Ada Lovelace", "ada@uni.edu", "08012345678", "Algorithms", "CS")
    lect2 = ums.add_lecturer("Prof. Alan Turing", "alan@uni.edu", "08087654321", "AI", "CS")
    cs.set_head(lect1)

    ums.add_course("CS101", "Introduction to Programming", 3, "CS")
    ums.add_course("CS201", "Data Structures", 4, "CS")
    ums.add_course("ENG101", "Engineering Mathematics", 3, "ENG")

    ums.assign_lecturer_to_course(lect1.id, "CS101")
    ums.assign_lecturer_to_course(lect2.id, "CS201")

    stu1 = ums.add_student("John Doe", "john@uni.edu", "07011112222", 2, "CS")
    stu2 = ums.add_student("Jane Smith", "jane@uni.edu", "07033334444", 1, "CS")

    ums.enroll_student_in_course(stu1.id, "CS101")
    ums.enroll_student_in_course(stu1.id, "CS201")
    ums.enroll_student_in_course(stu2.id, "CS101")

    ums.record_result(stu1.id, "CS101", 85)
    ums.record_result(stu1.id, "CS201", 72)
    ums.record_result(stu2.id, "CS101", 65)

    print("\nSample data loaded successfully!\n")

    while True:
        print("\n" + "=" * 50)
        print("UNIVERSITY MANAGEMENT SYSTEM MENU")
        print("=" * 50)
        print("1. View All Students")
        print("2. View All Lecturers")
        print("3. View All Courses")
        print("4. View All Departments")
        print("5. View Student Results")
        print("6. View All Results")
        print("7. Add New Student")
        print("8. Add New Course")
        print("9. Record Assessment/Result")
        print("10. Enroll Student in Course")
        print("0. Exit")
        print("=" * 50)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            ums.view_students()
        elif choice == "2":
            ums.view_lecturers()
        elif choice == "3":
            ums.view_courses()
        elif choice == "4":
            ums.view_departments()
        elif choice == "5":
            sid = input("Enter Student ID: ").strip()
            ums.view_student_results(sid)
        elif choice == "6":
            ums.view_all_results()
        elif choice == "7":
            name = input("Name: ")
            email = input("Email: ")
            phone = input("Phone: ")
            year = int(input("Year (1-6): ") or 1)
            dept = input("Department Code (optional): ").strip() or None
            try:
                ums.add_student(name, email, phone, year, dept)
            except Exception as e:
                print(f"Error: {e}")
        elif choice == "8":
            code = input("Course Code: ")
            title = input("Title: ")
            credits = int(input("Credits: ") or 3)
            dept = input("Department Code (optional): ").strip() or None
            try:
                ums.add_course(code, title, credits, dept)
            except Exception as e:
                print(f"Error: {e}")
        elif choice == "9":
            sid = input("Student ID: ").strip()
            ccode = input("Course Code: ").strip()
            try:
                score = float(input("Score (0-100): "))
                ums.record_result(sid, ccode, score)
            except Exception as e:
                print(f"Error: {e}")
        elif choice == "10":
            sid = input("Student ID: ").strip()
            ccode = input("Course Code: ").strip()
            ums.enroll_student_in_course(sid, ccode)
        elif choice == "0":
            print("Exiting system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
