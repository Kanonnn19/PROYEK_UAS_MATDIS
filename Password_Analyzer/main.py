import customtkinter as ctk
from tkinter import messagebox
from analyzer import analyze_password
from generator import generate_password
from database import save_password, get_history

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


class PasswordAnalyzerApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("🔐 Sistem Analisis Keamanan Password")
        self.geometry("1400x800")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_main_frame()

    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nswe")

        ctk.CTkLabel(
            self.sidebar,
            text="🔐\nPassword Analyzer",
            font=("Segoe UI", 24, "bold")
        ).pack(pady=30)

        ctk.CTkButton(self.sidebar, text="📊 Analisis Password",
                      command=self.show_analyzer, height=45).pack(pady=10, padx=20, fill="x")

        ctk.CTkButton(self.sidebar, text="⚙ Generator Password",
                      command=self.show_generator, height=45).pack(pady=10, padx=20, fill="x")

        ctk.CTkButton(self.sidebar, text="📜 Riwayat",
                      command=self.show_history, height=45).pack(pady=10, padx=20, fill="x")

    def create_main_frame(self):
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)
        self.show_analyzer()

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_analyzer(self):
        self.clear_frame()

        ctk.CTkLabel(
            self.main_frame,
            text="Dashboard Keamanan Password",
            font=("Segoe UI", 30, "bold")
        ).pack(pady=20)

        self.password_entry = ctk.CTkEntry(
            self.main_frame,
            width=500,
            height=45,
            placeholder_text="Masukkan password..."
        )
        self.password_entry.pack(pady=10)

        ctk.CTkButton(
            self.main_frame,
            text="Analisis Password",
            command=self.analyze,
            height=45
        ).pack(pady=10)

        self.progress = ctk.CTkProgressBar(self.main_frame, width=500)
        self.progress.pack(pady=10)
        self.progress.set(0)

        self.strength_label = ctk.CTkLabel(
            self.main_frame,
            text="Keamanan : Belum Dianalisis",
            font=("Segoe UI", 22, "bold")
        )
        self.strength_label.pack(pady=10)

        self.cards_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            width=1000,
            height=450
        )
        self.cards_frame.pack(fill="both", expand=True, padx=20, pady=20)

    def analyze(self):
        password = self.password_entry.get()

        if not password:
            messagebox.showwarning("Peringatan", "Masukkan password terlebih dahulu!")
            return

        data = analyze_password(password)
        save_password(password)

        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        strength = data["strength"]

        if strength == "WEAK":
            self.progress.set(0.25)
        elif strength == "MEDIUM":
            self.progress.set(0.50)
        elif strength == "STRONG":
            self.progress.set(0.75)
        else:
            self.progress.set(1.0)

        terjemahan = {
            "WEAK": "LEMAH",
            "MEDIUM": "SEDANG",
            "STRONG": "KUAT",
            "VERY STRONG": "SANGAT KUAT"
        }

        self.strength_label.configure(
            text=f"Keamanan : {terjemahan.get(strength, strength)}"
        )

        top = ctk.CTkFrame(self.cards_frame)
        top.pack(fill="x", pady=10)

        card = ctk.CTkFrame(top)
        card.pack(side="left", padx=15, pady=10)

        ctk.CTkLabel(
            card,
            text="📏 Panjang Password",
            font=("Segoe UI", 18, "bold")
        ).pack(padx=30, pady=10)

        ctk.CTkLabel(
            card,
            text=str(data["length"]),
            font=("Segoe UI", 30)
        ).pack(pady=10)

        boolean_card = ctk.CTkFrame(self.cards_frame)
        boolean_card.pack(fill="x", pady=10)

        ctk.CTkLabel(
            boolean_card,
            text="🔐 Komposisi Password",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=10)

        checks = [
            ("Huruf Kapital", data["upper"]),
            ("Huruf Kecil", data["lower"]),
            ("Angka", data["digit"]),
            ("Karakter Khusus", data["symbol"])
        ]

        for nama, nilai in checks:
            txt = f"✅ {nama}" if nilai else f"❌ {nama}"
            ctk.CTkLabel(boolean_card, text=txt,
                         font=("Segoe UI", 16)).pack(anchor="w", padx=20)

        brute = ctk.CTkFrame(self.cards_frame)
        brute.pack(fill="x", pady=10)

        ctk.CTkLabel(
            brute,
            text="⏱ Estimasi Waktu Pembobolan",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=10)

        ctk.CTkLabel(
            brute,
            text=f"{data['years']:,.2f} Tahun",
            font=("Segoe UI", 18)
        ).pack(pady=10)

    def show_generator(self):
        self.clear_frame()

        ctk.CTkLabel(self.main_frame, text="Generator Password",
                     font=("Segoe UI", 30, "bold")).pack(pady=20)

        self.length_label = ctk.CTkLabel(self.main_frame, text="Panjang : 16")
        self.length_label.pack()

        self.length_slider = ctk.CTkSlider(self.main_frame, from_=8, to=32)
        self.length_slider.set(16)
        self.length_slider.pack(fill="x", padx=50, pady=20)

        self.length_slider.configure(
            command=lambda v: self.length_label.configure(text=f"Panjang : {int(v)}")
        )

        ctk.CTkButton(
            self.main_frame,
            text="Buat Password",
            command=self.generate
        ).pack(pady=15)

        self.generated_box = ctk.CTkTextbox(self.main_frame, width=800, height=120)
        self.generated_box.pack(pady=20)

    def generate(self):
        password = generate_password(int(self.length_slider.get()))
        self.generated_box.delete("1.0", "end")
        self.generated_box.insert("end", password)

    def show_history(self):
        self.clear_frame()

        ctk.CTkLabel(self.main_frame, text="Riwayat Password",
                     font=("Segoe UI", 30, "bold")).pack(pady=20)

        history_box = ctk.CTkTextbox(self.main_frame, width=1000, height=500)
        history_box.pack(pady=20)

        for row in get_history():
            history_box.insert("end", f"{row[0]} | {row[1]}\n")


if __name__ == "__main__":
    app = PasswordAnalyzerApp()
    app.mainloop()
