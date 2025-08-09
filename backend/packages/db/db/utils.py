import textwrap
from typing import Any

from db.models import Base


def format_description(description: str) -> str:
    """
    Format the description by removing newlines and excessive spaces.
    """
    return textwrap.dedent(description).strip().replace("\n", " ").replace("  ", " ")


def model_to_dict(model: Base) -> dict[str, Any]:
    """
    Convert a Model to a Dictionary.
    """
    columns = model.__table__.columns.values()
    data = {}
    for column in columns:
        value = getattr(model, column.name)
        if any(
            [
                value is None and column.nullable,
                value is None and column.server_default is not None,
            ]
        ):
            continue
        else:
            data[column.name] = value
    return data
