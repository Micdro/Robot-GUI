import dearpygui.dearpygui as dpg
from gcode_maker import GCodeMaker, open_serial_port
from main import main
#GUI
# Rail length = 300 mm
dpg.create_context()


# with dpg.value_registry():
#     dpg.add_string_value(default_value="Default string", tag="string_value")

def button_save(sender, app_data, user_data):
    print(f"save sender is: {sender}")
    print(f"app_data is: {app_data}")
    print(f"user_data is: {user_data}")


def button_load(sender, app_data, user_data):
    print(f"load sender is: {sender}")
    print(f"app_data is: {app_data}")
    print(f"user_data is: {user_data}")
    dpg.set_value('string_value_file_name', app_data.get('file_path_name'))
    fn = dpg.get_value('string_value_file_name')
    print(f'newfilename={fn}')


def run_program_1(sender, app_data, user_data):
    print(f"run sender is: {sender}")
    print(f"app_data is: {app_data}")
    print(f"user_data is: {user_data}")
    prog_file = dpg.get_value('string_value_file_name')
    print(f'my file {prog_file}')
    if prog_file is not None:
        main(f"-f{prog_file}")


def button_stop(sender, app_data, user_data):
    print(f"stop sender is: {sender}")
    print(f"app_data is: {app_data}")
    print(f"user_data is: {user_data}")
    gcm.stop()

def button_resume(sender, app_data, user_data):
    print(f"stop sender is: {sender}")
    print(f"app_data is: {app_data}")
    print(f"user_data is: {user_data}")
    gcm.resume()


def go_home(sender, app_data, user_data):
    print(f"home sender is: {sender}")
    print(f"app_data is: {app_data}")
    print(f"user_data is: {user_data}")
    gcm.move_lin(-45, relative=True, speed=100)
    gcm.go_home()
    gcm.move_rot(180, speed=100)


def exit_program():
    dpg.destroy_context()


def sets_zero(sender, app_data, user_data):
    print(f"home sender is: {sender}")
    print(f"app_data is: {app_data}")
    print(f"user_data is: {user_data}")
    gcm.set_zero()


def button_rotate_l(sender, app_data, user_data):
    print(f"rotate left sender is: {sender}")
    print(f"app_data is: {app_data}")
    print(f"user_data is: {user_data}")


def button_rotate_r(sender, app_data, user_data):
    print(f"rotate right sender is: {sender}")
    print(f"app_data is: {app_data}")
    print(f"user_data is: {user_data}")


def linear_move_to():
    linear_value = dpg.get_value(linear_location)
    speed_value = dpg.get_value(speed)
    print(f"linear_move location is: {linear_value}")
    print(f"Speed: {speed_value}")
    gcm.move_lin(linear_value, speed=speed_value)


def linear_step_1():
    linear_value = dpg.get_value(linear_location)
    speed_value = dpg.get_value(speed)
    print(f"linear_move location is: {linear_value}")
    print(f"Speed: {speed_value}")
    gcm.move_lin(1, relative=True, speed=speed_value)


def linear_step_back_1():
    linear_value = dpg.get_value(linear_location)
    speed_value = dpg.get_value(speed)
    print(f"linear_move location is: {linear_value}")
    print(f"Speed: {speed_value}")
    gcm.move_lin(-1, relative=True, speed=speed_value)


def rotation():
    rotation_value = dpg.get_value(rotation_location)
    speed_value = dpg.get_value(speed)
    print(f"rotation location is: {rotation_value}")
    print(f"Speed: {speed_value}")
    gcm.move_rot(rotation_value, speed=speed_value)


def rotation_left():
    rotation_value = dpg.get_value(rotation_location)
    speed_value = dpg.get_value(speed)
    print(f"rotation location is: {rotation_value}")
    print(f"Speed: {speed_value}")
    gcm.move_rot(1, relative=True, speed=speed_value)


def rotation_right():
    rotation_value = dpg.get_value(rotation_location)
    speed_value = dpg.get_value(speed)
    print(f"rotation location is: {rotation_value}")
    print(f"Speed: {speed_value}")
    gcm.move_rot(-1, relative=True, speed=speed_value)


def gcode_send():
    cmd = dpg.get_value(gcode_input).upper()
    print(f"GCODE cmd is: {cmd}")
    gcm.send(cmd)


