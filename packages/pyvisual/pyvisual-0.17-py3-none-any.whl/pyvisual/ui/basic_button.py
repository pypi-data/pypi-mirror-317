from kivy.graphics import BoxShadow, Color, RoundedRectangle, Line
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.core.text import LabelBase
from kivy.core.window import Window as KivyWindow

class BasicButton(Widget):
    def __init__(self, window, x, y,
                 width=140, height=50, text="CLICK ME",
                 font="Roboto", font_size=16, font_color=(0, 0, 0, 1),
                 bold=False, italic=False, underline=False, strikethrough=False,
                 button_color=(0, 0.5, 0.5, 1), hover_opacity=0.7, clicked_opacity=0.5,
                 border_color=(1, 1, 0, 1), border_thickness=0, corner_radius=20,
                 shadow_color=(1, 1, 1, 0), shadow_offset=(0, 0),
                 blur_radius=0, spread_radius=(0, 0),
                 is_visible=True, is_disabled=False, disabled_opacity=0.3, opacity=1,
                 on_hover=None, on_click=None, on_release=None, tag=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)  # Explicitly disable size_hint

        self.window = window
        self.size = (width, height)
        self.pos = (x, y)
        self.text = text
        self.font = font
        self.font_size = font_size
        self.font_color = font_color
        self.bold = bold
        self.italic = italic
        self.underline = underline
        self.strikethrough = strikethrough
        self.button_color = button_color
        self.hover_opacity = hover_opacity
        self.clicked_opacity = clicked_opacity
        self.border_color = border_color
        self.border_thickness = border_thickness
        self.corner_radius = corner_radius
        self.on_click = on_click
        self.on_release = on_release
        self.on_hover = on_hover
        self.tag = tag
        self.is_pressed = False
        self.is_disabled = is_disabled
        self.disabled_opacity = disabled_opacity
        self.is_visible = is_visible
        self.shadow_color = shadow_color
        self.shadow_offset = shadow_offset
        self.blur_radius = blur_radius
        self.spread_radius = spread_radius
        self.border_radius = (corner_radius,corner_radius,corner_radius,corner_radius)

        # Apply markup to the text
        self.text = self.apply_markup(self.text)

        # Register font if provided
        if font.endswith((".ttf", ".otf")):
            LabelBase.register(name="CustomFont", fn_regular=font)
            self.font = "CustomFont"

        # Draw the border if thickness is greater than 0
        with self.canvas.before:

            # Draw shadow
            Color(*self.shadow_color)
            self.shadow = BoxShadow(
                pos=(self.pos[0] + self.shadow_offset[0], self.pos[1] + self.shadow_offset[1]),
                size=(self.size[0], self.size[1]),
                offset=self.shadow_offset,
                blur_radius=self.blur_radius,
                spread_radius=self.spread_radius,
                border_radius=self.border_radius
            )
            # Draw the rounded rectangle background
            self.bg_color = Color(*self.button_color)
            self.bg_color.a = opacity  # Apply initial opacity
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[self.corner_radius] * 4)

            # Update border if thickness > 0
            if self.border_thickness > 0:
                self.border_color_instruction = Color(*self.border_color)  # RGBA border color
                self.border_line = Line(
                    rounded_rectangle=(
                        self.pos[0] + self.border_thickness / 2,  # Shift inward
                        self.pos[1] + self.border_thickness / 2,  # Shift inward
                        self.size[0] - self.border_thickness,  # Reduce width
                        self.size[1] - self.border_thickness,  # Reduce height
                        self.corner_radius - self.border_thickness / 2  # Adjust corner radius
                    ),
                    width=self.border_thickness
                )





        # Add the button text as a label
        self.label = Label(
            text=self.text,
            font_name=self.font,
            font_size=self.font_size,
            color=self.font_color,
            size_hint=(None, None),
            size=self.size,
            pos=self.pos,
            halign="center",
            valign="middle",
            markup=True
        )


        if window:
            # Add to the provided pyvisual window
            self.add_widget(self.label)
            self.window.add_widget(self)
            print(self.window)

        self.set_visibility(self.is_visible)
        self.set_opacity(opacity)

        # Bind mouse position for hover detection
        KivyWindow.bind(mouse_pos=self.on_mouse_pos)
        self.label.bind(size=self._update_text, pos=self._update_text)

        # Bind position and size updates
        # self.bind(pos=self._update_canvas, size=self._update_canvas)

        # Bind the opacity property to update the canvas
        self.bind(opacity=self._on_opacity)


    def apply_markup(self, text):
        """Apply markup styles (bold, italic, underline, strikethrough) to text."""
        if self.strikethrough:
            text = f"[s]{text}[/s]"
        if self.underline:
            text = f"[u]{text}[/u]"
        if self.italic:
            text = f"[i]{text}[/i]"
        if self.bold:
            text = f"[b]{text}[/b]"
        return text

    def _update_text(self, *args):
        """Update the text alignment and position."""
        self.label.text_size = self.label.size
        self.label.pos = self.pos

    def _update_canvas(self, *args):
        """Update the rounded rectangle background position and size."""
        # Update shadow properties
        self.shadow.pos = (
            self.pos[0] + self.shadow_offset[0],
            self.pos[1] + self.shadow_offset[1]
        )
        self.shadow.size = self.size

        # Update button background
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

        # Update border if thickness > 0
        if self.border_thickness > 0:
            self.border_color_instruction = Color(*self.border_color)  # RGBA border color
            self.border_line = Line(
                rounded_rectangle=(
                    self.pos[0] + self.border_thickness / 2,  # Shift inward
                    self.pos[1] + self.border_thickness / 2,  # Shift inward
                    self.size[0] - self.border_thickness,  # Reduce width
                    self.size[1] - self.border_thickness,  # Reduce height
                    self.corner_radius - self.border_thickness / 2  # Adjust corner radius
                ),
                width=self.border_thickness
            )

        # Center the label within the button
        self.label.pos = (
            self.pos[0] + (self.size[0] - self.label.size[0]) / 2,
            self.pos[1] + (self.size[1] - self.label.size[1]) / 2,
        )
        self.label.size = self.size


    def _on_opacity(self, instance, value):
        """Update the canvas opacity when the widget's opacity changes."""
        self.bg_color.a = value

    def on_mouse_pos(self, window, pos):
        """Handle mouse hover events."""
        if not self.is_disabled:
            if self.collide_point(*pos):
                if not self.is_pressed:
                    self.bg_color.a = self.hover_opacity  # Set hover opacity
                    if self.on_hover:
                        self.on_hover(self)
            else:
                self.bg_color.a = self.opacity  # Reset to idle state if not hovering

    def on_touch_down(self, touch):
        """Handle mouse click events."""
        if self.collide_point(*touch.pos):
            if not self.is_disabled:
                self.is_pressed = True
                self.bg_color.a = self.clicked_opacity  # Set click opacity
                if self.on_click:
                    self.on_click(self)
                return True
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        """Handle mouse release events."""
        if self.is_pressed:
            self.is_pressed = False
            if not self.is_disabled:
                self.bg_color.a = self.hover_opacity if self.collide_point(*touch.pos) else self.opacity
                if self.on_release:
                    self.on_release(self)
            return True
        return super().on_touch_up(touch)

    def set_visibility(self, is_visible):
        """Set button visibility."""
        self.is_visible = is_visible
        self.opacity = 1 if self.is_visible else 0

    def set_disabled(self, is_disabled):
        """Enable or disable the button."""
        self.is_disabled = is_disabled
        self.opacity = self.disabled_opacity if self.is_disabled else 1
        self._update_disabled_state()

    def set_opacity(self, opacity):
        """Set button opacity."""
        self.opacity = opacity

    def set_text(self, text):
        """
        Set the text of the button and update the label.
        :param text: New text for the button.
        """
        self.text = self.apply_markup(text)  # Apply markup styles
        self.label.text = self.text  # Update the label's text
        self._update_text()

    def _update_disabled_state(self):
        """Update the button appearance based on the disabled state."""
        if self.is_disabled:
            self.bg_color.a = self.disabled_opacity
        else:
            self.bg_color.a = self.opacity

    def add_to_layout(self, layout):
        """Add the image to a layout."""
        if self.parent is not None:
            self.parent.remove_widget(self)
        layout.add_widget(self)

if __name__ == "__main__":
    import pyvisual as pv

    # Create a pyvisual window
    window = pv.Window()

    # # Create buttons with rounded edges
    # button1 = BasicButton(
    #     window=window, x=325, y=275, width=200, height=60, text="Button 1",
    #     font_size=24, corner_radius=20, opacity=1, border_thickness=5, border_color=(1, 0, 0, 1),
    #     on_click=lambda btn: print(f"{btn.text} clicked"),
    #     on_release=lambda btn: print(f"{btn.text} released")
    # )
    button2 = BasicButton(
        window=window, x=325, y=375, width=200, height=60, text="Button 2",
        font_size=24, corner_radius=0, opacity=1, border_thickness=0, border_color=(0, 1, 0, 1),
        on_click=lambda btn: print(f"{btn.text} clicked"),
        on_release=lambda btn: print(f"{btn.text} released"), button_color=(1,0,0,1)
    )

    # Show the window
    window.show()
