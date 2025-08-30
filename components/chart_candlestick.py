import json
import numpy as np
import yfinance as yf

from streamlit_lightweight_charts import renderLightweightCharts
from st_screen_stats import ScreenData

COLOR_BULL = 'rgba(38,166,154,0.9)' #26a69a
COLOR_BEAR = 'rgba(239,83,80,0.9)'  #ef5350

# function to load candlestick chart
def load_candlestick(symbol):
    # get initial screen size
    screenD = ScreenData(setTimeout=1000)
    screen_stats = screenD.st_screen_data()

    width = screen_stats['innerWidth'] * 0.88 - screen_stats['innerWidth'] * 0.2
    height = screen_stats['innerHeight'] * 0.8

    # Request historic pricing data via finance.yahoo.com API
    df = yf.Ticker(symbol).history(period='4mo')[['Open', 'High', 'Low', 'Close', 'Volume']]

    # Some data wrangling to match required format
    df = df.reset_index()
    df.columns = ['time','open','high','low','close','volume']                  # rename columns
    df['time'] = df['time'].dt.strftime('%Y-%m-%d')                             # Date to string
    df['color'] = np.where(df['open'] > df['close'], COLOR_BEAR, COLOR_BULL)    # bull or bear

    # export to JSON format
    candles = json.loads(df.to_json(orient = "records"))
    volume = json.loads(df.rename(columns={"volume": "value",}).to_json(orient = "records"))

    chartMultipaneOptions = [
        {
            "width": width,
            "height": height * 0.6,
            "layout": {
                "background": {
                    "type": "solid",
                    "color": 'white'
                },
                "textColor": "black"
            },
            "grid": {
                "vertLines": {
                    "color": "rgba(197, 203, 206, 0.5)"
                    },
                "horzLines": {
                    "color": "rgba(197, 203, 206, 0.5)"
                }
            },
            "crosshair": {
                "mode": 0
            },
            "priceScale": {
                "borderColor": "rgba(197, 203, 206, 0.8)"
            },
            "timeScale": {
                "borderColor": "rgba(197, 203, 206, 0.8)",
                "barSpacing": 15
            }
        },
            {
            "width": width,
            "height": height * 0.15,
            "layout": {
                "background": {
                    "type": 'solid',
                    "color": 'transparent'
                },
                "textColor": 'black',
            },
            "grid": {
                "vertLines": {
                    "color": 'rgba(42, 46, 57, 0)',
                },
                "horzLines": {
                    "color": 'rgba(42, 46, 57, 0.6)',
                }
            },
            "timeScale": {
                "visible": False,
            }
        },
        {
            "width": width,
            "height": height * 0.15,
            "layout": {
                "background": {
                    "type": 'solid',
                    "color": 'transparent'
                },
                "textColor": 'black',
            },
            "grid": {
                "vertLines": {
                    "color": 'rgba(42, 46, 57, 0)',
                },
                "horzLines": {
                    "color": 'rgba(42, 46, 57, 0.6)',
                }
            },
            "timeScale": {
                "visible": False,
            }
        }
    ]

    seriesCandlestickChart = [
        {
            "type": 'Candlestick',
            "data": candles,
            "options": {
                "upColor": COLOR_BULL,
                "downColor": COLOR_BEAR,
                "borderVisible": False,
                "wickUpColor": COLOR_BULL,
                "wickDownColor": COLOR_BEAR
            }
        }
    ]

    seriesVolumeChart = [
        {
            "type": 'Histogram',
            "data": volume,
            "options": {
                "priceFormat": {
                    "type": 'volume',
                },
                "priceScaleId": "" # set as an overlay setting,
            },
            "priceScale": {
                "scaleMargins": {
                    "top": 0,
                    "bottom": 0,
                },
                "alignLabels": True
            }
        }
    ]

    candlestick_chart = renderLightweightCharts([
        {
            "chart": chartMultipaneOptions[0],
            "series": seriesCandlestickChart
        },
        {
            "chart": chartMultipaneOptions[1],
            "series": seriesVolumeChart
        }
    ], 'multipane')

    # Handle screen size changes
    def onScreenSizeChange(candlestick_chart):
        return candlestick_chart

    screenD.st_screen_data(key="screen_stats_", on_change=onScreenSizeChange(candlestick_chart)) 
