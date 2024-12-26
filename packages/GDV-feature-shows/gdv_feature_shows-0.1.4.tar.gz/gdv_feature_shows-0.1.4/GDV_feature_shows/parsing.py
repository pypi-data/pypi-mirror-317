# coding: utf-8

import argparse
from GDV_feature_shows import __version__


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="GDV_feature_shows helps to visualize GDV scans. ")

    parser.add_argument("--version", action="version", version=f"V{__version__}", help="Check version. ")

    # subparsers = parser.add_subparsers(dest='command', required=True)

    # main
    # main_parser = subparsers.add_parser("main", help='main')

    # main_parser
    parser.add_argument("mode", type=str, choices=["tk", "gradio"], help="Interface mode. ")

    parser.add_argument("gdv_path", type=str, help="Path to folder with pictures of GDV scans. ")

    parser.add_argument("settings_path", type=str, help="Path to json file with settings. "
                                                        "It creates new if does not exists. ")

    return parser.parse_args()
