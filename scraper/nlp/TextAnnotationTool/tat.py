import tkinter as tk
import json

def main():
    # Create window
    root = tk.Tk()
    root.title("Text Annotation Tool")
    root.geometry("1000x800")
    DARK = '#555555'
    GREY = '#666666'
    root.configure(bg=DARK)

    # jobDesc
    jobDescLabel = tk.Label(root, text="Job Description String", font=("Arial", 10), bg=DARK, fg='white')
    jobDescLabel.pack(anchor="w", padx=20, pady=(10, 0))
    jobDescText = tk.Text(root, height=15, wrap="word", bg=GREY, fg='white')
    jobDescText.pack(padx=20, pady=5, fill="x")


    entityFrame = tk.Frame(root, bg=DARK)
    entityFrame.pack(fill='both', padx=20, pady = (10, 0))
    entityFrame.grid_columnconfigure(0, weight=1)
    entityFrame.grid_columnconfigure(1, weight=1)

    
    entries = []
    labelText = ['Expected Salary Entity', 
        'Expected Experience Entity', 
        'Expected Location Entities (separate with ; )']

    for i, txt in enumerate(labelText):
        curLabel = tk.Label(entityFrame, text=txt, font=("Arial", 10), bg=DARK, fg='white')
        curLabel.grid(row=i*2, column=0, sticky="w", pady=(10,0))
        
        if i == len(labelText)-1:
            curEntry = tk.Text(entityFrame, width=50, height=10, wrap='word', bg=GREY, fg='white')
        else:
            curEntry = tk.Entry(entityFrame, width=100, bg=GREY, fg='white')
        curEntry.grid(row=i*2+1, column=0, pady=5, sticky='ew')
        entries.append(curEntry)

    # Submit button
    submit_button = tk.Button(entityFrame, 
        text="Get Entities", 
        bg=GREY, 
        fg='white', 
        activebackground=DARK, 
        activeforeground='white', 
        command=lambda: getEntities(
            jobDescText, 
            entries, 
            outputText
            )
        )
    submit_button.grid(row=6, column=0, columnspan=1, padx=100, pady=20, sticky='ew')

    # Clear button
    clearButton = tk.Button(entityFrame, 
        text="Clear fields", 
        bg=GREY, 
        fg='white', 
        activebackground=DARK, 
        activeforeground='white', 
        command=lambda: clearFields(
            jobDescText, 
            entries
            )
        )
    clearButton.grid(row=7, column=0, columnspan=1, padx=100, pady=10, sticky='ew')

    # Output text
    outputText = tk.Text(entityFrame, height=10, width=70, wrap="word", bg=GREY, fg='white')
    outputText.grid(row=0, column=1, rowspan=8, padx=(20, 0), pady=5, sticky="nsew")

    entityFrame.grid_rowconfigure(0, weight=1)  # output text row
    entityFrame.grid_rowconfigure(1, weight=1)
    entityFrame.grid_rowconfigure(2, weight=1)
    entityFrame.grid_rowconfigure(3, weight=1)
    entityFrame.grid_rowconfigure(4, weight=1)
    entityFrame.grid_rowconfigure(5, weight=1)
    entityFrame.grid_rowconfigure(6, weight=1)
    entityFrame.grid_rowconfigure(7, weight=1)

    root.mainloop()


def getEntities(jobDescText, entries, outputText):

    entities = []
    jobDesc = jobDescText.get("1.0", tk.END)

    salary = entries[0].get()
    salaryStart = jobDesc.find(salary)
    salaryEnd = salaryStart + len(salary)
    entities.append(json.dumps([salaryStart, salaryEnd, "SALARY"]))

    experience = entries[1].get()
    experienceStart = jobDesc.find(experience)
    experienceEnd = experienceStart + len(experience)
    entities.append(json.dumps([experienceStart, experienceEnd, "EXPERIENCE"]))

    expectedLocations = entries[2].get("1.0", tk.END).strip() 
    expectedLocations = expectedLocations.split('; ')

    for loc in expectedLocations:
        print(repr(loc))
        locationStart = jobDesc.find(loc)
        locationEnd = locationStart + len(loc)
        entities.append(json.dumps([locationStart, locationEnd, "LOCATION"]))
    
    outputText.delete('1.0', tk.END)
    output = '\n\t\t\t' + ', \n\t\t\t'.join(entities) + '\n\t\t' #escape characters added for easy copy/paste
    outputText.insert('1.0', output)

def clearFields(jobDescText, entries):
    jobDescText.delete('1.0', tk.END)
    
    for e in entries:
        if isinstance(e, tk.Text):
            e.delete('1.0', tk.END)
        else:
            e.delete(0, tk.END)


if __name__ == '__main__':
    main()

