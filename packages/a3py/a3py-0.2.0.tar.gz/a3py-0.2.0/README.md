# a3py

Python utils. 

[History.](HISTORY.md)

## Install

```shell script
pip install a3py

```

## Examples

### 1. Simplified example

```python
from datetime import date
from a3py.simplified.datetime import date2str

assert date2str(date(2019, 10, 3)) == '2019-10-03'

```

### 2. Improved example

```python
from a3py.improved.json import fast_dumps

fast_dumps([1, 2, 3])

```

### 3. Readable example

```python
from a3py.improved.readable import get_readable_size

assert get_readable_size(1024 * 1024) == "1.0MB"

```
