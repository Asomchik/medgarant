"""
Модуль реализует построение расписания приема врача.
"""
import re


# Преобразование строки времени в минуты прошедшие от начала дня
def convert_time_to_minutes(time_stamp):
    expected_format = r'^\d{2}:\d{2}$'
    if not re.match(expected_format, time_stamp):
        raise ValueError(f'Ошибка в записи времени {time_stamp}')

    hours, minutes = map(int, time_stamp.split(':'))
    if hours < 0 or hours > 23 or minutes < 0 or minutes > 59:
        raise ValueError(f'Ошибка в данных времени {time_stamp}')
    return hours * 60 + minutes


# Преобразование минут от начала дня в строку времени
def convert_minutes_to_time(minutes_stamp):
    if not isinstance(minutes_stamp, int) or not(0 <= minutes_stamp <= 24*60):
        raise ValueError(f'Ошибка преобразования {minutes_stamp} в ЧЧ:ММ')
    hours = minutes_stamp // 60
    minutes = minutes_stamp % 60
    return f'{hours:02d}:{minutes:02d}'


def generate_free_time_slots(
        start_time: int,
        end_time: int,
        duration: int,
        busy_intervals: list[dict]) -> list[dict]:
    """
    Функция генерации свободных окон в расписании доктора.
    Возвращает окна свободного времени в виде списка словарей, если таковые
    окна имеются и пустой список [] в противном случае.
    """
    # Валидация времени длительности, начала и конца приема
    if start_time >= end_time:
        raise ValueError('Время начала работы специалиста '
                         'не может быть больше времени окончания работы')
    if not isinstance(duration, int) or duration <= 0:
        raise ValueError('Не верно задана длительность приема специалиста')

    # Построение списка занятых интервалов в минутах
    busy_slots = []
    for slot in busy_intervals:
        start = convert_time_to_minutes(slot['start'])
        end = convert_time_to_minutes(slot['stop'])

        # Валидация границ интервала перерыва и его включения в прием доктора
        if start >= end or start >= end_time or end <= start_time:
            continue
        # Отсекание времени перерывов вне интервала работы специалиста
        start = max(start, start_time)
        end = min(end, end_time)
        busy_slots.append((start, end))
    busy_slots.sort()

    # Построение списка свободных интервалов в минутах
    empty_slots = []
    for busy_start, busy_end in busy_slots:
        if start_time < busy_start:
            empty_slots.append([start_time, busy_start])
        start_time = max(start_time, busy_end)
    # Добавление интервала до окончания рабочего дня специалиста
    if start_time < end_time:
        empty_slots.append([start_time, end_time])
    # Разбивка свободных интервалов на слоты для приема пациентов
    available_slots = []
    for interval_start, interval_end in empty_slots:
        while interval_end - interval_start >= duration:
            available_slots.append((interval_start, interval_start + duration))
            interval_start += duration
    # Форматирование результата в заданный формат словаря
    schedule = []
    for start, end in available_slots:
        schedule.append(
            {
                'start': convert_minutes_to_time(start),
                'stop': convert_minutes_to_time(end),
            }
        )
    return schedule


if __name__ == '__main__':
    # Константы: Время начала и окончания приема у доктора, длительность приема
    _start_time = convert_time_to_minutes('09:00')
    _end_time = convert_time_to_minutes('21:00')
    _duration = 30

    _busy_intervals = [
        {'start': '10:30', 'stop': '10:50'},
        {'start': '18:40', 'stop': '18:50'},
        {'start': '14:40', 'stop': '15:50'},
        {'start': '16:40', 'stop': '17:20'},
        {'start': '20:05', 'stop': '20:20'}
    ]

    print(generate_free_time_slots(_start_time, _end_time, _duration, _busy_intervals))
