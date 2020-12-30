from pyservice import __version__
from mamba import description, it


with description("Version") as self:
    with it("verifies the package version"):
        assert __version__ == "0.1.0"
