from typing import List, Dict
from statistics import mean


class ReportingDict:
    def __init__(self, d):
        self._d = d

    def __getitem__(self, key):
        try:
            return self._d[key]
        except KeyError:
            raise KeyError(f"{key!r} is missing from {self._d!r}")


class Results:
    """
    Results handles calculating statistics based on a list of requests that were made.
    Here"s an example of what the information will look like:

    Successful requests     3000
    Slowest                 0.010s
    Fastest                 0.001s
    Average                 0.003s
    Total time              2.400s
    Requests Per Minute     90000
    Requests Per Second     125
    """

    def __init__(self, total_time: float, requests: List[Dict]):
        self.requests = sorted(
            requests, key=lambda r: ReportingDict(r)["request_time"], reverse=True
        )
        self.total_time = total_time

    def slowest(self) -> float:
        """
        return the slowest requests completion time
        >>> results = Results( 10.6, [{
        ...    "status_code": 200,
        ...    "request_time": 3.4
        ... }, {
        ...    "status_code": 500,
        ...    "request_time": 6.1
        ... }, {
        ...    "status_code": 200,
        ...    "request_time": 1.04
        ... }])
        >>> results.slowest()
        6.1
        """
        return self.requests[-1]["request_time"]

    def fastest(self) -> float:
        """
        return the fastest requests completion time
        >>> results = Results( 10.6, [{
        ...    "status_code": 200,
        ...    "request_time": 3.4
        ... }, {
        ...    "status_code": 500,
        ...    "request_time": 6.1
        ... }, {
        ...    "status_code": 200,
        ...    "request_time": 1.04
        ... }])
        >>> results.fastest()
        1.04
        """
        return self.requests[0]["request_time"]

    def average_time(self) -> float:
        """
        return the average requests completion time
        >>> results = Results( 10.6, [{
        ...    "status_code": 200,
        ...    "request_time": 3.4
        ... }, {
        ...    "status_code": 500,
        ...    "request_time": 6.1
        ... }, {
        ...    "status_code": 200,
        ...    "request_time": 1.04
        ... }])
        >>> results.average_time()
        3.513333333333333
        """
        return mean([r["request_time"] for r in self.requests])

    def successful_requests(self) -> int:
        """
        return the successful requests completion time
        >>> results = Results( 10.6, [{
        ...    "status_code": 200,
        ...    "request_time": 3.4
        ... }, {
        ...    "status_code": 500,
        ...    "request_time": 6.1
        ... }, {
        ...    "status_code": 200,
        ...    "request_time": 1.04
        ... }])
        >>> results.successful_requests()
        2
        """
        print(self.requests)
        return len(
            [req for req in self.requests if req["status_code"] in range(200, 299)]
        )

    def requests_per_minute(self) -> int:
        """
        return the successful requests completion time
        >>> results = Results( 10.6, [{
        ...    "status_code": 200,
        ...    "request_time": 3.4
        ... }, {
        ...    "status_code": 500,
        ...    "request_time": 6.1
        ... }, {
        ...    "status_code": 200,
        ...    "request_time": 1.04
        ... }])
        >>> results.requests_per_minute()
        17
        """
        return round(60 * len(self.requests) / self.total_time)

    def requests_per_second(self) -> int:
        """
        return the successful requests completion time
        >>> results = Results( 3.5, [{
        ...    "status_code": 200,
        ...    "request_time": 3.4
        ... }, {
        ...    "status_code": 500,
        ...    "request_time": 2.9
        ... }, {
        ...    "status_code": 200,
        ...    "request_time": 1.04
        ... }, {
        ...    "status_code": 200,
        ...    "request_time": 0.4
        ... }])
        >>> results.requests_per_second()
        1
        """
        return round(len(self.requests) / self.total_time)
