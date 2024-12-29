1. **`switch_case(variable, cases)`**
   - **`variable`**: A value to check against the dictionary `cases`.
   - **`cases`**: A dictionary where keys are the possible values of `variable` and values are the corresponding functions to execute.
   - **What it does**: Mimics a switch-case statement, executing the function associated with the value of `variable`.

2. **`pop(message)`**
   - **`message`**: A string to display in a message box.
   - **What it does**: Displays a simple message in a pop-up window.

3. **`popinp(message)`**
   - **`message`**: A string to display in an input dialog.
   - **What it does**: Prompts the user for input through a dialog box.

4. **`create_main_window()`**
   - **What it does**: Initializes and creates the main Tkinter window for the GUI.

5. **`set_window_size(width, height)`**
   - **`width`**: The desired width of the window.
   - **`height`**: The desired height of the window.
   - **What it does**: Sets the size of the window.

6. **`center_window(window, width, height)`**
   - **`window`**: The Tkinter window object.
   - **`width`**: The width of the window.
   - **`height`**: The height of the window.
   - **What it does**: Centers the window on the screen.

7. **`minimize_window(window)`**
   - **`window`**: The Tkinter window object.
   - **What it does**: Minimizes the window.

8. **`maximize_window(window)`**
   - **`window`**: The Tkinter window object.
   - **What it does**: Maximizes the window.

9. **`set_window_bg_color(window, color)`**
   - **`window`**: The Tkinter window object.
   - **`color`**: A string representing the color to set as the background (e.g., `"red"`, `"blue"`).
   - **What it does**: Sets the background color of the window.

10. **`create_button(window, text, command)`**
    - **`window`**: The Tkinter window object.
    - **`text`**: The label or text to display on the button.
    - **`command`**: The function to call when the button is clicked.
    - **What it does**: Creates a button widget.

11. **`create_label(window, text)`**
    - **`window`**: The Tkinter window object.
    - **`text`**: The text to display on the label.
    - **What it does**: Creates a label widget.

12. **`create_text_widget(window, height, width)`**
    - **`window`**: The Tkinter window object.
    - **`height`**: The height of the text widget.
    - **`width`**: The width of the text widget.
    - **What it does**: Creates a text widget for multi-line text input.

13. **`bind_mouse_click(widget, callback)`**
    - **`widget`**: The Tkinter widget to bind the mouse click event to.
    - **`callback`**: The function to call when the mouse click happens.
    - **What it does**: Binds a mouse click event to a widget.

14. **`bind_key_press(widget, callback)`**
    - **`widget`**: The Tkinter widget to bind the key press event to.
    - **`callback`**: The function to call when a key is pressed.
    - **What it does**: Binds a key press event to a widget.

15. **`move_file(src, dest)`**
    - **`src`**: The source file path.
    - **`dest`**: The destination file path.
    - **What it does**: Moves a file from `src` to `dest`.

16. **`copy_file(src, dest)`**
    - **`src`**: The source file path.
    - **`dest`**: The destination file path.
    - **What it does**: Copies a file from `src` to `dest`.

17. **`create_directory(path)`**
    - **`path`**: The directory path to create.
    - **What it does**: Creates a new directory at the specified `path`.

18. **`create_zip_file(file_paths, zip_path)`**
    - **`file_paths`**: A list of paths to files to include in the ZIP.
    - **`zip_path`**: The path where the resulting ZIP file should be saved.
    - **What it does**: Creates a ZIP file from the specified files.

19. **`extract_zip_file(zip_path, dest)`**
    - **`zip_path`**: The path of the ZIP file.
    - **`dest`**: The destination directory to extract the files to.
    - **What it does**: Extracts files from the ZIP to the destination directory.

20. **`capture_photo(output_path)`**
    - **`output_path`**: The file path where the captured photo should be saved.
    - **What it does**: Captures a photo using the webcam and saves it to `output_path`.

21. **`record_video(output_path, duration)`**
    - **`output_path`**: The file path to save the recorded video.
    - **`duration`**: The duration in seconds for which to record the video.
    - **What it does**: Records a video using the webcam for the specified duration and saves it to `output_path`.

22. **`start_http_server(port)`**
    - **`port`**: The port on which the server should run.
    - **What it does**: Starts an HTTP server listening on the specified port.

23. **`get_server_status()`**
    - **What it does**: Checks and returns the current status of the HTTP server.

24. **`upload_file_to_server(file_path, url)`**
    - **`file_path`**: The path of the file to upload.
    - **`url`**: The server URL where the file should be uploaded.
    - **What it does**: Uploads a file to the server at the specified URL.

25. **`text_to_speech(text)`**
    - **`text`**: The text to convert into speech.
    - **What it does**: Converts the `text` into speech.

26. **`speech_to_text()`**
    - **What it does**: Records speech from the microphone and converts it into text.

27. **`get_cpu_usage()`**
    - **What it does**: Retrieves the current CPU usage percentage.

28. **`get_memory_usage()`**
    - **What it does**: Retrieves the current memory usage percentage.

29. **`get_ip_address()`**
    - **What it does**: Retrieves the system's current IP address.

