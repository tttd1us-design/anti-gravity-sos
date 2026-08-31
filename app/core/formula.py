"""
Anti-Gravity Mathematical Physics Model
Activation Energy Calculation and Dynamic Task Downsizing (Bypass Protocol)
"""

def calculate_activation_energy(e_base: float, c_f: float, momentum: float, epsilon: float = 1e-5) -> float:
    """
    Calculate Cognitive Activation Energy E_act.
    Formula: E_act = (E_base * C_f) / (Momentum + epsilon)
    """
    if momentum < 0:
        momentum = 0.0
    return float(round((e_base * c_f) / (momentum + epsilon), 2))

def dynamic_task_downsizing(original_task: str, e_base: float = 8.0, c_f: float = 8.5, momentum: float = 1.0, threshold: float = 5.0) -> dict:
    """
    If E_act > threshold, force downscale task complexity (E_base -> 0.1)
    and create a zero-resistance micro-action (1~5 mins).
    """
    current_e_act = calculate_activation_energy(e_base, c_f, momentum)
    
    if current_e_act > threshold:
        bypassed_ebase = 0.1
        bypassed_cf = max(1.0, c_f * 0.4)
        new_momentum = momentum + 0.3
        new_e_act = calculate_activation_energy(bypassed_ebase, bypassed_cf, new_momentum)
        
        return {
            "is_downsized": True,
            "original_e_act": current_e_act,
            "new_e_act": new_e_act,
            "original_task": original_task,
            "micro_action": f"Obsidian을 열고 '[{original_task[:15]}...]' 아래 가장 형편없는 문장 1줄 적기 (5분 타이머)",
            "time_box_minutes": 5,
            "trigger_cue": "절대 비공개 1인 로컬 모드 발동 즉시 키보드 타이핑 개시",
            "momentum_gain": 0.3
        }
    
    return {
        "is_downsized": False,
        "original_e_act": current_e_act,
        "new_e_act": current_e_act,
        "original_task": original_task,
        "micro_action": original_task,
        "time_box_minutes": 25,
        "trigger_cue": "딥워크 타이머 25분 세팅",
        "momentum_gain": 0.1
    }
