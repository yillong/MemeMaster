import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk
import os

class MemeMasterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MemeMaster — Создай свой мем!")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        
        self.root.configure(bg="#2c3e50")

        self.image_path = None
        self.original_image = None
        self.display_image = None
        self.tk_image = None
        self.result_image = None

        self.create_widgets()
        self.apply_styles()

    def create_widgets(self):

        control_frame = tk.Frame(self.root, bg="#34495e", relief=tk.RAISED, bd=2)
        control_frame.pack(pady=10, padx=10, fill=tk.X)

        self.btn_load = tk.Button(
            control_frame, 
            text="📁 Загрузить изображение", 
            command=self.load_image,
            font=("Arial", 10, "bold"),
            cursor="hand2"
        )
        self.btn_load.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Поля для текста с метками
        tk.Label(
            control_frame, 
            text="Верхний текст:", 
            bg="#34495e", 
            fg="#ecf0f1", 
            font=("Arial", 10, "bold")
        ).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        
        self.entry_top = tk.Entry(control_frame, width=25, font=("Arial", 10), bg="#ecf0f1")
        self.entry_top.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(
            control_frame, 
            text="Нижний текст:", 
            bg="#34495e", 
            fg="#ecf0f1", 
            font=("Arial", 10, "bold")
        ).grid(row=2, column=0, padx=5, pady=5, sticky="e")
        
        self.entry_bottom = tk.Entry(control_frame, width=25, font=("Arial", 10), bg="#ecf0f1")
        self.entry_bottom.grid(row=2, column=1, padx=5, pady=5)

        # Кнопки управления в один ряд
        button_frame = tk.Frame(control_frame, bg="#34495e")
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)

        # Кнопка создания мема
        self.btn_create = tk.Button(
            button_frame, 
            text="✨ Создать мем ✨", 
            command=self.create_meme,
            font=("Arial", 11, "bold"),
            bg="#27ae60",
            fg="white",
            cursor="hand2"
        )
        self.btn_create.pack(side=tk.LEFT, padx=5)

        # Кнопка сохранения 
        self.btn_save = tk.Button(
            button_frame, 
            text="💾 Сохранить мем", 
            command=self.save_meme, 
            state=tk.DISABLED,
            font=("Arial", 10, "bold"),
            bg="#2980b9",
            fg="white",
            cursor="hand2"
        )
        self.btn_save.pack(side=tk.LEFT, padx=5)

        # Кнопка очистки
        self.btn_clear = tk.Button(
            button_frame, 
            text="🗑 Очистить всё", 
            command=self.clear_all,
            font=("Arial", 10, "bold"),
            bg="#e67e22",
            fg="white",
            cursor="hand2"
        )
        self.btn_clear.pack(side=tk.LEFT, padx=5)

        preview_frame = tk.Frame(self.root, bg="#ecf0f1", relief=tk.SUNKEN, bd=2)
        preview_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        self.preview_label = tk.Label(
            preview_frame, 
            text="🖼 Загрузите изображение для создания мема", 
            bg="#ecf0f1",
            font=("Arial", 12, "italic"),
            fg="#7f8c8d"
        )
        self.preview_label.pack(fill=tk.BOTH, expand=True)

        # Статусная строка
        self.status_var = tk.StringVar()
        self.status_var.set("✅ Готов к работе")
        self.status_bar = tk.Label(
            self.root, 
            textvariable=self.status_var, 
            bd=1, 
            relief=tk.SUNKEN, 
            anchor=tk.W,
            bg="#34495e",
            fg="#ecf0f1",
            font=("Arial", 9)
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def apply_styles(self):
        """Дополнительные стили для элементов"""
        def on_enter_focus(event, entry):
            entry.configure(bg="#fff9c4")
        
        def on_leave_focus(event, entry):
            entry.configure(bg="#ecf0f1")
        
        self.entry_top.bind("<FocusIn>", lambda e: on_enter_focus(e, self.entry_top))
        self.entry_top.bind("<FocusOut>", lambda e: on_leave_focus(e, self.entry_top))
        self.entry_bottom.bind("<FocusIn>", lambda e: on_enter_focus(e, self.entry_bottom))
        self.entry_bottom.bind("<FocusOut>", lambda e: on_leave_focus(e, self.entry_bottom))

    # Загрузка изображения
    def load_image(self):
        file_path = filedialog.askopenfilename(
            title="Выберите изображение",
            filetypes=[("Изображения", "*.jpeg *.jpg *.png *.bmp")]
        )
        if not file_path:
            return

        try:
            self.original_image = Image.open(file_path)
            self.image_path = file_path
            self.update_preview(self.original_image)
            self.status_var.set(f"✅ Загружено: {os.path.basename(file_path)}")
            self.btn_save.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить изображение:\n{e}")
            self.status_var.set("❌ Ошибка загрузки")

    def update_preview(self, pil_image):
        if pil_image is None:
            return
        self.display_image = pil_image.copy()
        preview_width = 600
        preview_height = 450
        self.display_image.thumbnail((preview_width, preview_height), Image.Resampling.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(self.display_image)
        self.preview_label.config(image=self.tk_image, text="")
        self.preview_label.image = self.tk_image

    # Наложение текста 
    def create_meme(self):
        if self.original_image is None:
            messagebox.showwarning("Предупреждение", "Сначала загрузите изображение!")
            return

        top_text = self.entry_top.get().strip()
        bottom_text = self.entry_bottom.get().strip()

        if not top_text and not bottom_text:
            if not messagebox.askyesno("Пустой текст", "Вы не ввели текст. Продолжить?"):
                return

        meme_image = self.original_image.copy()
        draw = ImageDraw.Draw(meme_image)

        try:
            font_path = "arial.ttf"
            if not os.path.exists(font_path):
                font_path = "times.ttf"
            font_size = int(meme_image.height / 12)
            font = ImageFont.truetype(font_path, font_size)
        except:
            font = ImageFont.load_default()
            font_size = 20

        def draw_text_with_outline(draw, text, position, font, outline_color="black", fill_color="white"):
            x, y = position
            for dx in [-2, -1, 0, 1, 2]:
                for dy in [-2, -1, 0, 1, 2]:
                    if dx != 0 or dy != 0:
                        draw.text((x + dx, y + dy), text, font=font, fill=outline_color)
            draw.text((x, y), text, font=font, fill=fill_color)

        if top_text:
            bbox = draw.textbbox((0, 0), top_text, font=font)
            text_width = bbox[2] - bbox[0]
            x_top = (meme_image.width - text_width) // 2
            y_top = 10
            draw_text_with_outline(draw, top_text, (x_top, y_top), font)

        if bottom_text:
            bbox = draw.textbbox((0, 0), bottom_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x_bottom = (meme_image.width - text_width) // 2
            y_bottom = meme_image.height - text_height - 10
            draw_text_with_outline(draw, bottom_text, (x_bottom, y_bottom), font)

        self.update_preview(meme_image)
        self.result_image = meme_image
        self.btn_save.config(state=tk.NORMAL)
        self.status_var.set("🎉 Мем создан! Можно сохранять")

    # Сохранение результата 
    def save_meme(self):
        if not hasattr(self, 'result_image') or self.result_image is None:
            messagebox.showwarning("Предупреждение", "Нет созданного мема. Сначала нажмите 'Создать мем'.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")]
        )
        if not file_path:
            return

        try:
            save_img = self.result_image
            if file_path.lower().endswith('.jpg') or file_path.lower().endswith('.jpeg'):
                if save_img.mode in ('RGBA', 'LA', 'P'):
                    rgb_img = Image.new('RGB', save_img.size, (255, 255, 255))
                    rgb_img.paste(save_img, mask=save_img.split()[-1] if save_img.mode == 'RGBA' else None)
                    save_img = rgb_img
            save_img.save(file_path)
            self.status_var.set(f"💾 Сохранено: {os.path.basename(file_path)}")
            messagebox.showinfo("Успех", "Мем успешно сохранён!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{e}")
            self.status_var.set("❌ Ошибка сохранения")

    #  Очистка всего 
    def clear_all(self):
        if messagebox.askyesno("Очистка", "Вы уверены, что хотите очистить всё?"):
            self.original_image = None
            self.result_image = None
            self.image_path = None
            self.entry_top.delete(0, tk.END)
            self.entry_bottom.delete(0, tk.END)
            self.preview_label.config(image="", text="🖼 Загрузите изображение для создания мема")
            self.btn_save.config(state=tk.DISABLED)
            self.status_var.set("🧹 Всё очищено")

if __name__ == "__main__":
    root = tk.Tk()
    app = MemeMasterApp(root)
    root.mainloop()