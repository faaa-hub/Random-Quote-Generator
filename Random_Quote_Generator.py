import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import random


class QuoteGenerator:
    """Класс для управления генератором цитат"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("?? Random Quote Generator")
        self.root.geometry("900x700")
        self.root.minsize(800, 650)
        self.root.configure(bg="#f0f0f0")
        
        self.quotes = []
        self.history = []
        self.filename = "quotes.json"
        self.history_file = "quote_history.json"
        
        # Предопределённые цитаты
        self.default_quotes = [
            {"text": "Единственный способ сделать великую работу — любить то, что вы делаете.", "author": "Стив Джобс", "topic": "Мотивация"},
            {"text": "Жизнь — это то, что с вами происходит, пока вы строите другие планы.", "author": "Джон Леннон", "topic": "Жизнь"},
            {"text": "Успех — это способность шагать от одной неудачи к другой, не теряя энтузиазма.", "author": "Уинстон Черчилль", "topic": "Успех"},
            {"text": "Лучший способ предсказать будущее — создать его.", "author": "Питер Друкер", "topic": "Мотивация"},
            {"text": "В знаниях сила.", "author": "Фрэнсис Бэкон", "topic": "Знания"},
            {"text": "Неудача — это просто возможность начать снова, но уже более мудро.", "author": "Генри Форд", "topic": "Успех"},
            {"text": "Счастье — это не что-то готовое. Оно происходит от ваших собственных действий.", "author": "Далай-лама", "topic": "Жизнь"},
            {"text": "Образование — это самое мощное оружие, которое вы можете использовать, чтобы изменить мир.", "author": "Нельсон Мандела", "topic": "Знания"},
            {"text": "Ваше время ограничено, не тратьте его, живя чужой жизнью.", "author": "Стив Джобс", "topic": "Жизнь"},
            {"text": "Победа — это ещё не всё, всё — это постоянное желание побеждать.", "author": "Винс Ломбарди", "topic": "Успех"}
        ]
        
        self.create_widgets()
        self.load_quotes()
        self.load_history()
    
    def create_widgets(self):
        """Создание элементов интерфейса"""
        
        # Заголовок
        title_label = tk.Label(
            self.root,
            text="?? Random Quote Generator",
            font=("Arial", 20, "bold"),
            bg="#f0f0f0",
            fg="#1a1a2e"
        )
        title_label.pack(pady=15)
        
        # Фрейм для генерации
        generate_frame = tk.LabelFrame(
            self.root,
            text="Генерация цитаты",
            font=("Arial", 12, "bold"),
            bg="#ffffff",
            padx=15,
            pady=15
        )
        generate_frame.pack(fill="x", padx=20, pady=10)
        
        # Область отображения цитаты
        self.quote_display = tk.Text(
            generate_frame,
            height=6,
            width=80,
            font=("Arial", 12, "italic"),
            bg="#fff9e6",
            fg="#333333",
            wrap="word",
            relief="solid",
            bd=2
        )
        self.quote_display.pack(pady=10, padx=10)
        
        # Автор и тема
        info_frame = tk.Frame(generate_frame, bg="#ffffff")
        info_frame.pack(pady=5)
        
        self.label_author = tk.Label(
            info_frame,
            text="Автор: —",
            font=("Arial", 11, "bold"),
            bg="#ffffff",
            fg="#1a1a2e"
        )
        self.label_author.pack(side="left", padx=20)
        
        self.label_topic = tk.Label(
            info_frame,
            text="Тема: —",
            font=("Arial", 11),
            bg="#ffffff",
            fg="#666666"
        )
        self.label_topic.pack(side="left", padx=20)
        
        # Кнопка генерации
        btn_generate = tk.Button(
            generate_frame,
            text="?? Сгенерировать цитату",
            command=self.generate_quote,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
            width=25,
            height=2
        )
        btn_generate.pack(pady=10)
        self.create_tooltip(btn_generate, "Выбрать случайную цитату из коллекции")
        
        # Фрейм для добавления новой цитаты
        add_frame = tk.LabelFrame(
            self.root,
            text="Добавить новую цитату",
            font=("Arial", 12, "bold"),
            bg="#ffffff",
            padx=15,
            pady=15
        )
        add_frame.pack(fill="x", padx=20, pady=10)
        
        # Текст цитаты
        tk.Label(add_frame, text="Цитата:", bg="#ffffff", 
                font=("Arial", 10)).grid(row=0, column=0, sticky="ne", pady=5)
        self.entry_quote = tk.Text(add_frame, width=50, height=3, font=("Arial", 10))
        self.entry_quote.grid(row=0, column=1, padx=10, pady=5)
        self.create_tooltip(self.entry_quote, "Введите текст цитаты")
        
        # Автор
        tk.Label(add_frame, text="Автор:", bg="#ffffff", 
                font=("Arial", 10)).grid(row=1, column=0, sticky="e", pady=5)
        self.entry_author = tk.Entry(add_frame, width=30, font=("Arial", 10))
        self.entry_author.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.create_tooltip(self.entry_author, "Введите имя автора")
        
        # Тема
        tk.Label(add_frame, text="Тема:", bg="#ffffff", 
                font=("Arial", 10)).grid(row=2, column=0, sticky="e", pady=5)
        self.entry_topic = tk.Entry(add_frame, width=30, font=("Arial", 10))
        self.entry_topic.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.create_tooltip(self.entry_topic, "Введите тему (Мотивация, Жизнь, Успех и т.д.)")
        
        # Кнопка добавления
        btn_add = tk.Button(
            add_frame,
            text="? Добавить цитату",
            command=self.add_quote,
            bg="#2196F3",
            fg="white",
            font=("Arial", 11, "bold"),
            width=20,
            height=2
        )
        btn_add.grid(row=3, column=0, columnspan=2, pady=10)
        self.create_tooltip(btn_add, "Добавить цитату в коллекцию")
        
        # Фрейм для фильтрации истории
        filter_frame = tk.LabelFrame(
            self.root,
            text="Фильтрация истории",
            font=("Arial", 12, "bold"),
            bg="#ffffff",
            padx=15,
            pady=10
        )
        filter_frame.pack(fill="x", padx=20, pady=10)
        
        # Фильтр по автору
        tk.Label(filter_frame, text="Автор:", bg="#ffffff", 
                font=("Arial", 10)).grid(row=0, column=0, padx=5)
        self.filter_author = tk.Entry(filter_frame, width=20, font=("Arial", 10))
        self.filter_author.grid(row=0, column=1, padx=5)
        self.filter_author.insert(0, "Все")
        self.create_tooltip(self.filter_author, "Фильтр по автору")
        
        # Фильтр по теме
        tk.Label(filter_frame, text="Тема:", bg="#ffffff", 
                font=("Arial", 10)).grid(row=0, column=2, padx=5)
        self.filter_topic = tk.Entry(filter_frame, width=15, font=("Arial", 10))
        self.filter_topic.grid(row=0, column=3, padx=5)
        self.filter_topic.insert(0, "Все")
        self.create_tooltip(self.filter_topic, "Фильтр по теме")
        
        # Кнопки фильтрации
        btn_filter = tk.Button(
            filter_frame,
            text="?? Применить",
            command=self.apply_filter,
            bg="#FF9800",
            fg="white",
            font=("Arial", 10, "bold"),
            width=12
        )
        btn_filter.grid(row=0, column=4, padx=10)
        self.create_tooltip(btn_filter, "Применить фильтры")
        
        btn_reset = tk.Button(
            filter_frame,
            text="?? Сбросить",
            command=self.reset_filter,
            bg="#9E9E9E",
            fg="white",
            font=("Arial", 10, "bold"),
            width=12
        )
        btn_reset.grid(row=0, column=5, padx=10)
        self.create_tooltip(btn_reset, "Сбросить все фильтры")
        
        # История (Listbox)
        history_frame = tk.Frame(self.root, bg="#ffffff")
        history_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        tk.Label(history_frame, text="?? История сгенерированных цитат:", 
                font=("Arial", 11, "bold"), bg="#ffffff").pack(anchor="w", padx=5, pady=5)
        
        self.history_listbox = tk.Listbox(
            history_frame,
            font=("Arial", 10),
            bg="#f9f9f9",
            fg="#333333",
            selectbackground="#4CAF50",
            selectforeground="white",
            relief="solid",
            bd=2
        )
        self.history_listbox.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        scrollbar = tk.Scrollbar(history_frame, orient="vertical", command=self.history_listbox.yview)
        self.history_listbox.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y", pady=5)
        
        # Кнопки управления
        btn_frame = tk.Frame(self.root, bg="#f0f0f0")
        btn_frame.pack(pady=10)
        
        btn_clear = tk.Button(
            btn_frame,
            text="??? Очистить историю",
            command=self.clear_history,
            bg="#f44336",
            fg="white",
            font=("Arial", 10, "bold"),
            width=18,
            height=2
        )
        btn_clear.pack(side="left", padx=5)
        self.create_tooltip(btn_clear, "Удалить всю историю")
        
        btn_save = tk.Button(
            btn_frame,
            text="?? Сохранить",
            command=self.save_data,
            bg="#9C27B0",
            fg="white",
            font=("Arial", 10, "bold"),
            width=18,
            height=2
        )
        btn_save.pack(side="left", padx=5)
        self.create_tooltip(btn_save, "Сохранить данные в JSON")
        
        # Статус бар
        self.status_label = tk.Label(
            self.root,
            text=f"Цитат в коллекции: 0 | В истории: 0",
            font=("Arial", 10),
            bg="#1a1a2e",
            fg="white",
            pady=5
        )
        self.status_label.pack(fill="x", side="bottom")
    
    def create_tooltip(self, widget, text):
        """Создание подсказки для виджета"""
        tooltip = tk.Toplevel(widget)
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry("+0+0")
        tooltip.withdraw()
        
        label = tk.Label(
            tooltip,
            text=text,
            background="#ffffe0",
            relief="solid",
            borderwidth=1,
            font=("Arial", 9)
        )
        label.pack()
        
        def show_tooltip(event):
            tooltip.deiconify()
            x = widget.winfo_rootx() + 20
            y = widget.winfo_rooty() + widget.winfo_height() + 5
            tooltip.wm_geometry(f"+{x}+{y}")
        
        def hide_tooltip(event):
            tooltip.withdraw()
        
        widget.bind("<Enter>", show_tooltip)
        widget.bind("<Leave>", hide_tooltip)
    
    def validate_input(self, text, author, topic):
        """Проверка корректности ввода"""
        
        if not text.strip():
            messagebox.showerror("Ошибка", "Введите текст цитаты!")
            return False
        
        if not author.strip():
            messagebox.showerror("Ошибка", "Введите имя автора!")
            return False
        
        if not topic.strip():
            messagebox.showerror("Ошибка", "Введите тему!")
            return False
        
        return True
    
    def generate_quote(self):
        """Генерация случайной цитаты"""
        
        if not self.quotes:
            messagebox.showwarning("Внимание", "Коллекция пуста! Добавьте цитаты.")
            return
        
        # Выбор случайной цитаты
        quote = random.choice(self.quotes)
        
        # Отображение
        self.quote_display.delete("1.0", tk.END)
        self.quote_display.insert("1.0", f'"{quote["text"]}"')
        
        self.label_author.config(text=f"Автор: {quote['author']}")
        self.label_topic.config(text=f"Тема: {quote['topic']}")
        
        # Добавление в историю
        history_entry = f"{quote['text'][:50]}... — {quote['author']} ({quote['topic']})"
        self.history.append({
            "text": quote["text"],
            "author": quote["author"],
            "topic": quote["topic"],
            "full_display": history_entry
        })
        
        self.update_history()
        self.save_data()
        
        self.status_label.config(
            text=f"Цитат в коллекции: {len(self.quotes)} | В истории: {len(self.history)}"
        )
    
    def add_quote(self):
        """Добавление новой цитаты"""
        
        text = self.entry_quote.get("1.0", tk.END).strip()
        author = self.entry_author.get().strip()
        topic = self.entry_topic.get().strip()
        
        if not self.validate_input(text, author, topic):
            return
        
        quote = {
            "text": text,
            "author": author,
            "topic": topic
        }
        
        self.quotes.append(quote)
        self.save_data()
        
        # Очистка полей
        self.entry_quote.delete("1.0", tk.END)
        self.entry_author.delete(0, tk.END)
        self.entry_topic.delete(0, tk.END)
        
        messagebox.showinfo("Успех", f"Цитата от {author} добавлена!")
        self.status_label.config(
            text=f"Цитат в коллекции: {len(self.quotes)} | В истории: {len(self.history)}"
        )
    
    def apply_filter(self):
        """Применение фильтрации истории"""
        
        author_filter = self.filter_author.get().strip().lower()
        topic_filter = self.filter_topic.get().strip().lower()
        
        self.history_listbox.delete(0, tk.END)
        
        for item in self.history:
            # Фильтр по автору
            if author_filter and author_filter != "все":
                if author_filter not in item["author"].lower():
                    continue
            
            # Фильтр по теме
            if topic_filter and topic_filter != "все":
                if topic_filter not in item["topic"].lower():
                    continue
            
            self.history_listbox.insert(tk.END, item["full_display"])
    
    def reset_filter(self):
        """Сброс фильтров"""
        
        self.filter_author.delete(0, tk.END)
        self.filter_author.insert(0, "Все")
        self.filter_topic.delete(0, tk.END)
        self.filter_topic.insert(0, "Все")
        
        self.update_history()
    
    def update_history(self):
        """Обновление списка истории"""
        
        self.history_listbox.delete(0, tk.END)
        
        for item in self.history:
            self.history_listbox.insert(tk.END, item["full_display"])
    
    def clear_history(self):
        """Очистка истории"""
        
        confirm = messagebox.askyesno("Подтверждение", "Удалить всю историю?")
        
        if confirm:
            self.history = []
            self.update_history()
            self.save_data()
            messagebox.showinfo("Успех", "История очищена!")
            self.status_label.config(
                text=f"Цитат в коллекции: {len(self.quotes)} | В истории: {len(self.history)}"
            )
    
    def save_data(self):
        """Сохранение данных в JSON"""
        
        try:
            # Сохранение коллекции цитат
            with open(self.filename, "w", encoding="utf-8") as file:
                json.dump(self.quotes, file, ensure_ascii=False, indent=4)
            
            # Сохранение истории
            with open(self.history_file, "w", encoding="utf-8") as file:
                json.dump(self.history, file, ensure_ascii=False, indent=4)
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить: {e}")
    
    def load_quotes(self):
        """Загрузка цитат из JSON"""
        
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as file:
                    self.quotes = json.load(file)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить цитаты: {e}")
                self.quotes = self.default_quotes.copy()
        else:
            # Если файла нет, используем предопределённые цитаты
            self.quotes = self.default_quotes.copy()
            self.save_data()
    
    def load_history(self):
        """Загрузка истории из JSON"""
        
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r", encoding="utf-8") as file:
                    self.history = json.load(file)
                self.update_history()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить историю: {e}")
                self.history = []
        else:
            self.history = []
        
        self.status_label.config(
            text=f"Цитат в коллекции: {len(self.quotes)} | В истории: {len(self.history)}"
        )


# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = QuoteGenerator(root)
    root.mainloop()
