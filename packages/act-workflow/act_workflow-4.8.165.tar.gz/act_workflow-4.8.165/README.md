# act-workflow

A library for executing workflow nodes based on Actfile configuration.

## Installation

```bash
pip install act-workflow



The error message indicates that you're trying to upload a file that already exists on TestPyPI. This is happening because you've already uploaded version 4.7.1 of your package. Let's fix this and upload the new version:

1. Clean up your dist directory:
   ```
   rm -rf dist/*
   ```

2. Update your package version in `setup.py`. Find the line with `version=get_version()` and update it to a new version, for example:
   ```python
   version='4.7.3',  # or use get_version() if it returns a new version
   ```

3. Rebuild your distribution:
   ```
   python setup.py sdist bdist_wheel
   ```

4. Now, try uploading again:
   ```
   twine upload -r testpypi --config-file /Users/taj/.pypirc dist/* --verbose
   ```

5. If you're still having issues, try uploading only the new version:
   ```
   twine upload -r testpypi --config-file /Users/taj/.pypirc dist/act_workflow-4.7.3* --verbose
   ```
   (Replace 4.7.3 with whatever new version number you've chosen)

6. If you're getting authentication errors, double-check your `.pypirc` file:
   ```
   cat /Users/taj/.pypirc
   ```
   Ensure it looks like this (with your actual token):
   ```ini
   [testpypi]
   repository = https://test.pypi.org/legacy/
   username = __token__
   password = pypi-YOUR_TESTPYPI_TOKEN_HERE
   ```

7. If you're still having issues, try setting the credentials via environment variables:
   ```
   export TWINE_USERNAME=__token__
   export TWINE_PASSWORD=your_testpypi_token_here
   twine upload --repository testpypi dist/* --verbose
   ```

8. Make sure you have the latest versions of setuptools, wheel, and twine:
   ```
   pip install --upgrade setuptools wheel twine
   ```

Remember, you can't upload the same version twice to PyPI or TestPyPI. Always increment your version number when you make changes and want to upload a new version.

If you're still encountering issues after trying these steps, please provide the new error message or output, and I'll be happy to help further.clear