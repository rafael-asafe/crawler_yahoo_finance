VALID_TABLE_HTML = """
<table>
  <thead>
    <tr>
      <th>Symbol</th>
      <th>Name</th>
      <th>Price (Intraday)</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>AAPL</td><td>Apple Inc.</td><td>150.00</td></tr>
    <tr><td>MSFT</td><td>Microsoft</td><td>1,234.56</td></tr>
  </tbody>
</table>
"""

INVALID_PRICE_HTML = """
<table>
  <thead>
    <tr>
      <th>Symbol</th>
      <th>Name</th>
      <th>Price (Intraday)</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>AAPL</td><td>Apple Inc.</td><td>-5.00</td></tr>
  </tbody>
</table>
"""

MISSING_COLUMNS_HTML = """
<table>
  <thead>
    <tr><th>Symbol</th><th>Name</th></tr>
  </thead>
  <tbody>
    <tr><td>AAPL</td><td>Apple Inc.</td></tr>
  </tbody>
</table>
"""
