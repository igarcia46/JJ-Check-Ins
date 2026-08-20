from pathlib import Path

import cv2
import customtkinter as ctk
from PIL import Image, ImageEnhance

from services.camera_service import CameraService
from services.check_in_service import CheckInService
from services.photo_service import PhotoService
from repositories.excel_repository import ExcelRepository

from utils.paths import (
    get_excel_path,
    get_photo_directory,
)


class MainWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Jonathan Jennings Visitor Check-In")
        icons_path = Path(__file__).resolve().parent.parent / "assets" / "icons"
        self.iconbitmap(str(icons_path / "JJ109PrimaryLogo.ico"))
        self.geometry("1000x1000")
        self.resizable(False, False)
        self.current_screen = "welcome"

        self.repository = ExcelRepository(
            get_excel_path()
        )
        self.check_in_service = CheckInService(self.repository)
        self.photo_service = PhotoService(
            get_photo_directory()
        )
        self.camera_service = CameraService()

        back_arrow_path = icons_path / "back-arrow.png"
        back_arrow = Image.open(back_arrow_path)
        self.back_arrow_image = ctk.CTkImage(
            light_image=back_arrow,
            dark_image=back_arrow,
            size=(46, 46),
        )

        welcome_background = Image.open(
            icons_path / "JJ109PrimaryLogo.webp"
        )
        welcome_background = ImageEnhance.Brightness(
            welcome_background
        ).enhance(0.35)
        background_scale = min(
            800 / welcome_background.width,
            800 / welcome_background.height,
        )
        background_size = (
            round(welcome_background.width * background_scale),
            round(welcome_background.height * background_scale),
        )
        self.welcome_background_image = ctk.CTkImage(
            light_image=welcome_background,
            dark_image=welcome_background,
            size=background_size,
        )

        self.captured_photo = None
        self.camera_running = False

        self.current_frame = None

        self.inactivity_timer = None
        self.inactivity_timeout = 90_000  # 1 minute 30 seconds

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
        self.welcome_background_label = ctk.CTkLabel(
            self.welcome_screen,
            text="",
            image=self.welcome_background_image,
        )
        self.welcome_background_label.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
        )

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
            text="",
            image=self.back_arrow_image,
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

        self.name_entry = ctk.CTkEntry(
            self.form_screen,
            placeholder_text="Name",
            height=50,
            width=500,
        )

        self.name_entry.pack(pady=10)

        self.phone_entry = ctk.CTkEntry(
            self.form_screen,
            placeholder_text="Phone",
            height=50,
            width=500,
        )
        self.phone_entry.pack(pady=10)

        # container for reason label + dropdown so they stay aligned with other inputs
        self.reason_container = ctk.CTkFrame(
            self.form_screen,
            width=500,
            fg_color="transparent",
        )
        self.reason_container.pack(pady=(10, 50))

        self.reason_label = ctk.CTkLabel(
            self.reason_container,
            text="Reason for visit",
            anchor="w",
        )
        self.reason_label.pack(fill="x")

        # create option menu and attempt to style the dropdown button separately
        self.reason_entry = ctk.CTkOptionMenu(
            self.reason_container,
            values=[
                "Observation/Observación",
                "Meeting/Reunión",
                "Lunch with student/Almuerzo con estudiante",
                "Volunteering/Voluntariado",
                "Tour/Recorrido escolar",
            ],
            width=500,
            height=50,
            corner_radius=8,
            fg_color=self.name_entry.cget("fg_color"),
            button_color="#3a7ebf",
            button_hover_color="#1f538d",
        )

        self.reason_entry.set("Observation/Observación")
        self.reason_entry.pack()

        self.form_error_label = ctk.CTkLabel(
            self.form_screen,
            text="",
            text_color="#E53935",
            font=ctk.CTkFont(weight="bold"),
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

        # Do not autofocus any input so user sees placeholders
        try:
            self.focus_set()
        except Exception:
            pass

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
            text="",
            image=self.back_arrow_image,
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
            phone = self.phone_entry.get().strip()
            reason = self.reason_entry.get().strip()

            photo_path = self.photo_service.save_photo(
                name=name,
                image=self.captured_photo,
            )

            self.check_in_service.check_in(
                name=name,
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
        self.phone_entry.delete(0, "end")
        try:
            self.reason_entry.set("Observation")
        except Exception:
            try:
                self.reason_entry.delete(0, "end")
            except Exception:
                pass

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
