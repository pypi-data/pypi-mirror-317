
## cprintf

## Install

`pip install cprintf`

## Usage

```python
import cprintf

cprintf.debug("Debug info")
cprintf.ok("Everything looks good.")
cprintf.info("This is some info.")
cprintf.warn("This is a warning.")
cprintf.err("This is an error message.")
cprintf.fatal("This is a fatal error.")
cprintf.line()
cprintf.custom("This is a custom color message in cyan!", "\033[96m")
cprintf.line(char='=', length=60, color='OK')

