from todolist.core.constants import ERR_MIN_LENGTH, ERR_MAX_LENGTH
from todolist.exceptions import ValidationError


def validate_length(
    field_name: str,
    value: str,
    min_length: int | None = None,
    max_length: int | None = None,
) -> None:
    value = value.strip()

    if min_length is not None and len(value) < min_length:
        raise ValidationError(
            ERR_MIN_LENGTH.format(field_name=field_name, min_length=min_length)
        )

    if max_length is not None and len(value) > max_length:
        raise ValidationError(
            ERR_MAX_LENGTH.format(field_name=field_name, max_length=max_length)
        )

def print_table(items, headers):
    if not items:
        print("No items to display.")
        return

    print("\n" + " | ".join(headers))
    print("-" * 60)
    for row in items:
        print(" | ".join(str(cell) for cell in row))
    print("-" * 60 + "\n")
