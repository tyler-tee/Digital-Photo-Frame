from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.animation import Animation
import os


class SwipeImage(Image):

    def on_touch_move(self, touch):
        """
        Detect if the user is swiping left or right and load the next or previous image
        accordingly.
        """

        if touch.dx < -40:  # Swipe Left
            app = App.get_running_app()
            app.load_next_image(force=True)

        elif touch.dx > 40:  # Swipe Right
            app = App.get_running_app()
            app.load_previous_image()

        return super(SwipeImage, self).on_touch_move(touch)


class PhotoFrameApp(App):

    def build(self):
        """Setup our Kivy app and return the root widget.

        Raises:
            Exception: If no images are found in the photos directory.

        Returns:
            Root widget of the Kivy app.
        """

        self.index = 0
        photos_path = os.path.join(os.path.dirname(__file__), '../photos')
        self.images = self.load_images(photos_path)

        if not self.images:
            raise Exception("No images found in the directory.")

        self.image_widget = SwipeImage(source=self.images[self.index], allow_stretch=True,
                                       keep_ratio=True, opacity=1)

        layout = BoxLayout()
        layout.add_widget(self.image_widget)

        Clock.schedule_interval(self.update_image, 15)

        return layout

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
        return [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg') or f.endswith('.png')]


if __name__ == '__main__':
    PhotoFrameApp().run()
