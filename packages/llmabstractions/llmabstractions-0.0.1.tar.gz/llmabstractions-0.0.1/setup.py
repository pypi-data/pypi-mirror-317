from setuptools import setup  # type: ignore


def get_version():
    return [
        ln.split("'")[1]
        for ln in open('llmabstractions/__init__.py')
        if '__version__' in ln
    ][0]


setup(
    version=get_version()
)
