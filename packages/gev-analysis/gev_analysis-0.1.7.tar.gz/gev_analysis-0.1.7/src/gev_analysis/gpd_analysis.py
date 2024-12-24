import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import genpareto
from .data_handler import DataHandler

class GPDExtremeValueAnalysis(DataHandler):


    COLORS = {
    'histogram': '#66FF66',
    'fitted_line': '#FF5733',
    'var_line': '#33FFCE',
    'shape': '#FF6F61',
    'location': '#A6FF33',
    'scale': '#3380FF'
    }

    def __init__(self, symbol, start, end, alpha_input, threshold):
        super().__init__(symbol, start, end)
        self.alpha_input = alpha_input
        self.alpha = 1 - alpha_input
        self.threshold = abs(threshold)

        self.exceedances = None
        self.shape = None
        self.scale = None
        self.var = None
        self.var_direct = None

        self.get_exceedances()
        if len(self.exceedances) == 0:
            print("Brak przekroczeń dla podanego thresholdu – GPD nie zostało dopasowane.")
        else:
            self._fit_gpd()

    def get_exceedances(self):
        self.exceedances = self.returns[self.returns > self.threshold] - self.threshold

    def _fit_gpd(self):
        params = genpareto.fit(self.exceedances, floc=0)
        self.shape, loc, self.scale = params

        self.var = self.threshold + genpareto.ppf(self.alpha, self.shape, scale=self.scale)
        if self.shape != 0:
            self.var_direct = self.threshold + (self.scale / self.shape) * (
                ((1 - self.alpha)**(-self.shape) - 1)
            )
        else:
            self.var_direct = self.threshold + self.scale * np.log(1 / (1 - self.alpha))

    # Metoda publiczna, jeśli ktoś chce ponownie dopasować GPD po zmianie threshold
    def fit_gpd(self):
        self.get_exceedances()
        if len(self.exceedances) == 0:
            print("Brak przekroczeń dla podanego thresholdu.")
            return
        self._fit_gpd()

    def plot_negative_returns(self):
        if self.exceedances is None:
            print("Brak danych o exceedances – GPD nie zostało dopasowane.")
            return

        fig, ax = plt.subplots(figsize=(12, 6))
        neg_returns = -self.returns

        ax.plot(neg_returns, label='Log Returns', color='white')
        ax.axhline(y=-self.threshold, color='grey', linestyle='--', label='Threshold')

        idx = self.exceedances.index
        ax.scatter(idx, -self.returns.loc[idx], color='red', label='Exceedances', zorder=5)

        ax.set_title('Log Returns with Exceedances', color='white')
        ax.set_xlabel('Date', color='white')
        ax.set_ylabel('-Log Returns', color='white')
        ax.tick_params(colors='white')
        ax.grid(color='gray', linestyle='--', linewidth=0.7, alpha=0.5)
        ax.legend()
        plt.show()

    def plot_fitted_distribution(self):
        """
        Rysuje histogram surowych zwrotów (returns) przekraczających próg,
        dopasowany PDF GPD oraz pionową kreskę VaR. Rozciąga wykres w dalszej części ogona,
        pozostawiając początki i okolice VaR nienaruszone.
        """

        # Jeśli brak dopasowanego modelu, przerywamy
        if self.exceedances is None or self.shape is None:
            print("Brak dopasowanego GPD – nie można narysować rozkładu.")
            return

        # 1) Surowe zwroty powyżej thresholdu
        ret_exceed = self.returns[self.returns > self.threshold]
        if ret_exceed.empty:
            print("Brak przekroczeń w skali surowych zwrotów – nic do narysowania.")
            return

        # 2) Zakres osi X – rozciągnięty w końcowej części ogona
        x_min = min(ret_exceed.min(), self.var)
        x_max = max(ret_exceed.max(), self.var)

        # Dodajmy margines na końcu ogona (np. 20% różnicy między VaR a max(ret_exceed))
        tail_extension = abs(x_max - x_min) * 0.2
        x_max += tail_extension

        # 3) Przygotowanie siatki: większa gęstość w okolicach VaR, rzadsza w dalszej części ogona
        x_near_var = np.linspace(x_min, self.var, 150)  # Wysoka gęstość wokół VaR
        x_tail = np.linspace(self.var, x_max, 150)     # Rozciągnięcie końca ogona
        x = np.concatenate([x_near_var, x_tail])

        # Gęstość GPD w skali 'x - threshold'
        pdf_gpd = genpareto.pdf(
            x - self.threshold,
            self.shape,
            loc=0,
            scale=self.scale
        )

        fig, ax = plt.subplots(figsize=(12, 6))

        # 4) Histogram surowych przekroczeń
        ax.hist(
            ret_exceed,
            bins=10,
            density=True,
            alpha=0.6,
            color=COLORS['histogram'],  # np. 'cyan'
            edgecolor='white',
            label='Exceedances Histogram'
        )

        # 5) Krzywa PDF (rozciągnięta w ogonie)
        ax.plot(
            x,
            pdf_gpd,
            color=COLORS['fitted_line'],  # np. 'orange'
            label='Fitted GPD Distribution (shifted by threshold)'
        )

        # 6) Linia VaR
        ax.axvline(
            self.var,
            color='cyan',
            linestyle='--',
            linewidth=2,
            label=f'VaR ({self.alpha_input*100:.2f}%)'
        )

        # 7) Punkty surowych przekroczeń i ich gęstość
        ax.scatter(
            ret_exceed,
            genpareto.pdf(ret_exceed - self.threshold, self.shape, loc=0, scale=self.scale),
            color='red',
            zorder=5,
            label='Exceedances Points'
        )

        # 8) Ustawienia wykresu
        ax.set_title('Fitted GPD Distribution with Extended Tail', color='white')
        ax.set_xlabel('Returns', color='white')
        ax.set_ylabel('Density', color='white')
        ax.tick_params(colors='white')
        ax.grid(color='gray', linestyle='--', linewidth=0.7, alpha=0.5)
        ax.legend()

        # Odwrócenie osi X
        ax.invert_xaxis()

        plt.show()

    def print_summary_table(self):
        if self.exceedances is None or self.shape is None:
            print("Nie wywołano jeszcze dopasowania GPD – brak wyników do wyświetlenia.")
            return

        dist_type = self._distribution_type()
        df = pd.DataFrame({
            "Parameter": [
                "Distribution",
                "Shape (xi)",
                "Scale (sigma)",
                "Threshold (u)",
                "Number of Exceedances",
                "VaR",
                "VaR Direct"
            ],
            "Value": [
                dist_type,
                self.shape,
                self.scale,
                -self.threshold,
                len(self.exceedances),
                -self.var,
                -self.var_direct
            ]
        })
        print("\nGeneralized Pareto Analysis:\n")
        print(df.to_string(index=False))

    def _distribution_type(self):
        if self.shape is None:
            return "Not fitted"
        elif self.shape > 0:
            return "GPD (Pareto-type)"
        elif self.shape == 0:
            return "GPD (Exponential-type)"
        else:
            return "GPD (Beta-type)"

    def _multiple_threshold_analysis(self, threshold_list):
        results = []
        for thr in threshold_list:
            thr_abs = abs(thr)
            exceedances = self.returns[self.returns > thr_abs] - thr_abs
            if len(exceedances) == 0:
                continue

            shape, _, scale = genpareto.fit(exceedances, floc=0)
            var_val = thr_abs + genpareto.ppf(self.alpha, shape, scale=scale)

            if shape != 0:
                var_direct_val = thr_abs + (scale / shape) * (((1 - self.alpha)**(-shape) - 1))
            else:
                var_direct_val = thr_abs + scale * np.log(1/(1 - self.alpha))

            results.append({
                "Threshold": thr,
                "Shape": shape,
                "Scale": scale,
                "VaR": -var_val,          # Ujemna konwencja
                "VaR_Direct": -var_direct_val
            })

        return pd.DataFrame(results)

    def plot_threshold_analysis(self, threshold_list):
        """
        1) Generuje DataFrame z parametrami (Shape, Scale, VaR, VaR_Direct) dla różnych thresholdów.
        2) Rysuje wykresy Shape & Scale vs. Threshold oraz VaR vs. Threshold.
        Jedyny argument to threshold_list.
        """

        df_results = self._multiple_threshold_analysis(threshold_list)

        if df_results.empty:
            print("DataFrame pusty – brak wyników do wyświetlenia.")
            return

        # -- Wykres 1: Shape & Scale vs. Threshold --
        fig, ax = plt.subplots(figsize=(8, 6))
        abs_shape = df_results["Shape"].abs()  # w oryginalnym kodzie do wykresu brałeś wartość bezwzględną
        ax.plot(df_results["Threshold"], abs_shape, marker='o', color='blue', label='Shape')
        ax.plot(df_results["Threshold"], df_results["Scale"], marker='x', color='red',
                linestyle='--', label='Scale')
        ax.set_title("Shape & Scale vs. Threshold", color='white')
        ax.set_xlabel("Threshold Input", color='white')
        ax.set_ylabel("Value", color='white')
        ax.tick_params(colors='white')
        ax.grid(color='gray', linestyle='--', linewidth=0.7, alpha=0.5)
        ax.legend()
        plt.show()

        # -- Wykres 2: VaR vs. Threshold --
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(df_results["Threshold"], df_results["VaR"], marker='o',
                label=f'VaR (Alpha={self.alpha_input})', color='purple')
        ax.set_title("VaR vs. Threshold", color='white')
        ax.set_xlabel("Threshold Input", color='white')
        ax.set_ylabel("VaR", color='white')
        ax.tick_params(colors='white')
        ax.grid(color='gray', linestyle='--', linewidth=0.7, alpha=0.5)
        ax.legend()
        plt.show()