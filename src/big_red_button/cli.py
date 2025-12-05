"""Command-line interface for Big Red Button."""

import argparse
import sys
import traceback
from pathlib import Path

from .config import init_config, load_config
from .snapshot import (
    create_snapshot,
    open_email_draft,
    reveal_in_file_manager,
    zip_snapshot,
)


def main() -> None:
    """Main entry point for the snapshot tool."""
    parser = argparse.ArgumentParser(
        description="Performance snapshot tool for creative workstations"
    )
    parser.add_argument(
        "--init-config",
        nargs="?",
        const="config.toml",
        help="Initialize a new configuration file. Optionally specify the path (default: config.toml)",
    )
    args = parser.parse_args()

    if args.init_config:
        init_config(Path(args.init_config))
        sys.exit(0)

    try:
        # Load config
        config = load_config()

        # Create snapshot
        snap_dir = create_snapshot(config)

        # Create ZIP
        zip_path = zip_snapshot(snap_dir)

        print()
        print("=" * 70)
        print(f"Snapshot created: {zip_path}")
        print("=" * 70)
        print()

        # Reveal in file manager
        reveal_in_file_manager(zip_path)

        # Open email client
        open_email_draft(zip_path, config)

        print(
            "Done! Please attach the snapshot ZIP to the email that "
            "just opened."
        )

    except KeyboardInterrupt:
        print("\n\nSnapshot cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nERROR during snapshot: {e}")
        print("Please report this error to IT/support.")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