30. **`safe_run(func)`**
    - **`func`**: The function to run safely.
    - **What it does**: Executes the function `func`, catching any exceptions and preventing the program from crashing.

31. **`track_mouse_position(callback)`**
    - **`callback`**: The function to call whenever the mouse position changes.
    - **What it does**: Tracks the mouse position and calls the `callback` when it moves.

32. **`run_shell_command(command)`**
    - **`command`**: The shell command to execute.
    - **What it does**: Runs a system shell command and returns the result.

33. **`send_email(subject, body, to_email)`**
    - **`subject`**: The subject of the email.
    - **`body`**: The body content of the email.
    - **`to_email`**: The recipient's email address.
    - **What it does**: Sends an email with the specified subject and body to the given recipient.

34. **`change_widget_bg_color(widget, color)`**
    - **`widget`**: The Tkinter widget.
    - **`color`**: The background color to apply to the widget.
    - **What it does**: Changes the background color of the widget.

35. **`change_widget_font(widget, font)`**
    - **`widget`**: The Tkinter widget.
    - **`font`**: The font to apply to the widget (e.g., `"Helvetica 12"`).
    - **What it does**: Changes the font of the widget.

36. **`add_widget_border(widget, width, color)`**
    - **`widget`**: The Tkinter widget.
    - **`width`**: The border width to apply.
    - **`color`**: The border color to apply.
    - **What it does**: Adds a border to the widget.

37. **`pack_with_padding(widget, padding)`**
    - **`widget`**: The Tkinter widget.
    - **`padding`**: The padding around the widget.
    - **What it does**: Packs the widget with the specified padding.

38. **`grid_widget(widget, row, column)`**
    - **`widget`**: The Tkinter widget.
    - **`row`**: The row in the grid where the widget should be placed.
    - **`column`**: The column in the grid where the widget should be placed.
    - **What it does**: Places the widget in a specific row and column in the grid.

39. **`place_widget(widget, x, y)`**
    - **`widget`**: The Tkinter widget.
    - **`x`**: The x-coordinate where to place the widget.
    - **`y`**: The y-coordinate where to place the widget.
    - **What it does**: Places the widget at the specified x and y coordinates.

40. **`delayed_pop(message, delay)`**
    - **`message`**: The message to display.
    - **`delay`**: The number of seconds to wait before displaying the message.
    - **What it does**: Displays a delayed pop-up message after the specified delay.

41. **`start_timer(duration, callback)`**
    - **`duration`**: The duration in seconds for the timer.
    - **`callback`**: The function to call when the timer finishes.
    - **What it does**: Starts a timer and triggers the `callback` after the specified duration.

42. **`get_weather(city, api_key)`**
    - **`city`**: The name of the city for which to get the weather.
    - **`api_key`**: The API key for accessing the weather API.
    - **What it does**: Retrieves the weather data for the specified city using an external weather API.

43. **`copy_to_clipboard(text)`**
    - **`text`**: The text to copy to the clipboard.
    - **What it does**: Copies the given `text` to the clipboard.

44. **`paste_from_clipboard()`**
    - **What it does**: Pastes the text from the clipboard.

45. **`text_to_speech(text)`**
   - **`text`**: The text to be converted to speech.
   - **What it does**: Converts the given `text` into speech using the `pyttsx3` engine.

46. **`speech_to_text()`**
   - **What it does**: Records audio from the microphone and converts the spoken words to text using Google's speech recognition API.

47. **`start_timer(seconds, callback)`**
   - **`seconds`**: The number of seconds to run the timer for.
   - **`callback`**: The function to call once every second during the timer's countdown.
   - **What it does**: Runs a countdown timer for `seconds`, calling `callback()` once every second.

48. **`generate_random_string(length=15)`**
   - **`length`**: The desired length of the generated string.
   - **What it does**: Generates a random alphanumeric string of length `length`, with possible special characters.

49. **`find_files_by_extension(directory, extension)`**
   - **`directory`**: The directory to search in.
   - **`extension`**: The file extension to search for (e.g., `'.txt'`).
   - **What it does**: Returns a list of files in `directory` that have the given `extension`.

50. **`get_ip_address()`**
   - **What it does**: Returns the local IP address of the machine.

51. **`send_email(subject, body, to_email, mailname, mailpass)`**
   - **`subject`**: The subject of the email.
   - **`body`**: The body content of the email.
   - **`to_email`**: The recipient's email address.
   - **`mailname`**: The sender's email username.
   - **`mailpass`**: The sender's email password.
   - **What it does**: Sends an email using Gmail's SMTP server.

52. **`convert_image_to_grayscale(image_path, output_path)`**
   - **`image_path`**: The path to the image to convert.
   - **`output_path`**: The path to save the grayscale image.
   - **What it does**: Converts the given image to grayscale and saves it at `output_path`.

53. **`play_audio(text)`**
   - **`text`**: The text to be converted to speech.
   - **What it does**: Converts the given `text` to speech using `pyttsx3`.

54. **`record_audio()`**
    - **What it does**: Records audio from the microphone and converts it to text using speech recognition.

55. **`get_cpu_usage()`**
    - **What it does**: Returns the current CPU usage as a percentage.

