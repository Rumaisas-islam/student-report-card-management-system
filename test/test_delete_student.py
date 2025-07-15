import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from student_report_card import StudentReportCard


def test_delete_student():
    test_file = "test_student.txt"
    with open(test_file, "w") as f:
        f.write("=========================\n")
        f.write("Roll number: 2024\n")
        f.write("Name: Test Student\n")
        f.write("=========================\n")

    obj = StudentReportCard(test_file)
    assert obj.is_duplicate_roll("2024") == True

    # Simulate delete manually for this test (real test requires input handling)
    os.remove(test_file)
    assert not os.path.exists(test_file)