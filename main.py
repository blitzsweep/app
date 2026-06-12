#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import libraries
import json
import os
import queue
import shlex
import shutil
import signal
import socket
import stat
import subprocess
import sys
import tempfile
import threading
import time

# Import PIP packages
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import QPropertyAnimation
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QAction
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtGui import QIcon
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QCheckBox
from PyQt6.QtWidgets import QComboBox
from PyQt6.QtWidgets import QDialog
from PyQt6.QtWidgets import QDialogButtonBox
from PyQt6.QtWidgets import QFormLayout
from PyQt6.QtWidgets import QGraphicsOpacityEffect
from PyQt6.QtWidgets import QGroupBox
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QHeaderView
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QMenuBar
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QProgressBar
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QScrollArea
from PyQt6.QtWidgets import QSpinBox
from PyQt6.QtWidgets import QTableWidget
from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6.QtWidgets import QTabWidget
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget
from typing import Callable
from typing import cast
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.request import Request
from urllib.request import urlopen

# Define 'VERSION'
VERSION = "v5.1.8"

# Define 'APPNAME'
APPNAME = "BlitzSweep"

# Define 'WEBSITEURL'
WEBSITEURL = "https://neoslab.com"

# Define 'CONFIGPATH'
CONFIGPATH = Path.home() / ".config" / "blitzsweep"

# Define 'CONFIGFILE'
CONFIGFILE = CONFIGPATH / "blitzsweep.conf"

# Define 'USERPATH'
USERPATH = [
    ".cache/babl",
    ".cache/fontconfig",
    ".cache/mesa_shader_cache",
    ".cache/npm",
    ".cache/obexd",
    ".cache/pip",
    ".cache/pnpm",
    ".cache/totem",
    ".cache/tracker3",
    ".cache/ubuntu-report",
    ".cache/yarn",
    ".config/Code/Cache",
    ".config/Code/CachedData",
    ".config/Code/logs",
    ".config/tiling-assistant",
    ".config/QtProject.conf",
    ".dotnet",
    ".gnupg",
    ".java",
    ".local/share/virtualenv",
    ".pki",
    ".profile.bak",
    ".putty",
    ".shell.pre-oh-my-zsh",
    ".thumbnails",
    ".wget-hsts",
    ".zcompdump",
    ".zshrc.bak"
]

# Define 'PROGRAMS' with structure
PROGRAMS = {
    "Android": {
        "paths": [".android", "Android"],
        "configfiles": [],
        "removecontent": ""
    },
    "Cargo": {
        "paths": [".cargo"],
        "configfiles": [".profile", ".zshenv"],
        "removecontent": '. "$HOME/.cargo/env"'
    },
    "BlitzClean": {
        "paths": [".config/blitzclean"],
        "configfiles": [],
        "removecontent": ""
    },
    "Brave": {
        "paths": [".cache/BraveSoftware", ".config/BraveSoftware"],
        "configfiles": [],
        "removecontent": ""
    },
    "Cubic": {
        "paths": [".cache/cubic"],
        "configfiles": [],
        "removecontent": ""
    },
    "Discord": {
        "paths": [".cache/discord", ".config/discord"],
        "configfiles": [],
        "removecontent": ""
    },
    "EasyTag": {
        "paths": [".cache/easytag"],
        "configfiles": [],
        "removecontent": ""
    },
    "Evolution": {
        "paths": [
            ".cache/evolution",
            ".config/evolution",
            ".config/goa-1.0",
            ".local/share/evolution",
            ".local/share/goa-1.0"
        ],
        "configfiles": [],
        "removecontent": ""
    },
    "FileZilla": {
        "paths": [".cache/filezilla", ".config/filezilla"],
        "configfiles": [],
        "removecontent": ""
    },
    "Gimp": {
        "paths": [".cache/gimp", ".config/GIMP"],
        "configfiles": [],
        "removecontent": ""
    },
    "Git": {
        "paths": [
            ".cache/gitstatus",
            ".config/GitKraken",
            ".gitconfig",
            ".gitkraken"
        ],
        "configfiles": [],
        "removecontent": ""
    },
    "Inkscape": {
        "paths": [".cache/inkscape", ".config/inkscape"],
        "configfiles": [],
        "removecontent": ""
    },
    "JetBrains": {
        "paths": [
            ".junie",
            ".cache/JetBrains",
            ".cache/JNA",
            ".config/JetBrains"
        ],
        "configfiles": [],
        "removecontent": ""
    },
    "Kdenlive": {
        "paths": [
            ".cache/kdenlive",
            ".config/kdeglobals",
            ".config/kdenlive-layoutsrc",
            ".config/kdenliverc"
        ],
        "configfiles": [],
        "removecontent": ""
    },
    "Keepassxc": {
        "paths": [".cache/keepassxc", ".config/keepassxc"],
        "configfiles": [],
        "removecontent": ""
    },
    "Mediasane": {
        "paths": [".config/mediasane"],
        "configfiles": [],
        "removecontent": ""
    },
    "Microsoft": {
        "paths": [".cache/Microsoft"],
        "configfiles": [],
        "removecontent": ""
    },
    "Opera": {
        "paths": [".cache/opera", ".config/opera"],
        "configfiles": [],
        "removecontent": ""
    },
    "Proton": {
        "paths": [
            ".cache/Proton AG",
            ".cache/Proton",
            ".cache/protonmail"
        ],
        "configfiles": [],
        "removecontent": ""
    },
    "Rclone": {
        "paths": [".config/rclone", ".config/rclone-browser"],
        "configfiles": [],
        "removecontent": ""
    },
    "Rhythmbox": {
        "paths": [".cache/rhythmbox", ".local/share/rhythmbox"],
        "configfiles": [],
        "removecontent": ""
    },
    "Rustup": {
        "paths": [".rustup"],
        "configfiles": [],
        "removecontent": ""
    },
    "Shotwell": {
        "paths": [".cache/shotwell", ".config/shotwell"],
        "configfiles": [],
        "removecontent": ""
    },
    "Shutter": {
        "paths": [".cache/shutter", ".shutter"],
        "configfiles": [],
        "removecontent": ""
    },
    "SublimeText": {
        "paths": [".cache/sublime-text"],
        "configfiles": [],
        "removecontent": ""
    },
    "Telegram": {
        "paths": [".local/share/TelegramDesktop"],
        "configfiles": [],
        "removecontent": ""
    },
    "Thunderbird": {
        "paths": [".cache/thunderbird"],
        "configfiles": [],
        "removecontent": ""
    },
    "Transmission": {
        "paths": [".cache/transmission", ".config/transmission"],
        "configfiles": [],
        "removecontent": ""
    },
    "TubeReaver": {
        "paths": [".config/tubereaver"],
        "configfiles": [],
        "removecontent": ""
    },
    "VirtualBox": {
        "paths": [
            ".config/virtualbox",
            ".config/VirtualBox",
            "VirtualBox VMs",
            "VirtualBox"
        ],
        "configfiles": [],
        "removecontent": ""
    },
    "VisualCode": {
        "paths": [".cache/vscode"],
        "configfiles": [],
        "removecontent": ""
    }
}

# Define 'USERAGGRESIVE'
USERAGGRESIVE = [
    "snap",
    ".ssh"
]

# Define 'USERBROWSERS'
USERBROWSERS = [
    ".cache/chromium",
    ".cache/google-chrome",
    ".config/BraveSoftware/Brave-Browser/Default/Cache",
    ".config/BraveSoftware/Brave-Browser/Default/Code Cache",
    ".config/chromium/Default/Cache",
    ".config/chromium/Default/Code Cache",
    ".config/google-chrome",
    ".mozilla/firefox/*/cache2",
    ".mozilla/firefox/*/startupCache"
]

# Define 'USERMISCS'
USERMISCS = [
    ".zcompdump-*",
    "~/.var/app/*/cache"
]

# Define 'USERHISTORY'
USERHISTORY = [
    ".bash_history",
    ".cache/recently-used.xbel",
    ".local/share/RecentDocuments",
    ".local/share/recently-used.xbel",
    ".zsh_history"
]

# Define 'ROOTITEMS'
ROOTITEMS = [
    "/root/.cache",
    "/root/.config",
    "/root/.history",
    "/root/.launchpadlib",
    "/root/.wget-hsts",
    "/root/.local/share/flatpak",
    "/root/.ssh"
]

# Define 'SYSDIRS'
SYSDIRS = [
    "/tmp",
    "/var/cache/fontconfig",
    "/var/cache/man",
    "/var/lib/snapd/cache",
    "/var/lib/systemd/coredump",
    "/var/tmp"
]

# Define 'SYSGLOBS'
SYSGLOBS = [
    ("/var/crash", "*.crash"),
    ("/var/log", "*.gz"),
    ("/var/log", "*.[0-9]")
]

# Define 'FileRowCB'
FileRowCB = Callable[[str, int, str], None]


