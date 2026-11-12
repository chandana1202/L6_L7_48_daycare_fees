import math


def _parse_float(value):
    """Return a finite float, or None if value is not a valid finite number."""
    try:
        number = float(value)
    except (ValueError, TypeError, OverflowError):
        return None
    if not math.isfinite(number):
        return None
    return number


def parse_enrolment(text):
    if not isinstance(text, str):
        return None
    parts = text.split(':')
    if len(parts) != 2:
        return None
    age_group = parts[0].strip()
    hours = _parse_float(parts[1])
    if not age_group or hours is None or not (0 <= hours <= 168):
        return None
    return age_group.title(), hours


def hours_average(hours_csv):
    if not isinstance(hours_csv, str):
        return None
    values = []
    for item in hours_csv.split(','):
        try:
            value = int(item)
        except ValueError:
            return None
        if not (0 <= value <= 168):
            return None
        values.append(value)
    return sum(values) / len(values)


def payable_fee(text):
    if not isinstance(text, str):
        return None
    parts = text.split('|')
    if len(parts) != 2:
        return None
    fee = _parse_float(parts[0])
    discount = _parse_float(parts[1])
    if fee is None or discount is None or fee < 0 or discount < 0:
        return None
    total = fee * 1.18 - discount
    if not math.isfinite(total):
        return None
    return max(total, 0)
def main():
    print("==== Running parse_enrolment ====")
    user_input = input("Enter age group:hours (e.g. toddler:25): ")
    result = parse_enrolment(user_input)
    print("Age Group and Hours:", result if result is not None else "Invalid input")

    print("\n==== Running hours_average ====")
    user_input = input("Enter weekly hours as CSV (e.g. 20,25,30): ")
    result = hours_average(user_input)
    print("Average Hours:", result if result is not None else "Invalid input")

    print("\n==== Running payable_fee ====")
    user_input = input("Enter fee|discount (e.g. 3000|250): ")
    result = payable_fee(user_input)
    print("Payable Fee:", result if result is not None else "Invalid input")

if __name__ == "__main__":
    main()
