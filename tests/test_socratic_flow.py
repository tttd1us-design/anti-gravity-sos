"
Unit Tests for Socratic Formula & Mathematical Physics
"
from app.core.formula import calculate_activation_energy, dynamic_task_downsizing

def test_activation_energy():
    # E_base=8.0, C_f=8.5, M=1.0 -> 68.0
    res = calculate_activation_energy(8.0, 8.5, 1.0)
    assert res == 68.0

def test_task_downsizing():
    downsized = dynamic_task_downsizing(도서 1장 초고 A4 10장 작성, 8.0, 8.5, 1.0)
    assert downsized[is_downsized] is True
    assert downsized[new_e_act] < 5.0
    assert Obsidian in downsized[micro_action]

if __name__ == __main__:
    test_activation_energy()
    test_task_downsizing()
    print(ALL TESTS PASSED SUCCESSFULLY.)
