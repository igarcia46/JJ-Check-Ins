import cv2
import customtkinter as ctk

from PIL import Image

from services.camera_service import CameraService
from services.check_in_service import CheckInService
from services.photo_service import PhotoService
from repositories.excel_repository import ExcelRepository


class MainWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Jonathan Jennings Visitor Check-In")
        self.geometry("1000x1000")
        self.current_screen = "welcome"

        self.repository = ExcelRepository("data/check_ins.xlsx")
        self.check_in_service = CheckInService(self.repository)
        self.photo_service = PhotoService("data/photos")
        self.camera_service = CameraService()

        self.captured_photo = None
        self.camera_running = False

        self.current_frame = None

        self.inactivity_timer = None
        self.inactivity_timeout = 20_000  # 2 minutes

        self.bind_all("<KeyPress>", self._reset_inactivity_timer)
        self.bind_all("<Button>", self._reset_inactivity_timer)
        self.bind_all("<Motion>", self._reset_inactivity_timer)

        self._create_screens()
        self._show_welcome_screen()
        self._reset_inactivity_timer()

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    # -------------------------
    # Screen Setup
    # -------------------------

    def _create_screens(self):
        self.welcome_screen = ctk.CTkFrame(self)
        self.form_screen = ctk.CTkFrame(self)
        self.photo_screen = ctk.CTkFrame(self)
        self.success_screen = ctk.CTkFrame(self)

        self._build_welcome_screen()
        self._build_form_screen()
        self._build_photo_screen()
        self._build_success_screen()

    def _hide_all_screens(self):
        self.welcome_screen.pack_forget()
        self.form_screen.pack_forget()
        self.photo_screen.pack_forget()
        self.success_screen.pack_forget()

    # -------------------------
    # Welcome Screen
    # -------------------------

    def _build_welcome_screen(self):
        title = ctk.CTkLabel(
            self.welcome_screen,
            text="Welcome",
            font=ctk.CTkFont(size=42, weight="bold"),
        )
        title.pack(pady=(180, 20))

        subtitle = ctk.CTkLabel(
            self.welcome_screen,
            text="Please check in before continuing.",
            font=ctk.CTkFont(size=20),
        )
        subtitle.pack(pady=10)

        start_button = ctk.CTkButton(
            self.welcome_screen,
            text="Start Check-In",
            height=55,
            width=250,
            command=self._show_form_screen,
        )
        start_button.pack(pady=40)

    def _show_welcome_screen(self):
        self.current_screen = "welcome"
        self._hide_all_screens()

        self.welcome_screen.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20,
        )

    # -------------------------
    # Form Screen
    # -------------------------

    def _build_form_screen(self):
        self.form_back_button = ctk.CTkButton(
            self.form_screen,
            text="←\nBack",
            width=70,
            height=65,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="transparent",
            text_color="#E53935",
            hover_color="#3a3a3a",
            command=self._back_to_welcome,
        )

        self.form_back_button.place(
            x=25,
            y=20,
        )

        title = ctk.CTkLabel(
            self.form_screen,
            text="Visitor Information",
            font=ctk.CTkFont(size=34, weight="bold"),
        )
        title.pack(pady=(60, 30))

        name_label = ctk.CTkLabel(
            self.form_screen,
            text="Name",
            anchor="w",
        )

        name_label.pack(
            fill="x",
            padx=250,
        )

        self.name_entry = ctk.CTkEntry(
            self.form_screen,
            height=50,
            width=500,
        )

        self.name_entry.pack(
            pady=(5, 15),
        )

        self.email_entry = ctk.CTkEntry(
            self.form_screen,
            placeholder_text="Email",
            height=50,
            width=500,
        )
        self.email_entry.pack(pady=10)

        self.phone_entry = ctk.CTkEntry(
            self.form_screen,
            placeholder_text="Phone",
            height=50,
            width=500,
        )
        self.phone_entry.pack(pady=10)

        self.reason_entry = ctk.CTkEntry(
            self.form_screen,
            placeholder_text="Reason for Visit",
            height=50,
            width=500,
        )
        self.reason_entry.pack(pady=10)

        self.form_error_label = ctk.CTkLabel(
            self.form_screen,
            text="",
        )
        self.form_error_label.pack(pady=10)

        continue_button = ctk.CTkButton(
            self.form_screen,
            text="Continue",
            height=50,
            width=500,
            command=self._continue_to_photo,
        )
        continue_button.pack(pady=20)

    def _show_form_screen(self):
        self.current_screen = "form"
        self._hide_all_screens()

        self.form_error_label.configure(text="")

        self.form_screen.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20,
        )

        self.name_entry.focus()

    def _back_to_welcome(self):
        self._clear_form()
        self._show_welcome_screen()

    def _continue_to_photo(self):
        name = self.name_entry.get().strip()

        if not name:
            self.form_error_label.configure(
                text="Name is required."
            )
            return

        self._show_photo_screen()

    # -------------------------
    # Photo Screen
    # -------------------------

    def _build_photo_screen(self):
        title = ctk.CTkLabel(
            self.photo_screen,
            text="Take Your Photo",
            font=ctk.CTkFont(size=34, weight="bold"),
        )
        title.pack(pady=(30, 20))

        self.back_button = ctk.CTkButton(
            self.photo_screen,
            text="←\nBack",
            width=70,
            height=65,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="transparent",
            text_color="#E53935",
            hover_color="#3a3a3a",
            command=self._back_to_form,
        )

        self.back_button.place(
            x=25,
            y=20,
        )

        self.camera_label = ctk.CTkLabel(
            self.photo_screen,
            text="Starting camera...",
        )
        self.camera_label.pack(
            pady=(20, 20),
            
        )

        self.photo_button = ctk.CTkButton(
            self.photo_screen,
            text="Take Photo",
            height=50,
            width=400,
            command=self._handle_photo_button,
        )
        self.photo_button.pack(pady=(10, 5))

        self.submit_button = ctk.CTkButton(
            self.photo_screen,
            text="Submit",
            height=50,
            width=400,
            command=self._submit_check_in,
            state="disabled",
        )
        self.submit_button.pack(pady=(5, 10))

    def _show_photo_screen(self):
        self.current_screen = "photo"
        self._hide_all_screens()

        self.captured_photo = None

        self.photo_button.configure(
            text="Take Photo"
        )

        self.submit_button.configure(
            state="disabled",
            fg_color=["#3a7ebf", "#1f538d"],
        )

        self.photo_screen.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20,
        )

        self._start_camera()

    def _start_camera(self):
        try:
            self.camera_service.start()
            self.camera_running = True

            self._update_camera()

        except RuntimeError as error:
            self.camera_label.configure(
                text=str(error)
            )

    def _back_to_form(self):
        self._stop_camera()

        self.captured_photo = None
        self.current_frame = None

        self.camera_label.configure(
            image=None,
            text="Starting camera...",
        )

        self._show_form_screen()

    def _update_camera(self):
        if not self.camera_running:
            return

        try:
            frame = self.camera_service.get_frame()

            self.current_frame = frame

            if self.captured_photo is None:
                self._display_frame(frame)

        except RuntimeError as error:
            self.camera_label.configure(
                text=str(error)
            )

        self.after(15, self._update_camera)

    def _display_frame(self, frame):
        frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB,
        )

        image = Image.fromarray(frame)

        image.thumbnail((600, 420))

        camera_image = ctk.CTkImage(
            light_image=image,
            dark_image=image,
            size=image.size,
        )

        self.camera_label.configure(
            image=camera_image,
            text="",
        )

        self.camera_label.image = camera_image

    def _handle_photo_button(self):
        if self.captured_photo is None:
            self._take_photo()
        else:
            self._retake_photo()

    def _take_photo(self):
        try:
            self.captured_photo = self.camera_service.capture_photo()

            self._display_frame(
                self.captured_photo
            )

            self.photo_button.configure(
                text="Retake Photo"
            )

            self.submit_button.configure(
                state="normal",
                fg_color="#2E8B57",
                hover_color="#246B45",
            )

        except RuntimeError as error:
            self.camera_label.configure(
                text=str(error)
            )

    def _retake_photo(self):
        self.captured_photo = None

        self.photo_button.configure(
            text="Take Photo"
        )

        self.submit_button.configure(
            state="disabled",
            fg_color=["#3a7ebf", "#1f538d"],
        )

    # -------------------------
    # Submit
    # -------------------------

    def _submit_check_in(self):
        try:
            name = self.name_entry.get().strip()
            email = self.email_entry.get().strip()
            phone = self.phone_entry.get().strip()
            reason = self.reason_entry.get().strip()

            photo_path = self.photo_service.save_photo(
                name=name,
                image=self.captured_photo,
            )

            self.check_in_service.check_in(
                name=name,
                email=email or None,
                phone=phone or None,
                reason=reason or None,
                photo_path=photo_path,
            )

            self._stop_camera()

            self._show_success_screen(name)

        except Exception as error:
            self.camera_label.configure(
                text=f"Check-in failed: {error}"
            )

    # -------------------------
    # Success Screen
    # -------------------------

    def _build_success_screen(self):
        self.success_label = ctk.CTkLabel(
            self.success_screen,
            text="",
            font=ctk.CTkFont(size=36, weight="bold"),
        )
        self.success_label.pack(
            pady=(220, 20)
        )

        subtitle = ctk.CTkLabel(
            self.success_screen,
            text="You have been checked in.",
            font=ctk.CTkFont(size=20),
        )
        subtitle.pack(pady=10)

    def _show_success_screen(self, name):
        self.current_screen = "success"
        self._hide_all_screens()

        self.success_label.configure(
            text=f"Thank you, {name}!"
        )

        self.success_screen.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20,
        )

        self.after(
            3000,
            self._reset_app,
        )

    # -------------------------
    # Reset
    # -------------------------

    def _reset_app(self):
        self._stop_camera()

        self.captured_photo = None
        self.current_frame = None

        self._clear_form()

        self.camera_label.configure(
            image=None,
            text="Starting camera...",
        )

        self._show_welcome_screen()

    # -------------------------
    # Camera Cleanup
    # -------------------------

    def _stop_camera(self):
        self.camera_running = False
        self.camera_service.release()

    def _on_close(self):
        if self.inactivity_timer is not None:
            self.after_cancel(self.inactivity_timer)

        self._stop_camera()
        self.destroy()

    def _clear_form(self):
        self.name_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.phone_entry.delete(0, "end")
        self.reason_entry.delete(0, "end")

        self.form_error_label.configure(text="")

    def _handle_inactivity_timeout(self):
        self.inactivity_timer = None

        if self.current_screen != "welcome":
            self._stop_camera()

            self.captured_photo = None
            self.current_frame = None

            self._clear_form()

            self.camera_label.configure(
                image=None,
                text="Starting camera...",
            )

            self._show_welcome_screen()

        self._reset_inactivity_timer()

    def _reset_inactivity_timer(self, event=None):
        if self.inactivity_timer is not None:
            self.after_cancel(self.inactivity_timer)

        self.inactivity_timer = self.after(
            self.inactivity_timeout,
            self._handle_inactivity_timeout,
        )