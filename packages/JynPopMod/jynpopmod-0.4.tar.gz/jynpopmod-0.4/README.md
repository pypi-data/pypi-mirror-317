switch_case(value, cases, default=None) 
# Executes the corresponding function for the given value based on a dictionary of cases.

pop(message, title="Information") 
# Displays an informational message.

popinp(prompt, title="Input") 
# Prompts the user for input via a dialog.

ifnull(value, default) 
# Returns the default value if the given value is None or empty.

popp(a, b) 
# Concatenates two values.

pop_with_image(message, img_path, title="Information") 
# Displays a message with an image.

set_theme(root, theme="light") 
# Sets the theme of the window. Can be "dark" or "light" to change the background color.

pop_switch(cases, default=None, name="User") 
# Provides an option for the user to select from, then shows the selected option.

create_main_window() 
# Creates the main window.

set_window_size(root, width=300, height=200) 
# Sets the size of the window.

set_window_title(root, title) 
# Sets the title of the window.

set_window_icon(root, icon_path) 
# Sets the window icon.

minimize_window(root) 
# Minimizes the window to the taskbar.

maximize_window(root) 
# Maximizes the window to full screen.

destroy_window(root) 
# Destroys (closes) the window.

center_window(root, width=300, height=200) 
# Centers the window on the screen.

set_window_bg_color(root, color) 
# Sets the background color of the window.

set_window_always_on_top(root) 
# Keeps the window always on top of other windows.

remove_window_always_on_top(root) 
# Removes the "always on top" attribute from the window.

set_window_opacity(root, opacity) 
# Sets the opacity (transparency) of the window.

hide_window(root) 
# Hides the window.

show_window(root) 
# Unhides the window.

set_window_fixed_size(root) 
# Fixes the window size (prevents resizing).

enable_window_resizing(root) 
# Allows the window to be resized.

set_window_bg_image(root, image_path) 
# Sets a background image for the window.

change_window_icon(root, icon_path) 
# Changes the window icon.

create_label(root, text) 
# Creates a label widget with the specified text.

create_button(root, text, command) 
# Creates a button widget that triggers a command when clicked.

create_entry(root) 
# Creates an entry (input) widget.

create_text_widget(root, width=30, height=10) 
# Creates a multi-line text widget.

create_checkbox(root, text, command) 
# Creates a checkbox widget with a command to be executed when clicked.

create_radio_buttons(root, options, command) 
# Creates a set of radio buttons for the user to select from.

create_dropdown(root, options, command) 
# Creates a dropdown list with given options.

create_listbox(root, items, command) 
# Creates a listbox with the provided items.

create_canvas(root, width=400, height=300) 
# Creates a canvas widget for drawing and displaying graphics.

create_progress_bar(root) 
# Creates a progress bar widget.

create_scrollbar(root, widget) 
# Creates a scrollbar and attaches it to a widget.

create_frame(root) 
# Creates a frame widget to organize other widgets.

create_menu_bar(root) 
# Creates a menu bar for the window.

bind_key_press(root, key, function) 
# Binds a function to a specific key press event.

bind_mouse_click(root, function) 
# Binds a function to the mouse click event.

bind_mouse_enter(widget, function) 
# Binds a function to the mouse entering a widget.

bind_mouse_leave(widget, function) 
# Binds a function to the mouse leaving a widget.

bind_mouse_wheel(root, function) 
# Binds a function to the mouse wheel scroll event.

trigger_event(widget, event) 
# Triggers a specific event on the widget.

update_label_text(label, new_text) 
# Updates the text of the label widget.

update_entry_text(entry, new_text) 
# Updates the text inside an entry widget.

update_text_widget(text_widget, new_content) 
# Updates the content of a text widget.

update_checkbox_state(checkbox, state) 
# Updates the state (checked/unchecked) of a checkbox.

update_radio_selection(var, value) 
# Updates the selected value of a set of radio buttons.

update_progress_bar(progress, value) 
# Updates the value of the progress bar.

disable_widget(widget) 
# Disables the widget, making it non-interactive.

enable_widget(widget) 
# Enables the widget, making it interactive again.

change_widget_bg_color(widget, color) 
# Changes the background color of the widget.

change_widget_fg_color(widget, color) 
# Changes the foreground (text) color of the widget.

change_widget_font(widget, font_name, font_size) 
# Changes the font and font size of the widget.

add_widget_border(widget, border_width=2, border_color="black") 
# Adds a border around the widget.

pack_with_padding(widget, padx=10, pady=10) 
# Packs the widget with specified padding.

grid_widget(widget, row, col, rowspan=1, columnspan=1) 
# Places the widget on a grid layout with specified row, column, and spans.

place_widget(widget, x, y) 
# Places the widget at specific coordinates.

set_grid_widget_sticky(widget, sticky="nsew") 
# Makes the widget "sticky" in a grid, allowing it to stretch across multiple areas.

show_info_messagebox(message) 
# Displays an informational message box.

show_error_messagebox(message) 
# Displays an error message box.

show_warning_messagebox(message) 
# Displays a warning message box.

ask_yes_no_question(question) 
# Asks a yes/no question and returns the user's response.

ask_for_input(prompt) 
# Asks the user for input.

show_messagebox_with_image(message, image_path) 
# Displays a message box with an image icon.

show_confirmation_messagebox(message) 
# Displays a confirmation message box with OK/Cancel options.

create_modal_dialog(root, message) 
# Creates a modal dialog window with the specified message.