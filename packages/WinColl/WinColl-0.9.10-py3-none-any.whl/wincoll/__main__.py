import re
import sys

from wincoll import main

sys.argv[0] = re.sub(r"__main__.py$", "wincoll", sys.argv[0])
main()
