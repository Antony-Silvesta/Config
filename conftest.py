def pytest_addoption(parser):
    parser.addoption(
        "--db", action="store", default="sampleupload", help="Database to use"
    )


