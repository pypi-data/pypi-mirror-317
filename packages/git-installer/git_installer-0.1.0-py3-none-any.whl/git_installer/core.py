import logging
import os
import shutil
import subprocess
import sys
import requests


class GitInstaller:

    WINDOWS_GITHUB_RELEASES_API = "https://api.github.com/repos/git-for-windows/git/releases/latest"

    @staticmethod
    def check_git_installed():
        """Check if Git is installed."""
        if shutil.which("git"):
            logging.info("Git is installed.")
            return True
        else:
            logging.warning("Git is not installed.")
            return False

    @staticmethod
    def get_latest_git_installer_url():
        """Get the URL of the latest Git installer."""
        try:
            logging.info(f"Fetching latest Git installer URL from {GitInstaller.WINDOWS_GITHUB_RELEASES_API}")
            response = requests.get(GitInstaller.WINDOWS_GITHUB_RELEASES_API, timeout=10)
            response.raise_for_status()
            release_data = response.json()

            for asset in release_data.get("assets", []):
                if asset["name"].endswith("64-bit.exe"):
                    logging.info(f"Found installer: {asset['name']}")
                    return asset["browser_download_url"]

            raise RuntimeError("No 64-bit Git installer found in the release data.")
        except requests.RequestException:
            logging.error("Failed to fetch the latest Git installer URL", exc_info=True)
            raise
        except (KeyError, ValueError):
            logging.error(f"Invalid response structure from the GitHub API.", exc_info=True)
            raise

    @staticmethod
    def download_git_installer():
        """Download the latest Git installer."""
        try:
            installer_url = GitInstaller.get_latest_git_installer_url()
            installer_path = "git_installer.exe"
            logging.info(f"Downloading Git installer from {installer_url}...")
            response = requests.get(installer_url, stream=True, timeout=30)
            response.raise_for_status()
            with open(installer_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            logging.info(f"Installer saved at {installer_path}.")
            return installer_path
        except requests.RequestException:
            logging.error("Failed to download Git installer", exc_info=True)
            raise
        except OSError:
            logging.error("File I/O error while saving installer", exc_info=True)
            raise

    @staticmethod
    def install_git_windows(installer_path):
        """Install Git on Windows."""
        try:
            if not os.path.isfile(installer_path):
                raise FileNotFoundError(f"The installer file does not exist: {installer_path}")

            logging.info(f"Installing Git using installer at {installer_path}")
            subprocess.run(
                [installer_path, "/VERYSILENT", "/NORESTART"],
                check=True
            )
            logging.info("Git installed successfully.")
        except subprocess.CalledProcessError:
            logging.error("Git installation failed", exc_info=True)
            raise
        except FileNotFoundError:
            logging.error("Installer not found or inaccessible", exc_info=True)
            raise

    @staticmethod
    def install_git_linux():
        """Install Git on Linux."""
        try:
            if shutil.which("apt"):
                logging.info("Using apt package manager to install Git.")
                subprocess.run(["sudo", "apt", "update"], check=True)
                subprocess.run(["sudo", "apt", "install", "git", "-y"], check=True)
            elif shutil.which("dnf"):
                logging.info("Using dnf package manager to install Git.")
                subprocess.run(["sudo", "dnf", "install", "git", "-y"], check=True)
            elif shutil.which("yum"):
                logging.info("Using yum package manager to install Git.")
                subprocess.run(["sudo", "yum", "install", "git", "-y"], check=True)
            elif shutil.which("zypper"):
                logging.info("Using zypper package manager to install Git.")
                subprocess.run(["sudo", "zypper", "install", "git", "-y"], check=True)
            elif shutil.which("pacman"):
                logging.info("Using pacman package manager to install Git.")
                subprocess.run(["sudo", "pacman", "-S", "git", "--noconfirm"], check=True)
            else:
                raise RuntimeError("Unsupported Linux distribution. Cannot install Git.")
        except subprocess.CalledProcessError:
            logging.error("An error occurred while installing Git on Linux", exc_info=True)
            sys.exit(1)

    @staticmethod
    def install_git_mac():
        """Install Git on macOS."""
        try:
            if shutil.which("brew"):
                logging.info("Using Homebrew to install Git.")
                subprocess.run(["brew", "install", "git"], check=True)
            elif shutil.which("xcode-select"):
                logging.info("Using Xcode Command Line Tools to install Git.")
                subprocess.run(["xcode-select", "--install"], check=True)
            else:
                logging.error("Neither Homebrew nor Xcode Command Line Tools are available.")
                sys.exit(1)
        except subprocess.CalledProcessError:
            logging.error("Error occurred while installing Git on macOS", exc_info=True)
            sys.exit(1)

    @staticmethod
    def ensure_git():
        """Ensure Git is installed on the current system."""
        try:
            if sys.platform.startswith("win"):
                if not GitInstaller.check_git_installed():
                    installer_path = GitInstaller.download_git_installer()
                    GitInstaller.install_git_windows(installer_path)
                    os.remove(installer_path)
                    if not GitInstaller.check_git_installed():
                        logging.error("Git is not installed correctly.")
                        sys.exit(1)
                logging.info("Git is ready to use on Windows.")
            elif sys.platform.startswith("linux"):
                GitInstaller.install_git_linux()
            elif sys.platform == "darwin":
                GitInstaller.install_git_mac()
            else:
                logging.error("Unsupported platform for Git installation.")
                sys.exit(1)
        except requests.RequestException:
            logging.error("Network error while downloading Git installer.", exc_info=True)
            sys.exit(1)
        except subprocess.CalledProcessError:
            logging.error("Error occurred while executing system commands.", exc_info=True)
            sys.exit(1)
        except FileNotFoundError:
            logging.error("Required file not found.", exc_info=True)
            sys.exit(1)
        except (OSError, RuntimeError):
            logging.error("Unexpected system or runtime error occurred.", exc_info=True)
            sys.exit(1)