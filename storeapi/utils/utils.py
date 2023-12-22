def convert_celsius_to_fahrenheit(celsius):
    """
    Convert temperature from Celsius to Fahrenheit.

    Parameters:
        celsius (float): Temperature in Celsius.

    Returns:
        float: Temperature in Fahrenheit.
    """
    fahrenheit = (9/5) * celsius + 32
    return fahrenheit

def convert_fahrenheit_to_celsius(fahrenheit):
    """
    Convert temperature from Fahrenheit to Celsius.

    Parameters:
        fahrenheit (float): Temperature in Fahrenheit.

    Returns:
        float: Temperature in Celsius.
    """
    celsius = (fahrenheit - 32) * 5/9
    return celsius
