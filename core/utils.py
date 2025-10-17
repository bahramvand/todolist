def validate_length(field_name: str, value: str, min_length: int):
  if len(value.strip()) < min_length:
    raise ValueError(f"{field_name} must have at least {min_length} characters.")