#!/usr/bin/env python3
"""
Stellar Blade Menu Background Changer
A mod tool for changing the main menu background video in Stellar Blade PC
Uses RAD Video Tools for proper BK2 conversion

Author: King3881
Version: 1.0.0
Compatible with: Stellar Blade PC Demo/Full Version
"""

import os
import sys
import shutil
import subprocess
import threading
import json
from pathlib import Path

# Enhanced error handling for tkinter import
try:
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk
except ImportError as e:
    print("ERROR: tkinter not found!")
    print("This usually means you need to install Python with tkinter support.")
    print("Please install Python from python.org (make sure to check 'Add Python to PATH')")
    input("Press Enter to exit...")
    sys.exit(1)

# Simple logging function instead of complex Logger class
def log_message(message):
    """Simple logging function"""
    try:
        log_file = os.path.join(os.path.dirname(sys.argv[0]), "stellar_blade_mod.log")
        with open(log_file, "a", encoding='utf-8') as f:
            f.write(f"{message}\n")
        print(message)
    except:
        # If logging fails, just print to console
        print(message)

def setup_logging():
    """Setup simple logging"""
    try:
        log_file = os.path.join(os.path.dirname(sys.argv[0]), "stellar_blade_mod.log")
        # Clear previous log
        with open(log_file, "w", encoding='utf-8') as f:
            f.write("Stellar Blade Mod Tool v1.0.0 - Log started\n")
            f.write(f"Python version: {sys.version}\n")
            f.write(f"Working directory: {os.getcwd()}\n")
            f.write("-" * 50 + "\n")
    except:
        pass  # If logging setup fails, continue without logging

