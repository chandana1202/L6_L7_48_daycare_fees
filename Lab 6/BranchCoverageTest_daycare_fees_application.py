import pytest
from daycare_fees import extra_hours_fee, enrolment_allowed, pickup_status


# ---------- extra_hours_fee: error branches ----------
@pytest.mark.parametrize("group, hours", [("baby", 10), ("", 5)])
def test_unknown_age_group(group, hours):
    with pytest.raises(ValueError, match="unknown age group"):
        extra_hours_fee(group, hours, False)

def test_negative_hours():
    with pytest.raises(ValueError, match="invalid hours"):
        extra_hours_fee("infant", -1, False)

def test_zero_hours_is_valid():
    assert extra_hours_fee("infant", 0, False) == 0


# ---------- extra_hours_fee: fee branches ----------
@pytest.mark.parametrize("group, hours, sibling, expected", [
    ("infant", 20, False, 0),        # exactly included hours
    ("toddler", 25, False, 0),
    ("toddler", 30, True, 0),        # sibling gives +5 hours
    ("infant", 30, False, 140),      # infant rate 14
    ("infant", 30, True, 140),       # sibling does NOT help infants
    ("toddler", 35, False, 90),      # non-infant rate 9
    ("toddler", 35, True, 45),
    ("preschool", 40, True, 45),     # included 30 + 5
    ("infant", 40, False, 280),      # extra == 20, no surcharge
    ("infant", 41, False, 462),      # extra == 21, rate 22
    ("infant", 50, False, 660),
    ("toddler", 45, False, 180),     # extra == 20, no surcharge
    ("toddler", 46, False, 294),     # extra == 21, rate 14 (no infant +3)
    ("preschool", 60, False, 420),   # extra 30, rate 14
])
def test_extra_hours_fee(group, hours, sibling, expected):
    assert extra_hours_fee(group, hours, sibling) == expected


# ---------- enrolment_allowed ----------
@pytest.mark.parametrize("age, vacancies, pending, expected", [
    (12, 0, True, True),     # pending, age exactly 12
    (11, 5, True, False),    # pending, too young
    (5, 3, False, False),    # under 6 months
    (6, 0, False, False),    # old enough, no vacancy
    (6, 1, False, True),     # old enough, 1 vacancy
    (24, 2, False, True),
])
def test_enrolment_allowed(age, vacancies, pending, expected):
    assert enrolment_allowed(age, vacancies, pending) is expected


# ---------- pickup_status ----------
@pytest.mark.parametrize("minutes, aftercare, friday, expected", [
    # normal day: cutoff 10, late down to -5
    (10, False, False, "on_time"),
    (9, False, False, "late"),
    (-5, False, False, "late"),
    (-6, False, False, "overdue"),
    # aftercare: cutoff 20, late down to 5
    (20, True, False, "on_time"),
    (19, True, False, "late"),
    (5, True, False, "late"),
    (4, True, False, "overdue"),
    # friday only: cutoff 20
    (20, False, True, "on_time"),
    (19, False, True, "late"),
    (4, False, True, "overdue"),
    # aftercare + friday: cutoff 30, late down to 15
    (30, True, True, "on_time"),
    (15, True, True, "late"),
    (14, True, True, "overdue"),
])
def test_pickup_status(minutes, aftercare, friday, expected):
    assert pickup_status(minutes, aftercare, friday) == expected