56. **`get_memory_usage()`**
    - **What it does**: Returns the current memory usage as a percentage.

57. **`open_url(url)`**
    - **`url`**: The URL to open.
    - **What it does**: Opens the specified URL in the default web browser.

58. **`create_zip_file(source_dir, output_zip)`**
    - **`source_dir`**: The directory containing files to zip.
    - **`output_zip`**: The output path for the zip file.
    - **What it does**: Creates a ZIP file from the contents of the `source_dir`.

59. **`extract_zip_file(zip_file, extract_dir)`**
    - **`zip_file`**: The path to the zip file.
    - **`extract_dir`**: The directory to extract files into.
    - **What it does**: Extracts the contents of the ZIP file to `extract_dir`.

60. **`capture_screenshot(output_path)`**
    - **`output_path`**: The path to save the screenshot.
    - **What it does**: Takes a screenshot of the current screen and saves it to `output_path`.

61. **`move_file(source, destination)`**
    - **`source`**: The file path of the source file.
    - **`destination`**: The file path to move the file to.
    - **What it does**: Moves a file from `source` to `destination`.

62. **`copy_file(source, destination)`**
    - **`source`**: The file path of the source file.
    - **`destination`**: The file path to copy the file to.
    - **What it does**: Copies a file from `source` to `destination`.

63. **`show_file_properties(file_path)`**
    - **`file_path`**: The path to the file.
    - **What it does**: Returns the file's size and last modified time.

63. **`check_website_status(url)`**
    - **`url`**: The URL of the website to check.
    - **What it does**: Returns `True` if the website is accessible (status code 200), else `False`.

65. **`run_shell_command(command)`**
    - **`command`**: The shell command to execute.
    - **What it does**: Executes a shell command and returns the output and any errors.

66. **`get_weather(city, api_key)`**
    - **`city`**: The name of the city to check the weather for.
    - **`api_key`**: The API key for accessing the weather service.
    - **What it does**: Retrieves the current weather for the specified city using the OpenWeatherMap API.

67. **`monitor_file_changes(file_path, callback)`**
    - **`file_path`**: The path to the file to monitor.
    - **`callback`**: The function to call when the file is modified.
    - **What it does**: Monitors the file for changes and calls `callback()` when the file is modified.

68. **`reverse_string(string)`**
    - **`string`**: The string to reverse.
    - **What it does**: Returns the reversed version of the input `string`.

69. **`calculate_factorial(number)`**
    - **`number`**: The number to calculate the factorial of.
    - **What it does**: Returns the factorial of `number`.

70. **`swap_values(a, b)`**
    - **`a`**: The first value.
    - **`b`**: The second value.
    - **What it does**: Returns `b` and `a` swapped.

71. **`find_maximum(numbers)`**
    - **`numbers`**: A list of numbers.
    - **What it does**: Returns the maximum value in the list `numbers`.

72. **`find_minimum(numbers)`**
    - **`numbers`**: A list of numbers.
    - **What it does**: Returns the minimum value in the list `numbers`.

73. **`get_random_choice(choices)`**
    - **`choices`**: A list of choices.
    - **What it does**: Returns a random element from the list `choices`.

74. **`generate_unique_id()`**
    - **What it does**: Generates and returns a unique ID using `uuid`.

75. **`concatenate_lists(list1, list2)`**
    - **`list1`**: The first list.
    - **`list2`**: The second list.
    - **What it does**: Returns a new list that is the concatenation of `list1` and `list2`.

76. **`write_to_file(filename, content)`**
    - **`filename`**: The file to write to.
    - **`content`**: The content to write to the file.
    - **What it does**: Writes `content` to the specified file.

77. **`read_from_file(filename)`**
    - **`filename`**: The file to read from.
    - **What it does**: Reads and returns the content of the specified file.

78. **`parse_json(json_string)`**
    - **`json_string`**: The JSON string to parse.
    - **What it does**: Parses the JSON string and returns the corresponding Python object.

79. **`create_file_if_not_exists(filename)`**
    - **`filename`**: The file to create if it doesn't exist.
    - **What it does**: Creates an empty file at `filename` if it doesn't already exist.

80. **`create_directory(directory)`**
    - **`directory`**: The directory to create if it doesn't exist.
    - **What it does**: Creates the specified directory if it doesn't already exist.

81. **`send_http_request(url, method='GET', data=None)`**
    - **`url`**: The URL to send the request to.
    - **`method`**: The HTTP method to use ('GET' or 'POST').
    - **`data`**: The data to send (only used with 'POST').
    - **What it does**: Sends an HTTP request to the specified `url` using the specified `method` and `data`, returning the response.

82. **`get_cpu_temperaturelinux()`**
    - **What it does**: Returns the CPU temperature (in Celsius) for Linux systems, or `None` if not available.

83. **`calculate_square_root(number)`**
    - **`number`**: The number to calculate the square root of.
    - **What it does**: Returns the square root of `number`.

84. **`track_mouse_position(callback)`**
    - **`callback`**: The function to call with the mouse's position as arguments.
    - **What it does**: Tracks the mouse position and calls `callback()` with the current `(x, y)` position.