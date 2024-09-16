import ast
import re
from datetime import datetime

def parse_value(value):
    if isinstance(value, str):
        value = value.strip()

        # Handle percentage
        if '%' in value:
            try:
                result = float(value.replace('%', '')) / 100
                return round(result, 2)  # Restrict to 2 decimal places
            except ValueError:
                raise ValueError(f"Cannot parse percentage value: {value}")

        # Handle currency
        currency_match = re.match(r'^(\$|€)?(\d+(,\d{3})*(\.\d+)?)\s*(USD|EUR)?$', value)
        if currency_match:
            value = re.sub(r'[^\d.]+', '', value)  # Remove symbols
            try:
                return float(value)
            except ValueError:
                raise ValueError(f"Cannot parse currency value: {value}")

        # Handle boolean
        if value.lower() in ['true', 'false']:
            return 1.0 if value.lower() == 'true' else 0.0

        # Handle datetime (not used in this formula, but can be useful in other cases)
        try:
            datetime.fromisoformat(value)
            return value  # Return as string if datetime is not required in computation
        except ValueError:
            pass

        # Handle numeric
        try:
            return float(value)
        except ValueError:
            raise ValueError(f"Cannot parse numeric value: {value}")

    # If value is not a string, return it directly
    return value