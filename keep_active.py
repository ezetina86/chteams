import time
import sys
import subprocess

def run_applescript(script):
    """Run an AppleScript command."""
    subprocess.run(['osascript', '-e', script], capture_output=True)

def keep_teams_active():
    print("Teams Active Script v3 (AppleScript Edition) started.")
    print("This script will focus Teams every 4 minutes and simulate activity.")
    print("Press Ctrl+C to stop.")

    # caffeinate prevents system sleep
    try:
        caf_proc = subprocess.Popen(['caffeinate', '-di'])
        print("System 'caffeinate' activated.")
    except FileNotFoundError:
        caf_proc = None

    try:
        while True:
            print(f"\n[{time.strftime('%H:%M:%S')}] Activating Teams...")
            
            # AppleScript to:
            # 1. Activate Teams
            # 2. Tell it to simulate a keystroke (Command + 1 goes to Activity tab, which is safe)
            script = '''
            tell application "Microsoft Teams"
                activate
            end tell
            delay 1
            tell application "System Events"
                keystroke "1" using {command down}
            end tell
            '''
            run_applescript(script)
            
            # Wait 4 minutes (Teams typically times out at 5 minutes)
            for _ in range(240):
                sys.stdout.write('.')
                sys.stdout.flush()
                time.sleep(1)
                
    except KeyboardInterrupt:
        if caf_proc:
            caf_proc.terminate()
        print("\nScript stopped.")

if __name__ == "__main__":
    keep_teams_active()
