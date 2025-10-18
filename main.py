import cv2
import numpy as np
import tensorflow as tf
import os
from datetime import datetime

from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

CAPTURES_FOLDER = "/storage/emulated/0/DentalCaptures"
os.makedirs(CAPTURES_FOLDER, exist_ok=True)
print(f"📁 Captures folder: {CAPTURES_FOLDER}")

MODEL_PATH = "/storage/emulated/0/pydroidapk/oral/yolov8_640_float32.tflite"

try:
    interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    print("✅ Model loaded successfully")
except Exception as e:
    print(f"❌ Model loading error: {e}")
    interpreter = None

CLASS_NAMES = [
    "Normal",
    "Initial Caries",
    "Moderate Caries",
    "Severe Caries",
    "Tooth Stain",
    "Dental Calculus",
    "Other Lesions"
]

class KivyCamera(Image):
    def __init__(self, camera_port=0, fps=30, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.camera_port = camera_port
        self.capture = None
        self.current_frame = None
        self.detection_enabled = True
        self.flip_horizontal = (camera_port == 1)
        self._opening = False

        Clock.schedule_once(lambda dt: self.initialize_camera(camera_port), 0.1)
        Clock.schedule_interval(self.update, 1.0 / fps)

    def initialize_camera(self, camera_port):
        if self._opening:
            return
        self._opening = True

        if self.capture:
            try:
                self.capture.release()
            except:
                pass
            self.capture = None

        Clock.schedule_once(lambda dt: self._open_camera(camera_port), 0.15)

    def _open_camera(self, camera_port):
        self.camera_port = camera_port
        self.flip_horizontal = (camera_port == 1)
        self._opening = False

        try:
            self.capture = cv2.VideoCapture(camera_port, cv2.CAP_ANDROID)
        except Exception:
            self.capture = cv2.VideoCapture(camera_port)

        if not (self.capture and self.capture.isOpened()):
            try:
                self.capture = cv2.VideoCapture(camera_port)
            except Exception:
                self.capture = None

        if self.capture and self.capture.isOpened():
            self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            print(f"✅ Camera {camera_port} initialized (flip_horizontal={self.flip_horizontal})")
        else:
            print(f"❌ Camera {camera_port} failed to open")
            self.capture = None

    def preprocess(self, frame):
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resized = cv2.resize(img_rgb, (640, 640)).astype(np.float32)
        input_tensor = np.expand_dims(resized, axis=0) / 255.0
        return input_tensor

    def detect_tflite(self, frame):
        if interpreter is None:
            return frame

        try:
            input_tensor = self.preprocess(frame)
            interpreter.set_tensor(input_details[0]['index'], input_tensor)
            interpreter.invoke()
            output = interpreter.get_tensor(output_details[0]['index'])[0]

            h, w, _ = frame.shape
            for det in output:
                x1, y1, x2, y2, score, class_id = det
                if score < 0.25:
                    continue

                x1, y1, x2, y2 = int(x1 * w), int(y1 * h), int(x2 * w), int(y2 * h)
                class_idx = int(class_id)

                if class_idx < len(CLASS_NAMES):
                    label = f"{CLASS_NAMES[class_idx]}: {score:.2f}"
                else:
                    label = f"Class {class_idx}: {score:.2f}"

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX,
                            0.7, (255, 0, 0), 2)

        except Exception as e:
            print(f"❌ Detection error: {e}")

        return frame

    def update(self, dt):
        if not self.capture or not self.capture.isOpened():
            return

        ret, frame = self.capture.read()
        if not ret or frame is None:
            return

        if self.flip_horizontal:
            frame = cv2.flip(frame, 1)
            frame = cv2.flip(frame, 0)

        self.current_frame = frame.copy()

        if self.detection_enabled:
            display_frame = self.detect_tflite(frame.copy())
        else:
            display_frame = frame

        frame_rgb = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
        buf = frame_rgb.tobytes()
        texture = Texture.create(size=(frame_rgb.shape[1], frame_rgb.shape[0]), colorfmt='rgb')
        texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        self.texture = texture

    def capture_image(self):
        if self.current_frame is not None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"dental_{timestamp}.jpg"
            filepath = os.path.join(CAPTURES_FOLDER, filename)

            frame_to_save = (
                self.detect_tflite(self.current_frame.copy())
                if self.detection_enabled else self.current_frame
            )

            try:
                cv2.imwrite(filepath, frame_to_save)
                print(f"✅ Image saved: {filepath}")
                return filepath
            except Exception as e:
                print(f"❌ Save error: {e}")
                return None
        return None


class CameraSelectionPopup(Popup):
    def __init__(self, callback, **kwargs):
        super().__init__(**kwargs)
        self.callback = callback
        self.title = "Choose Camera"
        self.size_hint = (0.8, 0.3)

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(Label(text="Select camera to use:", size_hint=(1, 0.4)))

        button_layout = BoxLayout(spacing=10, size_hint=(1, 0.6))

        back_btn = Button(text="📷 Back Camera (0)", font_size='18sp')
        back_btn.bind(on_press=lambda x: self.select_camera(0))
        button_layout.add_widget(back_btn)

        front_btn = Button(text="🤳 Front Camera (1)", font_size='18sp')
        front_btn.bind(on_press=lambda x: self.select_camera(1))
        button_layout.add_widget(front_btn)

        layout.add_widget(button_layout)
        self.content = layout

    def select_camera(self, camera_index):
        self.callback(camera_index)
        self.dismiss()


class GalleryPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "📸 Captured Images"
        self.size_hint = (0.95, 0.9)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        scroll = ScrollView()
        self.image_grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.image_grid.bind(minimum_height=self.image_grid.setter('height'))
        self.load_images()

        scroll.add_widget(self.image_grid)
        layout.add_widget(scroll)

        close_btn = Button(text="Close", size_hint=(1, 0.1), font_size='18sp')
        close_btn.bind(on_press=self.dismiss)
        layout.add_widget(close_btn)
        self.content = layout

    def load_images(self):
        self.image_grid.clear_widgets()

        if not os.path.exists(CAPTURES_FOLDER):
            self.image_grid.add_widget(Label(text="No images captured yet", size_hint_y=None, height=50))
            return

        images = sorted([f for f in os.listdir(CAPTURES_FOLDER) if f.endswith('.jpg')], reverse=True)
        if not images:
            self.image_grid.add_widget(Label(text="No images captured yet", size_hint_y=None, height=50))
            return

        for img_name in images:
            img_path = os.path.join(CAPTURES_FOLDER, img_name)
            item_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=80, spacing=10)
            info_label = Label(text=img_name, size_hint_x=0.5)
            item_layout.add_widget(info_label)

            delete_btn = Button(text="🗑️ Delete", size_hint_x=0.25, font_size='16sp')
            delete_btn.bind(on_press=lambda x, path=img_path, name=img_name: self.delete_image(path, name))
            item_layout.add_widget(delete_btn)
            self.image_grid.add_widget(item_layout)

    def delete_image(self, filepath, filename):
        try:
            os.remove(filepath)
            print(f"✅ Deleted: {filename}")
            self.load_images()
        except Exception as e:
            print(f"❌ Delete error: {e}")


class DentalDetectionApp(App):
    def build(self):
        Window.fullscreen = 'auto'
        self.camera_widget = None
        self.selected_camera = None

        self.main_layout = BoxLayout(orientation='vertical')
        self.placeholder = Label(text="Initializing...", font_size='20sp')
        self.main_layout.add_widget(self.placeholder)
        Clock.schedule_once(lambda dt: self.show_camera_selection(), 0.5)
        return self.main_layout

    def show_camera_selection(self):
        popup = CameraSelectionPopup(callback=self.on_camera_selected)
        popup.open()

    def on_camera_selected(self, camera_index):
        self.selected_camera = camera_index
        self.main_layout.clear_widgets()
        self.camera_widget = KivyCamera(camera_port=camera_index, fps=30)
        self.main_layout.add_widget(self.camera_widget)

        bottom_layout = BoxLayout(size_hint=(1, 0.08), spacing=5, padding=[5, 5, 5, 5])

        toggle_btn = Button(text="🤖 AI", font_size='16sp')
        toggle_btn.bind(on_press=self.toggle_detection)
        bottom_layout.add_widget(toggle_btn)

        capture_btn = Button(text="📸 Capture", font_size='16sp')
        capture_btn.bind(on_press=self.capture_image)
        bottom_layout.add_widget(capture_btn)

        gallery_btn = Button(text="🖼️ Gallery", font_size='16sp')
        gallery_btn.bind(on_press=self.show_gallery)
        bottom_layout.add_widget(gallery_btn)

        switch_btn = Button(text="🔄 Switch", font_size='16sp')
        switch_btn.bind(on_press=self.switch_camera)
        bottom_layout.add_widget(switch_btn)

        self.main_layout.add_widget(bottom_layout)

    def toggle_detection(self, instance):
        if self.camera_widget:
            self.camera_widget.detection_enabled = not self.camera_widget.detection_enabled
            status = "ON" if self.camera_widget.detection_enabled else "OFF"
            instance.text = f"🤖 AI: {status}"
            print(f"Detection: {status}")

    def capture_image(self, instance):
        if self.camera_widget:
            filepath = self.camera_widget.capture_image()
            if filepath:
                popup = Popup(
                    title="✅ Image Saved",
                    content=Label(text=f"Saved:\n{os.path.basename(filepath)}"),
                    size_hint=(0.8, 0.3)
                )
                popup.open()
                Clock.schedule_once(lambda dt: popup.dismiss(), 2)

    def show_gallery(self, instance):
        gallery = GalleryPopup()
        gallery.open()

    def switch_camera(self, instance):
        if self.camera_widget:
            new_camera = 1 if self.selected_camera == 0 else 0
            print(f"🔄 Switching from camera {self.selected_camera} to camera {new_camera}")
            self.selected_camera = new_camera
            self.camera_widget.initialize_camera(new_camera)

    def on_stop(self):
        if self.camera_widget and self.camera_widget.capture:
            self.camera_widget.capture.release()
            print("✅ Camera released")


if __name__ == '__main__':
    DentalDetectionApp().run()
