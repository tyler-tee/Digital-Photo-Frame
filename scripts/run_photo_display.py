from datetime import datetime
import json
import logging
import os
import requests
from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from sync_photos import sync_photos

# Setup logging
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')


class TapImage(Image):

    def __init__(self, **kwargs):
        super(TapImage, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        if touch.x < self.width / 2:  # Touched on the left side
            app = App.get_running_app()
            app.load_previous_image()
        else:  # Touched on the right side
            app = App.get_running_app()
            app.load_next_image(force=True)
        return super(TapImage, self).on_touch_down(touch)


class PhotoFrameApp(App):

    def build(self):
        """Setup our Kivy app and return the root widget.

        Raises:
            Exception: If no images are found in the photos directory.

        Returns:
            Root widget of the Kivy app.
        """

        self.image_cache = {}  # Cache of images and their last modified time
        self.local_config = self.load_config()  # Load our local configuration
        self.apply_settings()  # Configure Kivy with defined settings
        self.index = 0
        photos_path = os.path.join(os.path.dirname(__file__), '../photos')
        self.images = self.load_images(photos_path)

        if not self.images:
            raise Exception("No images found in the directory.")

        self.image_widget = TapImage(source=self.images[self.index], allow_stretch=True,
                                     keep_ratio=True, opacity=1)

        layout = FloatLayout()

        layout.add_widget(self.image_widget)
        Clock.schedule_interval(self.update_image, 15)  # Cycle images every 15 seconds

        # Schedule the check for new images every hour (3600 seconds)
        Clock.schedule_interval(self.check_for_new_images, 3600)

        # Build our weather widget
        self.weather_label = Label(
            text=self.fetch_weather_data(),
            font_size='15sp',
            color=[1, 1, 1, 1],  # White color
            size_hint=(None, None),
            pos_hint={'x': 0.06, 'y': 0.08},  # Adjust 'top' value as needed
            halign='left'
        )
        layout.add_widget(self.weather_label)
        Clock.schedule_interval(self.update_weather, 3600)  # Update weather every hour

        # Build our clock widget
        self.clock_label = Label(
            text=self.get_current_time(),
            font_size='60sp',
            color=[1, 1, 1, 1],  # White color
            size_hint=(None, None),
            pos_hint={'x': 0.06, 'y': 0.01},
            halign='left'
        )
        layout.add_widget(self.clock_label)
        Clock.schedule_interval(self.update_clock, 60)  # Update clock every minute

        # Build our refresh widget
        button_path = os.path.join(os.path.dirname(__file__), 'assets')
        refresh_button = os.path.join(button_path, 'refresh_icon.png')
        self.refresh_button = Button(
            background_normal=refresh_button,
            size_hint=(None, None),
            size=(50, 50),
            opacity=0.7
        )
        self.refresh_button.bind(on_press=self.check_for_new_images)

        # Create and add the new power-off button
        power_button = Button(
            background_normal=os.path.join(button_path, 'power_icon.png'),
            size_hint=(None, None),
            size=(50, 50),
            opacity=0.7
        )
        power_button.bind(on_press=self.power_off)

        # Create a vertical layout for buttons
        button_layout = BoxLayout(size_hint=(None, None), size=(50, 100),
                                  pos_hint={'right': 0.98, 'y': 0.03},
                                  orientation='vertical', spacing=10)

        # Add buttons to the layout
        button_layout.add_widget(self.refresh_button)
        button_layout.add_widget(power_button)

        # Add the button layout to the main layout
        layout.add_widget(button_layout)

        return layout

    def load_config(self):
        # Get the path to our config file
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')

        with open(config_path) as config_file:
            config = json.load(config_file)

        return config

    def apply_settings(self):
        """
        Configure Kivy to run in borderless fullscreen mode.
        """
        Config.set('graphics', 'fullscreen', 'auto')
        Config.set('graphics', 'borderless', True)
        Config.write()

        Window.show_cursor = False

    def power_off(self, instance):
        """
        Safely shut down the Raspberry Pi.
        """
        logging.info("Shutting down...")
        os.system('sudo shutdown now')

    def fetch_weather_data(self) -> str:
        """
        Fetch weather data from the OpenWeatherMap API.

        Returns:
            str: Weather data formatted as "temperature | weather".
        """
        api_key, location = self.local_config['weather_api_key'], self.local_config['weather_location']

        url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=imperial'

        try:
            response = requests.get(url)
            data = response.json()
            temperature = round(data['main']['temp'])
            weather = data['weather'][0]['description'].title()
            return f"{temperature}°F | {weather}"
        except Exception as e:
            logging.error("Error fetching weather data: %s", e)
            return "N/A"

    def get_current_time(self):
        return datetime.now().strftime('%H:%M')

    def update_clock(self, dt):
        self.clock_label.text = self.get_current_time()

    def update_weather(self, dt):
        self.weather_label.text = self.fetch_weather_data()

    def check_for_new_images(self, dt):
        """
        Check for new images in the photos directory and reload the images if new images are found.
        """
        try:
            sync_photos(self.local_config['local_folder'], self.local_config['album_id'])
        except Exception as e:
            logging.error("Error syncing photos:", e)

        new_images = self.load_images(os.path.join(os.path.dirname(__file__), '../photos'))
        if new_images != self.images:
            self.images = new_images
            self.load_next_image(force=True)

    def update_image(self, dt=None):
        """
        Update the image being displayed by fading the current image out and vice versa.
        """

        anim = Animation(opacity=0, duration=1.5)
        anim.bind(on_complete=self.load_next_image)
        anim.start(self.image_widget)

    def load_next_image(self, animation=None, widget=None, force=False):
        """
        Load the next image in the list and fade it in.
        """
        if (animation and widget) or force:
            self.index = (self.index + 1) % len(self.images)
            self.image_widget.source = self.images[self.index]
            anim = Animation(opacity=1, duration=1.5)
            anim.start(self.image_widget)

    def load_previous_image(self):
        """
        Load the previous image in the list and fade it in.
        """
        self.index = (self.index - 1) % len(self.images)
        self.image_widget.source = self.images[self.index]
        anim = Animation(opacity=1, duration=1.5)
        anim.start(self.image_widget)

    def load_images(self, path: str):
        """
        Load all images in the given path.

        Args:
            path (str): Path to our photos directory.

        Returns:
            List: List of images in our photos directory.
        """
        new_images = []
        for file in os.scandir(path):
            if file.is_file() and (file.name.endswith('.jpg') or file.name.endswith('.png')):
                full_path = os.path.join(path, file.name)
                mod_time = os.path.getmtime(full_path)

                # Check if this file is new or has been modified since last load
                if full_path not in self.image_cache or self.image_cache[full_path] < mod_time:
                    new_images.append(full_path)
                    self.image_cache[full_path] = mod_time

        return new_images


if __name__ == '__main__':
    PhotoFrameApp().run()
