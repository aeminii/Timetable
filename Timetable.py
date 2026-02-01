import csv
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog


class Timetable:

    def __init__(self, root):
        self.root = root
        self.root.title("Timetable Project")
        self.root.configure(bg="#183D3D")

        FilePathLB1 = tk.Label(root, width=21)
        FilePathLB1.config(text="Enter the file path:", bg="#5C8374")
        FilePathLB1.grid(row=0, column=0, padx=(5, 10), pady=(20, 0))

        self.PathEntry = tk.Entry(root)
        self.PathEntry.grid(row=0, column=1, padx=(0, 0), pady=(20, 0))
        self.PathEntry.configure(bg="#5C8374")

        YrLb1 = tk.Label(root, width=1)
        YrLb1.config(text="Year", bg="#5C8374")
        YrLb1.grid(row=1, column=0, padx=(5, 10), pady=(20, 0), sticky=tk.W + tk.E)

        n = tk.StringVar()
        self.YrBox = ttk.Combobox(root, width=17, textvariable=n)
        self.YrBox['values'] = ('1', '2', '3', '4', '5', '')
        self.YrBox.grid(column=1, row=1, padx=(8, 10), pady=(20, 0), sticky=tk.W + tk.E)
        self.YrBox.current()

        DepLb1 = tk.Label(root)
        DepLb1.config(text="Department:", bg="#5C8374")
        DepLb1.grid(row=1, column=3, padx=(5, 10), pady=(20, 0), sticky=tk.W + tk.E)

        m = tk.StringVar()
        self.DpEntry = ttk.Combobox(root, width=10, textvariable=m, style='TCombobox')
        self.DpEntry['values'] = (
            'CHI', 'CS', 'ECE', 'ECON', 'EE', 'EECS', 'ENGR', 'FRE', 'GER', 'IE', 'ISE', 'LIFE', 'MATH', 'MGT', 'UNI',
            '')
        self.DpEntry.grid(row=1, column=4, padx=(5, 10), pady=(20, 0), sticky=tk.W + tk.E)
        self.DpEntry.configure(style='TCombobox')

        DspBtn = tk.Button(root, command=self.enter_file_dir)
        DspBtn.config(text="Display", bg="#5C8374")
        DspBtn.grid(row=2, column=0, sticky=tk.E, padx=(0, 10), pady=(50, 0))

        ClrBtn = tk.Button(root)
        ClrBtn.config(text="Clear", bg="#5C8374", command=self.delete_items)
        ClrBtn.grid(row=2, column=1, sticky=tk.W + tk.E, padx=(0, 10), pady=(50, 0))

        SvBtn = tk.Button(root, command=self.save_timetable)
        SvBtn.config(text="Save", bg="#5C8374")
        SvBtn.grid(row=2, column=2, sticky=tk.W + tk.E, padx=(0, 10), pady=(50, 0))

        SelCrsLb1 = tk.Label(root)
        SelCrsLb1.config(text="Selected courses: ", bg="#5C8374")
        SelCrsLb1.grid(row=5, column=0, padx=(70, 0), pady=(50, 10))

        self.SelCrsLbx = tk.Listbox(root, width=25)
        self.SelCrsLbx.grid(row=6, column=0, columnspan=2, padx=(13, 32), pady=(10, 10))
        self.SelCrsLbx.configure(bg="#5C8374")
        self.SelCrsLbx.bind("<ButtonRelease-1>", self.onSelCrsLbxClick)

        CrsLb1 = tk.Label(root)
        CrsLb1.config(text="Courses: ", bg="#5C8374")
        CrsLb1.grid(row=5, column=2, columnspan=10, padx=(35, 0), pady=(50, 10))

        self.CrsLbx = tk.Listbox(root, width=50)
        self.CrsLbx.grid(row=6, column=5, columnspan=10, padx=(0, 71), pady=(10, 10))
        self.CrsLbx.bind("<<ListboxSelect>>", self.onSelect)
        self.CrsLbx.configure(bg='#5C8374')
        self.CrsLbx_scrollbar = tk.Scrollbar(root, orient="vertical", command=self.CrsLbx.yview)
        self.CrsLbx.configure(yscrollcommand=self.CrsLbx_scrollbar.set)
        self.CrsLbx_scrollbar.grid(row=6, column=13, sticky="ns", pady=(10, 10))

    def enter_file_dir(self):
        selected_year = self.YrBox.get()
        selected_department = self.DpEntry.get()

        self.CrsLbx.delete(0, tk.END)
        filepath = self.PathEntry.get()

        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as file:
                for line in file:
                    parts = line.strip().split(',')
                    if len(parts) == 4:
                        course_info, description, day_info, time_info = parts
                        course_parts = course_info.split()
                        if len(course_parts) >= 2:
                            course_code, semester = course_parts[:2]
                            if (not selected_year or selected_year == semester[0]) and \
                                    (not selected_department or selected_department == course_code[
                                                                                       :len(selected_department)]):
                                course_output = f"{course_code}{semester},{description},{day_info},{time_info}"
                                self.CrsLbx.insert(tk.END, course_output)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def delete_items(self):
        self.CrsLbx.delete(0, tk.END)
        self.SelCrsLbx.delete(0, tk.END)

    def onSelect(self, event):
        selected_course_index = self.CrsLbx.curselection()

        if selected_course_index:
            first_selected_index = selected_course_index[0]
            selected_course = self.CrsLbx.get(first_selected_index)

            _, _, selected_day, selected_time = selected_course.split(',')

            for i in range(self.SelCrsLbx.size()):
                existing_course = self.SelCrsLbx.get(i)

                if selected_course == existing_course:
                    messagebox.showwarning("Warning", "You cannot select the same course again.")
                    return

                _, _, day, time = existing_course.split(',')
                if day == selected_day and time == selected_time:
                    messagebox.showerror("Error", "Courses with the same schedule cannot be displayed.")
                    return

            if self.SelCrsLbx.size() < 6:
                self.SelCrsLbx.insert(tk.END, selected_course)
            else:
                messagebox.showwarning("Warning", "You can only select up to 6 courses.")

    def onSelCrsLbxClick(self, event):
        selected_index = self.SelCrsLbx.nearest(event.y)
        self.SelCrsLbx.delete(selected_index)

    def save_timetable(self):
        selected_courses = [self.SelCrsLbx.get(i) for i in range(self.SelCrsLbx.size())]

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[["CSV Files", "*.csv"]])

        if file_path:
            try:
                with open(file_path, mode='w', newline='', encoding="utf-8") as file:
                    csv_writer = csv.writer(file)
                    csv_writer.writerow(["Semester", "Description", "Day", "Time"])

                    if selected_courses:
                        for course in selected_courses:
                            course_info = course.split(',')
                            csv_writer.writerow(course_info)
                    else:
                        print("No courses selected. File not created.")

                messagebox.showinfo("Success", "Timetable saved successfully!")

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = (Timetable(root))
    root.mainloop()
