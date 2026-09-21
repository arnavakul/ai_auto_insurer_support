import subprocess
import sys
import time


SERVERS = [
    ("File Agent", "agent.file_agent.a2a.server"),
    ("Verification Agent", "agent.verification_agent.a2a.server"),
    ("Organization Agent", "agent.organizational_agent.a2a.server"),
    ("Cost Agent", "agent.cost_estimate_agent.a2a.server"),
]


processes = []


def start_servers():
    for name, module in SERVERS:
        print(f"Starting {name}...")

        process = subprocess.Popen(
            [sys.executable, "-m", module],
            cwd=".",
        )

        processes.append((name, process))

        time.sleep(1)


def stop_servers():
    print("\nStopping A2A servers...")

    for name, process in processes:
        if process.poll() is None:
            print(f"Stopping {name}...")
            process.terminate()

    for _, process in processes:
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()

    print("All A2A servers stopped.")


if __name__ == "__main__":
    try:
        start_servers()

        print("\nAll A2A servers started.")
        print("Press Ctrl+C to stop all servers.\n")

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        stop_servers()