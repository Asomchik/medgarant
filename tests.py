import unittest

from busy_doctor import (
    generate_free_time_slots,
    convert_time_to_minutes,
    convert_minutes_to_time,
)


class TestConvertTimeFromString(unittest.TestCase):
    def test_convert_time_to_minutes_good(self):
        # Проверка конвертации без ошибки
        cases = [
            ('00:00', 0),
            ('01:00', 60),
            ('00:10', 10),
            ('09:02', 542),
        ]
        for good_time, result in cases:
            self.assertEqual(convert_time_to_minutes(good_time), result)

    def test_convert_time_to_minutes_bad(self):
        # Проверка конвертации с ошибкой
        cases = [
            '000:00',
            '-1:00',
            'ab:10',
            '55:02',
            '00:72',
            '0:12',
        ]
        for bad_time in cases:
            with self.assertRaises(ValueError):
                convert_time_to_minutes(bad_time)


class TestConvertTimeToString(unittest.TestCase):
    def test_convert_minutes_to_time_good(self):
        # Проверка конвертации без ошибки
        cases = [
            (0, '00:00'),
            (60, '01:00'),
            (10, '00:10'),
            (542, '09:02'),
        ]
        for good_time_stamp, result in cases:
            self.assertEqual(convert_minutes_to_time(good_time_stamp), result)

    def test_convert_time_to_minutes_bad(self):
        # Проверка конвертации с ошибкой
        cases = [
            -10,
            '',
            24 * 60 + 1,
            '10',
            '00:72',
        ]
        for bad_time in cases:
            with self.assertRaises(ValueError):
                convert_minutes_to_time(bad_time)


class TestGenerateSlots(unittest.TestCase):
    def test_generate_free_time_slots(self):
        test_cases = [
            {
                'start_time': '09:00',
                'end_time': '10:00',
                'duration': 30,
                'busy': [
                    {'start': '08:30', 'stop': '10:20'},
                ],
                'result': [],
            },
            {
                'start_time': '09:00',
                'end_time': '10:00',
                'duration': 30,
                'busy': [
                    {'start': '09:40', 'stop': '10:50'},
                    {'start': '18:40', 'stop': '18:50'},
                    {'start': '14:40', 'stop': '15:50'},
                    {'start': '16:40', 'stop': '17:20'},
                    {'start': '20:05', 'stop': '20:20'}
                ],
                'result': [
                    {'start': '09:00', 'stop': '09:30'},
                ],
            },
            {
                'start_time': '09:00',
                'end_time': '21:00',
                'duration': 30,
                'busy': [
                    {'start': '10:30', 'stop': '10:50'},
                    {'start': '18:40', 'stop': '18:50'},
                    {'start': '14:40', 'stop': '15:50'},
                    {'start': '16:40', 'stop': '17:20'},
                    {'start': '20:05', 'stop': '20:20'}
                ],
                'result': [
                    {'start': '09:00', 'stop': '09:30'},
                    {'start': '09:30', 'stop': '10:00'},
                    {'start': '10:00', 'stop': '10:30'},
                    {'start': '10:50', 'stop': '11:20'},
                    {'start': '11:20', 'stop': '11:50'},
                    {'start': '11:50', 'stop': '12:20'},
                    {'start': '12:20', 'stop': '12:50'},
                    {'start': '12:50', 'stop': '13:20'},
                    {'start': '13:20', 'stop': '13:50'},
                    {'start': '13:50', 'stop': '14:20'},
                    {'start': '15:50', 'stop': '16:20'},
                    {'start': '17:20', 'stop': '17:50'},
                    {'start': '17:50', 'stop': '18:20'},
                    {'start': '18:50', 'stop': '19:20'},
                    {'start': '19:20', 'stop': '19:50'},
                    {'start': '20:20', 'stop': '20:50'}
                ],
            },
        ]

        for case in test_cases:
            start_time = case['start_time']
            start_time = convert_time_to_minutes(start_time)
            end_time = case['end_time']
            end_time = convert_time_to_minutes(end_time)
            duration = case['duration']
            busy = case['busy']
            result = case['result']
            self.assertEqual(
                generate_free_time_slots(start_time, end_time, duration, busy),
                result
            )


if __name__ == '__main__':
    unittest.main()
