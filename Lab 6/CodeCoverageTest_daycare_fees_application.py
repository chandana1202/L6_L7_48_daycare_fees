import pytest
from daycare_fees import extra_hours_fee, enrolment_allowed, pickup_status


# ---------- extra_hours_fee ----------
def test_unknown_age_group():
    with pytest.raises(ValueError):
        extra_hours_fee("baby", 10, False)

def test_negative_hours():
    with pytest.raises(ValueError):
        extra_hours_fee("infant", -1, False)

def test_within_included_hours():
    assert extra_hours_fee("toddler", 20, False) == 0

def test_toddler_with_sibling_extra_hours():
    # included 25 + 5 = 30, extra 5, rate 9
    assert extra_hours_fee("toddler", 35, True) == 45

def test_infant_high_extra_hours():
    # included 20, extra 30, rate 14 + 5 + 3 = 22
    assert extra_hours_fee("infant", 50, False) == 660


# ---------- enrolment_allowed ----------
def test_enrolment_allowed():
    assert enrolment_allowed(24, 2, False) is True

def test_enrolment_pending_immunisation_old_enough():
    assert enrolment_allowed(12, 0, True) is True

def test_enrolment_too_young():
    assert enrolment_allowed(5, 2, False) is False


# ---------- pickup_status ----------
def test_pickup_on_time():
    assert pickup_status(10, False, False) == "on_time"

def test_pickup_late():
    # aftercare + friday -> cutoff 30; 20 >= 15
    assert pickup_status(20, True, True) == "late"

def test_pickup_overdue():
    assert pickup_status(0, True, True) == "overdue"