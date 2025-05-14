from manim import *
import numpy as np
from scipy.interpolate import lagrange

# Белый фон
config.background_color = WHITE

class LagrangeInterpolationScene(Scene):
    def construct(self):
        # 1) Узлы и итоговый полином
        x = np.array([1, 2, 3])
        y = np.array([10, 21, 38])
        poly = lagrange(x, y)

        # 2) Оси
        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 50, 10],
            x_length=8,
            y_length=5,
            axis_config={"color": BLACK},
            x_axis_config={"numbers_to_include": [1, 2, 3], "color": BLACK},
            y_axis_config={"numbers_to_include": [10, 20, 30, 40], "color": BLACK},
        ).to_edge(DOWN, buff=1)
        self.add(axes)

        # 3) Подписи осей
        x_tex = MathTex("x", font_size=24).set_color(BLACK)
        y_tex = MathTex("f(x)", font_size=24).set_color(BLACK)
        x_label = axes.get_x_axis_label(x_tex, direction=DOWN, buff=0.2)
        y_label = axes.get_y_axis_label(y_tex, direction=LEFT, buff=0.2)
        self.play(Write(x_label), Write(y_label))

        # 4) Точки и их подписи
        dots = VGroup(*[
            Dot(axes.coords_to_point(xi, yi), color=BLACK)
            for xi, yi in zip(x, y)
        ])
        dot_labels = VGroup(*[
            MathTex(f"({xi},{yi})", font_size=20)
                .set_color(BLACK)
                .next_to(dots[i], UP+RIGHT, buff=0.05)
            for i, (xi, yi) in enumerate(zip(x, y))
        ])
        self.play(Create(dots), Write(dot_labels))
        self.wait(0.5)

        # 5) Все три базисных y_i * l_i(x) и их подписи
        colors = [BLUE, GREEN, RED]
        basis_graphs = VGroup()
        for i, color in enumerate(colors):
            xi, yi = x[i], y[i]
            # определяем функцию y_i * l_i(t)
            def yi_li(t, ii=i):
                num = np.prod([t - xj for j, xj in enumerate(x) if j != ii])
                den = np.prod([xi - xj for j, xj in enumerate(x) if j != ii])
                return yi * num / den

            graph = axes.plot(
                lambda t, fn=yi_li: fn(t),
                x_range=[0, 4],
                color=color,
                stroke_width=3,
            )
            basis_graphs.add(graph)
            # подпись вида "10 l₀(x)" над серединой кривой
            mid = graph.point_from_proportion(0.5)
            label = MathTex(rf"{yi}\,l_{{{i}}}(x)", font_size=28)\
                        .set_color(color)\
                        .next_to(mid, UP, buff=0.2)
            self.play(Create(graph), Write(label), run_time=2)

        self.wait(0.5)

        # 6) Итоговый полином поверх всех
        final = axes.plot(
            lambda t: poly(t),
            x_range=[0, 4],
            color=BLACK,
            stroke_width=5,
        )
        self.play(Create(final), run_time=2)

        # 7) Подпись итоговой формулы
        c0, c1, c2 = poly.coef
        sum_formula = MathTex(
            rf"L(x) = {c0:.0f}x^2 "
            rf"{'+' if c1>=0 else '-'} {abs(c1):.0f}x "
            rf"{'+' if c2>=0 else '-'} {abs(c2):.0f}",
            font_size=32
        ).set_color(BLACK).to_edge(UP, buff=0.5)
        self.play(Write(sum_formula))
        self.wait(2)
