import time
import os
import math

def clear_console():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_clock(radius, current_time):
    """Generate an ASCII clock based on the current time."""
    canvas_size = radius * 2 + 1
    canvas = [[' ' for _ in range(canvas_size)] for _ in range(canvas_size)]

    # Center of the clock
    center = radius

    # Draw clock face
    for angle in range(0, 360, 6):  # Increment by 6 degrees (1 minute spacing)
        rad = math.radians(angle)
        x = int(center + radius * math.cos(rad))
        y = int(center - radius * math.sin(rad))
        canvas[y][x] = '.'

    # Hour, minute, second hands
    hour, minute, second = current_time

    # Hour hand
    hour_angle = math.radians((hour % 12 + minute / 60) * 30)
    hour_x = int(center + (radius * 0.5) * math.cos(hour_angle))
    hour_y = int(center - (radius * 0.5) * math.sin(hour_angle))
    canvas[hour_y][hour_x] = 'H'

    # Minute hand
    minute_angle = math.radians(minute * 6)
    minute_x = int(center + (radius * 0.7) * math.cos(minute_angle))
    minute_y = int(center - (radius * 0.7) * math.sin(minute_angle))
    canvas[minute_y][minute_x] = 'M'

    # Second hand
    second_angle = math.radians(second * 6)
    second_x = int(center + (radius * 0.9) * math.cos(second_angle))
    second_y = int(center - (radius * 0.9) * math.sin(second_angle))
    canvas[second_y][second_x] = 'S'

    return canvas

def display_clock(canvas):
    """Display the ASCII clock on the console."""
    for row in canvas:
        print(''.join(row))

def main():
    radius = 10  # Radius of the clock
    while True:
        # Get current time
        now = time.localtime()
        current_time = (now.tm_hour, now.tm_min, now.tm_sec)

        # Generate clock face
        clock_canvas = generate_clock(radius, current_time)

        # Clear console and display clock
        clear_console()
        display_clock(clock_canvas)

        # Sleep for a second
        time.sleep(1)

if __name__ == "__main__":
    main()