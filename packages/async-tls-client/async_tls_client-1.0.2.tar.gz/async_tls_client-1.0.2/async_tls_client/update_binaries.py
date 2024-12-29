import ctypes
import logging
import os
import platform
from pathlib import Path
from typing import Optional

import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
GITHUB_API_LATEST_RELEASE = 'https://api.github.com/repos/bogdanfinn/tls-client/releases/latest'
DEPENDENCIES_DIR = Path(__file__).parent / 'dependencies'


def get_platform_file_ext() -> str:
    """
    Determine the file extension for the library based on the platform and architecture.

    Returns:
        str: File extension (e.g., '-arm64.dylib', '-64.dll', '-amd64.so').

    Raises:
        ValueError: If the platform is not supported.
    """
    system = platform.system().lower()
    machine_arch = platform.machine().lower()

    if system == 'darwin':
        return '-arm64.dylib' if machine_arch == 'arm64' else '-x86.dylib'
    elif system in ('windows', 'win32', 'cygwin'):
        return '-64.dll' if ctypes.sizeof(ctypes.c_voidp) == 8 else '-32.dll'
    elif system == 'linux':
        if machine_arch == 'aarch64':
            return '-arm64.so'
        elif 'x86' in machine_arch:
            return '-x86.so'
        else:
            return '-amd64.so'
    else:
        raise ValueError(f'Unsupported platform: {system}')


def get_latest_release_assets() -> list:
    """
    Retrieve a list of assets from the latest release using the GitHub API.

    Returns:
        list: List of assets from the latest release.

    Raises:
        RequestException: If the request to the GitHub API fails.
    """
    headers = {'Accept': 'application/vnd.github.v3+json'}
    response = requests.get(GITHUB_API_LATEST_RELEASE, headers=headers)
    response.raise_for_status()
    release_info = response.json()
    assets = release_info.get('assets', [])
    logger.info(f'Found {len(assets)} assets in the latest release.')
    return assets


def find_asset_url(assets: list, platform_ext: str) -> Optional[str]:
    """
    Find the URL of an asset matching the given file extension.

    Args:
        assets (list): List of release assets.
        platform_ext (str): File extension for the current platform.

    Returns:
        Optional[str]: URL of the asset or None if not found.
    """
    if platform_ext.endswith('.dll'):
        platform_ext = 'windows' + platform_ext[:-4]

    for asset in assets:
        asset_name = asset.get('name', '').lower()
        asset_url = asset.get('browser_download_url')

        if platform_ext in asset_name:
            return asset_url

    logger.error(f"No asset found for extension: {platform_ext}")
    return None


def download_asset(asset_url: str, filename: str) -> None:
    """
    Download an asset from the specified URL and save it with the given filename.

    Args:
        asset_url (str): URL to download the asset.
        filename (str): Filename to save the asset.

    Raises:
        RequestException: If the asset download fails.
        IOError: If saving the file fails.
    """
    with requests.get(asset_url, stream=True) as r:
        r.raise_for_status()
        DEPENDENCIES_DIR.mkdir(parents=True, exist_ok=True)
        file_path = DEPENDENCIES_DIR / filename
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    logger.info(f'Downloaded asset to {file_path}')


def update_binaries() -> None:
    """
    Update TLS client binaries by downloading the latest versions from GitHub.

    Raises:
        Exception: If an error occurs during the update process.
    """
    logger.info('Starting update_binaries...')
    try:
        root_dir = os.path.abspath(os.path.dirname(__file__))

        # Retrieve the list of assets from the latest release
        assets = get_latest_release_assets()

        # Determine the file extension for the current platform
        platform_ext = get_platform_file_ext()

        # Find the URL of the asset for the current platform
        asset_url = find_asset_url(assets, platform_ext)

        if not asset_url:
            logger.error('Asset URL not found. Aborting download.')
            return

        # Extract the filename from the URL
        filename = f'{root_dir}/dependencies/tls-client{platform_ext}'

        # Download and save the asset
        download_asset(asset_url, filename)

        logger.info('Binaries updated successfully.')
    except Exception as e:
        logger.exception(f'An error occurred while updating binaries: {e}')


if __name__ == "__main__":
    update_binaries()
