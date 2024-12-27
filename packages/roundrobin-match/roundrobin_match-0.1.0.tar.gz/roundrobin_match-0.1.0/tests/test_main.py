import random
import unittest
from roundrobin_match import round_robin_schedule
from roundrobin_match.main import _validate_round_robin_schedule


class TestMain(unittest.TestCase):
    def test_round_bin_schedule(self):
        try:
            for size in range(2, 100, 2):
                for seed in range(1, 50):
                    random.seed(seed)
                    round_robin_schedule(size, True)
        except Exception as err:
            self.fail(err)

    def test_validate_round_robin_schedule(self):
        schedule = [[(0, 1), (2, 3)], [(0, 2), (1, 3)], [(0, 3), (1, 2)]]

        valid, _ = _validate_round_robin_schedule(schedule, 4)
        self.assertTrue(valid)

        # odd size is invalid
        valid, _ = _validate_round_robin_schedule(schedule, 3)
        self.assertFalse(valid)

        # small column
        schedule = [
            [(0, 1), (2, 3)],
            [(0, 2), (1, 3)],
        ]
        valid, _ = _validate_round_robin_schedule(schedule, 4)
        self.assertFalse(valid)

        # long column
        schedule = [
            [(0, 1), (2, 3)],
            [(0, 2), (1, 3)],
            [(0, 3), (1, 2)],
            [(4, 5), (6, 7)],
        ]
        valid, _ = _validate_round_robin_schedule(schedule, 4)
        self.assertFalse(valid)

        # double row
        schedule = [
            [(0, 1), (0, 3)],
            [(0, 2), (1, 3)],
            [(0, 3), (1, 2)],
        ]
        valid, _ = _validate_round_robin_schedule(schedule, 4)
        self.assertFalse(valid)

        # same row
        schedule = [[(0, 1), (2, 3)], [(0, 2), (1, 3)], [(0, 1), (2, 3)]]
        valid, _ = _validate_round_robin_schedule(schedule, 4)
        self.assertFalse(valid)

        # over max size
        schedule = [[(1, 2), (3, 4)], [(1, 3), (2, 4)], [(1, 4), (2, 3)]]
        valid, _ = _validate_round_robin_schedule(schedule, 4)
        self.assertFalse(valid)


if __name__ == "__main__":
    unittest.main()
