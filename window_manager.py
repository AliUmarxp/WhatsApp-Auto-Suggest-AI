import pygetwindow as gw

class WindowManager:
    @staticmethod
    def is_whatsapp_active():
        try:
            active_window = gw.getActiveWindow()
            if active_window is None:
                return False
            title = active_window.title.lower()
            return "whatsapp" in title
        except Exception as e:
            return False

    @staticmethod
    def get_whatsapp_window():
        try:
            windows = gw.getWindowsWithTitle("WhatsApp")
            if windows:
                return windows[0]
            # Also try matching browser titles for WhatsApp Web
            all_windows = gw.getAllTitles()
            for title in all_windows:
                if "WhatsApp" in title:
                    return gw.getWindowsWithTitle(title)[0]
        except Exception:
            pass
        return None