# Class 'SysUtils'
class SysUtils:
    """
    Provides system-level utility functions for file operations.
    Includes methods for checking root privileges and calculating file sizes.
    Handles timestamp formatting and unit conversion for file sizes.
    """

    # Function 'rootcheck'
    @staticmethod
    def rootcheck() -> bool:
        """
        Checks if the current process has root (superuser) privileges.
        Returns True if effective user ID is 0 (root), otherwise False.
        Used to determine if system-wide cleanup operations are permitted.
        """
        return os.geteuid() == 0

    # Function 'unitsize'
    @staticmethod
    def unitsize(numbytes: int) -> str:
        """
        Converts a byte count into a human-readable string with appropriate units.
        Supports units from Bytes up to Yottabytes using 1024-based conversion.
        Returns formatted string like "1.50 MB" or "0.00 Bytes" for invalid input.
        """
        try:
            n = max(0, int(numbytes))
        except (ValueError, TypeError):
            n = 0
        units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
        i = 0
        x = float(n)
        while x >= 1024 and i < len(units) - 1:
            x /= 1024.0
            i += 1
        return f"{x:.2f} {units[i]}"

    # Function 'mtimestring'
    @staticmethod
    def mtimestring(p: Path) -> str:
        """
        Retrieves the last modification timestamp of a file or directory.
        Returns the timestamp as a formatted string (YYYY-MM-DD HH:MM:SS).
        Returns a dash '-' if the file cannot be accessed or doesn't exist.
        """
        try:
            return datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        except (OSError, ValueError, PermissionError, FileNotFoundError):
            return "-"

    # Function 'filesize'
    @staticmethod
    def filesize(p: Path) -> int:
        """
        Calculates total size of a file or directory in bytes.
        For directories, recursively sums sizes of all contained files.
        Returns 0 if the path cannot be accessed or doesn't exist.
        """
        try:
            if p.is_file():
                return p.stat().st_size
            if p.is_dir():
                total = 0
                for child in p.iterdir():
                    try:
                        if child.is_file():
                            total += child.stat().st_size
                    except (OSError, PermissionError, FileNotFoundError):
                        pass
                return total
        except (OSError, PermissionError, FileNotFoundError):
            pass
        return 0


# Class 'ShellExec'
class ShellExec:
    """
    Handles execution of system shell commands with proper error handling.
    Supports dry-run mode and user context switching for command execution.
    Provides both simple command execution and output capture functionality.
    """

    # Function 'cmdrun'
    @staticmethod
    def cmdrun(cmd: str, dryrun: bool) -> int:
        """
        Executes a shell command with optional dry-run mode simulation.
        In dry-run mode, returns 0 without actually executing the command.
        Returns the command's exit code (0 for success, non-zero for failure).
        """
        if dryrun:
            return 0
        try:
            proc = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

            if proc.stdout is not None:
                for _ in iter(proc.stdout.readline, ""):
                    pass
            proc.wait()
            return proc.returncode
        except (OSError, subprocess.SubprocessError):
            return 1

    # Function 'stdcapture'
    @staticmethod
    def stdcapture(cmd: str) -> Tuple[int, str]:
        """
        Executes a command and captures both its stdout and stderr output.
        Returns a tuple containing the exit code and the combined output string.
        Handles CalledProcessError by returning the error code and output.
        """
        try:
            out = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True)
            return 0, out
        except subprocess.CalledProcessError as e:
            return e.returncode, e.output
        except (OSError, subprocess.SubprocessError) as e:
            return 1, str(e)

    # Function 'userexec'
    @staticmethod
    def userexec(username: str, home: str, cmd: str, dryrun: bool) -> int:
        """
        Executes a command as a specific user with their environment variables.
        Attempts multiple methods (unuser, sudo, su) to switch user context.
        Returns 0 on success, 1 if all user switching attempts fail.
        """
        if dryrun:
            return 0
        envprefix = f"HOME={shlex.quote(home)} XDG_DATA_HOME={shlex.quote(os.path.join(home, '.local/share'))} "
        try:
            current = os.environ.get("SUDO_USER") or os.environ.get("USER") or ""
            if os.geteuid() != 0 or current == username:
                return ShellExec.cmdrun(envprefix + cmd, dryrun=False)
        except (OSError, AttributeError):
            pass

        attempts = [
            f"unuser -u {shlex.quote(username)} -- sh -lc {shlex.quote(envprefix + cmd)}",
            f"sudo -u {shlex.quote(username)} sh -lc {shlex.quote(envprefix + cmd)}",
            f"su -s /bin/sh -c {shlex.quote(envprefix + cmd)} {shlex.quote(username)}",
        ]

        for c in attempts:
            rc = ShellExec.cmdrun(c, dryrun=False)
            if rc == 0:
                return 0
        return 1


# Class 'ProcessManager'
class ProcessManager:
    """
    Manages user processes termination before system cleanup operations.
    Identifies and gracefully terminates non-essential user processes.
    Uses SIGTERM first, then SIGKILL for processes that don't terminate.
    """

    # Function 'closetasks'
    @staticmethod
    def closetasks(username: str, excpids: Optional[set] = None, gracesecs: int = 5) -> None:
        """
        Terminates non-critical processes belonging to a specific user.
        Skips essential system processes like Xorg, dbus, and shell components.
        Waits specified grace period before force-killing remaining processes.
        """
        if not username:
            return

        skipnames = {
            "dbus-daemon",
            "gnome-shell",
            "kwin_wayland",
            "kwin_x11",
            "loginctl",
            "pipewire",
            "pipewire-media-session",
            "plasmashell",
            "pulseaudio",
            "python",
            "python3",
            "systemd",
            "wireplumber",
            "Xorg",
            "Xwayland"
        }
        if excpids is None:
            excpids = set()
        excpids.add(os.getpid())
        ec, out = ShellExec.stdcapture(f"ps -u {shlex.quote(username)} -o pid=,comm=")
        if ec != 0 or not out.strip():
            return

        candidates: List[int] = []
        for line in out.splitlines():
            try:
                pstr, comm = line.strip().split(None, 1)
                pid = int(pstr)
                comm = os.path.basename(comm)
            except (ValueError, IndexError):
                continue
            if pid in excpids:
                continue
            if comm in skipnames:
                continue
            if pid == os.getppid():
                continue
            candidates.append(pid)

        for pid in candidates:
            try:
                os.kill(pid, signal.SIGTERM)
            except (ProcessLookupError, PermissionError):
                pass

        time.sleep(max(0, int(gracesecs)))
        for pid in candidates:
            try:
                os.kill(pid, 0)
            except ProcessLookupError:
                continue
            try:
                os.kill(pid, signal.SIGKILL)
            except (ProcessLookupError, PermissionError):
                pass


# Class 'ExecOpts'
@dataclass
class ExecOpts:
    """
    Configuration container for cleanup operation parameters.
    Stores all runtime options including dry-run mode and cleanup categories.
    Provides serialization methods for saving and loading configuration.
    """

    # Define 'dryrun'
    dryrun: bool = False

    # Define 'clearbrowsers'
    clearbrowsers: bool = False

    # Define 'clearkernels'
    clearkernels: bool = False

    # Define 'vacuumdays'
    vacuumdays: int = 7

    # Define 'vacuumsize'
    vacuumsize: str = "100M"

    # Define 'keepsnaps'
    keepsnaps: int = 2

    # Define 'shutafter'
    shutafter: bool = False

    # Define 'username'
    username: str = ""

    # Define 'userhome'
    userhome: str = ""

    # Define 'aggressive'
    aggressive: bool = False

    # Define 'dockercontainers'
    dockercontainers: bool = False

    # Define 'dockerimages'
    dockerimages: bool = False

    # Define 'dockervolumes'
    dockervolumes: bool = False

    # Define 'dockernetworks'
    dockernetworks: bool = False

    # Function 'todict'
    def todict(self) -> dict:
        """
        Converts the ExecOpts instance into a dictionary for serialization.
        Maps each configuration field to its corresponding dictionary key.
        Used for saving configuration to JSON or config files.
        """
        return {
            "dryrun": self.dryrun,
            "clearbrowsers": self.clearbrowsers,
            "clearkernels": self.clearkernels,
            "vacuumdays": self.vacuumdays,
            "vacuumsize": self.vacuumsize,
            "keepsnaps": self.keepsnaps,
            "shutafter": self.shutafter,
            "username": self.username,
            "userhome": self.userhome,
            "aggressive": self.aggressive,
            "dockercontainers": self.dockercontainers,
            "dockerimages": self.dockerimages,
            "dockervolumes": self.dockervolumes,
            "dockernetworks": self.dockernetworks,
        }

    # Function 'fromdict'
    @staticmethod
    def fromdict(d: dict) -> "ExecOpts":
        """
        Creates an ExecOpts instance from a dictionary configuration.
        Applies type conversion and provides safe defaults for missing keys.
        Used for loading saved configuration from storage.
        """
        return ExecOpts(
            dryrun=bool(d.get("dryrun", False)),
            clearbrowsers=bool(d.get("clearbrowsers", False)),
            clearkernels=bool(d.get("clearkernels", False)),
            vacuumdays=int(d.get("vacuumdays,") or d.get("vacuumdays", 7)) if isinstance(d.get("vacuumdays", 7), (str, int)) else 7,
            vacuumsize=str(d.get("vacuumsize", "100M")),
            keepsnaps=int(d.get("keepsnaps", 2)),
            shutafter=bool(d.get("shutafter", False)),
            username=str(d.get("username", "")),
            userhome=str(d.get("userhome", "")),
            aggressive=bool(d.get("aggressive", False)),
            dockercontainers=bool(d.get("dockercontainers", False)),
            dockerimages=bool(d.get("dockerimages", False)),
            dockervolumes=bool(d.get("dockervolumes", False)),
            dockernetworks=bool(d.get("dockernetworks", False)),
        )


