import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class Visualizations:
    """
    A class used to create visualizations for data analysis.

    Methods
    -------
    plot_histogram(df, column, bins=10, title=None, xlabel=None, ylabel=None)
        Plots a histogram for a specified column in the DataFrame.
    plot_scatter(df, x, y, hue=None, title=None, xlabel=None, ylabel=None)
        Plots a scatter plot for two specified columns in the DataFrame.
    plot_boxplot(df, column, by=None, title=None, xlabel=None, ylabel=None)
        Plots a boxplot for a specified column in the DataFrame.
    plot_heatmap(df, title=None, xlabel=None, ylabel=None)
        Plots a heatmap of the correlation matrix for the DataFrame.
    plot_line(df, x, y, title=None, xlabel=None, ylabel=None)
        Plots a line chart for two specified columns in the DataFrame.
    plot_bar(df, x, y, title=None, xlabel=None, ylabel=None)
        Plots a bar chart for two specified columns in the DataFrame.
    plot_pie(df, column, title=None)
        Plots a pie chart for a specified column in the DataFrame.
    plot_pairplot(df, hue=None)
        Plots a pairplot for the DataFrame.
    plot_violin(df, x, y, hue=None, title=None, xlabel=None, ylabel=None)
        Plots a violin plot for the DataFrame.
    """

    @staticmethod
    def plot_histogram(df, column, bins=10, title=None, xlabel=None, ylabel=None):
        """
        Plots a histogram for a specified column in the DataFrame.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame containing the data.
        column : str
            The column to plot.
        bins : int, optional
            The number of bins for the histogram (default is 10).
        title : str, optional
            The title of the plot.
        xlabel : str, optional
            The label for the x-axis.
        ylabel : str, optional
            The label for the y-axis.

        Returns
        -------
        None
        """
        plt.figure(figsize=(10, 6))
        sns.histplot(df[column], bins=bins, kde=True)
        plt.title(title if title else f"Histogram of {column}")
        plt.xlabel(xlabel if xlabel else column)
        plt.ylabel(ylabel if ylabel else "Frequency")
        plt.show()

    @staticmethod
    def plot_scatter(df, x, y, hue=None, title=None, xlabel=None, ylabel=None):
        """
        Plots a scatter plot for two specified columns in the DataFrame.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame containing the data.
        x : str
            The column for the x-axis.
        y : str
            The column for the y-axis.
        hue : str, optional
            The column to use for color encoding.
        title : str, optional
            The title of the plot.
        xlabel : str, optional
            The label for the x-axis.
        ylabel : str, optional
            The label for the y-axis.

        Returns
        -------
        None
        """
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=df, x=x, y=y, hue=hue)
        plt.title(title if title else f"Scatter Plot of {x} vs {y}")
        plt.xlabel(xlabel if xlabel else x)
        plt.ylabel(ylabel if ylabel else y)
        plt.show()

    @staticmethod
    def plot_boxplot(df, column, by=None, title=None, xlabel=None, ylabel=None):
        """
        Plots a boxplot for a specified column in the DataFrame.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame containing the data.
        column : str
            The column to plot.
        by : str, optional
            The column to group by.
        title : str, optional
            The title of the plot.
        xlabel : str, optional
            The label for the x-axis.
        ylabel : str, optional
            The label for the y-axis.

        Returns
        -------
        None
        """
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=df, x=by, y=column)
        plt.title(title if title else f"Boxplot of {column}")
        plt.xlabel(xlabel if xlabel else by)
        plt.ylabel(ylabel if ylabel else column)
        plt.show()

    @staticmethod
    def plot_heatmap(df, title=None, xlabel=None, ylabel=None):
        """
        Plots a heatmap of the correlation matrix for the DataFrame.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame containing the data.
        title : str, optional
            The title of the plot.
        xlabel : str, optional
            The label for the x-axis.
        ylabel : str, optional
            The label for the y-axis.

        Returns
        -------
        None
        """
        plt.figure(figsize=(12, 8))
        corr = df.corr()
        sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
        plt.title(title if title else "Heatmap of Correlation Matrix")
        plt.xlabel(xlabel if xlabel else "Features")
        plt.ylabel(ylabel if ylabel else "Features")
        plt.show()

    @staticmethod
    def plot_line(df, x, y, title=None, xlabel=None, ylabel=None):
        """
        Plots a line chart for two specified columns in the DataFrame.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame containing the data.
        x : str
            The column for the x-axis.
        y : str
            The column for the y-axis.
        title : str, optional
            The title of the plot.
        xlabel : str, optional
            The label for the x-axis.
        ylabel : str, optional
            The label for the y-axis.

        Returns
        -------
        None
        """
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=df, x=x, y=y)
        plt.title(title if title else f"Line Chart of {x} vs {y}")
        plt.xlabel(xlabel if xlabel else x)
        plt.ylabel(ylabel if ylabel else y)
        plt.show()

    @staticmethod
    def plot_bar(df, x, y, title=None, xlabel=None, ylabel=None):
        """
        Plots a bar chart for two specified columns in the DataFrame.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame containing the data.
        x : str
            The column for the x-axis.
        y : str
            The column for the y-axis.
        title : str, optional
            The title of the plot.
        xlabel : str, optional
            The label for the x-axis.
        ylabel : str, optional
            The label for the y-axis.

        Returns
        -------
        None
        """
        plt.figure(figsize=(10, 6))
        sns.barplot(data=df, x=x, y=y)
        plt.title(title if title else f"Bar Chart of {x} vs {y}")
        plt.xlabel(xlabel if xlabel else x)
        plt.ylabel(ylabel if ylabel else y)
        plt.show()

    @staticmethod
    def plot_pie(df, column, title=None):
        """
        Plots a pie chart for a specified column in the DataFrame.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame containing the data.
        column : str
            The column to plot.
        title : str, optional
            The title of the plot.

        Returns
        -------
        None
        """
        plt.figure(figsize=(8, 8))
        df[column].value_counts().plot.pie(
            autopct="%1.1f%%", startangle=90, cmap="viridis"
        )
        plt.title(title if title else f"Pie Chart of {column}")
        plt.ylabel("")
        plt.show()

    @staticmethod
    def plot_pairplot(df, hue=None):
        """
        Plots a pairplot for the DataFrame.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame containing the data.
        hue : str, optional
            The column to use for color encoding.

        Returns
        -------
        None
        """
        sns.pairplot(df, hue=hue)
        plt.show()

    @staticmethod
    def plot_violin(df, x, y, hue=None, title=None, xlabel=None, ylabel=None):
        """
        Plots a violin plot for the DataFrame.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame containing the data.
        x : str
            The column for the x-axis.
        y : str
            The column for the y-axis.
        hue : str, optional
            The column to use for color encoding.
        title : str, optional
            The title of the plot.
        xlabel : str, optional
            The label for the x-axis.
        ylabel : str, optional
            The label for the y-axis.

        Returns
        -------
        None
        """
        plt.figure(figsize=(10, 6))
        sns.violinplot(data=df, x=x, y=y, hue=hue, split=True)
        plt.title(title if title else f"Violin Plot of {x} vs {y}")
        plt.xlabel(xlabel if xlabel else x)
        plt.ylabel(ylabel if ylabel else y)
        plt.show()
