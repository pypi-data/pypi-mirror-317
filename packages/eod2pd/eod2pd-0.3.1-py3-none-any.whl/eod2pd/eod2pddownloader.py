"""
# =============================================================================
#
#  Licensed Materials, Property of Ralph Vogl, Munich
#
#  Project : eod2pd
#
#  Copyright (c) by Ralph Vogl
#
#  All rights reserved.
#
#  Description:
#
#  a simple library to quere EODHistoricalData in a multithreaded environment
#
# =============================================================================
"""

from dataclasses import dataclass
from typing import List
import datetime
import basefunctions
import pandas as pd
import secretfunctions
import eod2pd

# -------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------

# -------------------------------------------------------------
# DEFINITIONS REGISTRY
# -------------------------------------------------------------

# -------------------------------------------------------------
# DEFINITIONS
# -------------------------------------------------------------


@dataclass
class EOD2PDFormatOptions:
    """
    This class defines the format options for the EOD2PD message handler.

    """

    combine: bool = (False,)
    normalize: bool = (False,)
    dropna_tickers: bool = (False,)
    dropna: bool = (False,)
    drop_volume: bool = (False,)
    capitalize: bool = (False,)
    format_stockstats: bool = (False,)


@dataclass
class EOD2PDMessageContent:
    """
    This class defines the message content for the EOD2PD message handler.

    """

    type: str = None
    key: str = None
    url: str = None
    params: dict = None


# -------------------------------------------------------------
# VARIABLE DEFINTIONS
# -------------------------------------------------------------