# Class 'ConfigManager'
class ConfigManager:
    """
    Handles persistent storage and retrieval of application configuration.
    Reads/writes key-value pairs from/to the configuration file in XDG config directory.
    Manages both user preferences and program-specific cleanup options.
    """

    # Function 'load'
    @staticmethod
    def load() -> dict:
        """
        Loads configuration from the config file into a dictionary.
        Parses each line as key=value pairs, ignoring comments and empty lines.
        Returns an empty dictionary if the config file doesn't exist or is invalid.
        """
        data: Dict[str, str] = {}
        try:
            if CONFIGFILE.is_file():
                for line in CONFIGFILE.read_text(encoding="utf-8").splitlines():
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    data[k.strip()] = v.strip()
        except (OSError, UnicodeDecodeError):
            pass
        return data

    # Function 'save'
    @staticmethod
    def save(opts: ExecOpts, runbootstart: bool, runshutdown: bool, pathopts: Dict[str, bool]):
        """
        Saves application configuration to the config file.
        Includes general options, boot/shutdown flags, and path-specific preferences.
        Creates the config directory if it doesn't already exist.
        """
        try:
            CONFIGPATH.mkdir(parents=True, exist_ok=True)
            lines = [
                f"dryrun={'1' if opts.dryrun else '0'}",
                f"clearbrowsers={'1' if opts.clearbrowsers else '0'}",
                f"clearkernels={'1' if opts.clearkernels else '0'}",
                f"vacuumdays={opts.vacuumdays}",
                f"vacuumsize={opts.vacuumsize}",
                f"keepsnaps={opts.keepsnaps}",
                f"shutafter={'1' if opts.shutafter else '0'}",
                f"username={opts.username}",
                f"userhome={opts.userhome}",
                f"runbootstart={'1' if runbootstart else '0'}",
                f"runshutdown={'1' if runshutdown else '0'}",
                f"aggressive={'1' if opts.aggressive else '0'}",
                f"dockercontainers={'1' if opts.dockercontainers else '0'}",
                f"dockerimages={'1' if opts.dockerimages else '0'}",
                f"dockervolumes={'1' if opts.dockervolumes else '0'}",
                f"dockernetworks={'1' if opts.dockernetworks else '0'}",
            ]

            for k, v in sorted(pathopts.items()):
                lines.append(f"options.{k}={'1' if v else '0'}")
            CONFIGFILE.write_text("\n".join(lines) + "\n", encoding="utf-8")

        except OSError:
            pass


# Class 'UserDiscovery'
class UserDiscovery:
    """
    Discovers and lists all user accounts available on the system.
    Includes root user and all regular users with home directories under /home.
    Sorts users with the current user prioritized at the top of the list.
    """

    # Function 'listusers'
    @staticmethod
    def listusers() -> List[Tuple[str, str]]:
        """
        Returns a list of tuples containing username and home directory path.
        Scans /root and /home directories to identify all system users.
        Sorts results to place the currently logged-in user first.
        """
        users: List[Tuple[str, str]] = []
        if os.path.isdir("/root"):
            users.append(("root", "/root"))
        homedir = Path("/home")

        if homedir.is_dir():
            for child in sorted(homedir.iterdir()):
                if child.is_dir():
                    users.append((child.name, str(child)))

        current = os.environ.get("SUDO_USER") or os.environ.get("USER") or ""
        users.sort(key=lambda t: (t[0] != current, t[0]))
        return users


# Class 'FileOps'
class FileOps:
    """
    Performs file and directory operations with safety checks and callbacks.
    Supports dry-run mode to preview deletions without actually removing files.
    Provides methods for single file, recursive directory, and pattern-based deletions.
    """

    # Function 'emitrow'
    @staticmethod
    def emitrow(cb: FileRowCB, p: Path):
        """
        Emits a file entry to the callback with its size and modification time.
        Calculates size using SysUtils and formats the timestamp appropriately.
        Used for reporting deleted items during cleanup operations.
        """
        size = SysUtils.filesize(p)
        mtime = SysUtils.mtimestring(p)
        cb(str(p), size, mtime)

    # Function 'removefile'
    @staticmethod
    def removefile(path: Path, dryrun: bool, cb: FileRowCB) -> int:
        """
        Removes a single file or symbolic link and reports its size.
        Returns the size of the removed file (or 0 for directories).
        In dry-run mode, only reports the file without actual deletion.
        """
        try:
            if not path.exists():
                return 0
            FileOps.emitrow(cb, path)
            size = path.stat().st_size if path.is_file() else 0

            if dryrun:
                return size
            try:
                if path.is_file() or stat.S_ISLNK(path.stat().st_mode):
                    path.unlink(missing_ok=True)
                else:
                    shutil.rmtree(path, ignore_errors=True)
                    size = 0

            except IsADirectoryError:
                shutil.rmtree(path, ignore_errors=True)
                size = 0
            except PermissionError:
                ShellExec.cmdrun(f"rm -f {shlex.quote(str(path))}", dryrun=False)
            return size
        except (OSError, PermissionError, FileNotFoundError):
            return 0

    # Function 'removetree'
    @staticmethod
    def removetree(path: Path, dryrun: bool, cb: FileRowCB) -> int:
        """
        Recursively removes an entire directory tree and reports total size.
        Calculates cumulative size of all contained files before deletion.
        Returns total bytes freed (or estimated size in dry-run mode).
        """
        try:
            if not path.exists():
                return 0
            total = 0

            for p in path.rglob("*"):
                try:
                    if p.is_file():
                        total += p.stat().st_size
                    elif p.is_dir():
                        pass
                except (OSError, PermissionError, FileNotFoundError):
                    pass

            FileOps.emitrow(cb, path)
            for p in path.rglob("*"):
                FileOps.emitrow(cb, p)
            if dryrun:
                return total
            shutil.rmtree(path, ignore_errors=True)
            return total
        except (OSError, PermissionError, FileNotFoundError):
            return 0

    # Function 'wipedir'
    @staticmethod
    def wipedir(path: Path, dryrun: bool, cb: FileRowCB) -> int:
        """
        Wipes all contents of a directory without removing the directory itself.
        Recursively deletes all files and subdirectories inside the target.
        Returns total bytes freed from all deleted items.
        """
        if not path.exists() or not path.is_dir():
            return 0
        total = 0
        try:
            for item in path.iterdir():
                if item.is_dir():
                    total += FileOps.removetree(item, dryrun, cb)
                else:
                    total += FileOps.removefile(item, dryrun, cb)
            return total
        except (OSError, PermissionError, FileNotFoundError):
            return 0

    # Function 'globaldel'
    @staticmethod
    def globaldel(dirpath: Path, pattern: str, dryrun: bool, cb: FileRowCB) -> int:
        """
        Deletes all files matching a glob pattern within a directory tree.
        Searches recursively through all subdirectories for matching files.
        Returns total size of all deleted files matching the pattern.
        """
        if not dirpath.exists() or not dirpath.is_dir():
            return 0
        total = 0
        try:
            for p in dirpath.rglob(pattern):
                if p.is_file():
                    total += FileOps.removefile(p, dryrun, cb)
                elif dryrun and p.is_dir():
                    FileOps.emitrow(cb, p)
                elif p.is_dir():
                    total += FileOps.removefile(p, dryrun, cb)
            return total
        except (OSError, PermissionError, FileNotFoundError):
            return 0


# Class 'DockerCleaner'
class DockerCleaner:
    """
    Cleans up Docker resources including containers, images, volumes, and networks.
    Executes Docker commands to remove unused or all resources based on options.
    Supports dry-run mode to preview operations without executing them.
    """

    # Function 'clean'
    @staticmethod
    def clean(opts: "ExecOpts") -> None:
        """
        Performs Docker cleanup based on the provided execution options.
        Stops and removes containers, then removes images, volumes, and networks.
        Finally runs system prune to clean up remaining dangling resources.
        """
        dryrun = opts.dryrun
        if opts.dockercontainers:
            ec, out = ShellExec.stdcapture("docker ps -aq")
            if ec == 0 and out.strip():
                ShellExec.cmdrun("docker stop $(docker ps -aq)", dryrun)
                ShellExec.cmdrun("docker rm $(docker ps -aq)", dryrun)

        if opts.dockerimages:
            ec, out = ShellExec.stdcapture("docker images -q")
            if ec == 0 and out.strip():
                ShellExec.cmdrun("docker rmi -f $(docker images -q)", dryrun)

        if opts.dockervolumes:
            ec, out = ShellExec.stdcapture("docker volume ls -q")
            if ec == 0 and out.strip():
                ShellExec.cmdrun("docker volume rm $(docker volume ls -q)", dryrun)

        if opts.dockernetworks:
            ec, out = ShellExec.stdcapture("docker network ls -q")
            if ec == 0 and out.strip():
                ShellExec.cmdrun(
                    "docker network rm $(docker network ls -q | xargs -n1 docker network inspect -f '{{.Name}} {{.ID}}' | grep -v '^bridge ' | grep -v '^host ' | grep -v '^none ' | awk '{print $2}')",
                    dryrun)

        if any([opts.dockercontainers, opts.dockerimages, opts.dockervolumes, opts.dockernetworks]):
            ShellExec.cmdrun("docker system prune -a --volumes -f", dryrun)


