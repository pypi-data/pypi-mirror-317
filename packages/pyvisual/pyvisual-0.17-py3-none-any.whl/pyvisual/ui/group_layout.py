import pyvisual as pv
from pyvisual.ui.basic_button import BasicButton
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.uix.boxlayout import BoxLayout


class GroupLayout:
    def __init__(self, window=None, x=0, y=0, orientation="horizontal", spacing=10,
                 padding=(10, 10, 10, 10), background_color=(1, 1, 1, 0),
                 radius=0, border_color=(1, 0, 0, 1), border_width=1):
        self.window = window
        self.orientation = orientation
        self.spacing = spacing
        self.padding = padding
        self.background_color = background_color
        self.radius = radius
        self.border_color = border_color
        self.border_width = border_width

        # Create the container layout using Kivy's BoxLayout
        self.layout = BoxLayout(
            orientation=self.orientation,
            spacing=self.spacing,
            padding=self.padding,
            size_hint=(None, None),
            pos=(x, y)
        )
        # Custom background and border
        with self.layout.canvas.before:
            if self.background_color:
                Color(*self.background_color)
                self.bg_rect = RoundedRectangle(size=self.layout.size, pos=self.layout.pos, radius=[self.radius])

            if self.border_color and self.border_width > 0:
                Color(*self.border_color)
                self.border_line = Line(rounded_rectangle=(x, y, self.layout.size[0], self.layout.size[1], self.radius), width=self.border_width)

        # Bind size updates

        # Add the layout to the window if a window is provided
        if self.window:
            self.window.add_widget(self.layout)
        self.layout.bind(size=self.update_background, pos=self.update_background)


    def add_widget(self, widget):
        """
        Add a widget to the GroupLayout.
        """
        if isinstance(widget, GroupLayout):
            self.layout.add_widget(widget.layout)  # Add nested layout
        else:
            my_widget = widget if isinstance(widget, BasicButton) else widget

            if my_widget.parent is not None:
                my_widget.parent.remove_widget(my_widget)
            self.layout.add_widget(my_widget)

        # Update layout size dynamically
        self.update_layout_size()

        self.update_background()

    def update_layout_size(self):
        """
        Calculate and adjust layout size based on children.
        """
        if len(self.layout.children) == 0:
            total_width = self.padding[0] + self.padding[2]
            total_height = self.padding[1] + self.padding[3]
        elif self.orientation == "horizontal":
            total_width = (
                    sum(child.width for child in self.layout.children) +
                    (len(self.layout.children) - 1) * self.spacing +
                    self.padding[0] + self.padding[2]
            )
            total_height = (
                    max(child.height for child in self.layout.children) +
                    self.padding[1] + self.padding[3]
            )
        else:  # Vertical orientation
            total_width = (
                    max(child.width for child in self.layout.children) +
                    self.padding[0] + self.padding[2]
            )
            total_height = (
                    sum(child.height for child in self.layout.children) +
                    (len(self.layout.children) - 1) * self.spacing +
                    self.padding[1] + self.padding[3]
            )

        # Adjust the position to grow downward if vertical
        if self.orientation == "vertical":
            self.layout.pos = (self.layout.pos[0], self.layout.pos[1] - (total_height - self.layout.height))

        self.layout.size = (total_width, total_height)

    def update_background(self, *args):
        """
        Update the background and border on size changes.
        """
        if self.background_color:
            self.bg_rect.size = self.layout.size
            self.bg_rect.pos = self.layout.pos
            self.bg_rect.radius = [self.radius]

        if self.border_color and self.border_width > 0:
            self.border_line.rounded_rectangle = (
                self.layout.x, self.layout.y, self.layout.width, self.layout.height, self.radius
            )


# Example Usage
if __name__ == "__main__":
    # Initialize the pyvisual window
    window = pv.Window(title="Nested GroupLayout Example")

    # Main Horizontal GroupLayout
    vertical_group = GroupLayout(
        window=window, x=50, y=200, orientation="vertical", spacing=20,
        padding=(30, 30, 30, 30), background_color=(0.9, 0.9, 0.9, 1),
        radius=5, border_color=(0.3, 0.3, 0.3, 1), border_width=0
    )

    # Left Vertical GroupLayout
    horizontal_1_group = GroupLayout(
        window=None, orientation="horizontal", spacing=10,
        padding=(10, 10, 10, 10), background_color=(0, 0.9, 1, 1),
        radius=5, border_color=(0, 0, 1, 1), border_width=0
    )

    # Add buttons to the left vertical group
    button1 = BasicButton(window=None, x=0, y=0, text="Left 1", font_size=16, width=120, height=40)
    button2 = BasicButton(window=None, x=0, y=0, text="Left 2", font_size=16, width=120, height=40)
    button3 = BasicButton(window=None, x=0, y=0, text="Left 1", font_size=16, width=120, height=40)
    button10 = BasicButton(window=None, x=0, y=0, text="Left 1", font_size=16, width=120, height=40)
    button12 = BasicButton(window=None, x=0, y=0, text="Left 1", font_size=16, width=120, height=40)

    horizontal_1_group.add_widget(button1)
    horizontal_1_group.add_widget(button2)
    horizontal_1_group.add_widget(button3)
    horizontal_1_group.add_widget(button10)
    horizontal_1_group.add_widget(button12)

    # Left Vertical GroupLayout
    horizontal_2_group = GroupLayout(
        window=None, orientation="horizontal", spacing=10,
        padding=(10, 10, 10, 10), background_color=(0.7, 0.9, 0, 1),
        radius=10, border_color=(0, 0, 1, 1), border_width=0
    )

    # Add buttons to the left vertical group
    button4 = BasicButton(window=None, x=0, y=0, text="Left 1", font_size=16, width=120, height=40)
    button5 = BasicButton(window=None, x=0, y=0, text="Left 2", font_size=16, width=120, height=40)
    button6 = BasicButton(window=None, x=0, y=0, text="Left 1", font_size=16, width=120, height=40)

    # Left Vertical GroupLayout
    horizontal_3_group = GroupLayout(
        window=None, orientation="vertical", spacing=10,
        padding=(10, 10, 10, 10), background_color=(0.7, 0.9, 0, 1),
        radius=10, border_color=(0, 0, 1, 1), border_width=0
    )

    # Add buttons to the left vertical group
    button40 = BasicButton(window=None, x=0, y=0, text="Left 1", font_size=16, width=120, height=40)
    button50 = BasicButton(window=None, x=0, y=0, text="Left 2", font_size=16, width=120, height=40)
    button60 = BasicButton(window=None, x=0, y=0, text="Left 1", font_size=16, width=120, height=40)

    horizontal_3_group.add_widget(button40)
    horizontal_3_group.add_widget(button50)
    horizontal_3_group.add_widget(button60)



    # Add vertical groups to the main horizontal group
    vertical_group.add_widget(horizontal_1_group)
    vertical_group.add_widget(horizontal_2_group)
    vertical_group.add_widget(horizontal_3_group)




    # Show the window
    window.show()
