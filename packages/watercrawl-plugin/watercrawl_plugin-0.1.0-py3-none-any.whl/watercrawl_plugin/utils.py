import os

from jsonschema import Draft7Validator

try:
    from django.conf import settings
except ImportError:
    settings = None


def validate_json(schema, data):
    validator = Draft7Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
    formatted_errors = {}

    for error in errors:
        # Join the error path to create a field name
        field = ".".join(map(str, error.path)) if error.path else "non_field_errors"
        message = error.message

        # Add the error to the formatted dictionary
        if field in formatted_errors:
            formatted_errors[field].append(message)
        else:
            formatted_errors[field] = [message]

    return formatted_errors


def get_settings(key, default=None):
    try:
        if settings:
            return getattr(settings, key)
    except AttributeError:
        pass
    return os.environ.get(key, default)