# Class 'SysCleaner'
class SysCleaner:
    """
    Core cleanup engine that orchestrates system and user file removal.
    Tracks total bytes freed and supports cancellation via stop flag.
    Handles both system-wide operations and per-user cleanup tasks.
    """

    # Function '__init__'
    def __init__(self, opts: ExecOpts, filecb: FileRowCB, pathopts: Dict[str, bool]):
        """
        Initializes the cleaner with configuration, callback, and path options.
        Sets up tracking variables for bytes freed during cleanup operations.
        Prepares counters for home and root directory cleanup statistics.
        """
        self.opts = opts
        self.filecb = filecb
        self.pathopts = pathopts
        self.totalbytes = 0
        self.frontroot = 0
        self.fronthome = 0
        self.backroot = 0
        self.backhome = 0
        self.stopflag = False

    # Function 'loadstop'
    def loadstop(self):
        """
        Sets the stop flag to request cancellation of ongoing cleanup.
        Called by UI when user clicks the stop button during operation.
        Triggers graceful termination of the cleanup process.
        """
        self.stopflag = True

    # Function 'checkstop'
    def checkstop(self):
        """
        Checks if a stop has been requested and raises exception if true.
        Called at checkpoints during cleanup to enable graceful cancellation.
        Throws RuntimeError to unwind the call stack when stop is requested.
        """
        if self.stopflag:
            raise RuntimeError("Operation cancelled by user.")

    # Function 'addbytes'
    def addbytes(self, n: int):
        """
        Adds bytes to the total counter for freed space tracking.
        Safely handles type conversion and overflow errors.
        Updates running total of reclaimed disk space.
        """
        try:
            self.totalbytes += int(n)
        except (ValueError, TypeError, OverflowError):
            pass

    # Function 'pathkey'
    def pathkey(self, key: str) -> bool:
        """
        Checks whether a specific path or category is enabled for cleanup.
        Returns True if the key is not explicitly disabled in preferences.
        Used to filter which directories and file types to process.
        """
        return self.pathopts.get(key, True)

    # Function 'sumtree'
    @staticmethod
    def sumtree(p: Path) -> int:
        """
        Calculates total size of a directory tree recursively.
        Sums sizes of all files while ignoring permission errors.
        Returns 0 for non-existent paths or files that can't be read.
        """
        total = 0
        try:
            if p.is_file():
                return p.stat().st_size
            if p.is_dir():
                for root, _, files in os.walk(p, onerror=lambda e: None):
                    for fn in files:
                        try:
                            total += Path(root, fn).stat().st_size
                        except (OSError, PermissionError, FileNotFoundError):
                            pass
        except (OSError, PermissionError, FileNotFoundError):
            pass
        return 0

    # Function 'trashlist'
    def trashlist(self, username: str, home: str):
        """
        Empties the trash directory for a specific user.
        Reports sizes of items in trash before emptying.
        Executes trash-empty command to permanently remove deleted files.
        """
        trash_dir = Path(home) / ".local/share/Trash/files"
        if trash_dir.is_dir():
            try:
                for child in sorted(trash_dir.iterdir()):
                    self.checkstop()
                    size = self.sumtree(child)
                    mtime = SysUtils.mtimestring(child)
                    self.filecb(str(child), size, mtime)
                    self.addbytes(size)
            except (OSError, PermissionError, FileNotFoundError):
                pass

        ShellExec.userexec(username=username, home=home, cmd="trash-empty", dryrun=self.opts.dryrun)

    # Function 'useritem'
    def useritem(self, uh: Path, rel: str):
        """
        Deletes a specific user file or directory relative to home.
        Checks if the item is enabled via path options before processing.
        Handles both files and directories with appropriate deletion methods.
        """
        if not self.pathkey(rel):
            return
        p = (uh / rel).expanduser()
        if p.is_dir():
            self.addbytes(FileOps.removetree(p, self.opts.dryrun, self.filecb))
        else:
            self.addbytes(FileOps.removefile(p, self.opts.dryrun, self.filecb))

    # Function 'userpattern'
    def userpattern(self, uh: Path, pat: str):
        """
        Deletes files matching a pattern within a user's home directory.
        Supports wildcards and star patterns for flexible file matching.
        Handles special patterns like /*/ for nested directory traversal.
        """
        if not self.pathkey(pat):
            return
        if pat.startswith("~"):
            base = Path(os.path.expanduser("~"))
            pattern = pat.replace("~/", "")
        else:
            base = uh
            pattern = pat

        if "/*/" in pattern:
            pre, post = pattern.split("/*/", 1)
            basedir = base / pre
            if basedir.is_dir():
                for child in basedir.iterdir():
                    if child.is_dir():
                        tpath = child / post
                        if tpath.exists():
                            if tpath.is_dir():
                                self.addbytes(FileOps.removetree(tpath, self.opts.dryrun, self.filecb))
                            else:
                                self.addbytes(FileOps.removefile(tpath, self.opts.dryrun, self.filecb))
        elif "*" in pattern:
            prefix, suffix = pattern.split("*", 1)
            dirpart = Path(prefix).parent
            namepre = Path(prefix).name
            basedir = base / dirpart
            if basedir.is_dir():
                for child in basedir.iterdir():
                    if child.name.startswith(namepre) and child.name.endswith(suffix):
                        self.addbytes(FileOps.removefile(child, self.opts.dryrun, self.filecb))
        else:
            t = base / pattern
            if t.exists():
                if t.is_dir():
                    self.addbytes(FileOps.removetree(t, self.opts.dryrun, self.filecb))
                else:
                    self.addbytes(FileOps.removefile(t, self.opts.dryrun, self.filecb))

    # Function 'remcargo'
    def remcargo(self, filepath: Path, removecontent: str):
        """
        Removes Cargo environment configuration lines from shell profile files.
        Creates a backup before modifying the file for safety.
        Skips lines containing the specified content to be removed.
        """
        try:
            if self.opts.dryrun:
                self.filecb(f"Would remove Cargo line from {filepath}", 0, "-")
                return

            content = filepath.read_text(encoding='utf-8')
            lines = content.splitlines(keepends=True)

            remlines = []
            for line in lines:
                stripline = line.strip()
                if removecontent.strip() in stripline:
                    if (stripline == removecontent.strip() or
                            stripline.startswith(removecontent.strip())):
                        continue
                remlines.append(line)

            if len(remlines) != len(lines):
                pathbackup = filepath.with_suffix(filepath.suffix + '.blitzsweep.bak')
                try:
                    shutil.copy2(filepath, pathbackup)
                except (OSError, PermissionError):
                    pass

                new_content = ''.join(remlines)
                new_content = new_content.rstrip('\n') + '\n' if new_content.strip() else new_content.rstrip('\n')
                filepath.write_text(new_content, encoding='utf-8')

                try:
                    if pathbackup.exists():
                        pathbackup.unlink()
                except (OSError, PermissionError):
                    pass

                self.filecb(f"Removed Cargo line from {filepath}", 0, "-")

        except (OSError, PermissionError, UnicodeDecodeError) as e:
            self.filecb(f"Failed to process {filepath}: {str(e)}", 0, "-")

    # Function 'cleanuptasks'
    def cleanuptasks(self, uh: Path):
        """
        Cleans up application-specific directories for various programs.
        Processes each program defined in PROGRAMS dictionary.
        Handles special cases like Evolution dconf reset and Cargo config cleanup.
        """
        for program_name, program_data in PROGRAMS.items():
            if not self.pathkey(f"program.{program_name}"):
                continue
            self.checkstop()

            for rel in program_data["paths"]:
                self.checkstop()
                p = (uh / rel).expanduser()
                if p.exists():
                    if p.is_dir():
                        self.addbytes(FileOps.removetree(p, self.opts.dryrun, self.filecb))
                    else:
                        self.addbytes(FileOps.removefile(p, self.opts.dryrun, self.filecb))

            if program_name == "Evolution" and self.pathkey(f"program.{program_name}"):
                self.checkstop()
                if not self.opts.dryrun:
                    ShellExec.cmdrun("dconf reset -f /org/gnome/evolution/", dryrun=False)
                else:
                    self.filecb("dconf reset -f /org/gnome/evolution/", 0, "-")

            if program_name == "Cargo" and self.pathkey(f"program.{program_name}"):
                self.checkstop()
                if program_data["configfiles"] and program_data["removecontent"]:
                    for config_file in program_data["configfiles"]:
                        config_path = uh / config_file
                        if config_path.exists() and config_path.is_file():
                            removecontent = program_data.get("removecontent", "")
                            if isinstance(removecontent, str):
                                self.remcargo(config_path, removecontent)

    # Function 'cleanupuser'
    def cleanupuser(self, uh: Path):
        """
        Performs complete user-level cleanup for a specific home directory.
        Empties trash, removes user paths, histories, browser caches, and misc files.
        Also handles aggressive cleanup options if enabled by user.
        """
        username = Path(uh).name if str(uh) != "/root" else "root"
        self.trashlist(username=username, home=str(uh))

        self.cleanuptasks(uh)
        for rel in USERPATH:
            self.checkstop()
            self.useritem(uh, rel)
        for rel in USERHISTORY:
            self.checkstop()
            self.useritem(uh, rel)
        for pat in USERBROWSERS:
            self.checkstop()
            self.userpattern(uh, pat)
        for pat in USERMISCS:
            self.checkstop()
            self.userpattern(uh, pat)
        for rel in USERAGGRESIVE:
            self.checkstop()
            self.useritem(uh, rel)

    # Function 'cleanupsystem'
    def cleanupsystem(self):
        """
        Performs system-wide cleanup operations requiring root privileges.
        Cleans temporary directories, logs, journal entries, and package caches.
        Removes old kernels, Docker resources, and root-specific configuration files.
        """
        if not SysUtils.rootcheck():
            return

        for d in SYSDIRS:
            if not self.pathkey(d):
                continue
            self.checkstop()
            self.addbytes(FileOps.wipedir(Path(d), self.opts.dryrun, self.filecb))

        for base, pat in SYSGLOBS:
            key = f"{base}::{pat}"
            if not self.pathkey(key):
                continue
            self.checkstop()
            self.addbytes(FileOps.globaldel(Path(base), pat, self.opts.dryrun, self.filecb))

        ShellExec.cmdrun(f"journalctl --vacuum-time={self.opts.vacuumdays}d", self.opts.dryrun)
        ShellExec.cmdrun(f"journalctl --vacuum-size={self.opts.vacuumsize}", self.opts.dryrun)
        ShellExec.cmdrun(f"snap set system refresh.retain={self.opts.keepsnaps}", self.opts.dryrun)
        ShellExec.cmdrun("apt-get -y autoremove --purge", self.opts.dryrun)
        ShellExec.cmdrun("apt-get -y autoclean", self.opts.dryrun)
        ShellExec.cmdrun("apt-get -y clean", self.opts.dryrun)
        ShellExec.cmdrun("flatpak uninstall --unused -y", self.opts.dryrun)

        if not self.opts.dryrun:
            cmd = r"snap list --all 2>/dev/null | awk '/disabled/ {print $1, $3}'"
            ec, out = ShellExec.stdcapture(cmd)
            if ec == 0 and out.strip():
                for line in out.strip().splitlines():
                    parts = line.split()
                    if len(parts) == 2:
                        name, rev = parts
                        ShellExec.cmdrun(f"snap remove --revision={shlex.quote(rev)} {shlex.quote(name)} --purge",
                                         False)

        if self.opts.clearkernels:
            currentkernel = self.kernelused()
            pkgs = self.kernelold(currentkernel)
            for pkg in pkgs:
                ShellExec.cmdrun(f"apt-get remove --purge -y {shlex.quote(pkg)}", self.opts.dryrun)
            ShellExec.cmdrun("update-grub", self.opts.dryrun)

        if any([self.opts.dockercontainers, self.opts.dockerimages, self.opts.dockervolumes, self.opts.dockernetworks]):
            try:
                DockerCleaner.clean(self.opts)
            except (OSError, subprocess.SubprocessError, PermissionError):
                pass

        for p in ROOTITEMS:
            if not self.pathkey(p):
                continue
            self.checkstop()
            rp = Path(p)
            if rp.is_dir():
                self.addbytes(FileOps.wipedir(rp, self.opts.dryrun, self.filecb))
            else:
                self.addbytes(FileOps.removefile(rp, self.opts.dryrun, self.filecb))

    # Function 'kernelused'
    @staticmethod
    def kernelused() -> str:
        """
        Returns the version string of the currently running kernel.
        Removes the -generic suffix for consistent version comparison.
        Used to identify which kernel versions should be preserved during cleanup.
        """
        ec, out = ShellExec.stdcapture("uname -r | sed 's/-generic//'")
        return out.strip() if ec == 0 else ""

    # Function 'kernelold'
    @staticmethod
    def kernelold(basekernel: str) -> List[str]:
        """
        Returns a list of old kernel package names excluding the current kernel.
        Parses dpkg output to identify installed linux-image packages.
        Filters out packages matching the base kernel to keep it safe.
        """
        ec, out = ShellExec.stdcapture("dpkg -l | awk '/^ii\\s+linux-image-[0-9]/{print $2}'")
        pkgs: List[str] = []
        if ec == 0:
            for line in out.strip().splitlines():
                if basekernel and basekernel in line:
                    continue
                pkgs.append(line.strip())
        return pkgs

    # Function 'run'
    def run(self):
        """
        Main execution method that coordinates the entire cleanup process.
        Handles both root and non-root execution contexts appropriately.
        Initiates system shutdown after cleanup if the option is enabled.
        """
        try:
            if SysUtils.rootcheck():
                homes = [("root", "/root")]
                homes.extend(UserDiscovery.listusers())
                seen = set()
                for _, home in homes:
                    if home in seen:
                        continue
                    seen.add(home)
                    self.checkstop()
                    self.cleanupuser(Path(home))
                self.checkstop()
                self.cleanupsystem()
            else:
                self.cleanupuser(Path(self.opts.userhome))
                self.checkstop()
                self.cleanupsystem()
        except RuntimeError:
            pass
        except (OSError, PermissionError, subprocess.SubprocessError, ValueError):
            pass

        if self.opts.shutafter and not self.opts.dryrun:
            ShellExec.cmdrun("shutdown now", False)


