from cnb.utils.sensitive_data import sensitive_keys


def mask_sensitive_data(data: dict) -> dict:
    """
    Masks sensitive fields in a dictionary.

    Args:
        data (dict): The data dictionary to mask (headers or body).
    Returns:
        dict: A new dictionary with sensitive fields masked.
    """
    masked_data = data.copy()
    for key in sensitive_keys:
        if key in masked_data:
            data = str(masked_data[key])
            if len(data) <= 5:
                masked_data[key] = f"***********{data[-1:]}"  # Replace sensitive value with mask
            else:
                masked_data[key] = f"***********{data[-3:]}"
    return masked_data
