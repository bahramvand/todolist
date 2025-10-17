def validate_length(field_name: str, value: str, min_length: int):
    if len(value.strip()) < min_length:
        raise ValueError(f"{field_name} must have at least {min_length} characters.")

def print_table(items, headers):
    if not items:
        print("No items to display.")
        return

    print("\n" + " | ".join(headers))
    print("-" * 60)
    for row in items:
        print(" | ".join(str(cell) for cell in row))
    print("-" * 60 + "\n")