# Class 'DialogPrefs'
class DialogPrefs(QDialog):
    """
    Preferences dialog window for configuring cleanup options.
    Provides tabs for general settings and detailed category selection.
    Allows users to enable/disable specific paths and program cleanups.
    """

    # Function '__init__'
    def __init__(self, parent: QWidget, opts: ExecOpts, runbootstart: bool, runshutdown: bool, pathopts: Dict[str, bool]):
        """
        Initializes the preferences dialog with current configuration values.
        Creates tabbed interface with general settings and detailed options.
        Builds checkboxes for all configurable paths and program categories.
        """
        super().__init__(parent)
        self.setWindowTitle("Preferences")
        self.setModal(True)
        self.resize(780, 620)

        self.opts = ExecOpts.fromdict(opts.todict())
        self.execbootstart = bool(runbootstart)
        self.execshutdown = bool(runshutdown)
        self.pathopts = pathopts.copy()
        tabs = QTabWidget(self)

        wgen = QWidget()
        g = QFormLayout(wgen)
        self.cbshutdown = QCheckBox("Shutdown after cleanup")
        self.cbrunboot = QCheckBox("Run at boot")
        self.cbrunshutdown = QCheckBox("Run at shutdown")
        self.spindays = QSpinBox()
        self.spindays.setRange(0, 3650)
        self.editsize = QLineEdit()
        self.spinkeep = QSpinBox()
        self.spinkeep.setRange(1, 10)

        self.cbshutdown.setChecked(self.opts.shutafter)
        self.cbrunboot.setChecked(self.execbootstart)
        self.cbrunshutdown.setChecked(self.execshutdown)
        self.spindays.setValue(self.opts.vacuumdays)
        self.editsize.setText(self.opts.vacuumsize)
        self.spinkeep.setValue(self.opts.keepsnaps)

        g.addRow(self.cbshutdown)
        g.addRow(self.cbrunboot)
        g.addRow(self.cbrunshutdown)
        g.addRow(QLabel("Vacuum days:"), self.spindays)
        g.addRow(QLabel("Vacuum size:"), self.editsize)
        g.addRow(QLabel("Snap revisions:"), self.spinkeep)

        loadopts = QWidget()
        v = QVBoxLayout(loadopts)
        self.chk_map: Dict[str, QCheckBox] = {}

        # Function 'addsection'
        def addsection(title: str, keys: List[str]):
            """
            Creates a grouped section of checkboxes for related configuration items.
            Each checkbox represents a specific path or category that can be enabled/disabled.
            Stores references to checkboxes in a dictionary for later value retrieval.
            """
            box = QGroupBox(title)
            inner = QVBoxLayout(box)
            for k in keys:
                cb = QCheckBox(k)
                cb.setChecked(self.pathopts.get(k, True))
                self.chk_map[k] = cb
                inner.addWidget(cb)
            v.addWidget(box)

        # Function 'addblock'
        def addblock(title: str, programs: Dict[str, dict]):
            """
            Creates a grouped section for program-specific cleanup options.
            Each program gets a checkbox to enable or disable its cleanup.
            Program names are sorted alphabetically for consistent display.
            """
            box = QGroupBox(title)
            inner = QVBoxLayout(box)
            for program_name in sorted(programs.keys()):
                cb = QCheckBox(program_name)
                cb.setChecked(self.pathopts.get(f"program.{program_name}", True))
                self.chk_map[f"program.{program_name}"] = cb
                inner.addWidget(cb)
            v.addWidget(box)

        addblock("Programs", PROGRAMS)
        addsection("User: Paths", USERPATH)
        addsection("User: Histories", USERHISTORY)
        addsection("User: Browsers", USERBROWSERS)
        addsection("User: Miscs", USERMISCS)
        addsection("User: Aggressive (DANGEROUS)", USERAGGRESIVE)
        addsection("Root: Items", ROOTITEMS)
        addsection("System: Directories", SYSDIRS)
        addsection("System: Logs", [f"{base}::{pat}" for base, pat in SYSGLOBS])

        dockerbox = QGroupBox("Docker")
        dockerinner = QVBoxLayout(dockerbox)
        self.cbdockercontainers = QCheckBox("Containers")
        self.cbdockerimages = QCheckBox("Images")
        self.cbdockervolumes = QCheckBox("Volumes")
        self.cbdockernetworks = QCheckBox("Networks")
        self.cbdockercontainers.setChecked(self.opts.dockercontainers)
        self.cbdockerimages.setChecked(self.opts.dockerimages)
        self.cbdockervolumes.setChecked(self.opts.dockervolumes)
        self.cbdockernetworks.setChecked(self.opts.dockernetworks)
        dockerinner.addWidget(self.cbdockercontainers)
        dockerinner.addWidget(self.cbdockerimages)
        dockerinner.addWidget(self.cbdockervolumes)
        dockerinner.addWidget(self.cbdockernetworks)
        v.addWidget(dockerbox)

        scroll = QScrollArea()
        container = QWidget()
        container.setLayout(v)
        scroll.setWidget(container)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        tabs.addTab(wgen, "General")
        tabs.addTab(scroll, "Options")

        btns = QDialogButtonBox(parent=self)
        btnvalid = QPushButton("OK", self)
        btncancel = QPushButton("Cancel", self)
        btns.addButton(btnvalid, QDialogButtonBox.ButtonRole.AcceptRole)
        btns.addButton(btncancel, QDialogButtonBox.ButtonRole.RejectRole)

        btnvalid.clicked.connect(self.accept)
        btncancel.clicked.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addWidget(tabs)
        layout.addWidget(btns)

    # Function 'addvalues'
    def addvalues(self) -> Tuple[ExecOpts, bool, bool, Dict[str, bool]]:
        """
        Retrieves current values from all dialog controls and returns them.
        Collects general settings, Docker options, and path-specific checkboxes.
        Returns a tuple containing updated configuration and path options.
        """
        self.opts.shutafter = self.cbshutdown.isChecked()
        self.execbootstart = self.cbrunboot.isChecked()
        self.execshutdown = self.cbrunshutdown.isChecked()
        self.opts.vacuumdays = self.spindays.value()
        self.opts.vacuumsize = self.editsize.text().strip() or "100M"
        self.opts.keepsnaps = self.spinkeep.value()
        self.opts.dockercontainers = self.cbdockercontainers.isChecked()
        self.opts.dockerimages = self.cbdockerimages.isChecked()
        self.opts.dockervolumes = self.cbdockervolumes.isChecked()
        self.opts.dockernetworks = self.cbdockernetworks.isChecked()

        for k, cb in self.chk_map.items():
            self.pathopts[k] = cb.isChecked()
        return self.opts, self.execbootstart, self.execshutdown, self.pathopts


