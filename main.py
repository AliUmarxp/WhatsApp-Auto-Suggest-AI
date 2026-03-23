import tkinter as tk
from threading import Thread, Timer
import time
import pyautogui
import pyperclip
import traceback
from ai_engine import AIEngine
from window_manager import WindowManager

class WhatsAppAssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("WhatsApp AI Assistant")
        # Fixed the geometry format to prevent TclError crash, and provided ample vertical space
        self.root.geometry("450x600")
        self.root.attributes('-topmost', True) # Keep on top

        self.ai = None
        self.suggestions = ["(Loading model...)", "(Please wait)", ""]
        self.typing_timer = None
        self.last_clipboard = ""
        self.is_pasting = False 
        
        self.setup_ui()
        self.running = True
        
        # Withdraw the window so it is hidden on startup
        self.root.withdraw()
        
        # Start background threads
        Thread(target=self.init_ai_engine, daemon=True).start()
        Thread(target=self.monitor_clipboard, daemon=True).start()

    def setup_ui(self):
        # Header
        self.lbl_status = tk.Label(self.root, text="Status: Loading Model...", fg="red", font=("Arial", 10, "bold"))
        self.lbl_status.pack(pady=5)

        # Context Input
        tk.Label(self.root, text="Context / Friend's Message:").pack()
        self.entry_context = tk.Entry(self.root, width=60)
        self.entry_context.pack(pady=5)
        self.entry_context.bind("<KeyRelease>", self.on_typing)

        # Suggestion Buttons
        tk.Label(self.root, text="AI Suggestions (Click to Send):").pack(pady=5)
        
        # Changed button size and wrapping so large text is readable
        self.btn_sug1 = tk.Button(self.root, text=self.suggestions[0], width=50, height=4, wraplength=400, justify="left", command=lambda: self.send_suggestion(0), bg="#e8f4f8")
        self.btn_sug1.pack(pady=6)
        
        self.btn_sug2 = tk.Button(self.root, text=self.suggestions[1], width=50, height=4, wraplength=400, justify="left", command=lambda: self.send_suggestion(1), bg="#e8f4f8")
        self.btn_sug2.pack(pady=6)
        
        self.btn_sug3 = tk.Button(self.root, text=self.suggestions[2], width=50, height=4, wraplength=400, justify="left", command=lambda: self.send_suggestion(2), bg="#e8f4f8")
        self.btn_sug3.pack(pady=6)
        
        self.btn_hide = tk.Button(self.root, text="Hide Assistant", width=25, command=self.hide_window, bg="#ffcccc")
        self.btn_hide.pack(pady=10)

        self.buttons = [self.btn_sug1, self.btn_sug2, self.btn_sug3]

    def init_ai_engine(self):
        self.ai = AIEngine()
        # Ensure it pops up instantly once loading is complete (only initially)
        self.root.after(0, self.root.deiconify)
        self.root.after(0, self.update_status, "Status: Ready (Running in Background)", "green")
        self.root.after(0, self.update_suggestions_ui, ["Model Loaded! You can minimize or hide this window.", "Select any WhatsApp message,", "and press Ctrl+C. The Assistant will pop up automatically."])

    def update_status(self, text, color):
        self.lbl_status.config(text=text, fg=color)

    def update_suggestions_ui(self, suggestions):
        self.suggestions = suggestions
        for i, btn in enumerate(self.buttons):
            if i < len(suggestions):
                text_short = suggestions[i] if len(suggestions[i]) < 150 else suggestions[i][:147] + "..."
                btn.config(text=text_short)

    def on_typing(self, event=None):
        if self.ai is None: return
        context = self.entry_context.get().strip()
        if len(context) < 2: return
        if self.typing_timer is not None: self.typing_timer.cancel()
            
        self.update_status("Status: Generating...", "orange")
        self.typing_timer = Timer(1.0, self.trigger_generation, [context])
        self.typing_timer.start()

    def trigger_generation(self, context):
        Thread(target=self.generate_and_update, args=(context,), daemon=True).start()

    def generate_and_update(self, prompt):
        suggestions = self.ai.generate_suggestions(prompt)
        self.root.after(0, self.update_suggestions_ui, suggestions)
        self.root.after(0, self.update_status, "Status: Ready", "green")

    def hide_window(self):
        # Withdraw hides the window effectively dropping it into the background.
        self.root.withdraw()

    def show_window_and_paste(self, current_clipboard):
        # Reveal the app forcefully
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
        # Update text
        self.entry_context.delete(0, tk.END)
        self.entry_context.insert(0, current_clipboard)
        self.on_typing()

    def log_interaction(self, message, reply):
        try:
            with open("chat_history.txt", "a", encoding="utf-8") as f:
                f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}]\n")
                f.write(f"Friend: {message}\n")
                f.write(f"My Reply: {reply}\n")
                f.write("-" * 40 + "\n")
        except Exception as e:
            print("Logging error:", e)

    def send_suggestion(self, index):
        if self.ai is None:
            return
            
        try:
            text_to_send = self.suggestions[index]
            if text_to_send and text_to_send not in ["(Loading model...)", "(Please wait)", "", "Model Loaded! You can minimize or hide this window.", "Select any WhatsApp message,", "and press Ctrl+C. The Assistant will pop up automatically."]:
                
                self.is_pasting = True
                
                # Copy to clipboard
                pyperclip.copy(text_to_send)
                self.last_clipboard = text_to_send
                
                # Make sure WhatsApp is active if possible
                wa_window = WindowManager.get_whatsapp_window()
                if wa_window:
                    try:
                        if not wa_window.isActive: wa_window.activate()
                        time.sleep(0.3) 
                    except: pass
                else:
                    time.sleep(1)
                
                # Insta paste
                pyautogui.hotkey('ctrl', 'v')
                pyautogui.press('enter')
                
                # Log the history!
                self.log_interaction(self.entry_context.get().strip(), text_to_send)

                # Instantly hide the UI after sending so the user goes back to chatting freely
                self.hide_window()
                
                time.sleep(0.5)
                self.is_pasting = False
        except Exception as e:
            print("Error while sending suggestion:", e)
            traceback.print_exc()

    def monitor_clipboard(self):
        try:
            self.last_clipboard = pyperclip.paste()
        except:
            pass
            
        while self.running:
            if self.is_pasting:
                time.sleep(0.5) 
                continue
                
            try:
                current_clipboard = pyperclip.paste()
                if current_clipboard != self.last_clipboard and len(current_clipboard.strip()) > 0:
                    self.last_clipboard = current_clipboard
                    
                    if WindowManager.is_whatsapp_active():
                        # The thread calls main GUI back cleanly
                        self.root.after(0, self.show_window_and_paste, current_clipboard)
            except Exception:
                pass
            time.sleep(1.0) 

    def on_closing(self):
        # Pressing X will just hide the window, not kill the script
        self.hide_window()

if __name__ == "__main__":
    root = tk.Tk()
    app = WhatsAppAssistantGUI(root)
    # Re-route the cross button to just hide the app
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
