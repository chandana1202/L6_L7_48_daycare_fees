from hypothesis import given, strategies as st
from daycare_fees import parse_enrolment, hours_average, payable_fee


# ---------- Fuzz tests: must never crash ----------

@given(st.text() | st.none())
def test_parse_enrolment_no_crash(s):
    try:
        parse_enrolment(s)
    except Exception as e:
        assert False, f"parse_enrolment crashed with: {e!r}"


@given(st.text() | st.none())
def test_hours_average_no_crash(s):
    try:
        hours_average(s)
    except Exception as e:
        assert False, f"hours_average crashed with: {e!r}"


@given(st.text() | st.none())
def test_payable_fee_no_crash(s):
    try:
        payable_fee(s)
    except Exception as e:
        assert False, f"payable_fee crashed with: {e!r}"


# ---------- Property tests: correct behaviour on valid input ----------

@given(st.sampled_from(["toddler", "infant", "preschool"]), st.floats(0, 168))
def test_parse_enrolment_valid(group, hours):
    assert parse_enrolment(f"{group}:{hours}") == (group.title(), hours)


@given(st.lists(st.integers(0, 168), min_size=1))
def test_hours_average_within_range(nums):
    result = hours_average(",".join(map(str, nums)))
    assert result is not None
    assert min(nums) <= result <= max(nums)


@given(st.floats(0, 1e6), st.floats(0, 1e6))
def test_payable_fee_never_negative(fee, discount):
    result = payable_fee(f"{fee}|{discount}")
    assert result is not None and result >= 0