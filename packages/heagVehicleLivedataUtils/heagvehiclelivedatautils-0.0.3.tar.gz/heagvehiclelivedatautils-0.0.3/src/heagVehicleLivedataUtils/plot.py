"""
provides the DataAnalysis class which provides tools for plotting the vehicle data

TODO: stuff for ploting data
"""

import pandas as pd

from .vehicleDataUtils.read import vehicledata_from_json_files, verify_vehicledata_format
from .vehicleDataUtils.process import trams_in_service, number_of_trams_in_service, buses_in_service
from .vehicleInformation import decode_line_id, heagLineColormap, modern_tram_numbers, usual_tram_numbers, \
    electric_bus_numbers
import matplotlib.pyplot as plt
import seaborn as sns

from os import listdir
from os.path import isfile,join


def __plot_vehicle_service_timeseries__(vehicle_service_timeseries: pd.DataFrame,
                                      *,
                                      filename: str = None,
                                      show_plot: bool= True,
                                      show_line_annotation = False,
                                      datespec: str = '%d.%m.%Y-%H:%M',
                                      sample_time: str = '15Min',
                                      title: str = 'Vehicles in service',
                                      figsize: tuple[int,int] = (20,30)):
    """
    plots the timeseries

    Args:
        vehicle_service_timeseries: dataframe containing timeseries with vehicle service
        show_line_annotation: if true, line Names will also be plotted
        datespec: specifies how timestamp is displayed -> used as argument for pandas strftime
        filename: path of file that is used to save the plot. if left empty, nothing will be saved
        show_plot: true if the plot should be shown
        sample_time: sample size of the plot
        figsize: matplotlib figsize to be used for the plot
        title: title of the plot

    """

    vehicle_service_timeseries = vehicle_service_timeseries.fillna(0).resample(sample_time).max()

    # fillna a second time to account for missing timeframe
    vehicle_service_timeseries = vehicle_service_timeseries.fillna(0).astype('int64')

    # format index for plotting
    vehicle_service_timeseries.index = vehicle_service_timeseries.index.strftime(datespec)

    plt.figure(figsize=figsize)

    if show_line_annotation:
        line_annotation = vehicle_service_timeseries.map(lambda x: f'{decode_line_id(x)}' if x != 0 else '')
        sns.heatmap(vehicle_service_timeseries, annot=line_annotation, fmt='', vmin=0, vmax=10,
                    cmap=heagLineColormap, cbar=False)
    else:
        sns.heatmap(vehicle_service_timeseries, vmin=0, vmax=10, cmap=heagLineColormap, cbar=False)

    plt.title(title)
    if filename is not None:
        plt.savefig(filename)
    if show_plot:
        plt.show()
    plt.close()


