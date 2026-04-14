import customtkinter as ctk
from PIL import Image, ImageTk
import cv2


class GripperGUI:
    def __init__(self, serial_controller, hand_tracker):
        self.serial = serial_controller
        self.tracker = hand_tracker
        self.cap = None
        self.running = False
        self.gesture_enabled = True

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("Robot Gripper — Hand Gesture Control")
        self.root.geometry("1100x700")
        self.root.minsize(900, 600)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        self._build_ui()

    def _build_ui(self):
        self.root.grid_columnconfigure(0, weight=3)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # --- Left: Camera Feed ---
        left = ctk.CTkFrame(self.root)
        left.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        left.grid_rowconfigure(0, weight=1)
        left.grid_columnconfigure(0, weight=1)

        self.camera_label = ctk.CTkLabel(left, text="Camera feed will appear here", font=("Arial", 16))
        self.camera_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # --- Right: Controls ---
        right = ctk.CTkFrame(self.root, width=300)
        right.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Connection section
        conn_label = ctk.CTkLabel(right, text="Connection", font=("Arial", 18, "bold"))
        conn_label.pack(pady=(15, 5))

        self.port_var = ctk.StringVar(value="Auto-detect")
        self.port_menu = ctk.CTkOptionMenu(right, variable=self.port_var, values=["Auto-detect"], width=220)
        self.port_menu.pack(pady=5)

        self.refresh_btn = ctk.CTkButton(right, text="Refresh Ports", command=self._refresh_ports, width=220)
        self.refresh_btn.pack(pady=5)

        self.connect_btn = ctk.CTkButton(right, text="Connect", command=self._toggle_connection, width=220,
                                         fg_color="green", hover_color="darkgreen")
        self.connect_btn.pack(pady=5)

        self.conn_status = ctk.CTkLabel(right, text="Disconnected", text_color="red", font=("Arial", 13))
        self.conn_status.pack(pady=(0, 10))

        # Servo section
        sep1 = ctk.CTkFrame(right, height=2, fg_color="gray50")
        sep1.pack(fill="x", padx=15, pady=5)

        servo_label = ctk.CTkLabel(right, text="Servo Control", font=("Arial", 18, "bold"))
        servo_label.pack(pady=(10, 5))

        self.angle_display = ctk.CTkLabel(right, text="Angle: 90°", font=("Arial", 28, "bold"))
        self.angle_display.pack(pady=5)

        self.angle_slider = ctk.CTkSlider(right, from_=0, to=180, number_of_steps=180,
                                          command=self._on_slider_change, width=220)
        self.angle_slider.set(90)
        self.angle_slider.pack(pady=5)

        slider_labels = ctk.CTkFrame(right, fg_color="transparent")
        slider_labels.pack(fill="x", padx=40)
        ctk.CTkLabel(slider_labels, text="0", font=("Arial", 11)).pack(side="left")
        ctk.CTkLabel(slider_labels, text="180", font=("Arial", 11)).pack(side="right")

        # Gesture toggle
        sep2 = ctk.CTkFrame(right, height=2, fg_color="gray50")
        sep2.pack(fill="x", padx=15, pady=10)

        self.gesture_switch = ctk.CTkSwitch(right, text="Hand Gesture Control",
                                            command=self._toggle_gesture, width=220)
        self.gesture_switch.select()
        self.gesture_switch.pack(pady=5)

        # Hand status
        self.hand_status = ctk.CTkLabel(right, text="No hand detected", font=("Arial", 13), text_color="gray")
        self.hand_status.pack(pady=5)

        # Openness bar
        self.openness_bar = ctk.CTkProgressBar(right, width=220)
        self.openness_bar.set(0)
        self.openness_bar.pack(pady=5)

        openness_labels = ctk.CTkFrame(right, fg_color="transparent")
        openness_labels.pack(fill="x", padx=40)
        ctk.CTkLabel(openness_labels, text="Closed", font=("Arial", 11)).pack(side="left")
        ctk.CTkLabel(openness_labels, text="Open", font=("Arial", 11)).pack(side="right")

        # Angle range config
        sep3 = ctk.CTkFrame(right, height=2, fg_color="gray50")
        sep3.pack(fill="x", padx=15, pady=10)

        range_label = ctk.CTkLabel(right, text="Angle Range", font=("Arial", 14, "bold"))
        range_label.pack(pady=(5, 2))

        open_frame = ctk.CTkFrame(right, fg_color="transparent")
        open_frame.pack(fill="x", padx=30, pady=2)
        ctk.CTkLabel(open_frame, text="Open:", width=50).pack(side="left")
        self.open_angle_entry = ctk.CTkEntry(open_frame, width=60)
        self.open_angle_entry.insert(0, "10")
        self.open_angle_entry.pack(side="right")

        close_frame = ctk.CTkFrame(right, fg_color="transparent")
        close_frame.pack(fill="x", padx=30, pady=2)
        ctk.CTkLabel(close_frame, text="Close:", width=50).pack(side="left")
        self.close_angle_entry = ctk.CTkEntry(close_frame, width=60)
        self.close_angle_entry.insert(0, "170")
        self.close_angle_entry.pack(side="right")

        # Bottom status bar
        self.status_bar = ctk.CTkLabel(self.root, text="Ready", font=("Arial", 12), anchor="w")
        self.status_bar.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 5), sticky="ew")

    def _refresh_ports(self):
        ports = self.serial.list_ports()
        port_names = ["Auto-detect"] + [f"{dev} — {desc}" for dev, desc in ports]
        self.port_menu.configure(values=port_names)
        self.status_bar.configure(text=f"Found {len(ports)} port(s)")

    def _toggle_connection(self):
        if self.serial.connected:
            self.serial.disconnect()
            self.connect_btn.configure(text="Connect", fg_color="green", hover_color="darkgreen")
            self.conn_status.configure(text="Disconnected", text_color="red")
            self.status_bar.configure(text="Disconnected")
        else:
            try:
                selected = self.port_var.get()
                port = None if selected == "Auto-detect" else selected.split(" — ")[0]
                connected_port = self.serial.connect(port)
                self.connect_btn.configure(text="Disconnect", fg_color="red", hover_color="darkred")
                self.conn_status.configure(text=f"Connected: {connected_port}", text_color="green")
                self.status_bar.configure(text=f"Connected to {connected_port}")
            except ConnectionError as e:
                self.conn_status.configure(text="Connection failed", text_color="red")
                self.status_bar.configure(text=str(e))

    def _toggle_gesture(self):
        self.gesture_enabled = self.gesture_switch.get() == 1

    def _on_slider_change(self, value):
        angle = int(value)
        self.angle_display.configure(text=f"Angle: {angle}°")
        if not self.gesture_enabled:
            self.serial.send_angle(angle)

    def _get_angle_range(self):
        try:
            open_a = int(self.open_angle_entry.get())
            close_a = int(self.close_angle_entry.get())
            return max(0, min(180, open_a)), max(0, min(180, close_a))
        except ValueError:
            return 10, 170

    def _update_frame(self):
        if not self.running:
            return

        ret, frame = self.cap.read()
        if not ret:
            self.root.after(30, self._update_frame)
            return

        frame = cv2.flip(frame, 1)
        frame, openness = self.tracker.process_frame(frame)

        if openness is not None:
            self.hand_status.configure(text="Hand detected", text_color="green")
            self.openness_bar.set(openness)

            if self.gesture_enabled:
                open_a, close_a = self._get_angle_range()
                angle = self.tracker.openness_to_angle(openness, open_a, close_a)
                if angle is not None:
                    self.angle_display.configure(text=f"Angle: {angle}°")
                    self.angle_slider.set(angle)
                    self.serial.send_angle(angle)
        else:
            self.hand_status.configure(text="No hand detected", text_color="gray")

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)

        label_w = self.camera_label.winfo_width()
        label_h = self.camera_label.winfo_height()
        if label_w > 10 and label_h > 10:
            img_w, img_h = img.size
            scale = min(label_w / img_w, label_h / img_h)
            new_w, new_h = int(img_w * scale), int(img_h * scale)
            img = img.resize((new_w, new_h), Image.LANCZOS)

        photo = ImageTk.PhotoImage(img)
        self.camera_label.configure(image=photo, text="")
        self.camera_label._image = photo  # prevent garbage collection

        self.root.after(16, self._update_frame)  # ~60fps

    def start(self):
        """Open camera and start the main GUI loop."""
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.status_bar.configure(text="ERROR: Cannot open camera")
            self.root.mainloop()
            return

        self.running = True
        self.status_bar.configure(text="Camera active — show your hand to control gripper")
        self._refresh_ports()
        self.root.after(100, self._update_frame)
        self.root.mainloop()

    def _on_close(self):
        """Clean shutdown."""
        self.running = False
        if self.cap:
            self.cap.release()
        self.tracker.release()
        self.serial.disconnect()
        self.root.destroy()
