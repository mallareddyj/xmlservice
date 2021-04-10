from dataextractor import CsvDataExtractor


def factory(ending="csv"):
    extractors = {"csv": CsvDataExtractor}
    return extractors[ending]()