# Custom 'DialogAbout'
class DialogAbout(QDialog):
    """
    About dialog displaying application information and version details.
    Shows application icon, name, version, website link, and description.
    Provides a simple OK button to close the dialog window.
    """

    # Function '__init__'
    def __init__(self, parent: Optional[QWidget], version: str, website: str):
        """
        Initializes the about dialog with application metadata.
        Attempts to load the application icon from standard system paths.
        Sets up layout with centered text and clickable website link.
        """
        super().__init__(parent)
        self.setWindowTitle(f"About {APPNAME}")
        self.setModal(True)
        self.setMinimumSize(520, 360)

        logolabel = QLabel()
        logolabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logopath = [
            Path("/usr/share/pixmaps/blitzsweep.png")
        ]

        pix: Optional[QPixmap] = None
        for pth in logopath:
            if pth.is_file():
                tmp = QPixmap(str(pth))
                if not tmp.isNull():
                    pix = tmp
                    break

        if pix:
            logolabel.setPixmap(pix.scaled(96, 96, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

        title = QLabel(f"<b>{APPNAME}</b>")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 22px;")

        ver = QLabel(f"Version: {version}")
        ver.setAlignment(Qt.AlignmentFlag.AlignCenter)

        link = QLabel(f'<a href="{website}">{website}</a>')
        link.setAlignment(Qt.AlignmentFlag.AlignCenter)
        link.setTextFormat(Qt.TextFormat.RichText)
        link.setOpenExternalLinks(True)
        msg = QLabel(
            "Ubuntu Cleanup GUI to free space safely\n"
            "Removes caches, logs, and old system files"
        )
        msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        msg.setWordWrap(True)
        msg.setStyleSheet("color: #999;")

        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok, parent=self)
        btns.accepted.connect(self.accept)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)
        layout.addWidget(logolabel)
        layout.addSpacing(10)
        layout.addWidget(title)
        layout.addWidget(ver)
        layout.addWidget(msg)
        layout.addWidget(link)
        layout.addStretch(1)
        layout.addSpacing(10)
        layout.addWidget(btns)


