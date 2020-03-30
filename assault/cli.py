from typing import TextIO
import click
import json
import sys

from .http import assault
from .stats import Results


@click.command()
@click.option("--requests", "-r", default=500, help="number of requests")
@click.option("--concurrency", "-c", default=1, help="number of concurrent requests")
@click.option("--json-file", "-j", default=None, help="Path to JSON file")
@click.argument("url")
def clik(requests, concurrency, json_file, url):
    print(f"Requests: {requests}")
    print(f"Concurrency: {concurrency}")
    print(f"Json file name: {json_file}")
    print(f"URL : {url}")
    output_file = None
    if json_file:
        output_file = open(json_file, "w")
    else:
        print("unable to open file")
        sys.exit(1)

    total_time, request_dicts = assault(url, requests, concurrency)
    results = Results(total_time, request_dicts)
    display(results, output_file)


def display(results: Results, json_file: TextIO):
    if json_file:
        print("We are writing to a JSON file")
        json.dump(
            {
                "successful_requests": results.successful_requests(),
                "slowest": results.slowest(),
                "fastest": results.fastest(),
                "total_time": results.total_time,
                "requests per minute": results.requests_per_minute(),
                "requests per second": results.requests_per_second(),
            },
            json_file,
        )
        json_file.close()
        print("file copy done")
    else:
        print("......Done")
        print("----Results ----")
        print(f"successful requets  \t{results.successful_requests()}")
        print(f"slowest requets     \t{results.slowest()}s")
        print(f"fastest requets     \t{results.fastest()}s")
        print(f"Total time          \t{results.total_time}")
        print(f"requets per minute  \t{results.requests_per_minute()}")
        print(f"requets per second  \t{results.requests_per_second()}")


if __name__ == "__main__":
    clik()
