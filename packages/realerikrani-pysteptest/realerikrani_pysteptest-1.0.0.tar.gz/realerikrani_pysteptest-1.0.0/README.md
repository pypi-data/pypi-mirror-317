# pysteptest

After installing via pip, use the `@pytest.mark.pysteptest` marker on a class
for example for system tests
that need to happen in a specific order one after another.
When one test fails, then do not run the following ones.

```py
@pytest.mark.pysteptest
class TestTodos:
    def test_it_creates_todo(self):
        # ...

    def test_it_reads_todo(self):
        # ...

    def test_it_deletes_todo(self):
        # ...
```

This incremental marker is created by changing the code of <https://github.com/pytest-dev/pytest/blob/24e84f08f43216f95620135305cbebe9f646e433/doc/en/example/simple.rst#incremental-testing---test-steps>.
See pytest repo's MIT license, LICENSE_OF_PYTEST file, included in the repository of this pysteptest project.
