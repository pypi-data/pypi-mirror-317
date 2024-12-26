# coding: utf-8

import random
import os
import numpy as np
import math
from typing import Any

from ksupk import get_files_list

from GDV_feature_shows.feature_extraction import FeatureExtractor, KImage
from GDV_feature_shows.name_volume import get_settings_order, get_visualization, get_feature_names


def define_paths(folder_path: str) -> tuple[list, list]:
    names, paths = [], []
    files = sorted(get_files_list(folder_path))
    files = [os.path.abspath(file_i) for file_i in files]
    d = {}

    for file_i in files:
        file_i_folder = os.path.basename(os.path.dirname(file_i))
        if file_i_folder in d:
            d[file_i_folder].append(file_i)
        else:
            d[file_i_folder] = [file_i]

    for k_i in d:
        rng = random.Random(42)
        idx = rng.randint(0, len(d[k_i]) - 1)
        names.append(f"{k_i}_{idx}")
        paths.append(d[k_i][idx])

    return names, paths


def update_feature_extractor_with_settings(settings: dict):
    settings_order = get_settings_order()
    fe = FeatureExtractor()
    for setting_i in settings:
        if setting_i == settings_order[0]:
            val = int(settings[setting_i])
            fe.threshold_inner_circle = max(min(val, 255), 0)
        elif setting_i == settings_order[1]:
            val = int(settings[setting_i])
            fe.threshold_outer_circle = max(min(val, 255), 0)
        elif setting_i == settings_order[2]:
            val = int(settings[setting_i])
            fe.threshold_findings_petal = max(min(val, 255), 0)
        elif setting_i == settings_order[3]:
            val = int(settings[setting_i])
            fe.threshold_noise = max(min(val, 255), 0)
        else:
            print(f"update_feature_extractor_with_settings: Failed successfully. ")
            exit(1)


def fill_visualizations(pic_path: str, visualizations: dict[str: "VisualizationFrame | VisualizationEntity"],
                        target_width: int = 200):
    visualizations_names = get_visualization()
    fe = FeatureExtractor()

    kimg = KImage(pic_path).to_gray()
    kimg = kimg.crop(*fe.find_crops(kimg))
    blank = KImage.create_empty(*kimg.shape, 1, 0).to_3_channels()
    features = fill_all_features(kimg)
    try:
        xi_c, yi_c, ri = features[-2][0], features[-2][1], features[7]
        xo_c, yo_c, ro = features[-3][0], features[-3][1], features[8]
        kimg_with_radius = kimg.copy().to_3_channels().draw_circle(xi_c, yi_c, ri).draw_circle(xo_c, yo_c, ro,
                                                                                               (0, 255, 255))
    except Exception as e:
        print(e)
        kimg_with_radius = blank
    try:
        kimg_with_petals = kimg.copy().to_3_channels().draw_segments(features[-4], True)
    except Exception as e:
        print(e)
        kimg_with_petals = blank
    try:
        kimg_with_noised_petals = kimg.copy().to_3_channels().draw_segments(features[-5], True)
    except Exception as e:
        print(e)
        kimg_with_noised_petals = blank
    try:
        kimg_with_petals_only = blank.copy().draw_segments(features[-4], False)
    except Exception as e:
        print(e)
        kimg_with_petals_only = blank
    try:
        kimg_fft = kimg.copy().fft()
    except Exception as e:
        print(e)
        kimg_fft = blank
    try:
        kimg_dct = kimg.copy().dct()
    except Exception as e:
        print(e)
        kimg_dct = blank

    try:
        kimg_peaks = kimg.copy().threshold(fe.threshold_noise, 255).to_3_channels()
        for peak_i, d_i in zip(features[-10], features[-11]):
            kimg_peaks.draw_circle(peak_i[1], peak_i[0], 2)
            p1, p2 = min(d_i, key=d_i.get), max(d_i, key=d_i.get)
            kimg_peaks.draw_line((p1[1], p1[0]), (p2[1], p2[0]))
    except Exception as e:
        print(e)
        kimg_peaks = blank

    features_data = distribute_features(features)
    for visualization_i in visualizations:
        if visualization_i == visualizations_names[0]:  # global
            visualizations[visualization_i].set_pic(kimg.resize_wh(target_width))
            visualizations[visualization_i].set_features(features_data[visualization_i])
        elif visualization_i == visualizations_names[1]:  # circles
            visualizations[visualization_i].set_pic(kimg_with_radius.resize_wh(target_width))
            visualizations[visualization_i].set_features(features_data[visualization_i])
        elif visualization_i == visualizations_names[2]:  # petals 1
            visualizations[visualization_i].set_pic(kimg_with_petals.resize_wh(target_width))
            visualizations[visualization_i].set_features(features_data[visualization_i])
        elif visualization_i == visualizations_names[3]:  # petals 2
            visualizations[visualization_i].set_pic(kimg_with_petals_only.resize_wh(target_width))
            visualizations[visualization_i].set_features(features_data[visualization_i])
        elif visualization_i == visualizations_names[4]:  # Noised petals
            visualizations[visualization_i].set_pic(kimg_with_noised_petals.resize_wh(target_width))
            visualizations[visualization_i].set_features(features_data[visualization_i])
        elif visualization_i == visualizations_names[5]:  # Noises
            visualizations[visualization_i].set_pic(kimg_dct.resize_wh(target_width))
            visualizations[visualization_i].set_features(features_data[visualization_i])
        elif visualization_i == visualizations_names[6]:  # Extra
            visualizations[visualization_i].set_pic(kimg_peaks.resize_wh(target_width))
            visualizations[visualization_i].set_features(features_data[visualization_i])
        elif visualization_i == visualizations_names[7]:  # FFT
            visualizations[visualization_i].set_pic(kimg_fft.resize_wh(target_width))
            visualizations[visualization_i].set_features(features_data[visualization_i])
        else:
            print(f"fill_visualizations: Failed successfully. ")
            exit(1)


