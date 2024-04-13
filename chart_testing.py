import streamlit as st
import streamlit.components.v1 as components

# Define the TradingView widget HTML code
# Replace the placeholder content with your actual TradingView embed code
tradingview_html = """
<!-- TradingView Widget BEGIN -->
<div class="tradingview-widget-container">
  <div id="tradingview_12345"></div>
  <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
  <script type="text/javascript">
  new TradingView.widget(
  {
    "width": 980,
    "height": 610,
    "symbol": "NASDAQ:AAPL",
    "interval": "D",
    "timezone": "Etc/UTC",
    "theme": "light",
    "style": "1",
    "locale": "en",
    "toolbar_bg": "#f1f3f6",
    "enable_publishing": false,
    "allow_symbol_change": true,
    "container_id": "tradingview_12345"
  }
  );
  </script>
</div>
<!-- TradingView Widget END -->
"""

# Use the Streamlit components to render the HTML
components.html(tradingview_html, height=610)


