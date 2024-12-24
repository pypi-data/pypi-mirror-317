def json_to_html_table(data: list[dict], header_color: str = "green", graceful_error: bool = True) -> str:
    """
    Converts a list of dictionaries into an HTML table with customizable header color.

    Args:
        data (list[dict]): A list of dictionaries where each dictionary represents a row in the table.
        header_color (str, optional): The color of the table header. 
            Accepts predefined colors ('green', 'blue', 'red', 'gray', 'purple', 'orange') 
            or any valid CSS color code. Default is 'green'.

    Returns:
        str: A string containing the HTML representation of the table.
    """
    if not isinstance(data, list) or not all(isinstance(row, dict) for row in data):
        if graceful_error:
            return "<font color='red'>Invalid input data. Please provide a list of dictionaries.</font>"
        raise ValueError("Invalid input data. Please provide a list of dictionaries.")

    header_colors = {
        "green": "#006400",
        "blue": "#0000FF",
        "red": "#FF0000",
        "gray": "#808080",
        "purple": "#800080",
        "orange": "#FFA500",
    }
    header_color = header_colors.get(header_color.lower(), header_color)

    headers = data[0].keys()
    html_table = (
        f"<table style='width: 100%; border-collapse: collapse; font-size: 14px; color: #333;'>"
        f"<thead><tr style='background-color: {header_color}; color: white; font-weight: bold;'>"
        + "".join(
            f"<th style='padding: 8px 12px; text-align: left; border: 1px solid #B0B0B0; background-color: {header_color};'>{header}</th>"
            for header in headers
        )
        + "</tr></thead><tbody>"
    )

    html_table += "".join(
        f"<tr style='background-color: {'#FFFFFF' if idx % 2 == 0 else '#F4F4F4'};'>"
        + "".join(
            f"<td style='padding: 8px 12px; text-align: left; border: 1px solid #B0B0B0;'>{value}</td>"
            for value in row.values()
        )
        + "</tr>"
        for idx, row in enumerate(data)
    )

    return (
        html_table
        + "<style>tr:hover {background-color: #E0E0E0;}</style></tbody></table>"
    )