def distribute_features(features: dict) -> dict[str: dict]:
    visualizations_names = get_visualization()
    res, feas = {}, get_feature_names()
    for v_i in visualizations_names:
        if v_i == visualizations_names[0]:  # global
            res[v_i] = {
                feas[1]: features[1],  # Количество пикселей
                feas[2]: features[2],  # Количество пикселей без "шума"
                feas[3]: features[3],  # Средняя яркость изображения
                feas[4]: features[4],  # Стандартное отклонение яркости
                feas[5]: features[5],  # Разность между пик и минимум
            }
        elif v_i == visualizations_names[1]:  # circles
            res[v_i] = {
                feas[7]: features[7],  # Радиус внутренней окружности
                feas[8]: features[8],  # Радиус внешней окружности
                feas[9]: features[9],  # Разница между центром масс и центром внутренней откужности
                feas[10]: features[10],  # Разница между центром внутренней и внешней окружностей
            }
        elif v_i == visualizations_names[2]:  # petals 1
            res[v_i] = {
                feas[11]: features[11],  # Количество лепестков
                feas[12]: features[12],  # Средний размер лепестка (M)
                feas[13]: features[13],  # Разброс размеров лепестка (S)
                feas[14]: features[14],  # Средняя длина лепестка (M)
                feas[15]: features[15],  # Разброс длин лепестков (S)
                feas[16]: features[16],  # Средняя ширина лепестка (M)
                feas[17]: features[17],  # Разброс ширины лепестков (S)
                feas[18]: features[18],  # Размер самого большого лепестка
                feas[19]: features[19],  # Максимальная длина лепестка
                feas[20]: features[20],  # Максимальная ширина лепестка
            }
        elif v_i == visualizations_names[3]:  # petals 2
            res[v_i] = {
                feas[21]: features[21],  # Среднее расстояние между лепестками (M)
                feas[22]: features[22],  # Разброс расстояний между лепестками (S)
                feas[23]: features[23],  # Средний угол между лепестками (M)
                feas[24]: features[24],  # Разброс углов между лепестками (S)
                feas[25]: features[25],  # Самое большое расстоянием между лепестками
                feas[26]: features[26],  # Самый большой угол между лепестками
                feas[27]: features[27],  # Размер “центрального лепестка”
            }
        elif v_i == visualizations_names[4]:  # Noised petals
            res[v_i] = {
                feas[28]: features[28],  # Средний размер лепестка (M) (вместе с шумом)
                feas[29]: features[29],  # Разброс размеров лепестка (S) (вместе с шумом)
                feas[30]: features[30],  # Средняя длина лепестка (M) (вместе с шумом)
                feas[31]: features[31],  # Разброс длин лепестков (S) (вместе с шумом)
                feas[32]: features[32],  # Средняя ширина лепестка (M) (вместе с шумом)
                feas[33]: features[33],  # Разброс ширины лепестков (S) (вместе с шумом)
                feas[34]: features[34],  # Размер самого большого лепестка (вместе с шумом)
                feas[35]: features[35],  # Максимальная длина лепестка  (вместе с шумом)
                feas[36]: features[36],  # Максимальная ширина лепестка  (вместе с шумом)
            }
        elif v_i == visualizations_names[5]:  # Noises
            res[v_i] = {
                feas[37]: features[37],  # Общая зашумлённость (косинусное преобразование)
                feas[38]: features[38],  # Шум внутри окружности
                feas[45]: features[45],  # Взвешанный шум внутри окружности
                feas[39]: features[39],  # Средний шум вокруг лепестков
                feas[44]: features[44],  # Распределение шума вокруг лепестков
            }
        elif v_i == visualizations_names[6]:  # Extra
            res[v_i] = {
                feas[40]: features[40],  # Количество "островков" у лепестков
                feas[41]: features[41],
                # Соотношение площади изображения (пиксели) к площади внешней окружности с шумом
                feas[42]: features[42],
                # Соотношение площади изображения (пиксели) к площади внешней окружности без шума
                feas[43]: features[43],  # Среднее распределение интенсивности вдоль вектора от центра до лепестка
            }
        elif v_i == visualizations_names[7]:  # FFT
            res[v_i] = {
            }
    return res


