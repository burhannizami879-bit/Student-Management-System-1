
import ast
from abc import ABC, abstractmethod


class Person(ABC):

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def display_role(self):
        pass



class Student(Person):

    student_type = "Regular"

    def __init__(self, student_id, name, english, maths, computer):

        super().__init__(name)

        self.student_id = student_id
        self.__english = english
        self.__maths = maths
        self.__computer = computer


    @property
    def english(self):
        return self.__english

    @english.setter
    def english(self, value):
        if not 0 <= value <= 100:
            raise ValueError("Marks must be between 0 and 100!")
        self.__english = value

    @property
    def maths(self):
        return self.__maths

    @maths.setter
    def maths(self, value):
        if not 0 <= value <= 100:
            raise ValueError("Marks must be between 0 and 100!")
        self.__maths = value

    @property
    def computer(self):
        return self.__computer

    @computer.setter
    def computer(self, value):
        if not 0 <= value <= 100:
            raise ValueError("Marks must be between 0 and 100!")
        self.__computer = value

    def display_role(self):
        return "Regular Student"

    def calculate_total(self):
        return self.english + self.maths + self.computer

    def calculate_average(self):
        return self.calculate_total() / 3

    def calculate_grade(self):

        average = self.calculate_average()

        if average >= 90:
            return "A+"
        elif average >= 80:
            return "A"
        elif average >= 70:
            return "B"
        elif average >= 60:
            return "C"
        else:
            return "Fail"

    def to_dict(self):

        return {
            "student_id": self.student_id,
            "student_type": self.student_type,
            "name": self.name,
            "english": self.english,
            "maths": self.maths,
            "computer": self.computer,
            "total": self.calculate_total(),
            "average": self.calculate_average(),
            "grade": self.calculate_grade()
        }


class MeritStudent(Student):

    student_type = "Merit"

    def display_role(self):
        return "Merit Student"

    # Method Overriding
    def calculate_grade(self):

        average = self.calculate_average()

        if average >= 85:
            return "A+"

        return super().calculate_grade()


class StudentManagement:

    def __init__(self):

        self.students = []
        self.next_id = 1

        self.load_students()

    def load_students(self):

        try:
            with open("student.txt", "r") as file:

                for line in file:

                    if line.strip() == "":
                        continue

                    try:
                        data = ast.literal_eval(line)

                        student_id = data.get(
                            "student_id", self.next_id
                        )

                        student_class = Student

                        if data.get("student_type") == "Merit":
                            student_class = MeritStudent

                        student = student_class(
                            student_id,
                            data["name"],
                            data["english"],
                            data["maths"],
                            data["computer"]
                        )

                        self.students.append(student)

                        self.next_id = max(
                            self.next_id,
                            student.student_id + 1
                        )

                    except (ValueError, SyntaxError, KeyError, TypeError):
                        print("Invalid student record skipped!")

        except FileNotFoundError:
            pass

    def save_students(self):

        with open("student.txt", "w") as file:

            for student in self.students:
                file.write(str(student.to_dict()) + "\n")

    def show_menu(self):

        print("\n===== STUDENT MANAGEMENT SYSTEM =====")
        print("1. Add Student")
        print("2. Display Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Class Statistics")
        print("6. Display Passed Students")
        print("7. Delete Student")
        print("8. Exit")

    def add_student(self):

        name = input("Enter student name: ")

        print("1. Regular Student")
        print("2. Merit Student")

        student_choice = input("Select student type: ")

        if student_choice == "1":
            student_class = Student

        elif student_choice == "2":
            student_class = MeritStudent

        else:
            print("Invalid student type!")
            return

        try:
            english = int(input("Enter English marks: "))
            maths = int(input("Enter Maths marks: "))
            computer = int(input("Enter Computer marks: "))

            student = student_class(
                self.next_id,
                name,
                english,
                maths,
                computer
            )

        except ValueError as e:
            print("Invalid input:", e)
            return

        self.next_id += 1
        self.students.append(student)

        self.save_students()

        print("Student added successfully!")
        print("Student ID:", student.student_id)

    def display_students(self):

        if len(self.students) == 0:
            print("No students available!")

        else:

            print("\n===== ALL STUDENTS DETAILS =====")

            for x in self.students:

                print("\nID:", x.student_id)
                print("Type:", x.display_role())
                print("Name:", x.name)
                print("English:", x.english)
                print("Maths:", x.maths)
                print("Computer:", x.computer)
                print("Total:", x.calculate_total())
                print("Average:", x.calculate_average())
                print("Grade:", x.calculate_grade())

    def search_student(self):

        search_name = input("Enter student name: ")

        found = False

        for x in self.students:

            if x.name.lower() == search_name.lower():

                print("\nStudent found!")

                print("ID:", x.student_id)
                print("Type:", x.display_role())
                print("Name:", x.name)
                print("English:", x.english)
                print("Maths:", x.maths)
                print("Computer:", x.computer)
                print("Total:", x.calculate_total())
                print("Average:", x.calculate_average())
                print("Grade:", x.calculate_grade())

                found = True

        if not found:
            print("Student not found!")

    def update_student(self):

        try:
            student_id = int(input("Enter Student ID to Update: "))

        except ValueError:
            print("Invalid Student ID!")
            return

        for student in self.students:

            if student.student_id == student_id:

                print("\nStudent Found!")

                new_name = input("Enter new name: ")

                try:
                    english = int(input("Enter new English marks: "))
                    maths = int(input("Enter new Maths marks: "))
                    computer = int(input("Enter new Computer marks: "))

                    student.english = english
                    student.maths = maths
                    student.computer = computer

                except ValueError as e:
                    print("Invalid input:", e)
                    return

                student.name = new_name

                self.save_students()

                print("Student Updated Successfully!")
                return

        print("Student ID Not Found!")

    def delete_student(self):

        try:
            student_id = int(input("Enter Student ID to Delete: "))

        except ValueError:
            print("Invalid Student ID!")
            return

        for student in self.students:

            if student.student_id == student_id:

                self.students.remove(student)

                self.save_students()

                print("Student Deleted Successfully!")
                return

        print("Student ID Not Found!")

    def class_statistics(self):

        if len(self.students) == 0:
            print("No students available!")
            return

        averages = [
            student.calculate_average()
            for student in self.students
        ]

        print("\n===== CLASS STATISTICS =====")

        print("Total Students:", len(self.students))
        print("Highest Average:", max(averages))
        print("Lowest Average:", min(averages))
        print("Overall Class Average:", sum(averages) / len(averages))

    def passed_student(self):

        passed = [
            x for x in self.students
            if x.calculate_grade() != "Fail"
        ]

        if len(passed) == 0:
            print("No Passed Students!")

        else:

            print("\n===== PASSED STUDENTS =====")

            for x in passed:
                print(x.name, "-", x.calculate_grade())

    def run(self):

        while True:

            self.show_menu()

            choice = input("Enter your choice: ")

            if choice == "1":
                self.add_student()

            elif choice == "2":
                self.display_students()

            elif choice == "3":
                self.search_student()

            elif choice == "4":
                self.update_student()

            elif choice == "5":
                self.class_statistics()

            elif choice == "6":
                self.passed_student()

            elif choice == "7":
                self.delete_student()

            elif choice == "8":
                print("Thank you for using Student Management System!")
                break

            else:
                print("Invalid choice! Please try again!")


app = StudentManagement()
app.run()

