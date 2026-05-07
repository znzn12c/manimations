from manim import *

# Hello World text
class HelloWorld(Scene):
    def construct(self):
        circle = Circle()
        square = Square()

        text = Text("Hello World")
        text.to_edge(UP)

        square.to_edge(DOWN)

        self.add(circle, square, text)