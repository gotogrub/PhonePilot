import argparse
import asyncio
import sys

from app.core.agent import Agent
from app.device.manager import DeviceManager


async def run_command(command: str, device_id: str | None = None):
    manager = DeviceManager()
    device = await manager.get_device(device_id)

    if not device:
        print("No device found. Check ADB connection.")
        sys.exit(1)

    print(f"Device: {device.device_id}")
    print(f"Command: {command}")
    print("Executing...")

    agent = Agent()
    result = await agent.execute(command=command, device=device)

    if result.success:
        print("Task completed successfully.")
    else:
        print(f"Task failed: {result.error}")

    for action in result.actions:
        print(f"  Step {action['step']}: {action['action']} -> {action['result']}")


def main():
    parser = argparse.ArgumentParser(description="PhonePilot - AI Android Control")
    parser.add_argument("command", nargs="?", help="Command to execute")
    parser.add_argument("-d", "--device", help="Device ID")
    parser.add_argument("-s", "--server", action="store_true", help="Start API server")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)

    args = parser.parse_args()

    if args.server:
        import uvicorn
        uvicorn.run("app.main:app", host=args.host, port=args.port, reload=True)
    elif args.command:
        asyncio.run(run_command(args.command, args.device))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
