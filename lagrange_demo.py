from manim import *
import numpy as np
from scipy.interpolate import lagrange

config.background_color = WHITE

class LagrangeInterpolationScene(Scene):
    def construct(self):
        # 1) Задаём узлы и строим полином через SciPy
        x = np.array([1, 2, 3])
        y = np.array([10, 21, 38])
        poly = lagrange(x, y)

        # 2) Создаём оси (без font_size в get_axis_labels)
        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 50, 10],
            axis_config={"color": BLACK},
        ).to_edge(DOWN, buff=1)
        self.add(axes)

        # 3) Создаём метки осей с нужным шрифтом
        x_tex = MathTex("x", font_size=24)           # метка 'x' размером 24
        y_tex = MathTex("f(x)", font_size=24)         # метка 'f(x)' размером 24
        x_label = axes.get_x_axis_label(x_tex, direction=DOWN, buff=0.2)
        y_label = axes.get_y_axis_label(y_tex, direction=LEFT, buff=0.2)
        self.play(Write(x_label), Write(y_label))

        # 4) Отображаем узловые точки и их подписи
        dots = VGroup(*[
            Dot(axes.coords_to_point(xi, yi), color=BLACK)
            for xi, yi in zip(x, y)
        ])
        dot_labels = VGroup(*[
            MathTex(f"({xi},{yi})", font_size=20)
                .next_to(dots[i], UP+RIGHT, buff=0.05)
            for i, (xi, yi) in enumerate(zip(x, y))
        ])
        self.play(Create(dots), Write(dot_labels))
        self.wait(0.5)

        # 5) Рисуем три базисных y_i * l_i(x)
        colors = [BLUE, GREEN, RED]
        basis_graphs = VGroup()
        for i, color in enumerate(colors):
            xi, yi = x[i], y[i]
            def yi_li(t, ii=i):
                num = np.prod([t - xj for j, xj in enumerate(x) if j != ii])
                den = np.prod([xi - xj for j, xj in enumerate(x) if j != ii])
                return yi * num / den
            g = axes.plot(lambda t, fn=yi_li: fn(t), x_range=[0,4], color=color, stroke_width=3)
            basis_graphs.add(g)
        self.play(Create(basis_graphs), run_time=3)
        self.wait(0.5)

        # 6) Итоговый полином чёрным, поверх базисов
        final = axes.plot(lambda t: poly(t), x_range=[0,4], color=BLACK, stroke_width=5)
        c0, c1, c2 = poly.coef
        formula = MathTex(
            rf"L(x) = {c0:.0f}x^2 {'+' if c1>=0 else '-'} {abs(c1):.0f}x {'+' if c2>=0 else '-'} {abs(c2):.0f}",
            font_size=32
        ).set_color(BLACK).to_edge(UP, buff=0.5)
        self.play(Create(final), Write(formula), run_time=2)
        self.wait(1)
