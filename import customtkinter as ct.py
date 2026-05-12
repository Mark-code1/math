import customtkinter as ctk
import re

class ByrmaldaGrayEdition(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Math Solver by byrmalda 2026")
        self.geometry("1000x700")
        self.current_lang = "UKR"
        
        # Названия для перевода
        self.translations = {
            "UKR": {
                "task_label": "📝 ВВЕДІТЬ УМОВУ ЗАДАЧІ:",
                "solve_btn": "РОЗВ'ЯЗАТИ ЗАДАЧУ",
                "ans_label": "ВІДПОВІДЬ:",
                "calc_err": "Помилка",
                "theme_btn": "Змінити тему"
            },
            "RUS": {
                "task_label": "📝 ВВЕДИТЕ УСЛОВИЕ ЗАДАЧИ:",
                "solve_btn": "РЕШИТЬ ЗАДАЧУ",
                "ans_label": "ОТВЕТ:",
                "calc_err": "Ошибка",
                "theme_btn": "Сменить тему"
            },
            "ENG": {
                "task_label": "📝 ENTER TASK:",
                "solve_btn": "SOLVE NOW",
                "ans_label": "ANSWER:",
                "calc_err": "Error",
                "theme_btn": "Change theme"
            }
        }

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # --- ЛЕВАЯ ЧАСТЬ (Калькулятор) ---
        self.left_frame = ctk.CTkFrame(self, fg_color=("#e0e0e0", "#1e1e1e"))
        self.left_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.calc_entry = ctk.CTkEntry(self.left_frame, height=50, font=("Consolas", 22), justify="center", 
                                       fg_color=("#f0f0f0", "#121212"), border_color="#cccccc")
        self.calc_entry.pack(fill="x", padx=20, pady=20)

        self.btn_grid = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        self.btn_grid.pack(pady=10)
        
        btns = ['7','8','9','/','4','5','6','*','1','2','3','-','0','C','=','+']
        for i, txt in enumerate(btns):
            # Кнопки теперь светло-серые
            btn = ctk.CTkButton(self.btn_grid, text=txt, width=70, height=70, font=("Arial", 20, "bold"),
                                fg_color=("#d0d0d0", "#333333"), text_color=("#333333", "#ffffff"),
                                hover_color=("#bcbcbc", "#444444"), command=lambda x=txt: self.calc_press(x))
            btn.grid(row=i//4, column=i%4, padx=5, pady=5)

        self.calc_res_label = ctk.CTkLabel(self.left_frame, text="0", font=("Consolas", 20), height=50)
        self.calc_res_label.pack(fill="x", padx=20, pady=20)

        # --- ПРАВАЯ ЧАСТЬ (Задачи) ---
        self.right_frame = ctk.CTkFrame(self, fg_color=("#e0e0e0", "#1e1e1e"))
        self.right_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.task_label = ctk.CTkLabel(self.right_frame, text="", font=("Arial", 16, "bold"))
        self.task_label.pack(pady=(20, 5), padx=20, anchor="w")

        self.task_input = ctk.CTkTextbox(self.right_frame, height=200, font=("Arial", 15), 
                                         fg_color=("#f0f0f0", "#121212"), border_width=1, border_color="#cccccc")
        self.task_input.pack(fill="x", padx=20, pady=5)

        # Кнопка решения тоже серая
        self.solve_btn = ctk.CTkButton(self.right_frame, text="", fg_color=("#bcbcbc", "#444444"), 
                                       text_color=("#333333", "#ffffff"), hover_color=("#a0a0a0", "#555555"),
                                       font=("Arial", 16, "bold"), height=45, command=self.solve_text_task)
        self.solve_btn.pack(pady=20, fill="x", padx=40)

        self.ans_title = ctk.CTkLabel(self.right_frame, text="", font=("Arial", 14, "bold"))
        self.ans_title.pack(padx=20, anchor="w")

        # Поле ответа адаптивное: светло-серое в светлой теме, темно-серое в темной
        self.task_res_box = ctk.CTkTextbox(self.right_frame, height=120, font=("Consolas", 18), 
                                           fg_color=("#dcdcdc", "#0a0a0a"), text_color=("#333333", "#ffffff"))
        self.task_res_box.pack(fill="x", padx=20, pady=10)

        # --- НИЖНЯЯ ПАНЕЛЬ ---
        self.controls = ctk.CTkFrame(self, height=80, fg_color=("#cccccc", "#161616"))
        self.controls.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        self.author_label = ctk.CTkLabel(self.controls, text="byrmalda 2026", font=("Courier New", 18, "bold"), 
                                         text_color=("#555555", "#888888"))
        self.author_label.pack(side="left", padx=25)

        self.lang_menu = ctk.CTkOptionMenu(self.controls, values=["UKR", "RUS", "ENG"], command=self.change_lang, 
                                           width=100, fg_color=("#bcbcbc", "#333333"), button_color=("#a0a0a0", "#444444"),
                                           text_color=("#333333", "#ffffff"))
        self.lang_menu.pack(side="right", padx=10)

        self.theme_btn = ctk.CTkButton(self.controls, text="", width=120, command=self.toggle_theme, 
                                       fg_color=("#bcbcbc", "#333333"), text_color=("#333333", "#ffffff"),
                                       hover_color=("#a0a0a0", "#444444"))
        self.theme_btn.pack(side="right", padx=10)

        self.change_lang("UKR")

    def toggle_theme(self):
        mode = "Light" if ctk.get_appearance_mode() == "Dark" else "Dark"
        ctk.set_appearance_mode(mode)

    def change_lang(self, new_lang):
        self.current_lang = new_lang
        t = self.translations[new_lang]
        self.task_label.configure(text=t["task_label"])
        self.solve_btn.configure(text=t["solve_btn"])
        self.ans_title.configure(text=t["ans_label"])
        self.theme_btn.configure(text=t["theme_btn"])

    def calc_press(self, char):
        if char == "C": 
            self.calc_entry.delete(0, 'end')
            self.calc_res_label.configure(text="0")
        elif char == "=":
            try: self.calc_res_label.configure(text=f"Result: {eval(self.calc_entry.get())}")
            except: self.calc_res_label.configure(text=self.translations[self.current_lang]["calc_err"])
        else: self.calc_entry.insert('end', char)

    def solve_text_task(self):
        text = self.task_input.get("0.0", "end").lower()
        numbers = [int(n) for n in re.findall(r'\d+', text)]
        if not numbers: return

        minus_words = ["украли", "продали", "съели", "ушли", "вкрали", "з'їли", "stole", "sold", "ate", "потратил"]
        res = numbers[0] - sum(numbers[1:]) if any(w in text for w in minus_words) else sum(numbers)

        self.task_res_box.delete("0.0", "end")
        self.task_res_box.insert("0.0", f"> RESULT: {res}\n> STATUS: OK")

if __name__ == "__main__":
    app = ByrmaldaGrayEdition()
    app.mainloop()







#python "C:/Users/mark7/OneDrive/рабочий стол/CHAT/import customtkinter as ct.py"
#«На складі було 10000 ноутбуків. Зранку привезли ще 2500 нових моделей, але потім виявилося, що 1300 ноутбуків браковані і
# їх повернули. Протягом дня продали 4000 штук, а ввечері
# прийшов клієнт і забрав ще 200 ноутбуків за предзамовленням. Скільки ноутбуків зараз на складі?»