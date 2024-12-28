# coding: utf-8

import argparse
from GDV_feature_shows import __version__


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="GDV_feature_shows helps to visualize GDV scans. ")

    parser.add_argument("--version", action="version", version=f"V{__version__}", help="Check version. ")

    subparsers = parser.add_subparsers(dest='command', required=True)

    tk_parser = subparsers.add_parser("main", help='main')

    gradio_parser = subparsers.add_parser("main", help='main')

    tk_parser.add_argument("gdv_path", type=str, help="Path to folder with pictures of GDV scans. ")
    tk_parser.add_argument("settings_path", type=str, help="Path to json file with settings. "
                                                        "It creates new if does not exists. ")

    gradio_parser.add_argument("gdv_path", type=str, help="Path to folder with pictures of GDV scans. ")
    gradio_parser.add_argument("settings_path", type=str, help="Path to json file with settings. "
                                                        "It creates new if does not exists. ")
    gradio_parser.add_argument("--inf", type=str, help="Network interface. ", default="127.0.0.1")
    gradio_parser.add_argument("--port", type=int, help="Listened port. ", default=7860)
    gradio_parser.add_argument("--share", default=False, action='store_true', help="Share through gradio.app")

    return parser.parse_args()
