import tkinter as tk

class ScreenSelectApp:
    def __init__(self, master):
        self.master = master
        self.master.title("屏幕选择")
        self.master.attributes("-fullscreen", True)
        self.master.attributes("-alpha", 0.3)
        self.master.configure(bg='black')

        self.label = tk.Label(master, text="请拖动鼠标选择区域", bg='black', fg='white')
        self.label.pack(pady=10)

        self.canvas = tk.Canvas(master, bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.rect = None
        self.start_x = None
        self.start_y = None

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def on_button_press(self, event):
        self.master.attributes("-fullscreen", True)
        self.master.attributes("-alpha", 0.3)
        self.start_x = event.x
        self.start_y = event.y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red', fill='white', stipple='gray50')

    def on_mouse_drag(self, event):
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_button_release(self, event):
        x1, y1, x2, y2 = self.canvas.coords(self.rect)
        self.label.config(text=f"选择区域: ({x1}, {y1}) - ({x2}, {y2})")
        self.master.attributes("-fullscreen", False)
        self.master.attributes("-alpha", 1.0)
        self.master.configure(bg='SystemButtonFace')


if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenSelectApp(root)
    root.mainloop()