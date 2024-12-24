# Mock The Python

### What is it?

A library that makes mocking in Python better by building on type of Python's built in `mock` library.

### How?

Currently, just by allowing members of modules which are being patched to be patched by using references to the actual members, instead of bare strings.

Here's an example:

```Python
from mock_the_python.mock_path import at
from unittest.mock import patch

import another_module.module_under_test
from another_module.module_under_test import bacon

patch(at(another_module.module_under_test).member(bacon), return_value="mmmm, bacon")
```

Now you can freely rename `bacon` to `sausage` without worrying about whether or not your refactoring tools will find string references, and your tests will still pass.  Groovy.

More features will be added to this library