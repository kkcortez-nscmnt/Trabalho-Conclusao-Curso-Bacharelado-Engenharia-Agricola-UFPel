import numpy as np
import plotly.express as px
from sklearn.linear_model import LinearRegression
from src.criar_data_frame import CriarDataFrame
from yellowbrick.regressor import ResidualsPlot


class MinimosQuadradosNivelArea(LinearRegression):
    """
    Método dos mínimos quadrados considerando relação level-area
    """

    def __init__(self) -> None:
        self.data_frame = CriarDataFrame()
        self.lista_nivel = None
        self.lista_area = None
        self.file_path = None
        self.mmq_nivel_area = None

    def configurar_var_independente_nivel(self, file_path) -> np.ndarray:
        """
        Retorna matriz da variavel independente level.
        :param - file_path = string com caminho e nome do arquivo.
        :return - matriz numpy np.ndarray
        """
        self.file_path = file_path
        self.df = self.data_frame.cria_data_frame(self.file_path)
        self.lista_nivel = np.array(self.df.level)
        self.mtx_nivel = self.lista_nivel.reshape(-1, 1)

        return self.mtx_nivel

    def configurar_var_dependente_area(self, file_path) -> np.ndarray:
        """
        Retorna um matriz numpy da variavel independente area
        :param - file_path = string com o caminho e nome do arquivo.
        :return - Matriz numpy np.ndarray
        """
        self.file_path = file_path
        self.df = self.data_frame.cria_data_frame(file_path)
        self.lista_area = np.array(self.df.area)
        self.mtx_area = self.lista_area.reshape(-1, 1)

        return self.mtx_area

    def minimos_quadrados_nivel_area(self, mtx_nivel, mtx_area) -> None:
        """
        Executa o ajuste da reta pelo método dos mínimos quadrados.
        :param - mtx_nivel = matriz numpy com os valores de nível.
               - mtx_area = matriz numpy com os valores de area.
        :return - None
        """
        self.mtx_nivel = mtx_nivel
        self.mtx_area = mtx_area
        self.mmq_nivel_area = LinearRegression()
        self.mmq_nivel_area.fit(mtx_nivel, mtx_area)
        return None

    def obter_coef_linear(self) -> float:
        """
        Retorna o coeficiente linear da reta
        :param - None
        :return - float
        """
        self.coef_linear = self.mmq_nivel_area.intercept_
        return float(round(self.coef_linear[0], 3))

    def obter_coef_angular(self) -> float:
        """
        Retorna o coeficiente angular da reta
        :param - None
        :return - float
        """
        self.coef_angular = self.mmq_nivel_area.coef_
        return float(round(self.coef_angular[0][0], 3))

    def obter_variaveis_estimadas_de_area(self, var_independente) -> np.ndarray:
        """
        Realiza as previsões de acordo com a reta ajustada
        """
        self.var_independente_nivel = var_independente
        self.var_estimada = self.mmq_nivel_area.predict(self.var_independente_nivel)
        return self.var_estimada

    def plotar_grafico_do_ajuste_nivel_area(self, eixo_x, eixo_y, estimados) -> None:
        """
        Plota o gráfico do ajuste linear pelo mínimos quadrados.

        :param - eixo_x = variavel independente
               - eixo_y = variavel dependente
               - estimados = variaveis estimadas através do ajuste da reta pelo minimos quadrados
        :return - None
        """
        self.eixo_x = eixo_x
        self.eixo_y = eixo_y
        self.coef_cor = self.mmq_nivel_area.score(self.eixo_x, self.eixo_y)
        self.eixo_x = eixo_x.ravel()
        self.eixo_y = eixo_y.ravel()
        self.estimados = estimados.ravel()

        self.grafico = px.scatter(
            x=self.eixo_x,
            y=self.eixo_y,
            title=f"Área(m²) = {round(self.coef_angular[0][0],3)} * nível(m) + {round(self.coef_linear[0],3)} R² = {round(self.coef_cor, 3)} ",
        )
        self.grafico.add_scatter(
            x=self.eixo_x,
            y=self.estimados,
            name="Reta Ajustada",
        )
        self.grafico.update_layout(xaxis_title="Nível (m)", yaxis_title="Área (m²)")
        self.grafico.show()

    def plotar_grafico_residuais_nivel_area(self, eixo_x, eixo_y) -> None:
        """
        Plota o gráfico de visualização residual da relação entre os dados e a reta ajustada.
        :param - eixo_x = variavel independente
               - eixo_y = variavel dependente
        :return - None
        """
        self.eixo_x = eixo_x
        self.eixo_y = eixo_y

        self.visualizador = ResidualsPlot(self.mmq_nivel_area)
        self.visualizador.fit(self.eixo_x, self.eixo_y)
        self.visualizador.poof()