# -------------------------------------------------------------
#  CLASS DEFINITIONS
# -------------------------------------------------------------
class EOD2PDDownloader:

    def __init__(self, config_file_path: str = None):
        """
        Initialize the EOD2PDDownloader and load the configuration

        Parameters
        ----------
        config_file_path : str, optional
            The name of the configuration file to be used, default: None.
            If a configuration file is given, the configuration is loaded from this file.
        """
        # check if the config_file_name is given
        if config_file_path:
            # load the configuration from the file
            basefunctions.ConfigHandler().load_config(config_file_path)
                
        # register "eod2pd" message handler
        basefunctions.default_threadpool.register_message_handler(
            msg_type=eod2pd.EOD2PDMESSAGEIDENTIFIER,
            msg_handler=eod2pd.EOD2PDDownloaderCallable(),
        )

    # -------------------------------------------------------------
    #  start jobs get list of exchanges from EODHistoricalData
    # -------------------------------------------------------------
    def start_jobs_get_exchanges(
        self,
        params: dict = None,
        hook: basefunctions.ThreadPoolHookObjectInterface = None,
    ) -> None:
        """
        Get the list of exchanges from EODHistoricalData.

        Parameters
        ----------
        params : dict, optional
            Additional parameters to be used, default: None
        hook: basefunctions.ThreadPoolHookObjectInterface, optional
            A hook to be used, default: None

        Returns
        -------
        pandas.DataFrame
            DataFrame containing the list of exchanges.
        """
        # load api key from basefunctions secret handler
        api_key = basefunctions.SecretHandler().get_secret_value(
            key="EOD2PD_API_KEY", default_value=None
        )
        if api_key is None:
            raise ValueError("##FAILURE## EOD2PD_API_KEY is not set")
        # build url
        url = (
            f"https://eodhistoricaldata.com/api/exchanges-list/"
            f"?api_token={api_key}"
            f"&fmt=json"
        )

        # create message content
        message_content = EOD2PDMessageContent()
        message_content.type = "exchanges"
        message_content.key = "exchanges"
        message_content.url = url
        message_content.params = params

        # put message into input queue
        self.send_message(message_content, hook)

    # -------------------------------------------------------------
    #  get list of exchanges from EODHistoricalData
    # -------------------------------------------------------------
    def get_exchanges(self, dict_result: bool = True) -> pd.DataFrame:
        """
        Get the list of exchanges from EODHistoricalData.

        Parameters
        ----------
        dict_result : bool, optional
            A flag to indicate if the result should be a dictionary, default: True

        Returns
        -------
        pandas.DataFrame | dict
            DataFrame containing the list of exchanges or
            a dictionary containing the list of exchanges.
        """
        # start jobs to get exchanges
        self.start_jobs_get_exchanges()
        # wait until all jobs are done
        basefunctions.get_default_threadpool().get_input_queue().join()
        # add index to dataframe
        index_row = {
            "name": "Index Exchange",
            "code": "INDX",
            "operatingmic": "INDX",
            "country": "Unknown",
            "currency": "Unknown",
            "countryiso2": "Unknown",
            "countryiso3": "Unknown",
        }
        # get dataframes from output queue
        result = eod2pd.utils.get_dataframes_from_output_queue(dict_result=dict_result)

        # get the first dataframe or create an empty one if necessary
        df = (list(result.values())[0] if isinstance(result, dict) and result else result) if isinstance(result, pd.DataFrame) and not result.empty else pd.DataFrame()

        # append index_row to the dataframe
        df = df.append(index_row, ignore_index=True) if not df.empty else pd.DataFrame([index_row])

        # return the result
        return df if not dict_result else {"exchanges": df}


    # -------------------------------------------------------------
    #  start jobs get list of symbols for a specific exchange from EODHistoricalData
    # -------------------------------------------------------------
    def start_jobs_get_exchanges_symbols(
        self,
        exchange: str = None,
        params: dict = None,
        hook: basefunctions.ThreadPoolHookObjectInterface = None,
    ) -> None:
        """
        Get the list of symbols for a specific exchange from EODHistoricalData.

        Parameters
        ----------
        exchangeCode : str, optional
            The code of the exchange, default: "XETRA"
        params : dict, optional
            Additional parameters to be used, default: None
        hook: basefunctions.ThreadPoolHookObjectInterface, optional
            A hook to be used, default: None

        Returns
        -------
        pandas.DataFrame
            DataFrame containing the list of symbols for the specified exchange.
        """
        # load api key from basefunctions secret handler
        api_key = basefunctions.SecretHandler().get_secret_value(
            key="EOD2PD_API_KEY", default_value=None
        )
        if api_key is None:
            raise ValueError("##FAILURE## EOD2PD_API_KEY is not set")
        # check if exchange is None
        if exchange is None:
            exchange = "XETRA"
        # build url
        url = (
            f"https://eodhistoricaldata.com/api/exchange-symbol-list/"
            f"{exchange}"
            f"?api_token={api_key}"
            f"&fmt=json"
        )

        # create message content
        message_content = EOD2PDMessageContent()
        message_content.type = "exchange-symbols-list"
        message_content.key = exchange
        message_content.url = url
        message_content.params = params

        # put message into input queue
        self.send_message(message_content, hook)

    # -------------------------------------------------------------
    #  get list of symbols for a specific exchange from EODHistoricalData
    # -------------------------------------------------------------
    def get_exchanges_symbols(
        self,
        exchanges: List[str] = None,
        dict_result: bool = True,
    ) -> pd.DataFrame | dict:
        """
        Get the list of symbols for a specific exchanges from EODHistoricalData.

        Parameters
        ----------
        exchanges : list, optional
            A list of exchanges, default: None
        dict_result : bool, optional
            A flag to indicate if the result should be a dictionary, default: True

        Returns
        -------
        pandas.DataFrame | dict
            a DataFrame containing the list of symbols for the specified exchange or
            a dictionary containing the list of symbols for the specified exchanges
        """
        # check if exchanges is None
        if exchanges is None:
            exchanges = ["XETRA"]
        # check if exchanges is a string
        if isinstance(exchanges, str):
            exchanges = [exchanges]
        # loop over all exchanges
        for exchange in exchanges:
            # start jobs to get symbols for exchange
            self.start_jobs_get_exchanges_symbols(exchange.upper())
        # wait until all jobs are done
        basefunctions.get_default_threadpool().get_input_queue().join()
        # get dataframes from output queue
        return eod2pd.utils.get_dataframes_from_output_queue(dict_result=dict_result)

    # -------------------------------------------------------------
    #  start jobs get symbol prices in a bulk message from EODHistoricalData
    # -------------------------------------------------------------
    def start_jobs_get_symbols_prices_bulk(
        self,
        exchange: str = None,
        start_date: str | datetime.date = None,
        end_date: str | datetime.date = None,
        params: dict = None,
        hook: basefunctions.ThreadPoolHookObjectInterface = None,
    ) -> None:
        """
        Get bulk symbol prices for the given exchange and date.

        Parameters
        ----------
        exchange : str, optional
            The code of the exchange, default: "XETRA"
        start_date : str, optional
            The start date of the prices data, the format is "YY-mm-dd",
            default: None
        end_date : str, optional
            The end date of the prices data, the format is "YY-mm-dd",
            default: None
        params : dict, optional
            Additional parameters to be used, default: None
        hook: basefunctions.ThreadPoolHookObjectInterface, optional
            A hook to be used, default: None

        Returns
        -------
        pandas.DataFrame
            A DataFrame containing the bulk symbol prices for the given
            exchange and date.
        """
        # load api key from basefunctions secret handler
        api_key = basefunctions.SecretHandler().get_secret_value(
            key="EOD2PD_API_KEY", default_value=None
        )
        if api_key is None:
            raise ValueError("##FAILURE## EOD2PD_API_KEY is not set")
        # check if exchange is None
        if exchange is None:
            exchange = "XETRA"
        # make exchange uppercase
        exchange = exchange.upper()
        # check if start and end are None
        if start_date is None:
            start_date = datetime.datetime.today()
        if end_date is None:
            end_date = datetime.datetime.today()
        if isinstance(start_date, str):
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        if isinstance(end_date, str):
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        # check if date range is too big, we only allow a range of 30 days
        if (end_date - start_date).days > 30:
            raise ValueError("##FAILURE## date range is too big, we only allow a range of 30 days")
        # loop over all dates
        for date in pd.date_range(start=start_date, end=end_date):
            # build the url for the request
            url = (
                f"https://eodhistoricaldata.com/api/eod-bulk-last-day/"
                f"{exchange}"
                f"?api_token={api_key}"
                f"&date={date.date()}"
                f"&fmt=json"
            )

            # create message content
            message_content = EOD2PDMessageContent()
            message_content.type = "exchange-symbols-prices-bulk"
            message_content.key = (exchange, date.date())
            message_content.url = url
            message_content.params = params

            # put message into input queue
            self.send_message(message_content, hook)

    # -------------------------------------------------------------
    #  get symbol prices in a bulk message from EODHistoricalData
    # -------------------------------------------------------------
    def get_symbols_prices_bulk(
        self,
        exchanges: List[str] = None,
        start_date: str = None,
        end_date: str = None,
        dict_result: bool = True,
    ) -> pd.DataFrame | dict:
        """
        Get bulk symbol prices for the given exchanges and date.

        Parameters
        ----------
        exchanges : str, optional
            A list of exchanges, default: ["XETRA"]
        start_date : str, optional
            The start date of the prices data, the format is "YY-mm-dd",
            default: None
        end_date : str, optional
            The end date of the prices data, the format is "YY-mm-dd",
            default: None
        dict_result : bool, optional
            A flag to indicate if the result should be a dictionary, default: True

        Returns
        -------
        pandas.DataFrame | dict
            A DataFrame containing the bulk symbol prices for the given or
            a dictionary containing the bulk symbol prices for the given
            exchange and dates.
        """
        # check if exchanges is None
        if exchanges is None:
            exchanges = ["XETRA"]
        # check if exchanges is a string
        if isinstance(exchanges, str):
            exchanges = [exchanges]
        # loop over all exchanges
        for exchange in exchanges:
            # start jobs to get symbols bulk prices
            self.start_jobs_get_symbols_prices_bulk(exchange, start_date, end_date)

        # wait until all jobs are done
        basefunctions.get_default_threadpool().get_input_queue().join()

        # get dataframes from output queue
        return eod2pd.utils.get_dataframes_from_output_queue(dict_result=dict_result)

    # -------------------------------------------------------------
    #  start_jobs_get symbol prices from EODHistoricalData
    # -------------------------------------------------------------
    def start_jobs_get_symbols_prices(
        self,
        symbols: List[str] | None,
        start_date: str = "1900-01-01",
        end_date: str = "2999-12-31",
        freq: str = "D",
        params: dict = None,
        hook: basefunctions.ThreadPoolHookObjectInterface = None,
    ) -> None:
        """
        Get symbol prices for the given symbols and date.

        Parameters
        ----------
        symbols : list, optional
            The list of symbols to be used, default: BMW.XETRA
        start_date : str, optional
            The start date of the prices data, the format is "YY-mm-dd",
            default: "1900-01-01"
        end_date : str, optional
            The end date of the prices data, the format is "YY-mm-dd",
            default: "2999-12-31"
        freq : str, optional
            The frequency of the prices data, default: "D"
        params : dict, optional
            Additional parameters to be used, default: None
        hook: basefunctions.ThreadPoolHookObjectInterface, optional
            A hook to be used, default: None

        Returns
        -------
        pandas.DataFrame
            A DataFrame containing the symbol prices for the given symbols and date.
        """
        # load api key from basefunctions secret handler
        api_key = basefunctions.SecretHandler().get_secret_value(
            key="EOD2PD_API_KEY", default_value=None
        )
        if api_key is None:
            raise ValueError("##FAILURE## EOD2PD_API_KEY is not set")
        # check if symbol is None
        if symbols is None:
            symbols = ["BMW.XETRA"]
        # check if symbols is a string
        if isinstance(symbols, str):
            symbols = [symbols]
        # loop over all symbols
        for symbol in symbols:
            # make symbol uppercase
            symbol = symbol.upper()
            # build the url for the request
            url = (
                f"https://eodhistoricaldata.com/api/eod/{symbol}"
                f"?api_token={api_key}"
                f"&from={start_date}"
                f"&to={end_date}"
                f"&period={freq}"
                f"&fmt=json"
            )
            # create message content
            message_content = EOD2PDMessageContent()
            message_content.type = "exchange-symbols-prices"
            message_content.key = symbol
            message_content.url = url
            message_content.params = params

            # put message into input queue
            self.send_message(message_content, hook)

    # -------------------------------------------------------------
    #  get symbol prices from EODHistoricalData
    # -------------------------------------------------------------
    def get_symbols_prices(
        self,
        symbols: List[str] | None,
        start_date: str = "1900-01-01",
        end_date: str = "2999-12-31",
        freq: str = "D",
        dict_result: bool = True,
    ) -> dict:
        """
        Get symbol prices for the given symbols and date.

        Parameters
        ----------
        symbols : list, optional
            The list of symbols to be used, default: "BMW.XETRA"
        start_date : str, optional
            The start date of the prices data, the format is "YY-mm-dd",
            default: "1900-01-01"
        end_date : str, optional
            The end date of the prices data, the format is "YY-mm-dd",
            default: "2999-12-31"
        freq : str, optional
            The frequency of the prices data, default: "D"
        dict_result : bool, optional
            A flag to indicate if the result should be a dictionary, default: True

        Returns
        -------
        pandas.DataFrame | dict
            A DataFrame containing the symbol prices for the given symbols and date or
            a dictionary containing the symbols prices for the given symbols and date.
        """
        # start jobs to get symbols prices
        self.start_jobs_get_symbols_prices(symbols, start_date, end_date, freq)
        # wait until all jobs are done
        basefunctions.get_default_threadpool().get_input_queue().join()
        # get dataframes from output queue
        return eod2pd.utils.get_dataframes_from_output_queue(dict_result=dict_result)

    # -------------------------------------------------------------
    #  start jobs get symbol dividends from EODHistoricalData
    # -------------------------------------------------------------
    def start_jobs_get_symbols_dividends(
        self,
        symbols: List[str] | None,
        start_date: str = "1900-01-01",
        end_date: str = "2999-12-31",
        params: dict = None,
        hook: basefunctions.ThreadPoolHookObjectInterface = None,
    ) -> None:
        """
        Get historical symbol dividends for the given symbols.

        Parameters
        ----------
        symbols : list of str, optional
            The symbols to retrieve dividends for, default: "BMW.XETRA"
        start_date : str, optional
            The start date of the dividends data, default: "1900-01-01"
        end_date : str, optional
            The end date of the dividends, default: "2999-12-31"
        params : dict, optional
            Additional parameters to be used, default: None
        hook: basefunctions.ThreadPoolHookObjectInterface, optional
            A hook to be used, default: None

        Returns
        -------
        pandas.DataFrame
            A DataFrame containing the historical symbol dividends for the
            given symbols.
        """
        # load api key from basefunctions secret handler
        api_key = basefunctions.SecretHandler().get_secret_value(
            key="EOD2PD_API_KEY", default_value=None
        )
        if api_key is None:
            raise ValueError("##FAILURE## EOD2PD_API_KEY is not set")
        # check if symbols is None
        if symbols is None:
            symbols = ["BMW.XETRA"]
        # check if symbols is a string
        if isinstance(symbols, str):
            symbols = [symbols]
        # loop over all symbols
        for symbol in symbols:
            # make symbol uppercase
            symbol = symbol.upper()
            url = (
                f"https://eodhistoricaldata.com/api/div/{symbol}"
                f"?api_token={api_key}"
                f"&from={start_date}"
                f"&to={end_date}"
                f"&fmt=json"
            )
            # create message content
            message_content = EOD2PDMessageContent()
            message_content.type = "exchange-symbols-dividends"
            message_content.key = symbol
            message_content.url = url
            message_content.params = params

            # put message into input queue
            self.send_message(message_content, hook)

    # -------------------------------------------------------------
    #  get symbol dividends from EODHistoricalData
    # -------------------------------------------------------------
    def get_symbols_dividends(
        self,
        symbols: List[str] | None,
        start_date: str = "1900-01-01",
        end_date: str = "2999-12-31",
        dict_result: bool = True,
    ) -> pd.DataFrame | dict:
        """
        Get historical symbol dividends for the given symbols.

        Parameters
        ----------
        symbols : list of str, optional
            The symbols to retrieve dividends for, default: "BMW.XETRA"
        start_date : str, optional
            The start date of the dividends data, default: "1900-01-01"
        end_date : str, optional
            The end date of the dividends, default: "2999-12-31"
        dict_result : bool, optional
            A flag to indicate if the result should be a dictionary, default: True

        Returns
        -------
        pandas.DataFrame | dict
            A DataFrame containing the historical symbol dividends for the given symbols or
            a dictionary containing the historical symbols dividends for the given symbols.
        """
        # start jobs to get symbols dividends
        self.start_jobs_get_symbols_dividends(symbols, start_date, end_date)
        # wait until all jobs are done
        basefunctions.get_default_threadpool().get_input_queue().join()
        # get dataframes from output queue
        return eod2pd.utils.get_dataframes_from_output_queue(dict_result=dict_result)

    # -------------------------------------------------------------
    #  start jobs get symbol splits from EODHistoricalData
    # -------------------------------------------------------------
    def start_jobs_get_symbols_splits(
        self,
        symbols: List[str] | None,
        start_date: str = "1900-01-01",
        end_date: str = "2999-12-31",
        params: dict = None,
        hook: basefunctions.ThreadPoolHookObjectInterface = None,
    ) -> None:
        """
        Get historical symbol splits for the given symbols.

        Parameters
        ----------
        symbols : list of str, optional
            The symbols to retrieve splits for, default: "BMW.XETRA"
        start_date : str, optional
            The start date of the splits data, default: "1900-01-01"
        end_date : str, optional
            The end date of the splits, default: "2999-12-31"
        params : dict, optional
            Additional parameters to be used, default: None
        hook: basefunctions.ThreadPoolHookObjectInterface, optional
            A hook to be used, default: None

        Returns
        -------
        pandas.DataFrame
            A DataFrame containing the historical symbol dividends for the
            given symbols.
        """
        # load api key from basefunctions secret handler
        api_key = basefunctions.SecretHandler().get_secret_value(
            key="EOD2PD_API_KEY", default_value=None
        )
        if api_key is None:
            raise ValueError("##FAILURE## EOD2PD_API_KEY is not set")
        # check if symbol is a list
        if symbols is None:
            symbols = ["BMW.XETRA"]
        # check if symbols is a string
        if isinstance(symbols, str):
            symbols = [symbols]
        for symbol in symbols:
            # make symbol uppercase
            symbol = symbol.upper()
            url = (
                f"https://eodhistoricaldata.com/api/splits/{symbol}"
                f"?api_token={api_key}"
                f"&from={start_date}"
                f"&to={end_date}"
                f"&fmt=json"
            )
            # create message content
            message_content = EOD2PDMessageContent()
            message_content.type = "exchange-symbols-splits"
            message_content.key = symbol
            message_content.url = url
            message_content.params = params

            # put message into input queue
            self.send_message(message_content, hook)

    # -------------------------------------------------------------
    #  get symbol splits from EODHistoricalData
    # -------------------------------------------------------------
    def get_symbols_splits(
        self,
        symbols: List[str] | None,
        start_date: str = "1900-01-01",
        end_date: str = "2999-12-31",
        dict_result: bool = True,
    ) -> pd.DataFrame | dict:
        """
        Get historical symbol splits for the given symbols.

        Parameters
        ----------
        symbols : list of str, optional
            The symbols to retrieve splits for, default: "BMW.XETRA"
        start_date : str, optional
            The start date of the splits data, default: "1900-01-01"
        end_date : str, optional
            The end date of the splits, default: "2999-12-31"
        dict_result : bool, optional
            A flag to indicate if the result should be a dictionary, default: True

        Returns
        -------
        pandas.DataFrame | dict
            A DataFrame containing the historical symbol dividends for the given symbols or
            a dictionary containing the historical symbols dividends for the given symbols.
        """
        # start jobs to get symbols splits
        self.start_jobs_get_symbols_splits(symbols, start_date, end_date)
        # wait until all jobs are done
        basefunctions.get_default_threadpool().get_input_queue().join()
        # get dataframes from output queue
        return eod2pd.utils.get_dataframes_from_output_queue(dict_result=dict_result)

    # =========================================================================
    #
    # helper functions
    #
    # =========================================================================
    def send_message(
        self,
        content: EOD2PDMessageContent,
        hook: basefunctions.ThreadPoolHookObjectInterface = None,
    ) -> None:
        """
        Send a message to the EOD2PD message handler.

        Parameters
        ----------
        content : EOD2PDMessageContent
            The content of the message to be sent.
        hook : basefunctions.ThreadPoolHookObjectInterface, optional
            A callback function to be executed after sending the message.
        """
        timeout = basefunctions.ConfigHandler().get_config_value(
            path="eod2pd/EOD2PD_TIMEOUT", default_value=10
        )
        message = basefunctions.threadpool.create_threadpool_message(
            _type=eod2pd.EOD2PDMESSAGEIDENTIFIER,
            content=content,
            timeout=timeout,
            hook=hook,
        )
        basefunctions.get_default_threadpool().get_input_queue().put(message)
