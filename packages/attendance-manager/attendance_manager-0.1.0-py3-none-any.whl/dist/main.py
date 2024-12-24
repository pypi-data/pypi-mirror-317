import csv
import os

# 1. Import and export student lists from TXT/CSV files
def import_students(file_path):
    students = []
    with open(file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            students.append(row[0])
    return students

def export_students(file_path, students):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        for student in students:
            writer.writerow([student])

# 2. Add and manage students manually
def add_student(students, student_name):
    students.append(student_name)

def update_student_file(file_path, students):
    export_students(file_path, students)

# 3. Implement attendance checking
def check_attendance(students):
    attendance = {}
    for student in students:
        present = input(f"Is {student} present? (y/n): ").strip().lower()
        attendance[student] = present == 'y'
    return attendance

# 4. Manage attendance data
def manage_attendance_data(students):
    attendance = check_attendance(students)
    return attendance

# Menu to select action
def menu():
    print("Select an option:")
    print("1. Check presence")
    print("2. Add new students")
    choice = input("Enter choice (1/2): ").strip()
    return choice

# Example usage
if __name__ == "__main__":
    file_path = 'students.csv'
    if os.path.exists(file_path):
        students = import_students(file_path)
    else:
        students = []

    choice = menu()
    if choice == '1':
        attendance = manage_attendance_data(students)
        export_students('attendance.csv', [f"{student}: {'Present' if present else 'Absent'}" for student, present in attendance.items()])
    elif choice == '2':
        while True:
            student_name = input("Enter student name (or empty to finish): ").strip()
            if student_name.lower() == '':
                break
            add_student(students, student_name)
        update_student_file(file_path, students)
    else:
        print("Invalid choice. Exiting.")