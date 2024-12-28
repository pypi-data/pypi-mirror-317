import pyautogui
import numpy as np
import time
import keyboard
import logging
import random
import threading
import platform


def check_key_press():
    """
    Function to monitor key presses and stop the execution of the loop when a key is pressed.
    """
    global continue_execution
    keyboard.wait()  # Wait for any key press
    continue_execution = False


def switch_to_next_tab(x, y, duration):
    """
    Function to switch to the next tab.
    """
    if platform.system() == "Darwin":  # macOS
        pyautogui.hotkey("command", "shift", "[")
    elif platform.system() == "Windows":
        pyautogui.hotkey("ctrl", "tab")
    else:
        print("Unsupported operating system")


def move_mouse_to_position(x, y, duration):
    """
    Function to move the mouse to a specified position.
    """
    pyautogui.moveTo(x, y, duration=duration)


def switch_to_previous_tab(x, y, duration):
    """
    Function to switch to the previous tab.
    """
    if platform.system() == "Darwin":  # macOS
        pyautogui.hotkey("command", "shift", "]")
    elif platform.system() == "Windows":
        pyautogui.hotkey("ctrl", "shift", "tab")
    else:
        print("Unsupported operating system")


def main(delay_mean, delay_std_dev, move_duration):
    """
    Main function to execute the program.
    """
    # Set up basic logging configuration
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    # Get screen size
    screen_width, screen_height = pyautogui.size()
    logging.info(f"Screen size: {screen_width} x {screen_height}")

    # Set the center of the screen as the center of the 2D normal distribution
    mean = (screen_width / 2, screen_height / 2)

    # Set the standard deviation for x and y coordinates
    std_dev_x = screen_width / 6
    std_dev_y = screen_height / 6

    # Set the parameters for the delay distribution
    delay_mean = delay_mean
    delay_std_dev = delay_std_dev

    # Set the time lapse for the mouse movement
    move_duration = move_duration

    # Flag to control the execution of the loop
    continue_execution = True

    # Define a list of commands using lambda expressions and their descriptions
    commands = [
        {
            "command": switch_to_next_tab,
            "description": "Switched to the next tab",
        },
        {
            "command": move_mouse_to_position,
            "description": "Moved mouse to position",
        },
        {
            "command": switch_to_previous_tab,
            "description": "Switched to the previous tab",
        },
    ]

    # Start a separate thread to monitor key presses
    key_thread = threading.Thread(target=check_key_press)
    key_thread.start()

    while True:
        while continue_execution:
            # Sample x and y coordinates from the 2D normal distribution
            x, y = np.random.multivariate_normal(
                mean, [[std_dev_x**2, 0], [0, std_dev_y**2]]
            )

            # Clamp the values to be within the screen boundaries
            x, y = max(0, min(x, screen_width - 1)), max(0, min(y, screen_height - 1))

            # Choose a random command from the commands list
            random_command = random.choice(commands)

            # Execute the random command
            random_command["command"](x, y, move_duration)

            # Log the executed command
            logging.info(random_command["description"])

            # Sample a delay from the normal distribution
            delay = np.random.normal(delay_mean, delay_std_dev)

            # Clamp the delay to be non-negative
            delay = max(0, delay)

            # Log the delay
            logging.info(f"Delaying next movement for {delay:.2f} seconds")

            # Delay the next iteration
            time.sleep(delay)

        # Reset the flag to continue execution
        continue_execution = True

    logging.info("Key pressed. Exiting program.")


def run_jiggler():
    import argparse

    parser = argparse.ArgumentParser(
        description="This program moves the mouse cursor randomly on the screen and performs random actions such as switching tabs or clicking on buttons."
    )
    parser.add_argument(
        "--delay_mean",
        type=float,
        default=12,
        help="Mean value for delay distribution",
    )
    parser.add_argument(
        "--delay_std_dev",
        type=float,
        default=6,
        help="Standard deviation for delay distribution",
    )
    parser.add_argument(
        "--move_duration",
        type=float,
        default=0.5,
        help="Duration of the mouse movement in seconds",
    )
    args = parser.parse_args()

    main(args.delay_mean, args.delay_std_dev, args.move_duration)


run_jiggler()
