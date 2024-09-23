import sqlite3
from tkinter import *
from tkinter import ttk, messagebox

# Create the main window
root = Tk()
root.title("Student Management System")
root.geometry("800x600")
root.configure(bg='#f4f4f9')  # Soft background color for a modern look

# Connect to the SQLite database (or create it)
conn = sqlite3.connect('student.db')
cursor = conn.cursor()

# Create the students table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        class TEXT NOT NULL,
        dept TEXT NOT NULL,
        grade TEXT NOT NULL
    )
""")
conn.commit()

# Function to insert new student record
def save_student():
    name = entry_name.get()
    class_ = entry_class.get()
    dept = entry_dept.get()
    grade = combo_grade.get()

    if name and class_ and dept and grade:
        cursor.execute("INSERT INTO students (name, class, dept, grade) VALUES (?, ?, ?, ?)", (name, class_, dept, grade))
        conn.commit()
        messagebox.showinfo("Success", "Student record added successfully!")
        fetch_students()
        reset_form()
    else:
        messagebox.showwarning("Input Error", "All fields are required!")

# Function to fetch and display student records
def fetch_students():
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    update_table(rows)

# Function to update the Treeview table
def update_table(rows):
    for row in tree.get_children():
        tree.delete(row)
    for row in rows:
        tree.insert("", END, values=row)

# Function to reset the form
def reset_form():
    entry_id.delete(0, END)
    entry_name.delete(0, END)
    entry_class.delete(0, END)
    entry_dept.delete(0, END)
    combo_grade.set("")

# Function to delete a student record
def delete_student():
    student_id = entry_id.get()
    if student_id:
        cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
        conn.commit()
        messagebox.showinfo("Success", "Student record deleted successfully!")
        fetch_students()
        reset_form()
    else:
        messagebox.showwarning("Input Error", "Please enter the Student ID to delete.")

# Function to update an existing student record
def update_student():
    student_id = entry_id.get()
    name = entry_name.get()
    class_ = entry_class.get()
    dept = entry_dept.get()
    grade = combo_grade.get()

    if student_id and name and class_ and dept and grade:
        cursor.execute("UPDATE students SET name=?, class=?, dept=?, grade=? WHERE id=?", (name, class_, dept, grade, student_id))
        conn.commit()
        messagebox.showinfo("Success", "Student record updated successfully!")
        fetch_students()
        reset_form()
    else:
        messagebox.showwarning("Input Error", "All fields are required!")

# Function to search student by ID
def search_student():
    student_id = entry_search.get()
    cursor.execute("SELECT * FROM students WHERE id=?", (student_id,))
    rows = cursor.fetchall()
    update_table(rows)

# Function to reset the student ID sequence and delete all records
def reset_student_id():
    cursor.execute("DELETE FROM students")
    conn.commit()
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='students'")
    conn.commit()
    fetch_students()
    messagebox.showinfo("Reset Complete", "All student records have been deleted and ID has been reset!")

# Labels and Entries for the form
label_title = Label(root, text="Student Management System", font=("Helvetica", 24, "bold"), bg='#f4f4f9', fg='#333333')
label_title.pack(pady=10)

frame_form = Frame(root, bg='#f4f4f9')
frame_form.pack(pady=20)

# Using grid for alignment and padding for better spacing
Label(frame_form, text="Student ID", font=("Helvetica", 12), bg='#f4f4f9').grid(row=0, column=0, padx=10, pady=5, sticky=E)
entry_id = Entry(frame_form, font=("Helvetica", 12), width=25)
entry_id.grid(row=0, column=1, padx=10, pady=5)

Label(frame_form, text="Name", font=("Helvetica", 12), bg='#f4f4f9').grid(row=1, column=0, padx=10, pady=5, sticky=E)
entry_name = Entry(frame_form, font=("Helvetica", 12), width=25)
entry_name.grid(row=1, column=1, padx=10, pady=5)

Label(frame_form, text="Class", font=("Helvetica", 12), bg='#f4f4f9').grid(row=2, column=0, padx=10, pady=5, sticky=E)
entry_class = Entry(frame_form, font=("Helvetica", 12), width=25)
entry_class.grid(row=2, column=1, padx=10, pady=5)

Label(frame_form, text="Dept", font=("Helvetica", 12), bg='#f4f4f9').grid(row=3, column=0, padx=10, pady=5, sticky=E)
entry_dept = Entry(frame_form, font=("Helvetica", 12), width=25)
entry_dept.grid(row=3, column=1, padx=10, pady=5)

Label(frame_form, text="Grade", font=("Helvetica", 12), bg='#f4f4f9').grid(row=4, column=0, padx=10, pady=5, sticky=E)
combo_grade = ttk.Combobox(frame_form, font=("Helvetica", 12), values=["A", "B", "C", "D", "F"], width=23)
combo_grade.grid(row=4, column=1, padx=10, pady=5)

# Buttons for actions
btn_frame = Frame(root, bg='#f4f4f9')
btn_frame.pack(pady=20)

# Using consistent font, bg, and fg colors for a professional look
btn_style = {"font": ("Helvetica", 12, "bold"), "bg": "#5f6caf", "fg": "white", "width": 10, "bd": 0, "padx": 10, "pady": 5}
Button(btn_frame, text="Save", command=save_student, **btn_style).grid(row=0, column=0, padx=5)
Button(btn_frame, text="Update", command=update_student, **btn_style).grid(row=0, column=1, padx=5)
Button(btn_frame, text="Delete", command=delete_student, **btn_style).grid(row=0, column=2, padx=5)
Button(btn_frame, text="Reset ID", command=reset_student_id, **btn_style).grid(row=0, column=3, padx=5)

# Search section
frame_search = Frame(root, bg='#f4f4f9')
frame_search.pack(pady=20)

Label(frame_search, text="Search by Student ID", font=("Helvetica", 12), bg='#f4f4f9').grid(row=0, column=0, padx=10, pady=5, sticky=E)
entry_search = Entry(frame_search, font=("Helvetica", 12), width=25)
entry_search.grid(row=0, column=1, padx=10, pady=5)

Button(frame_search, text="Search", command=search_student, **btn_style).grid(row=0, column=2, padx=5)

# Treeview for displaying student records
tree_frame = Frame(root)
tree_frame.pack(pady=20)

columns = ("ID", "Name", "Class", "Dept", "Grade")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=8)
tree.pack()

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150, anchor=CENTER)

# Fetch and display the student records on launch
fetch_students()

# Run the main loop
root.mainloop()
