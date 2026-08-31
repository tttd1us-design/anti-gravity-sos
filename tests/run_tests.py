import sys
from tests.test_core import (
    test_ladder_is_task_aware_not_hardcoded,
    test_miner_silent_below_min_sample,
    test_miner_finds_time_pattern_with_evidence,
    test_sos_triggers_on_three_not_started,
    test_safety_screens_and_offers_resources
)

def run():
    print("Running 3-Minute Lab Core Test Suite...")
    test_ladder_is_task_aware_not_hardcoded()
    print("PASS: test_ladder_is_task_aware_not_hardcoded")

    test_miner_silent_below_min_sample()
    print("PASS: test_miner_silent_below_min_sample")

    test_miner_finds_time_pattern_with_evidence()
    print("PASS: test_miner_finds_time_pattern_with_evidence")

    test_sos_triggers_on_three_not_started()
    print("PASS: test_sos_triggers_on_three_not_started")

    test_safety_screens_and_offers_resources()
    print("PASS: test_safety_screens_and_offers_resources")

    print("\nSUCCESS: All 5 tests passed with zero errors!")

if __name__ == "__main__":
    run()
