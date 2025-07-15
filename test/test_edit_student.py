import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from student_report_card import StudentReportCard


def test_edit_structure():
    obj = StudentReportCard("test_student.txt")
    assert callable(obj.edit_student_info)
