import evdev
from evdev import UInput, ecodes, AbsInfo
from gpiozero import Button, MCP3008
import time

# Inicializace GPIO pinů
btn_up = Button(27)
btn_down = Button(17)
btn_left = Button(5)
btn_right = Button(22)

btn_a = Button(13)
btn_b = Button(26)
btn_x = Button(20)
btn_y = Button(12)

btn_l1 = Button(24)
btn_l2 = Button(23)
btn_r1 = Button(7)
btn_r2 = Button(25)

btn_select = Button(15)
btn_start = Button(14)

btn_l3 = Button(3)
btn_r3 = Button(2)

# Pravý joystick
joy_R_X = MCP3008(channel=0)
joy_R_Y = MCP3008(channel=1)

# Levý joystick
joy_L_Y = MCP3008(channel=3)
joy_L_X = MCP3008(channel=2)

# Vytvoření gamepadu
cap = {
    ecodes.EV_KEY: [
        ecodes.BTN_A, ecodes.BTN_B, ecodes.BTN_X, ecodes.BTN_Y,
        ecodes.BTN_TL, ecodes.BTN_TR, ecodes.BTN_TL2, ecodes.BTN_TR2,
        ecodes.BTN_THUMBL, ecodes.BTN_THUMBR,
        ecodes.BTN_START, ecodes.BTN_SELECT, ecodes.BTN_MODE,
    ],
    ecodes.EV_ABS: [
        (ecodes.ABS_X, AbsInfo(value=127, min=0, max=255, fuzz=0, flat=15, resolution=0)),
        (ecodes.ABS_Y, AbsInfo(value=127, min=0, max=255, fuzz=0, flat=15, resolution=0)),
        (ecodes.ABS_Z, AbsInfo(value=0, min=0, max=255, fuzz=0, flat=0, resolution=0)),   # Levý trigger (L2)
        (ecodes.ABS_RX, AbsInfo(value=127, min=0, max=255, fuzz=0, flat=15, resolution=0)),
        (ecodes.ABS_RY, AbsInfo(value=127, min=0, max=255, fuzz=0, flat=15, resolution=0)),
        (ecodes.ABS_RZ, AbsInfo(value=0, min=0, max=255, fuzz=0, flat=0, resolution=0)),  # Pravý trigger (R2)
        (ecodes.ABS_HAT0X, AbsInfo(value=0, min=-1, max=1, fuzz=0, flat=0, resolution=0)),
        (ecodes.ABS_HAT0Y, AbsInfo(value=0, min=-1, max=1, fuzz=0, flat=0, resolution=0)),
    ]
}

ui = UInput(cap, name="Xbox Gamepad", vendor=0x045e, product=0x028e)
# Vendor je Microsoft
# Product je Xbox 360 ovladač
def stav(tlacitko):
    return 1 if tlacitko.is_pressed else 0

def packa(mcp_kanal):
    return int(mcp_kanal.value * 255)

start_zmacknuto = False
start_cas = 0
home_odeslano = False

try:
    while True:
        # Start a home tlačítka
        if btn_start.is_pressed:
            if not start_zmacknuto:
                start_zmacknuto = True
                start_cas = time.time()
                home_odeslano = False
            else:
                if (time.time() - start_cas) >= 1.0 and not home_odeslano:
                    ui.write(ecodes.EV_KEY, ecodes.BTN_MODE, 1)
                    ui.syn()
                    home_odeslano = True
        else:
            if start_zmacknuto:
                # Právě jsi to pustil
                if home_odeslano:
                    ui.write(ecodes.EV_KEY, ecodes.BTN_MODE, 0) # Pustit Home
                else:
                    # Bylo to kratší než vteřina -> Odeslat krátký START klik
                    ui.write(ecodes.EV_KEY, ecodes.BTN_START, 1)
                    ui.syn()
                    time.sleep(0.05)
                    ui.write(ecodes.EV_KEY, ecodes.BTN_START, 0)
                ui.syn()
                start_zmacknuto = False

        # Obyčejná tlačítka
        ui.write(ecodes.EV_KEY, ecodes.BTN_A, stav(btn_a))
        ui.write(ecodes.EV_KEY, ecodes.BTN_B, stav(btn_b))
        ui.write(ecodes.EV_KEY, ecodes.BTN_X, stav(btn_x))
        ui.write(ecodes.EV_KEY, ecodes.BTN_Y, stav(btn_y))
        
        ui.write(ecodes.EV_KEY, ecodes.BTN_TL, stav(btn_l1))
        ui.write(ecodes.EV_KEY, ecodes.BTN_TR, stav(btn_r1))
        ui.write(ecodes.EV_KEY, ecodes.BTN_TL2, stav(btn_l2))
        ui.write(ecodes.EV_KEY, ecodes.BTN_TR2, stav(btn_r2))

        # Analogových triggery (L2 a R2)
        ui.write(ecodes.EV_ABS, ecodes.ABS_Z, 255 if btn_l2.is_pressed else 0)
        ui.write(ecodes.EV_ABS, ecodes.ABS_RZ, 255 if btn_r2.is_pressed else 0)
        
        ui.write(ecodes.EV_KEY, ecodes.BTN_THUMBL, stav(btn_l3))
        ui.write(ecodes.EV_KEY, ecodes.BTN_THUMBR, stav(btn_r3))
        ui.write(ecodes.EV_KEY, ecodes.BTN_SELECT, stav(btn_select))
        
        # D-PAD
        hat_x = 0
        if btn_left.is_pressed: hat_x = -1
        elif btn_right.is_pressed: hat_x = 1
        
        hat_y = 0
        if btn_up.is_pressed: hat_y = -1
        elif btn_down.is_pressed: hat_y = 1
        
        ui.write(ecodes.EV_ABS, ecodes.ABS_HAT0X, hat_x)
        ui.write(ecodes.EV_ABS, ecodes.ABS_HAT0Y, hat_y)
        
        # Analogové páčky
        ui.write(ecodes.EV_ABS, ecodes.ABS_X, 255 - packa(joy_L_Y))
        ui.write(ecodes.EV_ABS, ecodes.ABS_Y, packa(joy_L_X))
        ui.write(ecodes.EV_ABS, ecodes.ABS_RX, 255 - packa(joy_R_Y))
        ui.write(ecodes.EV_ABS, ecodes.ABS_RY, packa(joy_R_X))
        
        # Odeslání všech změn do systému
        ui.syn()
        
        time.sleep(0.01)

except KeyboardInterrupt:
    pass
