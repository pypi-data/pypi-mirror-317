import imageio
import time
from PIL import ImageGrab
import argparse
import numpy as np

from threading import Timer
import sys

if sys.platform == "win32":
    import ctypes

    user32 = ctypes.windll.user32

    def get_active_window_info():
        hwnd = user32.GetForegroundWindow()

        if not hwnd:
            return None

        rect = ctypes.create_string_buffer(16)
        user32.GetWindowRect(hwnd, rect)

        x = int.from_bytes(rect[:4], byteorder="little")
        y = int.from_bytes(rect[4:8], byteorder="little")
        width = int.from_bytes(rect[8:12], byteorder="little")
        height = int.from_bytes(rect[12:], byteorder="little")

        return x, y, width, height

    def screensize():
        """Returns the width and height of the screen as a two-integer tuple.

        Returns:
        (width, height) tuple of the screen size, in pixels.
        """
        return (
            ctypes.windll.user32.GetSystemMetrics(0),
            ctypes.windll.user32.GetSystemMetrics(1),
        )


if sys.platform == "darwin":
    from Quartz import (
        CGWindowListCopyWindowInfo,
        kCGWindowListOptionOnScreenOnly,
        kCGNullWindowID,
    )
    from AppKit import NSWorkspace
    import Quartz

    def get_active_window_info():
        # Get the currently active application
        active_app = NSWorkspace.sharedWorkspace().frontmostApplication()
        active_pid = active_app.processIdentifier()

        # Get the list of all on-screen windows
        window_list = CGWindowListCopyWindowInfo(
            kCGWindowListOptionOnScreenOnly, kCGNullWindowID
        )

        # Filter windows belonging to the active application
        for window in window_list:
            if window.get("kCGWindowOwnerPID") == active_pid:
                window_title = window.get("kCGWindowName", "Unknown")
                window_bounds = window.get("kCGWindowBounds", {})
                returndict = {
                    "application": active_app.localizedName(),
                    "pid": active_pid,
                    "title": window_title,
                    "bounds": window_bounds,
                }
                return (
                    window_bounds["X"],
                    window_bounds["Y"],
                    window_bounds["Width"],
                    window_bounds["Height"],
                )

        return None

    def screensize():
        return (
            Quartz.CGDisplayPixelsWide(Quartz.CGMainDisplayID()),
            Quartz.CGDisplayPixelsHigh(Quartz.CGMainDisplayID()),
        )


def get_win_size():

    if sys.platform == "darwin":
        screen_width, screen_height = screensize()
    else:
        screen_width, screen_height = ImageGrab.grab().size

    window = get_active_window_info()
    # Get window geometry
    win_x, win_y, win_width, win_height = window

    # Calculate as a percentage of screen size
    width = round((win_width / screen_width) * 100, 2)
    height = round((win_height / screen_height) * 100, 2)
    left = round((win_x / screen_width) * 100, 2)
    top = round((win_y / screen_height) * 100, 2)
    return left, top, width, height


def get_window(args):
    print("Starting in 5 secs....")

    def wrapper():
        main_active(args)

    t = Timer(5.0, wrapper)
    t.start()


def create_parser():
    parser = argparse.ArgumentParser(
        prog="record", description="Screen Recording with python"
    )
    parser.add_argument(
        "filename",
        type=str,
        default="test.gif",
        help="filename can be mp4 or gif or mov",
    )
    parser.add_argument(
        "-i",
        "--initdelay",
        type=int,
        default=5,
        help="Initial delay in seconds, default 5 s",
    )
    parser.add_argument(
        "-d",
        "--delay",
        type=float,
        default=0.5,
        help="Delay between frames in seconds, default 0.5 s",
    )
    parser.add_argument(
        "-dur",
        "--duration",
        type=int,
        default=20,
        help="Duration of capture, default 20 s",
    )
    parser.add_argument(
        "--bbox",
        type=float,
        nargs="+",
        default=[0, 0, 50, 50],
        help="Bounding box, default (0, 0, 50, 50)",
    )
    parser.add_argument("-f", "--fullscreen", action="store_true")
    parser.add_argument("-aw", "--activewindow", action="store_true")

    return parser


def record(outfilename, initdelay=5, delay=0.1, duration=5, area=None):

    area_pix = area
    if area:
        screen_width, screen_height = ImageGrab.grab().size
        left_percent, top_percent, width_percent, height_percent = area
        # Convert percentages to pixel values
        left = int(screen_width * (left_percent / 100))
        top = int(screen_height * (top_percent / 100))
        right = int(screen_width * ((left_percent + width_percent) / 100))
        bottom = int(screen_height * ((top_percent + height_percent) / 100))
        area_pix = (left, top, right, bottom)
        # print(area_pix)

    img = []
    time.sleep(initdelay)
    print("Started..\a")
    # sc = imageio.get_reader("<screen>")
    t0 = time.time()
    while True:
        t1 = time.time()
        # still = sc.get_next_data()
        still = ImageGrab.grab()
        if area:
            still = still.crop(area_pix)
        img.append(still)
        t2 = time.time()
        time.sleep(abs(delay - (t2 - t1)))
        if t2 - t0 > duration:
            break
    print("Ended..\a\a")
    imageio.mimsave(outfilename, img, fps=2)


def main_active(args):
    active_window_info = get_win_size()
    record(
        args.filename,
        initdelay=0,
        duration=args.duration,
        delay=args.delay,
        area=active_window_info,
    )


def main():
    parser = create_parser()
    args = parser.parse_args()
    mainrun(args)


def mainrun(args):
    if args.activewindow:
        print("Please select active window")
        get_window(args)
    else:
        area = args.bbox
        if args.fullscreen:
            area = None

        record(
            args.filename,
            initdelay=args.initdelay,
            duration=args.duration,
            delay=args.delay,
            area=area,
        )


if __name__ == "__main__":
    main()
