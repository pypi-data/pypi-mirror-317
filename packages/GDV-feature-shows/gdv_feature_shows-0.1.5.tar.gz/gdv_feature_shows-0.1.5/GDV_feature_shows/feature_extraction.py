# coding: utf-8

from ksupk import singleton_decorator
import cv2
import numpy as np
import PIL
from PIL import Image
import random
import copy
from typing import Self
from collections.abc import Sized, Iterable
import math


class KImage:
    def __init__(self, pic: np.ndarray | PIL.Image.Image | str):
        if isinstance(pic, str):
            self.img = cv2.imread(pic)
        elif isinstance(pic, np.ndarray):
            self.img = pic.copy()
        elif isinstance(pic, PIL.Image.Image):
            opencv_image = np.array(pic)
            opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_RGB2BGR)
            self.img = opencv_image
        else:
            raise ValueError(f"{type(self)}: param pic must be np.ndarray or PIL.Image.Image) only. ")

    @staticmethod
    def create_empty(w: int, h: int, channels: int = 1, color: int | tuple = 0) -> "KImage":
        if channels != 1 and channels != 3:
            raise ValueError("Channels must be 1 or 3")
        if channels == 1 and not isinstance(color, int):
            raise ValueError(f"Color must be int, if channels == {channels}")
        if channels == 1 and (color < 0 or color > 255):
            raise ValueError("Color must be 0–255. ")
        if channels == 3 and isinstance(color, Sized) and len(color) != 3:
            raise ValueError("Color must be (B, G, R) (3 elements). ")
        if channels == 3 and isinstance(color, Sized):
            for c_i in color:
                if c_i < 0 or c_i > 255:
                    raise ValueError("Each color must be 0–255. ")
        if channels == 3 and isinstance(color, int):
            if color < 0 or color > 255:
                raise ValueError("Color must be 0-255. ")
            color = (color, color, color)

        if channels == 1:
            res = np.full((h, w), color, dtype=np.uint8)
        else:
            res = np.zeros((h, w, 3), dtype=np.uint8)
            res[:] = color

        return KImage(res)

    def get(self, x: int, y: int) -> int | tuple[int, int, int]:
        """Return RGB, if 3 channel mode"""
        assert self.count_channels() in [1, 3]
        if self.count_channels() == 1:
            return int(self.img[y][x])
        else:
            blue_channel = int(self.img[y, x, 0])
            green_channel = int(self.img[y, x, 1])
            red_channel = int(self.img[y, x, 2])
            return red_channel, green_channel, blue_channel

    def get_as_pillow(self) -> PIL.Image.Image:
        if self.count_channels() == 1:
            rgb_image = cv2.cvtColor(self.img, cv2.COLOR_GRAY2RGB)
        else:
            rgb_image = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        pillow_image = Image.fromarray(rgb_image)
        return pillow_image

    def get_as_opencv(self) -> np.ndarray:
        return self.img.copy()

    def get_as_opencv_l(self) -> np.ndarray:
        return self.img

    def get_as_tk(self) -> "ImageTk":
        from PIL import ImageTk
        return ImageTk.PhotoImage(self.get_as_pillow())

    def count_channels(self) -> int:
        if len(self.img.shape) == 2:  # only w and h
            return 1
        else:
            return self.img.shape[2]

    def to_3_channels(self) -> Self:
        if self.count_channels() == 1:
            self.img = cv2.cvtColor(self.img, cv2.COLOR_GRAY2BGR)
        return self

    def to_gray(self) -> Self:
        if self.count_channels() == 3:
            self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        return self

    def to_bin(self, threshold_value: int = 127) -> Self:
        _, res = cv2.threshold(self.img, threshold_value, 255, cv2.THRESH_BINARY)
        self.img = res
        return self

    def threshold(self, start_brightness: int, end_brightness: int) -> Self:
        if self.count_channels() == 1:
            mask = (self.img >= start_brightness) & (self.img <= end_brightness)
            filtered_img = np.zeros_like(self.img)
            filtered_img[mask] = self.img[mask]
        else:
            filtered_img = np.zeros_like(self.img)

            for channel in range(3):  # Цикл по каналам
                mask = (self.img[:, :, channel] >= start_brightness) & (self.img[:, :, channel] <= end_brightness)
                filtered_img[:, :, channel][mask] = self.img[:, :, channel][mask]

        self.img = filtered_img

        return self

    def __copy__(self) -> Self:
        return type(self)(self.img)

    def __deepcopy__(self, memo) -> Self:
        return type(self)(self.img)

    def copy(self) -> Self:
        return copy.copy(self)

    @property
    def shape(self):
        return self.img.shape

    def resize(self, factor: float) -> Self:
        img = self.img
        height, width = img.shape[:2]
        new_width = int(width * factor)
        new_height = int(height * factor)
        resized_image = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_NEAREST)
        self.img = resized_image
        return self

    def resize_wh(self, needed_w: int, needed_h: int = None) -> Self:
        height, width = self.img.shape[:2]
        if needed_h is None:
            new_width = needed_w
            new_height = int(height*(needed_w/width)+0.5)
        else:
            new_width = needed_w
            new_height = needed_h
        # cv2.INTER_LINEAR, cv2.INTER_NEAREST
        self.img = cv2.resize(self.img, (new_width, new_height), interpolation=cv2.INTER_NEAREST)
        return self

    def crop(self, top_row: int, right_column: int, bottom_row: int, left_column: int) -> Self:
        self.img = self.img[top_row:bottom_row, left_column:right_column]
        return self

    def show(self, title: str = ""):
        cv2.imshow(title, self.img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def draw_segments(self, segments: list, random_colors: bool = False) -> Self:
        image = self.img
        if_grayed = self.count_channels() == 1
        if if_grayed:
            image_with_segments = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        else:
            image_with_segments = image.copy()

        for seg_i in segments:
            segment_pixels = seg_i
            if random_colors:
                color = tuple(np.random.randint(0, 255, 3).tolist())
            else:
                color = (255, 255, 255)  # BGR

            for pixel in segment_pixels:
                y, x = pixel
                image_with_segments[y, x] = color

        self.img = image_with_segments
        if if_grayed:
            self.to_gray()
        return self

    def draw_circle(self, x_c: int, y_c: int, r: int, color: tuple = (0, 0, 255)) -> Self:
        image = self.img
        if_grayed = self.count_channels() == 1
        if if_grayed:
            image_with_circle = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        else:
            image_with_circle = image.copy()

        cv2.circle(image_with_circle, (x_c, y_c), r, color, 1)

        self.img = image_with_circle
        if if_grayed:
            self.to_gray()
        return self

    def draw_line(self, start_point, end_point, color: tuple = (0, 0, 255)):
        image = self.img
        if_grayed = self.count_channels() == 1
        if if_grayed:
            image_with_line = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        else:
            image_with_line = image.copy()

        cv2.line(image_with_line, start_point, end_point, color, 1)

        self.img = image_with_line
        if if_grayed:
            self.to_gray()
        return self

    def fft(self) -> Self:
        f = np.fft.fft2(self.img)
        fshift = np.fft.fftshift(f)
        magnitude_spectrum = 20 * np.log(np.abs(fshift) + 1)
        magnitude_spectrum = cv2.normalize(magnitude_spectrum, None, 0, 255, cv2.NORM_MINMAX)
        self.img = np.uint8(magnitude_spectrum)
        return self

    def ifft(self) -> Self:
        f_ishift = np.fft.ifftshift(self.img)
        img_reconstructed = np.fft.ifft2(f_ishift)
        img_reconstructed = np.abs(img_reconstructed)
        img_reconstructed = cv2.normalize(img_reconstructed, None, 0, 255, cv2.NORM_MINMAX)
        self.img = np.uint8(img_reconstructed)
        return self

    def dct(self) -> Self:
        img_float = np.float32(self.img)
        dct = cv2.dct(img_float)
        dct_norm = cv2.normalize(dct, None, 0, 255, cv2.NORM_MINMAX)
        self.img = np.uint8(dct_norm)
        return self

    def idct(self) -> Self:
        dct_float = np.float32(self.img)
        idct = cv2.idct(dct_float)
        idct_norm = cv2.normalize(idct, None, 0, 255, cv2.NORM_MINMAX)
        self.img = np.uint8(idct_norm)
        return self


@singleton_decorator
class FeatureExtractor:
    def __init__(self):
        self._threshold_crop = 20
        self._threshold_inner_circle = 120  # 80 150
        self._threshold_outer_circle = 20  # 80
        self._threshold_findings_petal = 120
        self._threshold_noise = 80

    @property
    def threshold_inner_circle(self):
        return self._threshold_inner_circle

    @threshold_inner_circle.setter
    def threshold_inner_circle(self, value: int):
        self._threshold_inner_circle = value

    @property
    def threshold_outer_circle(self):
        return self._threshold_outer_circle

    @threshold_outer_circle.setter
    def threshold_outer_circle(self, value: int):
        self._threshold_outer_circle = value

    @property
    def threshold_findings_petal(self):
        return self._threshold_findings_petal

    @threshold_findings_petal.setter
    def threshold_findings_petal(self, value: int):
        self._threshold_findings_petal = value

    @property
    def threshold_noise(self):
        return self._threshold_noise

    @threshold_noise.setter
    def threshold_noise(self, value: int):
        self._threshold_noise = value

    @property
    def threshold_crop(self):
        return self._threshold_crop

    @staticmethod
    def calc_pixels(kimg: KImage):
        if kimg.count_channels() == 1:
            return cv2.countNonZero(kimg.get_as_opencv_l())
        else:
            return cv2.countNonZero(kimg.copy().to_gray().get_as_opencv_l())

    @staticmethod
    def brightness_mean_std_range(kimg: KImage) -> tuple[float, float, float]:
        assert kimg.count_channels() == 1
        img = kimg.get_as_opencv_l()
        res = tuple(map(float, (np.mean(img), np.std(img), np.max(img) - np.min(img))))
        return res[0], res[1], res[2]

    @staticmethod
    def get_mass_center(img: np.ndarray) -> tuple[int, int]:
        moments = cv2.moments(img)
        if moments['m00'] != 0:
            x_center = int(moments['m10'] / moments['m00'])
            y_center = int(moments['m01'] / moments['m00'])
        else:
            x_center, y_center = 0, 0

        return x_center, y_center

    @staticmethod
    def find_touching_pixels(img, x_center: int, y_center: int, radius: int, threshold=80) -> list:
        """img is gray or bin"""
        height, width = img.shape
        touching_pixels = []
        for angle in range(0, 360):
            x = int(x_center + radius * np.cos(np.radians(angle)))
            y = int(y_center + radius * np.sin(np.radians(angle)))
            if 0 <= x < width and 0 <= y < height and img[y, x] > threshold:
                touching_pixels.append((x, y))
        return touching_pixels

    @staticmethod
    def get_inner_circle(kimg: KImage) -> tuple[int, int, int, list | None]:
        fe = FeatureExtractor()
        threshold = fe.threshold_inner_circle
        threshold_findings_petal = fe.threshold_findings_petal
        radius = 1
        n_iters = 100
        step = 3
        img_bin = kimg.copy().to_bin(threshold).get_as_opencv_l()
        img_bin = fe.do_openning(img_bin)

        x_center, y_center = fe.get_mass_center(kimg.get_as_opencv_l())
        segs = fe.find_segments(kimg, threshold_findings_petal, openning=False)
        central_petal_seg = fe.find_central_petal(segs, x_center, y_center)
        if central_petal_seg is not None:
            # show_cv2_img(img_bin, "1")
            # show_cv2_img(draw_segments(img_bin, segs, random_colors=True), "3")
            # show_cv2_img(draw_segments(img_bin, [central_petal_seg]), "4")
            for pix_i in central_petal_seg:
                y, x = pix_i
                img_bin[y, x] = 0
            # show_cv2_img(img_bin, "2")

        last_vectors, x_center_prev, y_center_prev = set(), None, None

        for _ in range(n_iters):
            while True:
                touching_pixels = fe.find_touching_pixels(img_bin, x_center, y_center, radius, threshold)
                if touching_pixels:
                    break
                radius += 1
                if radius >= max(kimg.shape):
                    return -1, -1, max(kimg.shape)

            dx_total, dy_total = 0, 0
            for touch_x, touch_y in touching_pixels:
                dx_total += x_center - touch_x
                dy_total += y_center - touch_y

            num_touching = len(touching_pixels)
            avg_dx = dx_total / num_touching
            avg_dy = dy_total / num_touching
            vector_length = np.sqrt(avg_dx ** 2 + avg_dy ** 2)

            x_center_prev, y_center_prev = x_center, y_center
            x_center += int(step * avg_dx / vector_length)
            y_center += int(step * avg_dy / vector_length)

            if (avg_dx, avg_dy) in last_vectors:
                step -= 1
                if step <= 0:
                    x_center = int((x_center + x_center_prev) / 2 + 0.5)
                    y_center = int((y_center + y_center_prev) / 2 + 0.5)
                    break
            last_vectors.add((avg_dx, avg_dy))

            if not (0 <= x_center < kimg.shape[1] and 0 <= y_center < kimg.shape[0]):
                break

        return x_center, y_center, radius, central_petal_seg

    @staticmethod
    def get_outer_circle(kimg: KImage) -> tuple[int, int, int]:
        fe = FeatureExtractor()
        threshold = fe.threshold_outer_circle
        radius = max(kimg.img.shape[0], kimg.img.shape[1])
        n_iters = 100
        step = 5

        x_center, y_center = fe.get_mass_center(kimg.get_as_opencv_l())

        last_vectors, x_center_prev, y_center_prev = set(), None, None

        for _ in range(n_iters):
            while True:
                touching_pixels = fe.find_touching_pixels(kimg.get_as_opencv_l(), x_center, y_center, radius, threshold)
                if touching_pixels:
                    break
                radius -= 1
                if radius <= 0:
                    return -1, -1, 0
            # radius += 5
            dx_total, dy_total = 0, 0
            for touch_x, touch_y in touching_pixels:
                dx_total += x_center - touch_x
                dy_total += y_center - touch_y

            num_touching = len(touching_pixels)
            avg_dx = dx_total / num_touching
            avg_dy = dy_total / num_touching
            vector_length = np.sqrt(avg_dx ** 2 + avg_dy ** 2)

            x_center_prev, y_center_prev = x_center, y_center
            x_center -= int(step * avg_dx / vector_length)
            y_center -= int(step * avg_dy / vector_length)

            if (avg_dx, avg_dy) in last_vectors:
                x_center = int((x_center + x_center_prev) / 2 + 0.5)
                y_center = int((y_center + y_center_prev) / 2 + 0.5)
                break
            last_vectors.add((avg_dx, avg_dy))

            if not (0 <= x_center < kimg.shape[1] and 0 <= y_center < kimg.shape[0]):
                break

        return x_center, y_center, radius

    @staticmethod
    def do_openning(img_bin: np.ndarray) -> np.ndarray:
        """img_bin is bin"""
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        morphed = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, kernel)
        return morphed

    @staticmethod
    def find_segments(kimg: KImage, threshold: int, openning: bool = True) -> list:
        """img is gray or bin"""
        fe = FeatureExtractor()
        binary = kimg.copy().to_bin(threshold).get_as_opencv_l()
        if openning:
            morphed = fe.do_openning(binary)
        else:
            morphed = binary

        num_labels, labels = cv2.connectedComponents(morphed, connectivity=4)

        segments = []
        for i in range(1, num_labels):  # background is 0, so from 1
            segment = np.argwhere(labels == i)  # segment is list of lists of coords(y, x)
            segments.append(segment)

        return segments

    @staticmethod
    def find_petals(kimg: KImage) -> list:
        assert kimg.count_channels() == 1
        fe = FeatureExtractor()
        segments = fe.find_segments(kimg, fe.threshold_findings_petal)
        # ...
        res_segs = []
        for seg_i in segments:
            if len(seg_i) > 5:
                res_segs.append(seg_i)
        # show_cv2_img(draw_segments(self.img, res_segs), "segments")
        return res_segs

    @staticmethod
    def find_central_petal(segs: list, x_c_mass: int, y_c_mass: int) -> list | None:
        """img is gray or bin"""
        for seg_i in segs:
            for pixel in seg_i:
                y, x = pixel
                if y == y_c_mass and x == x_c_mass:
                    return seg_i
        return None

    @staticmethod
    def find_crops(kimg: KImage) -> tuple:
        """image is gray"""
        image = kimg.get_as_opencv_l()
        threshold = FeatureExtractor().threshold_crop
        crop_shift = 5

        shape = image.shape

        mask = image > threshold
        top_row = np.argmax(mask.any(axis=1)) - crop_shift

        mask = image > threshold
        bottom_row = np.argmax(mask.any(axis=1)[::-1])
        bottom_row = image.shape[0] - bottom_row - 1 + crop_shift

        mask = image > threshold
        left_column = np.argmax(mask.any(axis=0)) - crop_shift

        mask = image > threshold
        right_column = np.argmax(mask.any(axis=0)[::-1])
        right_column = image.shape[1] - right_column - 1 + crop_shift

        top_row = 0 if top_row < 0 else top_row
        left_column = 0 if left_column < 0 else left_column

        bottom_row = shape[0] if bottom_row >= shape[0] else bottom_row
        right_column = shape[1] if right_column >= shape[1] else right_column

        return top_row, right_column, bottom_row, left_column

    @staticmethod
    def project_points(seg: list, xy_center: tuple) -> tuple[list[int], list[int], dict[tuple[int, int]: int]]:
        xy_seg_mass_center = np.mean(seg, axis=0)

        x1, y1 = xy_center
        x2, y2 = xy_seg_mass_center
        # y2, x2 = x2, y2  # !!!

        line_vec = np.array([x2 - x1, y2 - y1])
        line_vec_norm = line_vec / np.linalg.norm(line_vec)

        perp_vec = np.array([-line_vec[1], line_vec[0]])
        perp_vec_norm = perp_vec / np.linalg.norm(perp_vec)

        relative_coords_line = []
        relative_coords_perp = []
        d_l = {}

        for x, y in seg:
            point_vec = np.array([x - x1, y - y1])

            # Проекция точки на прямую (скалярное произведение на нормированный вектор прямой)
            proj_on_line = np.dot(point_vec, line_vec_norm)

            # Проекция точки на перпендикулярную прямую
            proj_on_perp = np.dot(point_vec, perp_vec_norm)

            # Добавляем результаты
            relative_coords_line.append(proj_on_line)
            relative_coords_perp.append(proj_on_perp)
            d_l[(x, y)] = proj_on_line

        return relative_coords_line, relative_coords_perp, d_l

    @staticmethod
    def cal_petal_len_and_width(petals: list, x_c: int, y_c: int) -> tuple[list, list]:
        fe = FeatureExtractor()
        ls, ws = [], []
        for petal_i in petals:
            l_i, w_i, _ = fe.project_points(petal_i, (x_c, y_c))
            ls.append(max(l_i)-min(l_i)), ws.append(max(w_i)-min(w_i))
        return ls, ws

    @staticmethod
    def cal_petal_distance_and_angle(petals: list, x_c: int, y_c: int) -> tuple[list, list]:
        fe = FeatureExtractor()
        ds, ans = [], []
        mass_centers = []
        # buff_d = {}
        for petal_i in petals:
            xy_seg_mass_center = np.mean(petal_i, axis=0)
            x_m_c, y_m_c = xy_seg_mass_center
            mass_centers.append((x_m_c, y_m_c))
            # buff_d[(x_m_c, y_m_c)] = petal_i
        mass_centers = fe.sort_points_clockwise(mass_centers, x_c, y_c)
        mass_centers = mass_centers + [mass_centers[0]]
        for i in range(len(mass_centers) - 1):
            mc_i, mc_i1 = mass_centers[i], mass_centers[i+1]
            ans_i = fe.angle_from_vertical(*mc_i1, x_c, y_c) - fe.angle_from_vertical(*mc_i, x_c, y_c)
            while ans_i < 0:
                ans_i += 360
            ans.append(ans_i)
            ds_i = math.sqrt((mc_i1[0]-mc_i[0])*(mc_i1[0]-mc_i[0])+(mc_i1[1]-mc_i[1])*(mc_i1[1]-mc_i[1]))
            ds.append(ds_i)
            # print(ans_i, ds_i, (x_c, y_c))
            # (KImage.create_empty(300, 300).to_3_channels().draw_segments([buff_d[mc_i], buff_d[mc_i1]], True)
            #  .draw_line((x_c, y_c), tuple(map(int, list(mc_i)[::-1])))
            #  .draw_line((x_c, y_c), tuple(map(int, list(mc_i1)[::-1])))
            #  .show())

        return ds, ans

    @staticmethod
    def find_petal_by_point(petals: list, y: int, x: int) -> list | None:
        for petal_i in petals:
            for y_i, x_i in petal_i:
                if y_i == y and x_i == x:
                    return petal_i
        return None

    @staticmethod
    def fix_petals(x_c: int, y_c: int, petals: list, peaks: list[tuple[int, int]]) -> list:
        """
        Некоторые petals лежат на одной прямой, это на самом деле одни и теже лепестки.
        """
        assert len(petals) == len(peaks)
        fe = FeatureExtractor()
        epsilon = 0.0001
        vectors = np.array([(y - y_c, x - x_c) for y, x in peaks])

        # Нормализуем векторы для получения направлений
        directions = np.array([v / np.linalg.norm(v) if np.linalg.norm(v) != 0 else v for v in vectors])

        similar_pairs = []

        for i in range(len(directions)):
            for j in range(i + 1, len(directions)):
                dot_product = np.dot(directions[i], directions[j])
                # Углы близки, если скалярное произведение близко к 1 (0) или -1 (180)
                # if abs(dot_product - 1) < epsilon or abs(dot_product + 1) < epsilon:
                if abs(dot_product - 1) < epsilon:
                    similar_pairs.append([peaks[i], peaks[j]])
        # print(len(similar_pairs), len(petals))
        d = {}

        for peak_i in peaks:
            d[peak_i] = fe.find_petal_by_point(petals, *peak_i)
            assert d[peak_i] is not None

        similared, no_similared = [], []
        for peak_i in peaks:
            f = False
            for fimilars_i in similar_pairs:
                if peak_i in fimilars_i:
                    f = True
                    break
            if f:
                similared.append(peak_i)
            else:
                no_similared.append(peak_i)

        combined = []
        for peak_i in similared:
            f = None
            for i, combine_i in enumerate(combined):
                if peak_i in combine_i:
                    f = i
            if f is not None:
                cur_combine = combined[f]
            else:
                cur_combine = {peak_i}
            to_remove = []
            for j, fimilars_i in enumerate(similar_pairs):
                if peak_i in fimilars_i:
                    to_remove.append(j)
                    to_combine = fimilars_i[0] if fimilars_i[0] != peak_i else fimilars_i[1]
                    cur_combine.add(to_combine)
            for to_remove_i in to_remove:
                similar_pairs.pop(to_remove_i)
            combined.append(cur_combine)

        for peak_i in no_similared:
            combined.append({peak_i})

        res_d = {}
        for i, combine_i in enumerate(combined):
            if len(combine_i) == 1:
                for shit_i in combine_i:
                    res_d[i] = d[shit_i]
                    break
            else:
                for j, combine_i_j in enumerate(combine_i):
                    if j == 0:
                        res_d[i] = d[combine_i_j]
                    else:
                        res_d[i] = np.append(res_d[i], d[combine_i_j], axis=0)

        res = []
        for k_i in res_d:
            res.append(res_d[k_i])

        return res

    @staticmethod
    def angle_from_vertical(y, x, y_c, x_c):
        """
        Вычисляет угол между вертикальной прямой вверх от (x_c, y_c) и вектором от (x_c, y_c) до (y, x).
        Угол возвращается в диапазоне [0, 360) градусов.
        """
        dy = y - y_c
        dx = x - x_c
        angle = np.degrees(np.arctan2(dx, -dy))  # -dy, так как вертикальная вверх
        while angle < 0:
            angle += 360  # Приводим к диапазону [0, 360)
        return angle

    @staticmethod
    def sort_points_clockwise(peaks: list[tuple[int, int]], x_c: int, y_c: int) -> list:
        """
        Сортирует точки вокруг центральной точки (x_c, y_c) в порядке обхода по часовой стрелке.

        Args:
            peaks (list): Список координат точек [(y1, x1), (y2, x2), ...].
            x_c (int): Координата x центральной точки.
            y_c (int): Координата y центральной точки.

        Returns:
            list: Упорядоченный список координат в порядке обхода по часовой стрелке.
        """
        coords = peaks
        fe = FeatureExtractor()
        angles = [fe.angle_from_vertical(y, x, y_c, x_c) for y, x in coords]

        sorted_points = sorted(zip(coords, angles), key=lambda pair: pair[1])

        return [point for point, _ in sorted_points]

    @staticmethod
    def calculate_sector_borders(peaks: list[tuple[int, int]], x_c, y_c):
        """
        Вычисляет середины между каждой парой соседних точек и направляющие векторы для разделяющих прямых.

        Args:
            peaks (list): Список координат точек [(y1, x1), (y2, x2), ...].
            x_c (int): Координата x центра окружности.
            y_c (int): Координата y центра окружности.

        Returns:
            list: Список разделяющих прямых в виде углов в радианах.
        """
        coords = peaks + [peaks[0]]

        mids = [
            ((coords[i][0] + coords[i + 1][0]) / 2, (coords[i][1] + coords[i + 1][1]) / 2)
            for i in range(len(coords) - 1)
        ]

        angles = [np.arctan2(mid[0] - y_c, mid[1] - x_c) for mid in mids]

        # Приводим углы к диапазону [0, 2π]
        angles = [angle if angle >= 0 else angle + 2 * np.pi for angle in angles]

        return sorted(angles)

    @staticmethod
    def is_point_in_sector(x: float, y: float, x_c: float, y_c: float, angles: list, cheching_sector: int, r: float):
        """
        Проверяет, принадлежит ли точка заданному сектору.

        Args:
            x
            y (float): Координаты точки.
            x_c
            y_c (float): Центр окружности.
            angles (list): Углы разделяющих прямых.
            cheching_sector (int): этот сектор?
            r (float): Радиус окружности.

        Returns:
            bool: True, если точка принадлежит сектору.
        """
        angle = np.arctan2(y - y_c, x - x_c)
        angle = angle if angle >= 0 else angle + 2 * np.pi

        distance = np.sqrt((x - x_c) ** 2 + (y - y_c) ** 2)
        if distance <= r:
            return False

        start_angle = angles[cheching_sector]
        end_angle = angles[(cheching_sector + 1) % len(angles)]
        if start_angle < end_angle:
            return start_angle <= angle < end_angle
        else:  # Угол сектора пересекает 0
            return angle >= start_angle or angle < end_angle

    @staticmethod
    def find_points_in_sectors(kimg: KImage, x_c, y_c, peaks: list[tuple[int, int]], r):
        """
        Разбивает точки по секторам, образованным разделяющими прямыми.

        Args:
            kimg: Само изображение
            x_c
            y_c (int): Центр окружности.
            peaks (list): Точки, задающие разделяющие прямые.
            r (float): Радиус окружности.

        Returns:
            list: Список списков, где каждый подсписок содержит точки в соответствующем секторе.
        """
        assert kimg.count_channels() == 1
        fe = FeatureExtractor()
        peaks = fe.sort_points_clockwise(peaks, x_c, y_c)
        angles = fe.calculate_sector_borders(peaks, x_c, y_c)
        sectors = [[] for _ in range(len(angles))]

        non_black = np.argwhere(kimg.get_as_opencv_l() != 0)
        for yx in non_black:
            y, x = yx
            for i in range(len(angles)):
                if fe.is_point_in_sector(x, y, x_c, y_c, angles, i, r):
                    sectors[i].append((y, x))
                    break

        return sectors

    @staticmethod
    def cal_mean_and_std(data: Iterable) -> tuple[float, float]:
        data = list(data)
        if not data:
            raise ValueError("Данные не могут быть пустыми.")

        n = len(data)
        mean = sum(data) / n

        variance = sum((x - mean) ** 2 for x in data) / n
        std_dev = math.sqrt(variance)

        return mean, std_dev

    @staticmethod
    def get_circle_pixels(kimg: KImage, x_c: int, y_c: int, r: int) -> dict[tuple[int, int]: int]:
        mask = np.zeros(kimg.shape, dtype=np.uint8)
        cv2.circle(mask, (x_c, y_c), r, 255, -1)
        y_coords, x_coords = np.where(mask > 0)
        coords = list(zip(y_coords, x_coords))  # list in (y, x)
        d = {}
        for coord_i in coords:
            y, x = coord_i
            v = kimg.get(x, y)
            if v != 0:
                d[(x, y)] = v
        return d
