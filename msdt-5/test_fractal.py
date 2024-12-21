import math
import pytest
from unittest.mock import MagicMock
from fractal import GFractal, Line, DrawBoard, State, draw_fractal, update_bounds, choose_step

# Тесты на инициализацию обьектов и на использование внутренних методов

def test_gfractal_initialization():
    fractal = GFractal()
    assert fractal.fractal == "F+F+F"

def test_gfractal_generation():
    fractal = GFractal(1)
    assert fractal.fractal == "F-F+F+F-F+F+F-F+F"

def test_gfractal_gen_down():
    fractal = GFractal(1)
    fractal.gen_down()
    assert fractal.fractal == "F+F+F"

def test_gfractal_gen_up():
    fractal = GFractal()
    fractal.gen_up()
    assert fractal.fractal == "F-F+F+F-F+F+F-F+F"

def test_line_initialization():
    line = Line(0, 0, 10, 10)
    assert line.x1 == 0
    assert line.y1 == 0
    assert line.x2 == 10
    assert line.y2 == 10

def test_update_bounds():
    bounds = [0, 0, 0, 0]
    update_bounds(bounds, 5, 5)
    assert bounds == [0, 0, 5, 5]

    update_bounds(bounds, -3, -3)
    assert bounds == [-3, -3, 5, 5]

def test_state_initialization():
    state = State(0, 0, 0)
    assert state.x == 0
    assert state.y == 0
    assert state.angle == 0

# Параметризованный тест на проверку функции изменения состояния рисующего объекта

@pytest.mark.parametrize("step, expected_state, expected_stack_length", [
    ('F', State(10, 0, 0), 1),
    ('f', State(10, 0, 0), 1),
    ('+', State(0, 0, 2.0943951023931954923084289221863), 1),
    ('-', State(0, 0, -2.0943951023931954923084289221863), 1),
    ('[', State(0, 0, 0), 2),
    (']', State(5, -5, 0), 0),
])
def test_choose_step(step, expected_state, expected_stack_length):
    state = State(0, 0, 0)
    turtle_memory = [State(5, -5, 0)]
    new_state = choose_step(turtle_memory, state, step)
    assert new_state.x == expected_state.x
    assert new_state.y == expected_state.y
    assert math.isclose(new_state.angle, expected_state.angle)
    assert len(turtle_memory) == expected_stack_length

def test_draw_fractal_with_mock():
    board = MagicMock()
    fractal = GFractal(1)
    draw_fractal(board, fractal)
    assert board.add_line.call_count > 0  # Проверяет, что метод add_line был вызван хотя бы один раз