def report_pos(homed):
    pos = gcm.get_position()
    print(pos)
    dpg.set_value(pos_text, pos)
    print(pos_text)


def go_safe_lock(sender, app_data, user_data):
    speed_value = dpg.get_value(speed)
    x = 1
    total_cycles = dpg.get_value(cycles)
    print(f"Total Cycles {total_cycles}")
    for i in range(total_cycles):
        gcm.move_lin(-2, relative=True, speed=speed_value)
        gcm.wait(1.5)
        gcm.move_lin(2, relative=True, speed=speed_value)
        gcm.wait(1.5)
        print(f"Count: {x}")
        x += 1


# ------------------END CALL BACKS ----------------------------------
homed = False

with dpg.value_registry():
    dpg.add_string_value(default_value=None, tag='string_value_file_name')

# file dialog
with dpg.file_dialog(label="File Dialog", width=600, height=400, show=False, callback=button_load,
                     tag="file_dialog_tag"):
    dpg.add_file_extension("Program files(.nps){.nps}", color=(255, 0, 0, 255), custom_text="[robot]")
    dpg.add_file_extension("Python(.py){.py}", color=(0, 255, 0, 255))

# Main screen
with dpg.window(label="Robot", width=900, height=800):
    dpg.add_input_text(label="Name", default_value="NPD Robot Interface")
    # dpg.add_button(label="Load", callback=button_load, user_data="Some Data")
    # dpg.add_same_line()
    # dpg.add_button(label="Save", callback=button_save, user_data="Some Data")
    with dpg.group(horizontal=True):
        dpg.add_button(label="Load Program", callback=lambda: dpg.show_item("file_dialog_tag"),
                       user_data=dpg.last_container(), width=100, height=50)
        dpg.add_button(label="RESUME", callback=button_resume, user_data="RESUME", width=100, height=50)
        dpg.add_button(label="STOP", callback=button_stop, user_data="STOP", width=100, height=50)
        dpg.add_button(label="Home", callback=go_home, user_data="Home", width=60, height=50)
        dpg.add_button(label="Exit", callback=exit_program, width=60, height=50)
    dpg.add_spacer(height=20)
    # dpg.add_button(label="Set Zero", callback=sets_zero, user_data="Set Zero")
    # dpg.add_button(label="Run Program 1", callback=run_program_1, user_data="Run Program 1", width=150, height=75)
    cycles = dpg.add_input_int(label="cycles")

    speed = dpg.add_slider_int(label="Speed (%)", default_value=100, min_value=1, max_value=100)

    # Move the key to a specific location
    with dpg.group(horizontal=True):
        linear_location = dpg.add_slider_int(min_value=0, max_value=325)
        dpg.add_button(label="Move to", callback=linear_move_to)
        dpg.add_button(label="-1", callback=linear_step_back_1)
        dpg.add_button(label="+1",  callback=linear_step_1)


    with dpg.group(horizontal=True):
        rotation_location = dpg.add_slider_int(default_value=180, min_value=0, max_value=360)
        dpg.add_button(label="Rotate to", callback=rotation)
        dpg.add_button(label="-1", callback=rotation_left)
        dpg.add_button(label="+1", callback=rotation_right)

    with dpg.group(horizontal=True):
        gcode_input = dpg.add_input_text(label="GCODE", default_value="")
        dpg.add_button(label="Send", callback=gcode_send)

    dpg.add_spacer(height=20)
    with dpg.group(horizontal=True):
        dpg.add_text("Programs (Start with key inserted)")
    dpg.add_spacer(height=20)


    with dpg.group(horizontal=True):

        dpg.add_button(label="SafeLock", callback=go_safe_lock, user_data="wp5", width=120, height=30)
    with dpg.group(horizontal=True):
        dpg.add_spacer(height=20)
    with dpg.group(horizontal=True):
        dpg.add_button(label="Positions", callback=report_pos, width=120, height=20)
        pos_text = dpg.add_input_text(width=140, height=40)

dpg.create_viewport(title='Robot Programmer', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()

with open_serial_port('COM13', outfile=None) as sport:
    gcm = GCodeMaker(sport, None)
    dpg.start_dearpygui()
    dpg.destroy_context()
