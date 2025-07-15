import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from student_report_card import StudentReportCard

def test_duplicate_roll_check():
    obj = StudentReportCard("test_student.txt")
    with open("test_student.txt", "w") as f:
        f.write("Roll number: 9999\n")

    assert obj.is_duplicate_roll("9999") == True
    assert obj.is_duplicate_roll("1234") == False

    os.remove("test_student.txt")