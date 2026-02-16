# src/module/reports/plot_generator.py
import logging
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

logger = logging.getLogger(__name__)

class BasePlot:

    def __init__(self, df: pd.DataFrame, base_dir: Path, name: str):
        """
        Clase base para generar gráficos.

        :param df: DataFrame con los datos
        :param base_dir: raíz del proyecto (para crear generated/plots)
        :param name: nombre base del plot (ej: 'category_plot')
        """
        self.df = df
        self.name = name
        self._base_dir = Path(base_dir)

        # Carpeta de plots
        self.plots_dir = self._base_dir / "generated" / "plots"
        self.plots_dir.mkdir(parents=True, exist_ok=True)

    def save_plot(self, fig: plt.Figure, filename: str = None):
        """
        Guarda la figura en la carpeta generated/plots

        :param fig: Figura de matplotlib a guardar
        :param filename: Nombre del archivo
        """
        if filename is None:
            filename = f"{self.name}.png"
        output_path = self.plots_dir / filename
        fig.savefig(output_path, bbox_inches='tight')
        plt.close(fig)

    def plot(self):
        """
        Método que debe implementar cada plot concreto
        """
        raise NotImplementedError("Cada plot debe implementar el método plot()")

# ----------------------------------------------------------
# Plot concreto: BarPlot
# ----------------------------------------------------------
class BarPlot(BasePlot):
    """
    Genera un bar_plot.
    Recibe opcionalmente título, xlabel, ylabel y color.
    :param df: DataFrame con los datos
    :param base_dir: raíz del proyecto (para crear generated/plots)
    :param name: nombre base del plot
    :param column: columna del DataFrame para el grafico
    :param title: título del gráfico
    :param xlabel: etiqueta del eje x
    :param ylabel: etiqueta del eje y
    :param color: color de las barras
    """
    def __init__(self, df: pd.DataFrame, base_dir: Path, name: str,
                 column: str, title: str = None, xlabel: str = None,
                 ylabel: str = None, color: str = "blue") -> None:
        super().__init__(df, base_dir, name)
        self.column = column
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.color = color

    def plot(self):
        if self.column not in self.df.columns:
            logger.error(f"'{self.column}' no existe en el DataFrame")
            return

        counts = self.df[self.column].value_counts()
        fig, ax = plt.subplots(figsize=(8, 6))
        counts.plot(kind='bar', ax=ax, color=self.color)

        # Añadir etiquetas sobre cada barra
        ax.bar_label(ax.containers[0], fontsize=10)

        ax.set_title(self.title or f"Gráfico de {self.column}")
        ax.set_xlabel(self.xlabel or self.column)
        ax.set_ylabel(self.ylabel or "Cantidad")
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        filename = f"{self.column}_plot.png"

        self.save_plot(fig, filename)
