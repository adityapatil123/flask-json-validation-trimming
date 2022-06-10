from jsonschema import validators
from jsonschema.validators import _LATEST_VERSION as LATEST_VALIDATOR


def extend_with_trimming(validator_class):
    validate_properties = validator_class.VALIDATORS["properties"]

    def trim_unnecessary_fields(validator, properties, instance, schema):
        for prop in list(instance.keys()):
            if prop not in properties:
                del instance[prop]

        for error in validate_properties(
                validator, properties, instance, schema,
        ):
            yield error

    return validators.extend(
        validator_class, {"properties": trim_unnecessary_fields},
    )


ExtendedTrimValidator = extend_with_trimming(LATEST_VALIDATOR)
