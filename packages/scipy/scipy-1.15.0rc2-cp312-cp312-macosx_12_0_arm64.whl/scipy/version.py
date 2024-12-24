
"""
Module to expose more detailed version info for the installed `scipy`
"""
version = "1.15.0rc2"
full_version = version
short_version = version.split('.dev')[0]
git_revision = "a3d40a89355b14bdc8c2c99b6545a68802cc94b3"
release = 'dev' not in version and '+' not in version

if not release:
    version = full_version
