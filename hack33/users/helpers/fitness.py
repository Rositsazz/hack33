POINTS = 5

def is_any_empty_day(schedule):
    for k, v in schedule.items():
        if v == []:
            return True
    return False

def more_than_7_hours(schedule):
    for k, v in schedule.items():
        if len(v) > 7:
            return True
    return False

def get_class_rating(week_schedule):
    ordered = True
    for day, schedule in week_schedule.items():
        for i in range(len(schedule)):
            for j in range(i+1, len(schedule)):
                if schedule[i] != schedule[j]:
                    continue
                if schedule[i] == schedule[j] and i == (j-1):
                    break
                if schedule[i] == schedule[j] and i != (j-1):
                    ordered = False
                    break
    if ordered:
        return POINTS
    return 0

def give_rating_by_arrangement(schedule):
    schedule_rating = 0
    for c, week_schedule in schedule.items():
        class_rating = get_class_rating(week_schedule)
        schedule_rating += class_rating
    # print(schedule_rating)
    return schedule_rating
