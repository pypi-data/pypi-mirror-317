"""
Модуль для реализации вспомогательного класса Calculator
 отвечающего за различные математические вычисления

"""

from datetime import datetime, timedelta
from math import log10
from typing import Tuple

import numpy as np
from numpy.typing import NDArray
from scipy.signal import bilinear, lfilter
from refactor_app.core.services.base_noise_equivalent import Equivalent


class Calculator:
    """
    Класс для расчета и ковертации различных значений

    convert_signal_in_24_bit - метод для конвертации сигнала из Б-строки

    ac_rms - метод вычисления RMS по формуле

    get_la_max - получение текущего значения шума


    """

    @staticmethod
    def convert_signal_in_24_bit(signal: NDArray) -> NDArray:
        """Перевод сигнала в формате байтстроки в формат 24-битного сигнала"""
        signal_int32 = np.frombuffer(signal, dtype=np.int32)

        data_np = np.frombuffer(signal_int32, dtype=np.uint8)
        data_np = data_np.reshape(-1, 3)
        data_int24 = (
            data_np[:, 0].astype(np.int32)
            + (data_np[:, 1].astype(np.int32) << 8)
            + (data_np[:, 2].astype(np.int32) << 16)
        )
        data_int24_signed = np.where(data_int24 & 0x800000, data_int24 - 0x1000000, data_int24)

        return data_int24_signed.astype("float") / 2**23

    @staticmethod
    def ac_rms(signal: NDArray) -> float:
        """Метод для вычисления RMS - Root Mean Square"""
        sig = signal - np.mean(signal)
        return np.sqrt(np.mean(np.abs(sig**2)))

    @staticmethod
    def time_weighting(
        p_series: np.ndarray,
        tau: float = 1,
        p_0: float = 20e-6,
        discret_freq: int = 1,
    ) -> float:
        """
        Корректировка по времени. Корректировка проводится с помощью алгоритма
        скользящей средней

        Parameters
        ----------
            Args:
                p_series: массив давлений за прошедшие 11 секунд
                tau: временная константа сглаживания, определяющая скорость реакции
                     алгоритма на изменения в данных
                p_0: опорное давление для вычисления дБ
                discret_freq: частота дискретизации сигнала

            Returns:
                float: значение уровня шума
        """

        result_list = [0]

        t_array = np.arange(p_series.shape[0]) / discret_freq

        for t in np.arange(1, p_series.shape[0]):
            if t == (p_series.shape[0] - 1):
                L_t = 10 * np.log10(
                    (1 / tau / discret_freq)
                    * np.sum((p_series[:t] ** 2) * np.exp(-(t_array[t] - t_array[:t]) / tau))
                    / p_0**2
                )

                result_list.append(L_t)
        result = np.array(result_list)

        return result[-1]

    @staticmethod
    def get_filter(sample_rate: int = 48000) -> Tuple[NDArray, NDArray]:
        """Returns b and a coeff of a A-weighting filter.

        Parameters
        ----------
        sample_rate : scalar
            Sample rate of the signals that well be filtered.

        Returns
        -------
        b, a : ndarray
            Filter coefficients for a digital weighting filter.
        """
        f1 = 20.598997
        f2 = 107.65265
        f3 = 737.86223
        f4 = 12194.217
        A1000 = 1.9997

        NUMs = [(2 * np.pi * f4) ** 2 * (10 ** (A1000 / 20)), 0, 0, 0, 0]
        DENs = np.convolve(
            [1, +4 * np.pi * f4, (2 * np.pi * f4) ** 2],
            [1, +4 * np.pi * f1, (2 * np.pi * f1) ** 2],
            mode="full",
        )
        DENs = np.convolve(
            np.convolve(DENs, [1, 2 * np.pi * f3], mode="full"),
            [1, 2 * np.pi * f2],
            mode="full",
        )
        return bilinear(NUMs, DENs, sample_rate)

    @staticmethod
    def frequency_weighting(signal: NDArray, B: NDArray, A: NDArray) -> Tuple[NDArray, NDArray]:
        """Return the given signal after passing through an A-weighting filter"""
        return lfilter(B, A, signal)

    @staticmethod
    def equivalent_la(la_max: float, la_eq: Equivalent, per_hour: bool = False) -> float:
        """
            Метод расчета эквивалентного уровня шума за интервал времени.

        Args:
            la_max: текущий уровень шума
            la_eq: объект, содержащий в себе временное предрасчётное эквивалентное значение
            per_hour: параметр указывается, как True, если считается эквивалент за час

        Return:
            float: текущий эквивалентный уровень шума
        """

        current_hour = datetime.now().hour

        if la_eq.end_hour == current_hour:
            if per_hour:
                end_hour = (datetime.now() + timedelta(hours=1)).hour
            else:
                end_hour = 23 if 7 <= current_hour < 23 else 7

            la_eq.la_eq_temp = 0
            la_eq.iters = 0
            la_eq.end_hour = end_hour

        la_eq.la_eq_temp += 10 ** (0.1 * la_max)
        la_eq.iters += 1

        return round(10 * log10(la_eq.la_eq_temp / la_eq.iters), 2)