class DataAnalysis:
    """
    Class to provide tools to analyze given vehicle data.
    In particular it provides vehicles in service and number of vehicles in service plots

    TODO: add a bit of detail
    """

    def __init__(self,
                 /,
                 vehicledata: pd.DataFrame = None,
                 *,
                 vehicledata_path: str = None,
                 response_paths: list[str] = None
                 ):
        """


        Args:
            vehicledata: dataframe containing vehicle data. if vehicledata_path or response_paths are specified, this will be disregarded

            vehicledata_path: path to directory where to look for vehicle data json files. if vehicledata is specified, this will be disregarded
            response_paths: paths of files containing vehicle data json. if vehicledata_path or vehicledata are specified, this will be disregarded
        """

        self.__vehicledata__: pd.DataFrame
        self.__trams_in_servie__: pd.DataFrame
        self.__buses_in_service__: pd.DataFrame

        if (vehicledata_path is not None) + (response_paths is not None) + (vehicledata is not None) > 1:
            # more than one data sources specified
            Warning("more than one data sources specified, only the fist one will be regarded")


        if vehicledata is not None:
            self.__set_vehicledata_dataframe__(vehicledata)
        elif vehicledata_path is not None:
            self.__set_analyse_path__(vehicledata_path)
        elif response_paths is not None:
            self.__set_response_paths__(response_paths)


    def __set_analyse_path__(self, vehicledata_path: str):
        """
        provide vehicle data via a directory to scan.

        Args:
            vehicledata_path: path to directory where to look for vehicle data json files
        """
        response_paths = [
            join(vehicledata_path,f) for f in listdir(vehicledata_path)
            if isfile(join(vehicledata_path,f)) and f[-4:]== 'json'
        ]
        self.__set_response_paths__(response_paths)

    def __set_response_paths__(self, api_response_paths: list[str]):
        """
        provide vehicle via files containing vehicle data json.

        Args:
            api_response_paths: paths of files containing vehicle data json
        """
        self.__set_vehicledata_dataframe__(vehicledata_from_json_files(api_response_paths))

    def __set_vehicledata_dataframe__(self, vehicledata: pd.DataFrame):
        """
        provide vehicledata dataframe directly
        Args:
            vehicledata: dataframe to analyze
        """
        verify_vehicledata_format(vehicledata)

        self.__vehicledata__ = vehicledata
        self.__trams_in_servie__ = trams_in_service(vehicledata)
        self.__buses_in_service__ = buses_in_service(vehicledata)

    def get_vehicledata(self) -> pd.DataFrame:
        """

        Returns: the vehicledata dataframe

        """
        return self.__vehicledata__

    def get_trams_in_service(self) -> pd.DataFrame:
        """

        Returns: the dataframe containing the service assignemt of the trams in this analysis

        """
        return self.__trams_in_servie__

    def get_buses_in_service(self) -> pd.DataFrame:
        """

        Returns: the dataframe containing the service assignemt of the buses in this analysis

        """

        return self.__buses_in_service__

    def plot_number_of_trams_in_service(self,
                                        *,
                                        filename: str = None,
                                        show_plot: bool = True,
                                        sample_time: str = '15Min',
                                        datespec: str = '%d.%m.%Y-%H:%M',
                                        figsize: tuple[int, int] = (25,10)
                                        ):
        """

        Args:
            datespec: specififes how timestamp is displayed TODO: was ist da der spec?
            sample_time: sample size of the plot
            figsize:  figsize to be used for the plot
            show_plot: currently only placeholder
            filename: path of file that is used to save the plot. if left empty, nothing will be saved

        """
        number_of_trams_over_time = number_of_trams_in_service(self.__trams_in_servie__)
        number_of_trams_over_time = number_of_trams_over_time.resample(sample_time).mean()

        number_of_trams_over_time.index = number_of_trams_over_time.index.strftime(datespec)

        ax = number_of_trams_over_time.plot(
            kind="bar",
            stacked=True,
            title='HEAG Fahrzeugeinsätzte',
            ylim=(0, 45),
            ylabel="Anzahl Fahrzeuge im Linienbetrieb",
            figsize=figsize,
            width=1)

        if filename is not None:
            ax.figure.savefig(filename)
        # TODO: how does this work in the context here?
        #if show_plot:
        #    plt.show()

    def plot_trams_in_servie(self,
                             /,
                             tram_numbers: list[str],
                             *,
                             filename: str = None,
                             show_plot: bool= True,
                             show_line_annotation = False, #testing has shown that annotation is what takes most of the runtime
                             datespec: str = '%d.%m.%Y-%H:%M',
                             sample_time: str = '15Min',
                             figsize: tuple[int,int] = (20,30)):
        """
        plots the line assignment for the specifid trams

        Args:
            show_line_annotation: if true, line Names will also be plotted
            datespec: specififes how timestamp is displayed TODO: was ist da der spec?
            tram_numbers: list of operational Numbers of the for witch the service status is supposed to be displayed
            filename: path of file that is used to save the plot. if left empty, nothing will be saved
            show_plot: true if the plot should be shown
            sample_time: sample size of the plot
            figsize: figsize to be used for the plot
        """

        __plot_vehicle_service_timeseries__(self.__trams_in_servie__.reindex(columns=tram_numbers),
                                          title = "Trams in service",
                                          filename=filename,
                                          show_line_annotation=show_line_annotation,
                                          show_plot=show_plot,
                                          datespec=datespec,
                                          sample_time=sample_time,
                                          figsize=figsize )

    def plot_modern_trams_in_service(self,
                                     *,
                                     filename: str = None,
                                     show_plot: bool= True,
                                     show_line_annotation = False,
                                     datespec: str = '%d.%m.%Y-%H:%M',
                                     sample_time: str = '15Min',
                                     figsize: tuple[int,int] = (20,30)):
        """
        like plot_trams_in_servie, but only plots modern trams

        Args:
            show_line_annotation: if true, line Names will also be plotted
            datespec: specififes how timestamp is displayed TODO: was ist da der spec?
            filename: path of file that is used to save the plot. if left empty, nothing will be saved
            show_plot: true if the plot should be shown
            sample_time: sample size of the plot
            figsize: figsize to be used for the plot

        """
        self.plot_trams_in_servie(modern_tram_numbers, filename=filename, show_plot=show_plot, show_line_annotation=show_line_annotation, datespec=datespec, sample_time=sample_time, figsize=figsize)

    # das ist eventuell redundent, könnte auch einfach als default wert bei plot_trams_in_servie gemacht werden
    def plot_all_trams_in_service(self,
                                     *,
                                     filename: str = None,
                                     show_plot: bool= True,
                                     show_line_annotation = False,
                                     datespec: str = '%d.%m.%Y-%H:%M',
                                     sample_time: str = '15Min',
                                     figsize: tuple[int,int] = (20,30)):
        """
       like plot_trams_in_servie, but without the ability to specify trams

       Args:
            show_line_annotation: if true, line Names will also be plotted
           datespec: specififes how timestamp is displayed TODO: was ist da der spec?
           filename: path of file that is used to save the plot. if left empty, nothing will be saved
           show_plot: true if the plot should be shown
           sample_time: sample size of the plot
           figsize: figsize to be used for the plot

       """
        self.plot_trams_in_servie(usual_tram_numbers, filename=filename, show_plot=show_plot, show_line_annotation=show_line_annotation, datespec=datespec, sample_time=sample_time, figsize=figsize)

    def plot_electric_buses_in_service(self,
                                       *,
                                     filename: str = None,
                                     show_plot: bool= True,
                                     show_line_annotation = True,
                                     datespec: str = '%d.%m.%Y-%H:%M',
                                     sample_time: str = '15Min',
                                     figsize: tuple[int,int] = (20,30)):
        """
        plots the line assignment for the electric buses

        Args:
            show_line_annotation: if true, line Names will also be plotted
            datespec: specififes how timestamp is displayed TODO: was ist da der spec?
            filename: path of file that is used to save the plot. if left empty, nothing will be saved
            show_plot: true if the plot should be shown
            sample_time: sample size of the plot
            figsize: figsize to be used for the plot
        """

        __plot_vehicle_service_timeseries__(self.__buses_in_service__.reindex(columns=electric_bus_numbers),
                                          title="Buses in service",
                                          filename=filename,
                                          show_line_annotation=show_line_annotation,
                                          show_plot=show_plot,
                                          datespec=datespec,
                                          sample_time=sample_time,
                                          figsize=figsize)

    def plot_buses_in_service(self,
                              bus_numbers: list[str],
                               *,
                              filename: str = None,
                             show_plot: bool= True,
                             show_line_annotation = True,
                             datespec: str = '%d.%m.%Y-%H:%M',
                             sample_time: str = '15Min',
                             figsize: tuple[int,int] = (20,30)):
        """
        plots the line assignment for the electric buses

        Args:
            bus_numbers: list of Betriebsnummber of the buses whose servie is to be plotted
            show_line_annotation: if true, line Names will also be plotted
            datespec: specififes how timestamp is displayed TODO: was ist da der spec?
            filename: path of file that is used to save the plot. if left empty, nothing will be saved
            show_plot: true if the plot should be shown
            sample_time: sample size of the plot
            figsize: figsize to be used for the plot
        """

        __plot_vehicle_service_timeseries__(self.__buses_in_service__.reindex(columns=bus_numbers),
                                          title="Buses in service",
                                          filename=filename,
                                          show_line_annotation=show_line_annotation,
                                          show_plot=show_plot,
                                          datespec=datespec,
                                          sample_time=sample_time,
                                          figsize=figsize)
