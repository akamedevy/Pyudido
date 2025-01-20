import customtkinter
import sys
import io

class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()

        self.title("RIP Visual Studio Code")

        self.auto_complete = ["(", '"', "{", "["] # palavras que serão auto completadas ao digitar
        self.complete_words = ["()", '""', "{}", "[]"]

        self.keywords = [
    "False", "await", "else", "import", "pass",
    "None", "break", "except", "in", "raise",
    "True", "class", "finally", "is", "return",
    "and", "continue", "for", "lambda", "try",
    "as", "def", "from", "nonlocal", "while",
    "assert", "del", "global", "not", "with",
    "async", "elif", "if", "or", "yield"
]
        self.geometry('1280x720')

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.textbox = customtkinter.CTkTextbox(master=self, height=400, corner_radius=0, font=("Fira Code", 30), text_color=("#4dc242"))
        self.textbox.grid(row=0, column=0, sticky="nsew")

        self.resultado = customtkinter.CTkTextbox(master=self, height=200, font=("Fira Code", 21, "bold"), state="disabled")
        self.resultado.grid(row=1, column=0, sticky="nsew")

        self.executar = customtkinter.CTkButton(self, text="Executar", command=self.run_code)
        self.executar.grid(row=2, column=0, pady=10)

        self.textbox.bind('<Tab>', self.tab_action)
        self.textbox.bind('<Return>', self.enter_action)
        self.textbox.bind('<KeyPress>', self.key_press_action)
        self.textbox.bind("<KeyRelease>", self.on_key_release)

    def tab_action(self, event):
        self.textbox.insert('insert', '    ')
        return 'break'
    

    def enter_action(self, event):
        cursor_position = self.textbox.index('insert')
        
        current_line = int(cursor_position.split('.')[0])
        
        indentation_level = 1
        for i in range(current_line - 1, 0, -1):
            line_content = self.textbox.get(f'{i}.0', f'{i}.end').strip()
            if line_content.endswith(':'):
                indentation_level += 1
            else:
                break
        
        
        indent = '    ' * indentation_level
        self.textbox.insert('insert', f'\n{indent}')
        
        return 'break'

    def key_press_action(self, event):
        for i, char in enumerate(self.auto_complete):
            if event.char == char:

                cursor_pos = self.textbox.index('insert')
                self.textbox.insert('insert', self.complete_words[i])

                start_pos = cursor_pos
                end_pos = self.textbox.index('insert')

                self.textbox.tag_add(f"completed_{i}", cursor_pos, end_pos)
                self.textbox.tag_config(f"completed_{i}", foreground="white") 

                self.center()
                return "break"

    def on_key_release(self, event):
        code = self.textbox.get("1.0", "end-1c")

        for keyword in self.keywords:
            start_idx = "1.0"
            while True:
                start_idx = self.textbox.search(f"{keyword} ", start_idx, nocase=1, stopindex="end")
                if not start_idx:
                    break

                end_idx = f"{start_idx}+{len(keyword)}c"

                self.textbox.tag_add("highlight", start_idx, end_idx)
                self.textbox.tag_config("highlight", foreground="#e368b2")

                start_idx = end_idx

    def center(self):
            current_position = self.textbox.index("insert")
            line, column = map(int, current_position.split('.'))
            self.textbox.mark_set("insert", f"{line}.{column - 1}")

    def run_code(self):
        code = self.textbox.get("1.0", "end-1c")
        
        output = io.StringIO()
        sys.stdout = output
        sys.stderr = output
        
        try:
            exec(code)
        except Exception as e:
            output.write(f"Erro: {e}")
        
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

        self.resultado.configure(state="normal")
        self.resultado.delete("1.0", "end")
        self.resultado.insert("1.0", output.getvalue())
        self.resultado.configure(state="disabled")

if __name__ == "__main__":
    App = App()
    App.mainloop()