# Custom 'DialogCompleted'
class DialogCompleted(QDialog):
    """
    Dialog shown after cleanup completion with success or error message.
    Displays appropriate icon and message based on operation outcome.
    Provides visual feedback to user about cleanup results.
    """

    # Function '__init__'
    def __init__(self, parent: Optional[QWidget], error_message: Optional[str] = None):
        """
        Initializes completion dialog with success or failure information.
        Loads corresponding icon (success or error) from system paths.
        Sets dialog title and message based on error presence.
        """
        super().__init__(parent)
        self.setWindowTitle("Cleanup Completed" if not error_message else "Cleanup Failed")
        self.setModal(True)
        self.setMinimumSize(420, 280)

        iconlabel = QLabel()
        iconlabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        iconpath = [
            Path("/usr/share/blitzsweep/icons/success.png")
        ] if not error_message else [
            Path("/usr/share/blitzsweep/icons/error.png")
        ]

        pix: Optional[QPixmap] = None
        for pth in iconpath:
            if pth.is_file():
                tmp = QPixmap(str(pth))
                if not tmp.isNull():
                    pix = tmp
                    break
        if pix:
            iconlabel.setPixmap(pix.scaled(96, 96, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

        title = QLabel("<b>Cleanup finished successfully</b>" if not error_message else "<b>Cleanup failed</b>")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        msg = QLabel(
            "All selected files have been removed\n"
            "You can safely close this window"
            if not error_message else
            f"{error_message}\nPlease review logs or try again"
        )
        msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        msg.setWordWrap(True)

        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Close, parent=self)
        btns.rejected.connect(self.reject)
        btns.accepted.connect(self.accept)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        layout.addWidget(iconlabel)
        layout.addSpacing(10)
        layout.addWidget(title)
        layout.addWidget(msg)
        layout.addStretch(1)
        layout.addSpacing(10)
        layout.addWidget(btns)

    # Function 'showcenter'
    def showcenter(self):
        """
        Centers the dialog relative to its parent window before showing.
        Calculates optimal position to place dialog in the middle of parent.
        Executes the dialog modally after positioning.
        """
        self.adjustSize()
        parent_obj = self.parent()
        if isinstance(parent_obj, QWidget):
            parent = cast(QWidget, parent_obj)
            center = parent.geometry().center()
            self.move(center - self.rect().center())
        self.exec()


# Class 'BlitzSweep'
class BlitzSweep(QWidget):
    """
    Main application window for BlitzSweep cleanup tool.
    Provides user interface with user selection, cleanup controls, and results display.
    Manages cleanup operations in background threads with real-time progress updates.
    """

    # Define 'completed'
    completed = pyqtSignal(bool, str)

    # Function '__init__'
    def __init__(self):
        """
        Initializes the main window with menu bar, controls, and table view.
        Sets up user selection combo box with discovered system users.
        Configures timer for batch processing of file deletion updates.
        """
        super().__init__()
        iconpath = Path("/usr/share/pixmaps/blitzsweep.png")
        if iconpath.is_file():
            appicon = QIcon(str(iconpath))
            self.setWindowIcon(appicon)
            appinstance = QApplication.instance()
            if appinstance is not None:
                app = cast(QApplication, appinstance)
                app.setWindowIcon(appicon)

        self.setWindowTitle(f"{APPNAME} {VERSION} - Ubuntu Cleanup GUI")
        self.resize(1000, 720)

        self.workerthread = None
        self.cleaner: Optional[SysCleaner] = None
        self.file_queue: "queue.Queue[Tuple[str, int, str]]" = queue.Queue()

        menubar = QMenuBar(self)
        mfile = menubar.addMenu("File")
        if mfile is not None:
            actquit = QAction("Quit", self)
            actquit.triggered.connect(QApplication.quit)
            mfile.addAction(actquit)

        medit = menubar.addMenu("Edit")
        if medit is not None:
            actprefs = QAction("Preferences", self)
            actprefs.triggered.connect(self.onprefs)
            medit.addAction(actprefs)

        mhelp = menubar.addMenu("Help")
        if mhelp is not None:
            actabout = QAction("About", self)
            actabout.triggered.connect(self.onabout)
            mhelp.addAction(actabout)

        self.cmb_user = QComboBox()
        self.users = UserDiscovery.listusers()
        for u, home in self.users:
            self.cmb_user.addItem(f"{u}  —  {home}", (u, home))

        self.lbltotal = QLabel("Cleared Space\n0.00 MB")
        self.lbltotal.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.lbltotal.setStyleSheet("font-weight: 600;")

        userrow = QHBoxLayout()
        userrow.addWidget(QLabel("User to clean:"))
        userrow.addWidget(self.cmb_user)
        userrow.addStretch()
        userrow.addWidget(self.lbltotal)

        self.btndry = QPushButton("Dry-Run")
        self.btnrun = QPushButton("Run")
        self.btnstop = QPushButton("Stop")
        self.btnstop.setEnabled(False)

        btns = QHBoxLayout()
        btns.addWidget(self.btndry)
        btns.addWidget(self.btnrun)
        btns.addWidget(self.btnstop)
        btns.addStretch()

        self.progress = QProgressBar()
        self.progress.setRange(0, 0)
        self.progress.setVisible(False)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Filepath", "Size", "Modified"])

        header = self.table.horizontalHeader()
        if header is not None:
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(
                1,
                QHeaderView.ResizeMode.ResizeToContents
            )
            header.setSectionResizeMode(
                2,
                QHeaderView.ResizeMode.ResizeToContents
            )

        vertical_header = self.table.verticalHeader()
        if vertical_header is not None:
            vertical_header.setVisible(False)

        self.table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.table.setShowGrid(True)

        root = QVBoxLayout()
        root.setMenuBar(menubar)
        root.addLayout(userrow)
        root.addLayout(btns)
        root.addWidget(self.table, stretch=1)
        root.addWidget(self.progress)
        self.setLayout(root)

        self.btndry.clicked.connect(lambda: self.onrun(dry=True))
        self.btnrun.clicked.connect(lambda: self.onrun(dry=False))
        self.btnstop.clicked.connect(self.onstop)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.flushrows)
        self.timer.start(100)

        self.opts = ExecOpts()
        self.prefsexecbootstart = False
        self.prefsexecshutdown = False
        self.pathopts: Dict[str, bool] = {}
        self.showbytes = 0

        self.confloader()
        self.completed.connect(self.showhandler)
        self.fadeanimation: Optional[QPropertyAnimation] = None

    # Function 'confloader'
    def confloader(self):
        """
        Load persisted configuration values and apply them to controls.
        Reads key=value config, coerces types, and restores check states.
        Also restores saved user selection if present.
        """
        cfg = ConfigManager.load()

        # Function 'loadbool'
        def loadbool(key: str, default: bool = False) -> bool:
            """
            Helper function to convert config string values to boolean.
            Recognizes common true values like '1', 'true', 'True', 'yes'.
            Returns default value if key is not present in configuration.
            """
            return cfg.get(key, "1" if default else "0") in ("1", "true", "True", "yes")

        # Function 'loadstring'
        def loadstring(key: str, default: str = "") -> str:
            """
            Helper function to retrieve string values from configuration.
            Returns default value if the configuration key doesn't exist.
            Used for loading text-based configuration parameters.
            """
            return cfg.get(key, default)

        try:
            self.opts.vacuumdays = int(cfg.get("vacuumdays", "7") or 7)
        except (ValueError, TypeError):
            self.opts.vacuumdays = 7
        self.opts.vacuumsize = loadstring("vacuumsize", "100M")
        try:
            self.opts.keepsnaps = int(cfg.get("keepsnaps", "2") or 2)
        except (ValueError, TypeError):
            self.opts.keepsnaps = 2

        self.opts.shutafter = loadbool("shutafter", False)
        self.opts.clearkernels = loadbool("clearkernels", False)
        self.prefsexecbootstart = loadbool("runbootstart", False)
        self.prefsexecshutdown = loadbool("runshutdown", False)

        self.opts.dockercontainers = loadbool("dockercontainers", False)
        self.opts.dockerimages = loadbool("dockerimages", False)
        self.opts.dockervolumes = loadbool("dockervolumes", False)
        self.opts.dockernetworks = loadbool("dockernetworks", False)

        all_keys = (
            USERPATH
            + USERHISTORY
            + USERBROWSERS
            + USERMISCS
            + USERAGGRESIVE
            + ROOTITEMS
            + SYSDIRS
            + [f"{base}::{pat}" for base, pat in SYSGLOBS]
        )

        for k in all_keys:
            self.pathopts[k] = loadbool(f"options.{k}", True)

        for program_name in PROGRAMS.keys():
            self.pathopts[f"program.{program_name}"] = loadbool(f"options.program.{program_name}", True)

        saved_user = loadstring("username", "")
        for i in range(self.cmb_user.count()):
            u, _ = self.cmb_user.itemData(i)
            if u == saved_user:
                self.cmb_user.setCurrentIndex(i)
                break

    # Function 'confpersist'
    def confpersist(self):
        """
        Saves current configuration to persistent storage.
        Retrieves current user selection and writes all options to config file.
        Called when preferences are changed or before starting cleanup.
        """
        user, home = self.cmb_user.currentData()
        self.opts.username = user
        self.opts.userhome = home
        ConfigManager.save(self.opts, self.prefsexecbootstart, self.prefsexecshutdown, self.pathopts)

    # Function 'filerow'
    def filerow(self, path: str, size_bytes: int, mtime: str):
        """
        Adds a file entry to the queue for table display.
        Called from worker thread to report deleted files.
        Queues items for batch processing in the main thread.
        """
        self.file_queue.put((path, size_bytes, mtime))

    # Function 'flushrows'
    def flushrows(self):
        """
        Processes queued file entries and updates the display table.
        Batches multiple updates to improve UI performance.
        Updates total cleared space counter as items are displayed.
        """
        updated = False
        try:
            while True:
                path, size_b, mtime = self.file_queue.get_nowait()
                r = self.table.rowCount()
                self.table.insertRow(r)
                self.table.setItem(r, 0, QTableWidgetItem(path))
                self.table.setItem(r, 1, QTableWidgetItem(SysUtils.unitsize(size_b)))
                self.table.setItem(r, 2, QTableWidgetItem(mtime))
                try:
                    self.showbytes += int(size_b)
                    updated = True
                except (ValueError, TypeError, OverflowError):
                    pass
        except queue.Empty:
            if updated:
                self.lbltotal.setText(f"Cleared Space\n{SysUtils.unitsize(self.showbytes)}")

    # Function 'onabout'
    def onabout(self):
        """
        Opens the about dialog when menu item is clicked.
        Displays application information and version details.
        Creates and shows modal about dialog window.
        """
        dlg = DialogAbout(self, VERSION, WEBSITEURL)
        dlg.exec()

    # Function 'onprefs'
    def onprefs(self):
        """
        Opens preferences dialog when menu item is clicked.
        Updates configuration with user's changes if dialog is accepted.
        Saves modified preferences to persistent storage.
        """
        dlg = DialogPrefs(self, self.opts, self.prefsexecbootstart, self.prefsexecshutdown, self.pathopts)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            new_opts, boot, shut, popts = dlg.addvalues()
            self.opts = new_opts
            self.prefsexecbootstart = boot
            self.prefsexecshutdown = shut
            self.pathopts = popts
            self.confpersist()

    # Function 'onstop'
    def onstop(self):
        """
        Handles stop button click to cancel running cleanup.
        Signals the cleaner to stop at the next checkpoint.
        Disables stop button to prevent multiple stop requests.
        """
        if self.cleaner:
            self.cleaner.loadstop()
            self.btnstop.setEnabled(False)

    # Function 'onrun'
    def onrun(self, dry: bool):
        """
        Initiates cleanup operation in a background thread.
        Clears previous results and disables buttons during operation.
        Handles both direct execution and privilege-escalated worker processes.
        """
        self.table.setRowCount(0)
        self.showbytes = 0
        self.lbltotal.setText("Cleared Space\n0.00 MB")

        user, home = self.cmb_user.currentData()
        self.opts.username = user
        self.opts.userhome = home
        self.opts.dryrun = dry

        if self.workerthread and self.workerthread.is_alive():
            QMessageBox.warning(self, "Busy", "A cleanup task is already running.")
            return

        self.confpersist()

        if not self.opts.dryrun and self.opts.username and SysUtils.rootcheck():
            try:
                ProcessManager.closetasks(
                    self.opts.username,
                    excpids={os.getpid()},
                    gracesecs=5
                )
            except (OSError, PermissionError, subprocess.SubprocessError, ValueError):
                pass

        self.progress.setVisible(True)
        self.btnstop.setEnabled(True)
        self.btnrun.setEnabled(False)
        self.btndry.setEnabled(False)

        rootneed = (self.opts.username == "root") and not SysUtils.rootcheck()

        # Function 'workload'
        def workload():
            """
            Background thread function that executes the cleanup process.
            Handles privilege escalation via pkexec when needed for root operations.
            Emits completion signal with success status and error message.
            """
            success = True
            errmsg = ""

            try:
                if rootneed:
                    with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as tf:
                        tf.write(json.dumps(self.opts.todict()))
                        tf.flush()
                        optsfile = tf.name

                    try:
                        cmd = [
                            "pkexec",
                            sys.executable,
                            sys.argv[0],
                            "--worker",
                            optsfile
                        ]

                        proc = subprocess.Popen(
                            cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            text=True
                        )

                        if proc.stdout is not None:
                            for line in iter(proc.stdout.readline, ""):
                                if not line:
                                    break

                                line = line.rstrip("\n")

                                if line.startswith("ROW\t"):
                                    parts = line.split("\t", 3)
                                    if len(parts) == 4:
                                        _, path, size_str, mtime = parts
                                        try:
                                            size_b = int(size_str)
                                        except ValueError:
                                            size_b = 0
                                        self.filerow(path, size_b, mtime)

                                elif line.startswith("TOTAL\t"):
                                    parts = line.split("\t", 2)
                                    if len(parts) >= 2:
                                        try:
                                            total_b = int(parts[1])
                                            self.showbytes = total_b
                                            self.lbltotal.setText(
                                                f"Cleared Space\n{SysUtils.unitsize(total_b)}"
                                            )
                                        except (ValueError, TypeError, OverflowError):
                                            pass

                                elif line.startswith("ERROR\t"):
                                    success = False
                                    errmsg = (
                                        line.split("\t", 1)[1]
                                        if "\t" in line
                                        else "Unknown error."
                                    )

                        proc.wait()

                        if proc.returncode != 0:
                            success = False
                            if not errmsg:
                                errmsg = f"Worker exited with code {proc.returncode}."

                    finally:
                        try:
                            os.unlink(optsfile)
                        except OSError:
                            pass

                else:
                    try:
                        cleaner = SysCleaner(self.opts, self.filerow, self.pathopts)
                        self.cleaner = cleaner

                        cleaner.run()
                        self.showbytes = getattr(
                            cleaner,
                            "totalbytes",
                            self.showbytes
                        )
                        self.lbltotal.setText(
                            f"Cleared Space\n{SysUtils.unitsize(self.showbytes)}"
                        )

                    except (
                        OSError,
                        PermissionError,
                        subprocess.SubprocessError,
                        ValueError,
                        RuntimeError
                    ) as e:
                        success = False
                        errmsg = f"{e}"

            finally:
                self.progress.setVisible(False)
                self.btnstop.setEnabled(False)
                self.btnrun.setEnabled(True)
                self.btndry.setEnabled(True)

                try:
                    self.completed.emit(success, errmsg)
                except RuntimeError:
                    pass

        self.workerthread = threading.Thread(target=workload, daemon=True)
        self.workerthread.start()

    # Function 'showhandler'
    def showhandler(self, success: bool, errmsg: str):
        """
        Handles completion signal from worker thread.
        Shows appropriate completion dialog based on success status.
        Initiates fade animation for results table when applicable.
        """
        if self.opts.dryrun:
            return

        dlg = DialogCompleted(self, error_message=(errmsg if not success else None))
        dlg.showcenter()
        self.fadecleaner()

    # Function 'fadecleaner'
    def fadecleaner(self):
        """
        Animates table fade-out after successful cleanup.
        Applies opacity effect and creates fade animation.
        Clears table rows after animation completes.
        """
        if self.table.rowCount() == 0:
            return

        effect = QGraphicsOpacityEffect(self.table)
        self.table.setGraphicsEffect(effect)
        effect.setOpacity(1.0)

        anim = QPropertyAnimation(effect, b"opacity", self)
        anim.setDuration(700)
        anim.setStartValue(1.0)
        anim.setEndValue(0.0)

        # Function 'fadeafter'
        def fadeafter():
            """
            Clears the table and removes opacity effect after animation ends.
            Called when fade animation completes to reset table display.
            Ensures clean state for next cleanup operation.
            """
            self.table.setRowCount(0)
            self.table.setGraphicsEffect(None)

        anim.finished.connect(fadeafter)
        self.fadeanimation = anim
        anim.start()


