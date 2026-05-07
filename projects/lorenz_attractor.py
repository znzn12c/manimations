from manim import *
from scipy.integrate import odeint
from scipy.integrate import solve_ivp


def lorenz_system(t, state, sigma=10, rho=28, beta=8 / 3):
    x, y, z = state
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z
    return [dxdt, dydt, dzdt]

def ode_solution_points(function, state0, time, dt=0.01):
    solution = solve_ivp(
        function,
        t_span=(0, time),
        y0=state0,
        t_eval=np.arange(0, time, dt)
    )
    return solution.y.T

class LorenzAttractor(ThreeDScene):

    def construct(self):
        # Font sizes
        h1 = 70
        h2 = 40
        equation_font_size = 60

        title = Text("Lorenz Attractor", font_size=h1)

        # Set up axes
        axes = ThreeDAxes(z_range=[0, 10, 1], z_length=10)
        self.set_camera_orientation(
            phi=75 * DEGREES,
            theta=-45 * DEGREES,
            zoom=1.4,
            frame_center=(0, 0, 2),
        )
        
        #Add the equations
        equations = MathTex(r"""
            \begin{aligned}
            \frac{\mathrm{d} x}{\mathrm{d} t} &= \sigma(y-x) \\
            \frac{\mathrm{d} y}{\mathrm{d} t} &= x(\rho-z)-y \\
            \frac{\mathrm{d} z}{\mathrm{d} t} &= x y-\beta z
            \end{aligned}
            """,
            font_size=equation_font_size
        )

        mathematical_expressions = Group(title, equations)

        equations.set_color_by_gradient(BLUE, YELLOW)
        
        # Display Lorenz solutions
        epsilon = 0.001
        nu_values = 5 # Number of different solutions
        states = [
            [10, 10, 10 + n * epsilon]
            for n in range(nu_values)
        ]
        colors = color_gradient([BLUE, YELLOW], len(states))
        evolution_time = 30

        curves = VGroup()
        for state, color in zip(states, colors):
            points = ode_solution_points(lorenz_system, state, evolution_time)
            scaled_points = points * 0.1
            curve = VMobject(color=color).set_points_as_corners([axes.c2p(x, y, z) for x, y, z in scaled_points])
            curve.set_stroke(color=color, width=2)
            curves.add(curve)

        dots = Group(*(Dot3D(color=color) for color in colors))

        # Different initial conditions for different nu value
        values = [VGroup(Dot3D(color=color), MathTex(fr"\epsilon\cdot\nu={epsilon*n}", font_size=equation_font_size, color=color)).arrange(RIGHT) for n, color in zip(range(nu_values), colors)] # Probably the line I'm most proud of in this code (I did it myself!!!)

        explain = VGroup(Text("Initial conditions", font_size=h2), MathTex(r"(10, 10, 10 + \epsilon\cdot\nu)", font_size=equation_font_size), values).arrange(DOWN)

        # 3Blue1Brown uses the "cursed line" globals().update(locals()), but the same can be done by creating a predefinite value curves=curves inside the update_dots functions as done below (he corrects himself in the video)
        def update_dots(dots, curves=curves):
            for dot, curve in zip(dots, curves):
                dot.move_to(curve.get_end())
        
        dots.add_updater(update_dots)

        # Introduction
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))
        
        self.add_fixed_in_frame_mobjects(equations)
        self.play(Write(equations))

        self.play(mathematical_expressions.animate.to_corner(UL, buff=-0.5).scale(0.6))

        # Initial conditions
        self.add_fixed_in_frame_mobjects(explain)
        self.play(Write(explain))
        self.play(explain.animate.to_corner(UR, buff=0.5).scale(0.6))

        # Lorenz Attractor animation
        self.play(FadeIn(axes))
        self.begin_ambient_camera_rotation(0.15)
        self.add(dots)
        self.play(
            *(
                Create(curve, run_time=evolution_time, rate_func=linear)
                for curve in curves
            ),
            run_time=evolution_time
        )
        self.stop_ambient_camera_rotation()

        
        
        