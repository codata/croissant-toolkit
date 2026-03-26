import os
import sys
import argparse
import subprocess
import time
import signal

def record_screen(output_path, command=None, duration=None, fps=10, screen_index="1", audio=False, audio_index="none"):
    """
    Records the screen using FFmpeg. 
    If a command is provided, it records until the command finishes.
    If a duration is provided, it records for that length of time.
    """
    print(f"[Photograph] Preparing to record screen to: {output_path}")
    
    # Ensure directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Detect FFmpeg binary
    ffmpeg_bin = "/opt/homebrew/bin/ffmpeg"
    if not os.path.exists(ffmpeg_bin):
        ffmpeg_bin = "ffmpeg" # Fallback to path

    # FFmpeg command for macOS screen capture
    # avfoundation syntax for input is "VideoDeviceIndex:AudioDeviceIndex"
    input_device = screen_index
    if audio:
        input_device = f"{screen_index}:{audio_index}"

    # Base FFmpeg command
    ffmpeg_cmd = [
        ffmpeg_bin, "-y",
        "-f", "avfoundation",
        "-r", str(fps),
        "-i", input_device,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p"
    ]
    
    # Add audio codec if audio is enabled
    if audio:
        ffmpeg_cmd.extend(["-c:a", "aac", "-b:a", "128k"])
    else:
        ffmpeg_cmd.append("-an") # No audio

    ffmpeg_cmd.append(output_path)

    print(f"[Photograph] Starting FFmpeg recording (FPS: {fps})...")
    
    # Start FFmpeg as a background process
    # We use a pseudo-terminal or just pipe stdin so we can send 'q' to stop it cleanly
    process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    try:
        # Give FFmpeg a moment to initialize
        time.sleep(2)
        
        if command:
            print(f"[Photograph] Executing process: {command}")
            # Run the actual process
            start_time = time.time()
            cmd_process = subprocess.run(command, shell=True)
            end_time = time.time()
            print(f"[Photograph] Process finished with exit code {cmd_process.returncode} (Duration: {end_time - start_time:.2f}s)")
        elif duration:
            print(f"[Photograph] Recording for {duration} seconds...")
            time.sleep(duration)
        else:
            print("[Photograph] Recording... Press Ctrl+C to stop.")
            while True:
                time.sleep(1)
                
    except KeyboardInterrupt:
        print("[Photograph] Stop requested by user.")
    except Exception as e:
        print(f"[Photograph] Error during recording: {e}")
    finally:
        print("[Photograph] Stopping recording and finalizing video file...")
        # Send 'q' to FFmpeg to stop it gracefully
        if process.poll() is None:
            try:
                process.stdin.write(b'q')
                process.stdin.flush()
                # Wait for FFmpeg to finish saving
                process.wait(timeout=10)
            except Exception:
                # If 'q' fails, terminate it
                process.terminate()
        
        if os.path.exists(output_path):
            print(f"[Photograph] Recording Complete! [RESULT_PATH]: {os.path.abspath(output_path)}")
            return True
        else:
            print("[Photograph] Error: Recording failed or output file not found.")
            return False

def main():
    parser = argparse.ArgumentParser(description="Record the screen while a process is running.")
    parser.add_argument('--command', '-c', help='The command to execute while recording')
    parser.add_argument('--output', '-o', default='data/recordings/screen_record.mp4', help='Path to save the video')
    parser.add_argument('--duration', '-d', type=float, help='Recording duration in seconds (if no command is provided)')
    parser.add_argument('--fps', type=int, default=10, help='Frames per second')
    parser.add_argument('--screen', '-s', default='1', help='Screen index for video capture (default: 1)')
    parser.add_argument('--audio', '-a', action='store_true', help='Enable audio recording')
    parser.add_argument('--audio-device', default='1', help='Audio device index (default: 1, usually Microphone)')
    parser.add_argument('--list-devices', action='store_true', help='List available capture devices and exit')

    args = parser.parse_args()

    if args.list_devices:
        ffmpeg_bin = "/opt/homebrew/bin/ffmpeg"
        if not os.path.exists(ffmpeg_bin):
            ffmpeg_bin = "ffmpeg"
        subprocess.run([ffmpeg_bin, "-f", "avfoundation", "-list_devices", "true", "-i", ""])
        sys.exit(0)

    # Generate filename if default
    target_output = args.output
    if target_output == 'data/recordings/screen_record.mp4':
        timestamp = int(time.time())
        if not os.path.exists('data/recordings'):
            os.makedirs('data/recordings')
        target_output = f"data/recordings/record_{timestamp}.mp4"

    success = record_screen(
        output_path=target_output,
        command=args.command,
        duration=args.duration,
        fps=args.fps,
        screen_index=args.screen,
        audio=args.audio,
        audio_index=args.audio_device if args.audio else "none"
    )
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
