# coding: utf-8

from GDV_feature_shows.interface_tk import App

from GDV_feature_shows.interface_gradio import start_gradio_interface

from GDV_feature_shows.resource_manager import ResourceManager
from GDV_feature_shows.feature_extraction import FeatureExtractor

from GDV_feature_shows.parsing import get_args

# TODO: 2940167 (extra), several peaks. 
# TODO: 2944804, fix noised petals. 
# TODO: except zero pixels, while calculating general parameters.

def main():
    args = get_args()
    FeatureExtractor()
    ResourceManager()
    if args.mode == "tk":
        app = App(args.gdv_path, args.settings_path)
        app.mainloop()
    elif args.mode == "gradio":
        start_gradio_interface(args.gdv_path, args.settings_path)
    else:
        print(f"main: Failed successfully. ")
        exit(-1)


if __name__ == "__main__":
    main()
