from app.models import Admission, Base, Student


def test_admission_table_has_expected_columns():
    columns = Admission.__table__.columns

    expected = {
        "id",
        "application_number",
        "full_name",
        "email",
        "phone_number",
        "course_applied",
        "branch_applied",
        "status",
        "created_at",
        "updated_at",
    }

    assert expected.issubset(columns.keys())


def test_student_table_has_expected_columns():
    columns = Student.__table__.columns

    expected = {
        "id",
        "student_number",
        "admission_id",
        "full_name",
        "course",
        "branch",
        "current_year",
        "created_at",
        "updated_at",
    }

    assert expected.issubset(columns.keys())


def test_student_admission_relationship_is_unique_foreign_key():
    table = Student.__table__
    admission_id = table.c.admission_id

    assert admission_id.unique is True
    assert admission_id.nullable is False

    foreign_keys = list(admission_id.foreign_keys)
    assert len(foreign_keys) == 1
    assert foreign_keys[0].target_fullname == "admissions.id"


def test_admission_status_constraint_exists():
    constraints = {
        constraint.name: constraint
        for constraint in Admission.__table__.constraints
    }

    assert "ck_admissions_status" in constraints


def test_percentage_and_percentile_constraints_exist():
    constraints = {
        constraint.name
        for constraint in Admission.__table__.constraints
    }

    expected = {
        "ck_admissions_class_10_percentage_range",
        "ck_admissions_class_12_percentage_range",
        "ck_admissions_jee_percentile_range",
        "ck_admissions_cuet_percentile_range",
    }

    assert expected.issubset(constraints)


def test_both_models_are_registered_in_metadata():
    assert "admissions" in Base.metadata.tables
    assert "students" in Base.metadata.tables