def fill_all_features(kimg_src: KImage) -> dict[int: Any]:
    kimg = kimg_src.copy()
    fe = FeatureExtractor()
    res, feas = {}, get_feature_names()
    for fea_i in feas:
        res[fea_i] = -1

    try:
        res[1] = fe.calc_pixels(kimg)  # Количество пикселей
        res[2] = fe.calc_pixels(kimg.copy().threshold(fe.threshold_noise, 255))  # Количество пикселей без шума"
        res[3], res[4], res[5] = fe.brightness_mean_std_range(kimg)  # Средняя яркость изображения, Стандартное отклонение яркости, Разность между пик и минимум
    except Exception as e:
        print(e)

    try:
        res[-1] = fe.get_mass_center(kimg.get_as_opencv_l())  # Mass_center
        xi_c, yi_c, ri, res[-12] = fe.get_inner_circle(kimg)  # central petal segment
        xo_c, yo_c, ro = fe.get_outer_circle(kimg)
        res[-2], res[-3] = (xi_c, yi_c), (xo_c, yo_c)  # Inner_circle_center, Outer_circle_center
        res[7], res[8] = ri, ro  # Радиус внутренней окружности, Радиус внешней окружности
        res[9] = ((xi_c - res[-1][0]) * (xi_c - res[-1][0]) + (yi_c - res[-1][1]) * (yi_c - res[-1][1])) ** 0.5  # Разница между центром масс и центром внутренней откужности
        res[10] = ((xi_c - xo_c) * (xi_c - xo_c) + (yi_c - yo_c) * (yi_c - yo_c)) ** 0.5  # Разница между центром внутренней и внешней окружностей
    except Exception as e:
        print(e)

    try:
        res[-4] = fe.find_petals(kimg)  # Pentals
    except Exception as e:
        print(e)

    try:
        res[-6], res[-7] = [], []  # Projections l, Projections w
        res[-8], res[-9] = [], []  # petal lens, petal widths
        res[-10] = []  # petal peak points
        # ===== Фикс дополнительных пиков на лепестках
        for seg_i in res[-4]:
            l, w, d = fe.project_points(seg_i, (xi_c, yi_c))
            res[-10].append(max(d, key=d.get))
        res[-4] = fe.fix_petals(xi_c, yi_c, res[-4], res[-10])
        res[-10] = []  # petal peak points
        # ===== Фикс дополнительных пиков на лепестках
        res[-11] = []  # petal d=[point: l projections]
        for seg_i in res[-4]:
            if len(seg_i) == 0:
                print(f"ZERO PETAL LEN!!!")
            l, w, d = fe.project_points(seg_i, (xi_c, yi_c))
            res[-11].append(d)
            res[-6].append(l), res[-7].append(w)
            res[-8].append(max(l) - min(l)), res[-9].append(max(w) - min(w))
            res[-10].append(max(d, key=d.get))
    except Exception as e:
        print(e)

    try:
        res[-5] = fe.find_points_in_sectors(kimg, xi_c, yi_c, res[-10], ri)  # Pentals_with_noises
        for petal_i in res[-5]:
            if len(petal_i) == 0:
                print(f"ZERO NOISED PETAL LEN!!!")
    except Exception as e:
        print(e)

    # ===== Petals 1
    try:
        res[11] = len(res[-4])  # Количество лепестков
        petal_size_seq = [len(petal_i) for petal_i in res[-4]]
        res[12], res[13] = fe.cal_mean_and_std(petal_size_seq)  # Средний размер лепестка (M), Разброс размеров лепестка (S)
        petal_l_seq, petal_w_seq = fe.cal_petal_len_and_width(res[-4], xi_c, yi_c)
        res[14], res[15] = fe.cal_mean_and_std(petal_l_seq)  # Средняя длина лепестка (M), Разброс длин лепестков (S)
        res[16], res[17] = fe.cal_mean_and_std(petal_w_seq)  # Средняя ширина лепестка (M), Разброс ширины лепестков (S)
        res[18] = max(petal_size_seq)  # Размер самого большого лепестка
        res[19] = max(petal_l_seq)  # Максимальная длина лепестка
        res[20] = max(petal_w_seq)  # Максимальная ширина лепестка
    except Exception as e:
        print(e)

    # ===== Noised petals
    try:
        petal_size_seq = [len(petal_i) for petal_i in res[-5]]
        res[28], res[29] = fe.cal_mean_and_std(petal_size_seq)  # Средний размер лепестка (M) (вместе с шумом), Разброс размеров лепестка (S) (вместе с шумом)
        petal_l_seq, petal_w_seq = fe.cal_petal_len_and_width(res[-5], xi_c, yi_c)
        res[30], res[31] = fe.cal_mean_and_std(petal_l_seq)  # Средняя длина лепестка (M) (вместе с шумом), Разброс длин лепестков (S) (вместе с шумом)
        res[32], res[33] = fe.cal_mean_and_std(petal_w_seq)  # Средняя ширина лепестка (M) (вместе с шумом), Разброс ширины лепестков (S) (вместе с шумом)
        res[34] = max(petal_size_seq)  # Размер самого большого лепестка (вместе с шумом)
        res[35] = max(petal_l_seq)  # Максимальная длина лепестка (вместе с шумом)
        res[36] = max(petal_w_seq)  # Максимальная ширина лепестка (вместе с шумом)
    except Exception as e:
        print(e)

    # ===== Petals 2
    try:
        petal_d_seq, petal_a_seq = fe.cal_petal_distance_and_angle(res[-4], xi_c, yi_c)
        res[21], res[22] = fe.cal_mean_and_std(petal_d_seq)  # Среднее расстояние между лепестками (M), Разброс расстояний между лепестками (S)
        res[23], res[24] = fe.cal_mean_and_std(petal_a_seq)  # Средний угол между лепестками (M), Разброс углов между лепестками (S)
        res[25] = max(petal_d_seq)  # Самое большое расстоянием между лепестками
        res[26] = max(petal_a_seq)  # Самый большой угол между лепестками
        if res[-12] is None:
            res[27] = 0  # Размер “центрального лепестка
        else:
            res[27] = len(res[-12])  # Размер “центрального лепестка
    except Exception as e:
        print(e)

    try:
        inside_circle = fe.get_circle_pixels(kimg, xi_c, yi_c, ri)
        res[38] = len(inside_circle)  # Шум внутри окружности
        inside_circle_values = inside_circle.values()
        scale = max(inside_circle_values) - min(inside_circle_values)
        res[45] = sum([inside_circle[k_i]/scale for k_i in inside_circle])  # Взвешанный шум внутри окружности
    except Exception as e:
        print(e)

    try:
        area = math.pi * ro ** 2
        res[41] = np.count_nonzero(kimg.get_as_opencv_l()) / area  # Соотношение площади изображения (пиксели) к площади внешней окружности с шумом
        res[42] = np.count_nonzero(kimg.threshold(fe.threshold_noise, 255).get_as_opencv_l()) / area  # Соотношение площади изображения (пиксели) к площади внешней окружности без шума
    except Exception as e:
        print(e)

    return res