class StellarBladeModTool:
    def __init__(self):
        log_message("Initializing Stellar Blade Mod Tool...")
        try:
            self.root = tk.Tk()
            self.root.title("Stellar Blade Menu Background Changer v1.0.0")
            self.root.geometry("650x600")
            self.root.minsize(650, 500)  # Set minimum size

            # Center the window
            self.root.update_idletasks()
            x = (self.root.winfo_screenwidth() // 2) - (700 // 2)
            y = (self.root.winfo_screenheight() // 2) - (600 // 2)
            self.root.geometry(f"650x600+{x}+{y}")

            log_message("Tkinter window created successfully")
        except Exception as e:
            log_message(f"ERROR creating main window: {e}")
            messagebox.showerror("Initialization Error", f"Failed to create main window: {e}")
            sys.exit(1)

        # Default paths
        self.default_game_path = r"C:\Program Files (x86)\Steam\steamapps\common\StellarBladeDemo"
        self.default_rad_path = r"C:\Program Files (x86)\RADVideo"
        self.movies_path = ""
        self.backup_path = ""
        self.rad_tools_path = ""

        # Load configuration
        self.config_file = "sb_mod_config.json"

        try:
            self.load_config()
            log_message("Configuration loaded")
        except Exception as e:
            log_message(f"Warning: Could not load config: {e}")

        try:
            self.setup_ui()
            log_message("UI setup completed")
        except Exception as e:
            log_message(f"ERROR setting up UI: {e}")
            messagebox.showerror("UI Error", f"Failed to setup user interface: {e}")
            sys.exit(1)

        try:
            self.check_dependencies()
            log_message("Dependencies checked")
        except Exception as e:
            log_message(f"Warning: Dependency check failed: {e}")

    def load_config(self):
        """Load saved configuration"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                self.default_game_path = config.get('game_path', self.default_game_path)
                self.default_rad_path = config.get('rad_path', self.default_rad_path)
                log_message(f"Config loaded: game_path={self.default_game_path}, rad_path={self.default_rad_path}")
        except Exception as e:
            log_message(f"Error loading config: {e}")

    def save_config(self):
        """Save current configuration"""
        try:
            config = {
                'game_path': self.default_game_path,
                'rad_path': self.default_rad_path
            }
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            log_message(f"Error saving config: {e}")

    def setup_ui(self):
        """Setup the user interface"""
        # Create main container with scrollable frame
        main_container = tk.Frame(self.root)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Title section (fixed at top)
        title_frame = tk.Frame(main_container)
        title_frame.pack(fill="x", pady=(0, 10))

        title_label = tk.Label(title_frame, text="Stellar Blade Menu Background Changer", 
                              font=("Arial", 16, "bold"))
        title_label.pack()

        subtitle_label = tk.Label(title_frame, text="Replace EVE_Title.bk2 with your custom video", 
                                 font=("Arial", 10))
        subtitle_label.pack()

        version_label = tk.Label(title_frame, text="v1.0.0", 
                                font=("Arial", 9), fg="blue")
        version_label.pack()

        # Scrollable content area
        canvas = tk.Canvas(main_container)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack scrollable components
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Game path section
        path_frame = tk.LabelFrame(scrollable_frame, text="Game Installation Path", padx=10, pady=10)
        path_frame.pack(fill="x", padx=10, pady=10)

        self.path_var = tk.StringVar(value=self.default_game_path)
        path_entry = tk.Entry(path_frame, textvariable=self.path_var, width=70)
        path_entry.pack(side="left", fill="x", expand=True)

        path_browse_btn = tk.Button(path_frame, text="Browse", command=self.browse_game_path)
        path_browse_btn.pack(side="right", padx=(5, 0))

        # RAD Video Tools path section
        rad_frame = tk.LabelFrame(scrollable_frame, text="RAD Video Tools Path", padx=10, pady=10)
        rad_frame.pack(fill="x", padx=10, pady=10)

        self.rad_var = tk.StringVar(value=self.default_rad_path)
        rad_entry = tk.Entry(rad_frame, textvariable=self.rad_var, width=70)
        rad_entry.pack(side="left", fill="x", expand=True)

        rad_browse_btn = tk.Button(rad_frame, text="Browse", command=self.browse_rad_path)
        rad_browse_btn.pack(side="right", padx=(5, 0))

        # Progress bar
        self.progress_frame = tk.Frame(scrollable_frame)
        self.progress_frame.pack(fill="x", padx=10, pady=10)

        self.progress = ttk.Progressbar(self.progress_frame, mode='indeterminate')
        self.progress_label = tk.Label(self.progress_frame, text="")

        # Buttons section
        button_frame = tk.Frame(scrollable_frame)
        button_frame.pack(fill="x", padx=10, pady=20)

        # First row of buttons
        button_row1 = tk.Frame(button_frame)
        button_row1.pack(fill="x", pady=(0, 10))

        self.convert_btn = tk.Button(button_row1, text="Video Conversion", 
                                    command=self.start_conversion, bg="#4CAF50", fg="white",
                                    font=("Arial", 11, "bold"), padx=15, pady=8)
        self.convert_btn.pack(side="left", padx=(0, 10))

        self.use_file_btn = tk.Button(button_row1, text="Use Converted File", 
                                     command=self.use_converted_file, bg="#2196F3", fg="white",
                                     font=("Arial", 11, "bold"), padx=15, pady=8)
        self.use_file_btn.pack(side="left", padx=(0, 10))

        self.restore_btn = tk.Button(button_row1, text="Restore Original", 
                                    command=self.restore_original, bg="#FF9800", fg="white",
                                    font=("Arial", 11, "bold"), padx=15, pady=8)
        self.restore_btn.pack(side="left", padx=(0, 10))


        # Status section
        status_frame = tk.Frame(scrollable_frame)
        status_frame.pack(fill="x", padx=10, pady=10)

        self.status_label = tk.Label(status_frame, text="Ready", fg="green", font=("Arial", 10, "bold"))
        self.status_label.pack()

        # Instructions section (now fully visible and expandable)
        instructions_frame = tk.LabelFrame(scrollable_frame, text="Instructions", padx=10, pady=10)
        instructions_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Create text widget with scrollbar
        text_container = tk.Frame(instructions_frame)
        text_container.pack(fill="both", expand=True)

        instructions_text = tk.Text(text_container, height=15, wrap="word", font=("Arial", 9))
        text_scrollbar = ttk.Scrollbar(text_container, orient="vertical", command=instructions_text.yview)
        instructions_text.configure(yscrollcommand=text_scrollbar.set)

        instructions_text.pack(side="left", fill="both", expand=True)
        text_scrollbar.pack(side="right", fill="y")

        instructions = """REQUIREMENTS (MUST INSTALL FIRST):
1. Download and install RAD Video Tools from: https://www.radgametools.com/down/Bink/RADTools.7z
2. Extract and install to C:\Program Files (x86)\RADVideo (default location)

OPTION 1 - GUIDED CONVERSION:
1. Set your Stellar Blade installation path (usually auto-detected)
2. Verify RAD Video Tools path is correct
3. Click "Start Video Conversion" - this will:
   • Launch RAD Video Tools
   • Show you step-by-step instructions
   • Guide you through the conversion process
4. Follow the detailed instructions shown in the popup dialog

OPTION 2 - USE EXISTING CONVERTED FILE:
1. If you already have a converted BK2 file, click "Use Converted File"
2. Browse and select your pre-converted EVE_Title.bk2 file
3. The mod will install it directly without needing RAD Video Tools

CONVERSION STEPS (for Option 1):
1. RAD Video Tools will open
2. Load your MP4 video file (Click "Browse" in RAD Video Tools)
3. Click "Bink it!" to open conversion dialog
4. Set these conversion settings:
   • Output format: "Bink 2"
5. Click "Browse" for output location and save as "EVE_Title.bk2"
6. Click "Bink" to start conversion
7. Wait for conversion to complete (may take several minutes)
8. Close RAD Video Tools
9. Click "Conversion Complete" in this app

RESTORE ORIGINAL:
• Use "Restore Original" to revert back to the default background
• This restores from the automatically created backup

NOTES:
• Video should ideally be 1920x1080 resolution for best results
• Keep video length reasonable (30-60 seconds recommended)
• RAD Video Tools is REQUIRED for proper BK2 conversion
• Original file will be automatically backed up as "EVE_Title_original.bk2"
• Always backup your save files before modding!
• If conversion fails, try reducing video quality/resolution in RAD Video Tools

TROUBLESHOOTING:
• If RAD Video Tools won't launch, try running this app as Administrator
• If converted video shows black screen in game, the BK2 conversion may have failed
• Try different video formats (MP4 with H.264 codec works best)
• Ensure your video file isn't corrupted before conversion"""

        instructions_text.insert("1.0", instructions)
        instructions_text.config(state="disabled")

        # Enable mouse wheel scrolling for canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def check_dependencies(self):
        """Check if RAD Video Tools is available"""
        log_message("Checking for RAD Video Tools...")
        rad_found = False

        # Try to find RAD Video Tools
        rad_paths = [
            self.default_rad_path,
            os.path.join(self.default_rad_path, "radvideo64.exe"),
            os.path.join(self.default_rad_path, "radvideo32.exe"),
            r"C:\Program Files\RADVideo\radvideo64.exe",
            r"C:\Program Files\RADVideo\radvideo32.exe",
            os.path.join(os.getcwd(), "radvideo64.exe"),
            os.path.join(os.getcwd(), "radvideo32.exe")
        ]

        for path in rad_paths:
            if os.path.isdir(path):
                # Check for executables in directory
                for exe in ["radvideo64.exe", "radvideo32.exe"]:
                    exe_path = os.path.join(path, exe)
                    if os.path.exists(exe_path):
                        self.rad_tools_path = exe_path
                        rad_found = True
                        log_message(f"RAD Video Tools found at: {exe_path}")
                        break
            elif os.path.exists(path) and path.endswith('.exe'):
                self.rad_tools_path = path
                rad_found = True
                log_message(f"RAD Video Tools found at: {path}")
                break

            if rad_found:
                break

        if rad_found:
            self.status_label.config(text="Ready - RAD Video Tools detected", fg="green")
        else:
            self.status_label.config(text="WARNING: RAD Video Tools not found!", fg="red")
            self.show_rad_tools_warning()

    def show_rad_tools_warning(self):
        """Show warning about missing RAD Video Tools"""
        warning_msg = (
            "RAD Video Tools is REQUIRED for video conversion!\n\n"
            "You can still use the 'Use Converted File' option if you have a pre-converted BK2 file.\n\n"
            "To enable video conversion, please download and install RAD Video Tools from:\n"
            "https://www.radgametools.com/down/Bink/RADTools.7z\n\n"
            "Extract and install to: C:\\Program Files (x86)\\RADVideo\n"
            "Then restart this tool."
        )

        messagebox.showwarning("RAD Video Tools Required", warning_msg)

    def browse_game_path(self):
        """Browse for game installation directory"""
        path = filedialog.askdirectory(title="Select Stellar Blade Installation Directory",
                                      initialdir=os.path.dirname(self.default_game_path))
        if path:
            self.path_var.set(path)
            self.default_game_path = path
            self.save_config()

    def browse_rad_path(self):
        """Browse for RAD Video Tools directory"""
        path = filedialog.askdirectory(title="Select RAD Video Tools Installation Directory",
                                      initialdir=self.default_rad_path)
        if path:
            self.rad_var.set(path)
            self.default_rad_path = path
            self.save_config()
            # Re-check dependencies
            self.check_dependencies()

    def validate_paths(self):
        """Validate game path and create necessary paths"""
        game_path = self.path_var.get()

        # Check if game directory exists
        if not os.path.exists(game_path):
            messagebox.showerror("Error", f"Game directory not found:\n{game_path}")
            return False

        # Check for Movies folder
        self.movies_path = os.path.join(game_path, "SB", "Content", "Movies")
        if not os.path.exists(self.movies_path):
            messagebox.showerror("Error", 
                                f"Movies directory not found:\n{self.movies_path}\n\n"
                                "Please ensure you've selected the correct Stellar Blade installation directory.")
            return False

        # Create backup directory
        self.backup_path = os.path.join(os.getcwd(), "backups")
        os.makedirs(self.backup_path, exist_ok=True)

        return True

    def show_progress(self, text):
        """Show progress bar and text"""
        self.progress_label.config(text=text)
        self.progress_label.pack()
        self.progress.pack(fill="x", pady=(0, 5))
        self.progress.start()
        self.root.update()

    def hide_progress(self):
        """Hide progress bar"""
        self.progress.stop()
        self.progress.pack_forget()
        self.progress_label.pack_forget()
        self.root.update()

    def use_converted_file(self):
        """Use an already converted BK2 file"""
        if not self.validate_paths():
            return

        # Browse for BK2 file
        bk2_file = filedialog.askopenfilename(
            title="Select your converted BK2 file",
            filetypes=[
                ("BK2 files", "*.bk2"),
                ("All files", "*.*")
            ],
            initialdir=os.getcwd()
        )

        if not bk2_file:
            return

        if not os.path.exists(bk2_file):
            messagebox.showerror("Error", "Selected file does not exist.")
            return

        # Confirm installation
        confirm_msg = (
            f"Selected file: {os.path.basename(bk2_file)}\n"
            f"Size: {os.path.getsize(bk2_file) / (1024*1024):.1f} MB\n\n"
            f"This will replace the current menu background.\n"
            f"The original file will be backed up.\n\n"
            f"Continue with installation?"
        )

        if not messagebox.askyesno("Confirm Installation", confirm_msg):
            return

        # Run installation in separate thread
        threading.Thread(target=self._install_converted_file, args=(bk2_file,), daemon=True).start()

    def _install_converted_file(self, bk2_file):
        """Install a pre-converted BK2 file"""
        try:
            self.show_progress("Backing up original file...")

            # Backup original file
            original_file = os.path.join(self.movies_path, "EVE_Title.bk2")
            backup_file = os.path.join(self.backup_path, "EVE_Title_original.bk2")

            if os.path.exists(original_file) and not os.path.exists(backup_file):
                shutil.copy2(original_file, backup_file)
                log_message(f"Original file backed up to: {backup_file}")

            self.show_progress("Installing converted file...")

            # Install the converted file
            final_output = os.path.join(self.movies_path, "EVE_Title.bk2")
            shutil.copy2(bk2_file, final_output)

            self.hide_progress()
            self.status_label.config(text="Converted file installed successfully!", fg="green")

            success_msg = (
                "Converted BK2 file installed successfully!\n\n"
                "Launch Stellar Blade to see your new menu background.\n"
                f"Original file backed up to: {backup_file}\n\n"
                "If the video doesn't work properly, the BK2 file may not be properly converted."
            )

            messagebox.showinfo("Success", success_msg)

        except Exception as e:
            self.hide_progress()
            self.status_label.config(text="Installation failed", fg="red")
            messagebox.showerror("Error", f"Installation failed:\n{str(e)}")

    def start_conversion(self):
        """Start the video conversion process"""
        if not self.rad_tools_path:
            messagebox.showerror("Error", 
                                "RAD Video Tools not found!\n\n"
                                "Please install RAD Video Tools first:\n"
                                "https://www.radgametools.com/down/Bink/RADTools.7z\n\n"
                                "Or use 'Use Converted File' if you already have a BK2 file.")
            return

        if not self.validate_paths():
            return

        # Show confirmation dialog with detailed instructions
        output_path = os.path.join(self.backup_path, "EVE_Title.bk2")

        instruction_msg = (
            f"Ready to start video conversion process!\n\n"
            f"This will:\n"
            f"1. Backup your original EVE_Title.bk2 file\n"
            f"2. Launch RAD Video Tools for you to convert your video\n"
            f"3. Install the converted file when you're done\n\n"
            f"Output location: {output_path}\n\n"
            f"Continue?"
        )

        if not messagebox.askyesno("Start Conversion", instruction_msg):
            return

        # Run conversion process in separate thread
        threading.Thread(target=self._conversion_thread, daemon=True).start()

    def _conversion_thread(self):
        """Conversion thread with step-by-step guidance"""
        try:
            self.show_progress("Backing up original file...")

            # Backup original file
            original_file = os.path.join(self.movies_path, "EVE_Title.bk2")
            backup_file = os.path.join(self.backup_path, "EVE_Title_original.bk2")

            if os.path.exists(original_file) and not os.path.exists(backup_file):
                shutil.copy2(original_file, backup_file)
                log_message(f"Original file backed up to: {backup_file}")

            self.hide_progress()

            # Launch RAD Video Tools
            log_message(f"Launching RAD Video Tools: {self.rad_tools_path}")

            try:
                # Try different launch methods
                subprocess.Popen([self.rad_tools_path])
                log_message("RAD Video Tools launched successfully")
            except Exception as e:
                log_message(f"Standard launch failed, trying alternative method: {e}")
                try:
                    subprocess.Popen([self.rad_tools_path], shell=True)
                    log_message("RAD Video Tools launched with shell=True")
                except Exception as e2:
                    log_message(f"Shell launch also failed: {e2}")
                    raise Exception(f"Could not launch RAD Video Tools: {e2}")

            # Show detailed conversion instructions
            output_path = os.path.join(self.backup_path, "EVE_Title.bk2")

            instruction_msg = (
                f"RAD Video Tools has been launched!\n\n"
                f"Please follow these steps EXACTLY:\n\n"
                f"1. In RAD Video Tools, click 'Browse' to select your MP4 video file\n"
                f"2. Click 'Bink it!' button\n"
                f"3. In the conversion dialog:\n"
                f"   • Set output format to 'Bink 2'\n"
                f"4. Click 'Browse' for output location and save as:\n"
                f"   {output_path}\n"
                f"5. Click 'Bink' to start conversion\n"
                f"6. Wait for conversion to complete\n"
                f"7. Close RAD Video Tools\n"
                f"8. Click 'Conversion Complete' below\n\n"
                f"IMPORTANT: Save the output file exactly as shown above!"
            )

            result = messagebox.askokcancel("Conversion Instructions", instruction_msg)

            if not result:
                self.status_label.config(text="Conversion cancelled", fg="orange")
                return

            # Check if conversion was successful
            if not os.path.exists(output_path):
                retry_msg = (
                    f"Output file not found at:\n{output_path}\n\n"
                    f"Please make sure you saved the converted file to the exact location shown.\n"
                    f"Would you like to browse for the converted file manually?"
                )

                if messagebox.askyesno("File Not Found", retry_msg):
                    converted_file = filedialog.askopenfilename(
                        title="Select your converted BK2 file",
                        filetypes=[("BK2 files", "*.bk2"), ("All files", "*.*")],
                        initialdir=self.backup_path
                    )

                    if converted_file and os.path.exists(converted_file):
                        # Copy to expected location
                        shutil.copy2(converted_file, output_path)
                        log_message(f"Manually selected file copied to: {output_path}")
                    else:
                        raise Exception("No valid converted file selected")
                else:
                    raise Exception("Conversion output file not found")

            self.show_progress("Installing new background...")

            # Install the converted file
            final_output = os.path.join(self.movies_path, "EVE_Title.bk2")
            shutil.copy2(output_path, final_output)

            self.hide_progress()
            self.status_label.config(text="Mod installed successfully!", fg="green")

            success_msg = (
                "Custom background installed successfully!\n\n"
                "Launch Stellar Blade to see your new menu background.\n"
                f"Original file backed up to: {backup_file}\n\n"
                "Note: The new BK2 file was created using RAD Video Tools for proper game compatibility."
            )

            messagebox.showinfo("Success", success_msg)

        except Exception as e:
            self.hide_progress()
            self.status_label.config(text="Installation failed", fg="red")
            messagebox.showerror("Error", f"Installation failed:\n{str(e)}")

    def restore_original(self):
        """Restore the original background"""
        if not self.validate_paths():
            return

        backup_file = os.path.join(self.backup_path, "EVE_Title_original.bk2")

        if not os.path.exists(backup_file):
            messagebox.showerror("Error", "Original backup file not found.\n"
                                "Cannot restore original background.")
            return

        if not messagebox.askyesno("Confirm Restore", 
                                  "This will restore the original menu background.\n"
                                  "Continue?"):
            return

        try:
            original_file = os.path.join(self.movies_path, "EVE_Title.bk2")
            shutil.copy2(backup_file, original_file)

            self.status_label.config(text="Original background restored!", fg="green")
            messagebox.showinfo("Success", "Original background restored successfully!")

        except Exception as e:
            self.status_label.config(text="Restore failed", fg="red")
            messagebox.showerror("Error", f"Restore failed:\n{str(e)}")

    def run(self):
        """Run the application"""
        self.root.mainloop()

def main():
    """Main function with enhanced error handling"""
    print("=" * 60)
    print("Stellar Blade Menu Background Changer v1.0.0")
    print("Expandable GUI + Use Converted File option!")
    print("=" * 60)

    # Setup logging
    setup_logging()

    try:
        log_message("Creating application instance...")
        app = StellarBladeModTool()
        log_message("Starting application...")
        app.run()
    except KeyboardInterrupt:
        log_message("Application interrupted by user")
    except Exception as e:
        log_message(f"FATAL ERROR: {e}")
        log_message(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()

        # Show error dialog if possible
        try:
            if 'tk' in globals():
                root = tk.Tk()
                root.withdraw()  # Hide main window
                messagebox.showerror("Fatal Error", 
                                    f"Application crashed with error:\n\n{e}\n\n"
                                    f"Please check the log file: stellar_blade_mod.log")
        except:
            pass

        input("\nPress Enter to exit...")
    finally:
        log_message("Application ended")

if __name__ == "__main__":
    main()
