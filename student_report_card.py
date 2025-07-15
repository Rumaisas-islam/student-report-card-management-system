import re
import getpass
class StudentReportCard:
  def is_valid_name(self,name):
    return bool(re.fullmatch(r"[A-Za-z ]+", name))
  def is_valid_class(self,cls):
    return bool(re.fullmatch(r"[A-Za-z0-9 ]+", cls)) 
  def __init__(self,filename="student.txt"):
    self.filename=filename

  def is_duplicate_roll(self, roll_number):
    try:
        with open(self.filename, "r") as f:
            for line in f:
                if line.strip().lower().startswith("roll number:"):
                    if line.strip().split(":", 1)[1].strip() == roll_number:
                        return True
    except FileNotFoundError:
        pass
    return False
  def get_valid_marks(self,subject):  
    while True:
      try:
        marks = int(input(f"Enter {subject} marks out of 100: "))
        if 0 <= marks <= 100:
          return marks
        else:
          print("Marks must be between 0 and 100.")
      except ValueError:
        print("❌ Please enter valid numeric marks.")
  def create_backup(self):
    import shutil
    shutil.copyfile(self.filename, "student_backup.txt")
    print("🔄 Backup created as 'student_backup.txt'")
  def calculate_grade(self,percentage):
     if percentage>=80:
      grade="A+"
     elif percentage>=70:
      grade="A"
     elif percentage>=60:
      grade="B"
     elif percentage>=50:
      grade="C"
     elif percentage>=40:
      grade="D"
     else:
      grade="Fail"
     return grade

  def add_student(self):
    name=input("Enter your name: ").strip()
    while not self.is_valid_name(name):
      print("❌Invalid name.Only letters are allowed.")
      name=input("Enter your name: ").strip()
    while True:
      roll_number = input("Enter your roll number: ").strip()
      if self.is_duplicate_roll(roll_number):
          print("⚠️ This roll number already exists. Please enter a unique one.")
      else:
          break

    cls=input("Enter your class: ").strip()
    while not self.is_valid_class(cls):
      print("❌ Invalid class. Only letters and numbers are allowed.")
      cls=input("Enter your class: ").strip()

    try:
      english=self.get_valid_marks("English")
      maths=self.get_valid_marks("Maths")
      science=self.get_valid_marks("Science")
      computer=self.get_valid_marks("Computer")
      urdu=self.get_valid_marks("Urdu")
      islamiat=self.get_valid_marks("Islamiat")
    except ValueError:
      print("❌Please enter valid numeric marks.")
      return

    total_marks=600
    obtained_marks=english+maths+science+computer+urdu+islamiat
    percentage=(obtained_marks/total_marks)*100
    grade=self.calculate_grade(percentage)
    try:
      with open(self.filename,"a") as f:
        f.write("=========================\n")
        f.write("📄Students Report Card\n")
        f.write(f"Name:{name}\n")
        f.write(f"Roll number: {roll_number}\n")
        f.write(f"Class: {cls}\n")
        f.write(f"English marks: {english}\n")
        f.write(f"Maths marks: {maths}\n")
        f.write(f"Science marks: {science}\n")
        f.write(f"Computer marks: {computer}\n")
        f.write(f"Urdu marks: {urdu}\n")
        f.write(f"Islamiat marks: {islamiat}\n")
        f.write(f"Total marks: {obtained_marks}/{total_marks}\n")
        f.write(f"Percentage: {percentage:.2f}%\n")
        f.write(f"Grade: {grade}\n")
        f.write("=========================\n")
      print("✅ Student report saved successfully!")
    except Exception as e:
      print(f"❌Error saving:{e}")
  def search_student_info(self,field):
    try:
      with open(self.filename,"r") as f:
        lines=f.readlines()
    except FileNotFoundError:
      print("No file found")
      return
    value=input(f"Enter {field.lower()} to search student info: ").strip()
    pattern=rf"^{re.escape(field.lower())}:\s*{re.escape(value.lower())}"
    found=False
    for i,line in enumerate(lines):
      if re.search(pattern,line,re.IGNORECASE):
        for j in range(i-1,i+15):
          if 0<=j<len(lines):
            print(lines[j].strip())
        found=True
    if not found:
      print(f"No student bio found with that {field.lower()}")
  def delete_student_info(self,field):
    try:
      with open(self.filename,"r") as f:
        lines=f.readlines()
    except FileNotFoundError:
      print("No file found")
    value=input(f"Enter the {field.lower()} to delete student info: ")
    confirm=input("Are you sure you want to delete this student (yes/no): ").lower()
    if confirm != "yes":
      print("❌Deletion cancelled.")
      return
    pattern=rf"^{re.escape(field.lower())}:\s*{re.escape(value.lower())}\s*$"
    new_lines=[]
    found=False
    i=0
    while i < len(lines):
      line=lines[i]
      if re.search(pattern,line,re.IGNORECASE):
        self.create_backup()
        found=True
        while i>0 and not lines[i-1].startswith("========================="):
          i-=1
        while i<len(lines) and not lines[i].startswith("========================="):
          i+=1 
        if i<len(lines):
          i+=1
      else:
        new_lines.append(line)
        i+=1
    if found:
      with open(self.filename,"w") as f:
        f.write("".join(new_lines))
      print("Student info deleted successfully")
    else:
      print(f"No student info found with that {field.lower()}")
  def edit_student_info(self,field):
    try:
      with open(self.filename,"r") as f:
        lines=f.readlines()
    except FileNotFoundError:
      print("No file found")
      return
    value=input(f"Enter the {field.lower()} to edit student info: ")
    confirm = input("Are you sure you want to edit this student info? (yes/no): ").lower()
    if confirm != "yes":
        print("❌ Edit cancelled.")
        return

    new_lines=[]
    pattern=rf"^{re.escape(field.lower())}:\s*{re.escape(value.lower())}\s*$"
    found=False
    i=0
    while i<len(lines):
      line=lines[i]
      if re.search(pattern,line,re.IGNORECASE):
        self.create_backup()
        found=True
        while i>0 and not lines[i-1].startswith("========================="):
          i-=1
        while i<len(lines) and not lines[i].startswith("========================="):
          i+=1
        if i<len(lines):
          i+=1
        new_name = input("Enter name: ").strip()
        while not self.is_valid_name(new_name):
          print("❌ Invalid name. Only letters are allowed.")
          new_name = input("Enter name: ").strip()
        if field.lower() == "roll number":
          new_roll_number = value
        else:
          new_roll_number = input("Enter new roll number: ")
          if new_roll_number != value and self.is_duplicate_roll(new_roll_number):
            print("⚠️ This roll number already exists. Please enter a unique one.")
            return
        new_class = input("Enter class: ").strip()
        while not self.is_valid_class(new_class):
          print("❌ Invalid class. Only letters and numbers are allowed.")
          new_class = input("Enter class: ").strip()

        try:
          new_english=self.get_valid_marks("English")
          new_maths=self.get_valid_marks("Maths")
          new_science=self.get_valid_marks("Science")
          new_computer=self.get_valid_marks("Computer")
          new_urdu=self.get_valid_marks("Urdu")
          new_islamiat=self.get_valid_marks("Islamiat")
        except ValueError:
          print("❌Please enter valid numeric marks.")
          return
        total_marks=600

        new_obtained_marks=new_english+new_maths+new_science+new_computer+new_urdu+new_islamiat

        new_percentage=(new_obtained_marks/total_marks)*100
        new_grade=self.calculate_grade(new_percentage)
        
        new_lines.append("=========================\n")
        new_lines.append(f"Name:{new_name}\n")
        new_lines.append(f"Roll number:{new_roll_number}\n")
        new_lines.append(f"Class:{new_class}\n")
        new_lines.append(f"English marks:{new_english}\n")
        new_lines.append(f"Maths marks:{new_maths}\n")
        new_lines.append(f"Science marks:{new_science}\n")
        new_lines.append(f"Computer marks:{new_computer}\n")
        new_lines.append(f"Urdu marks:{new_urdu}\n")
        new_lines.append(f"Islamiat marks:{new_islamiat}\n")
        new_lines.append(f"Total marks:{new_obtained_marks}/{total_marks}\n")
        new_lines.append(f"Percentage:{new_percentage:.2f}%\n")
        new_lines.append(f"Grade:{new_grade}\n")
        new_lines.append("=========================\n") 

      else:
        new_lines.append(line)
        i+=1
    if found:
      with open(self.filename,"w") as f:
        f.writelines(new_lines)
    else:
      print(f"No student info found with that {field.lower()}")
  def show_all_students_info(self):
    try:
      with open(self.filename,"r")as f:
        content=f.read().strip()
        print("\n-----All Saved Students Info-----\n")
        parts=re.findall(r"=+\n(.*?)\n=+",content,re.DOTALL)
        if parts:
          for i,part in enumerate(parts,1):
            print(f"📄 Student:{i}")
            print(part.strip())
            print()
        else:
          print("No students info found")
    except FileNotFoundError:
      print("No file found")
  def show_top_positions(self):
    try:
      with open(self.filename,"r") as f:
        content=f.read().strip()
      records = re.findall(r"=+\n(.*?)\n=+", content, re.DOTALL)
      students=[]
      for record in records:
        name=re.search(r"Name:(.*)", record)
        roll=re.search(r"Roll number:(.*)", record)
        perc= re.search(r"Percentage:(.*)%", record)
        if name and roll and perc:
          students.append({"name":name.group(1).strip(),"roll":roll.group(1).strip(),"percentage":float(perc.group(1).strip())})
      if not students:
        print("No student record found")
        return
      sorted_students=sorted(students,key=lambda x:x['percentage'],reverse=True)
      print("\n 🏆 Top 3 Students By Percentage \n")
      for i,student in enumerate(sorted_students[:3],1):
        print(f"{i}.{student['name']} (Roll:{student['roll']})) - {student['percentage']}%")
    except FileNotFoundError:
      print("No file found")
  def show_leaderboard(self):
    try:
      with open(self.filename,"r") as f:
        content=f.read().strip()
        records = re.findall(r"=+\n(.*?)\n=+", content, re.DOTALL)
        students=[]
        for record in records:
          name=re.search(r"Name:(.*)", record)
          roll=re.search(r"Roll number:(.*)", record)
          perc=re.search(r"Percentage:(.*)%", record)
          if name and roll and perc:
            students.append((name.group(1).strip(),roll.group(1).strip(),float(perc.group(1))))
        if not students:
            print("No students found")
            return
        students.sort(key=lambda x: x[2], reverse=True)
        print("\n📊 Full Leaderboard")
        print("------------------------")
        print(f"{'Rank':<6}{'Name':<20}{'Roll No.':<12}{'Percentage'}")
        print("------------------------")
        medals = ["🥇", "🥈", "🥉"]
        for i,student in enumerate(students,start=1):
            medal = medals[i-1] if i <= 3 else "   "
            print(f"{i:<6}{student[0]:<20}{student[1]:<12}{student[2]:.2f}% {medal}")      
    except FileNotFoundError:
      print("No file found")
  def show_menu(self):
    print("\n🎯 Students Report Card Menu")
    print("1.Add student")
    print("2.Search student info")
    print("3.Delete student info")
    print("4.Edit student info")
    print("5.View all students info")
    print("6.Show Position Holders")
    print("7.Show Leaderboard")
    print("8.Exit")
if __name__ == "__main__":
#enter username=admin and password=1234
  print("First login then use")
  username=input("Enter username: ")
  password = getpass.getpass("Enter password: ")
  if username == "admin" and password == "1234":
    print("Successfully login")
  else:
    print("Invalid login")
    exit()

  obj=StudentReportCard()

  while True:
    obj.show_menu()
    choice=input("Enter your choice: ")
    if choice == "1":
      obj.add_student()
    elif choice == "2":
      field=input("Enter search by (Name/Roll number/Class)").strip().capitalize()
      obj.search_student_info(field)
    elif choice == "3":
      field=input("Enter delete by (Name/Roll number/Class): ").strip().capitalize()
      obj.delete_student_info(field)
    elif choice == "4":
      field=input("Edit by (Name/Roll number/Class): ").strip().capitalize()
      obj.edit_student_info(field)
    elif choice == "5":
      obj.show_all_students_info()
    elif choice == "6":
      obj.show_top_positions()
    elif choice == "7":
      obj.show_leaderboard()
    elif choice == "8":
      print("Exiting report card.Goodbye!")
      break
    else:
      print("Invalid choice!Please enter valid choice.")