# Class 'UpdateChecker'
class UpdateChecker:
    """
    Checks for application updates from GitHub releases.
    Compares current version with latest available release.
    Shows notification dialog when newer version is available.
    """

    # Function '__init__'
    def __init__(self, parent: QWidget, appname: str, currvers: str, gitrepo: str, logopaths: Optional[List[Path]] = None):
        """
        Initializes update checker with application metadata and GitHub repository.
        Stores parent widget reference for dialog display.
        Configures paths for loading application icon in notification dialog.
        """
        self.parent = parent
        self.appname = appname
        self.currvers = currvers
        self.gitrepo = gitrepo
        self.logopaths = logopaths or [
            Path(f"/usr/share/pixmaps/{appname.lower()}.png")
        ]

    # Function 'versionparser'
    @staticmethod
    def versionparser(ver: str) -> Tuple[int, ...]:
        """
        Parses version string into tuple of integers for comparison.
        Strips leading 'v' or 'V' characters from version string.
        Returns tuple with parts converted to integers for lexicographic comparison.
        """
        v = ver.strip()
        if v.startswith(("v", "V")):
            v = v[1:]
        parts: List[int] = []
        for part in v.split("."):
            try:
                parts.append(int(part))
            except ValueError:
                break
        return tuple(parts) or (0,)

    # Function 'checknewer'
    def checknewer(self, current: str, latest: str) -> bool:
        """
        Compares two version strings to determine if latest is newer.
        Normalizes version length by padding with zeros.
        Returns True if latest version is greater than current version.
        """
        c = self.versionparser(current)
        l = self.versionparser(latest)
        ln = max(len(c), len(l))
        c = c + (0,) * (ln - len(c))
        l = l + (0,) * (ln - len(l))
        return c < l

    # Function 'checknotify'
    def checknotify(self, timeout: int = 3):
        """
        Checks for updates and shows notification if newer version exists.
        Fetches latest version from GitHub and compares with current.
        Shows update dialog when newer release is available.
        """
        latest = self.fetchtag(timeout=timeout)
        if not latest:
            return
        if not self.checknewer(self.currvers, latest):
            return
        url = f"https://github.com/{self.gitrepo}/releases/tag/{latest}"
        self.showupdate(latest, url)

    # Function 'fetchtag'
    def fetchtag(self, timeout: int = 3) -> Optional[str]:
        """
        Fetches latest release tag name from GitHub API.
        Makes HTTP request with timeout to prevent UI freezing.
        Returns tag name string or None if request fails.
        """
        try:
            url = f"https://api.github.com/repos/{self.gitrepo}/releases/latest"
            req = Request(
                url,
                headers={
                    "Accept": "application/vnd.github+json",
                    "User-Agent": self.appname,
                },
            )
            with urlopen(req, timeout=timeout) as resp:
                data = json.loads(resp.read().decode("utf-8", "ignore"))

            tag = str(data.get("tag_name") or "").strip()
            return tag or None

        except (HTTPError, URLError, socket.timeout, ValueError, OSError):
            return None

    # Function 'showupdate'
    def showupdate(self, latest: str, url: str):
        """
        Displays update notification dialog with version information.
        Shows current version, latest version, and download link.
        Provides OK button to dismiss dialog after reading.
        """
        dlg = QDialog(self.parent)
        dlg.setWindowTitle("Update Available")
        dlg.setModal(True)
        dlg.setMinimumSize(520, 360)

        logolabel = QLabel()
        logolabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        pix: Optional[QPixmap] = None
        for pth in self.logopaths:
            if pth.is_file():
                tmp = QPixmap(str(pth))
                if not tmp.isNull():
                    pix = tmp
                    break
        if pix:
            logolabel.setPixmap(pix.scaled(96, 96, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

        title = QLabel(f"<b>A new version of {self.appname} is available</b>")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px;")

        ver = QLabel(f"Current version {self.currvers}\nLatest version {latest}")
        ver.setAlignment(Qt.AlignmentFlag.AlignCenter)

        msg = QLabel(
            "A newer release is available on GitHub.\n"
            "Please download the latest version from the link below."
        )
        msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        msg.setWordWrap(True)
        msg.setStyleSheet("color: #999;")

        link = QLabel(f'<a href="{url}">{url}</a>')
        link.setAlignment(Qt.AlignmentFlag.AlignCenter)
        link.setTextFormat(Qt.TextFormat.RichText)
        link.setOpenExternalLinks(True)

        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok, parent=dlg)
        btns.accepted.connect(dlg.accept)

        layout = QVBoxLayout(dlg)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)
        layout.addWidget(logolabel)
        layout.addSpacing(10)
        layout.addWidget(title)
        layout.addWidget(ver)
        layout.addWidget(msg)
        layout.addWidget(link)
        layout.addStretch(1)
        layout.addSpacing(10)
        layout.addWidget(btns)
        dlg.exec()


# Class 'AppEntry'
class AppEntry:
    """
    Application entry point handling command-line arguments and execution modes.
    Supports worker mode for privilege-separated cleanup operations.
    Initializes main application window and checks for updates.
    """

    # Function 'main'
    @staticmethod
    def main():
        """
        Main entry point for the BlitzSweep application.
        Parses command line arguments to determine execution mode.
        Starts Qt application, creates main window, and runs event loop.
        """
        if len(sys.argv) == 3 and sys.argv[1] == "--worker":
            opts_path = Path(sys.argv[2])
            data = json.loads(opts_path.read_text(encoding="utf-8"))
            opts = ExecOpts.fromdict(data)

            cfg = ConfigManager.load()
            pathopts: Dict[str, bool] = {}
            all_keys = (
                    USERPATH
                    + USERHISTORY
                    + USERBROWSERS
                    + USERMISCS
                    + USERAGGRESIVE
                    + ROOTITEMS
                    + SYSDIRS
                    + [f"{base}::{pat}" for base, pat in SYSGLOBS]
            )

            for k in all_keys:
                pathopts[k] = cfg.get(f"options.{k}", "1") in ("1", "true", "True", "yes")

            for program_name in PROGRAMS.keys():
                pathopts[f"program.{program_name}"] = cfg.get(f"options.program.{program_name}", "1") in ("1", "true", "True", "yes")

            # Function 'rowcheckbox'
            def rowcheckbox(path: str, size_b: int, mtime: str):
                """
                Callback function for worker mode to report file deletions.
                Outputs tab-separated file information to stdout for parent process.
                Used for real-time progress reporting from privileged worker.
                """
                print(f"ROW\t{path}\t{size_b}\t{mtime}", flush=True)

            cleaner = SysCleaner(opts, rowcheckbox, pathopts)
            try:
                cleaner.run()
                try:
                    print(f"TOTAL\t{int(cleaner.totalbytes)}", flush=True)
                except (ValueError, TypeError, OverflowError):
                    print("TOTAL\t0", flush=True)
                return 0
            except (OSError, PermissionError, subprocess.SubprocessError, ValueError, RuntimeError) as e:
                print(f"ERROR\t{e}", flush=True)
                try:
                    print(f"TOTAL\t{int(getattr(cleaner, 'totalbytes', 0))}", flush=True)
                except (ValueError, TypeError, OverflowError):
                    print("TOTAL\t0", flush=True)
                return 1

        os.environ["QT_LOGGING_RULES"] = "qt.qpa.*=false"
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        app = QApplication(sys.argv)

        if hasattr(QGuiApplication, "setDesktopFileName"):
            QGuiApplication.setDesktopFileName("blitzsweep")

        app.setApplicationName(f"{APPNAME}")
        app.setWindowIcon(QIcon("/usr/share/pixmaps/blitzsweep.png"))

        win = BlitzSweep()
        win.show()
        checker = UpdateChecker(
            parent=win,
            appname=APPNAME,
            currvers=VERSION,
            gitrepo="neoslab/blitzsweep",
            logopaths=[Path("/usr/share/pixmaps/blitzsweep.png")],
        )

        win.updatecheck = checker
        QTimer.singleShot(1500, checker.checknotify)
        sys.exit(app.exec())


# Callback
if __name__ == "__main__":
    AppEntry.main()