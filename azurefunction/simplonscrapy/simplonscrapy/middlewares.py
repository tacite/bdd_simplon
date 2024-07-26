from scrapy import signals
from itemadapter import is_item, ItemAdapter

class SimplonscrapySpiderMiddleware:
    """
    ## SimplonscrapySpiderMiddleware()

    Middleware for processing responses and exceptions at the spider level.

    This class allows for handling responses and exceptions that occur during
    the processing of responses by the spider, as well as modifying start requests.
    """

    @classmethod
    def from_crawler(cls, crawler):
        """
        ## from_crawler()

        Creates an instance of SimplonscrapySpiderMiddleware from the crawler.

        Connects the `spider_opened` signal to the `spider_opened` method.

        Args:
            crawler (scrapy.crawler.Crawler): The Scrapy crawler object.

        Returns:
            SimplonscrapySpiderMiddleware: An instance of the middleware.
        """
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        """
        ## process_spider_input()

        Processing of each response before it enters the spider.

        This method can be used to modify the response before it is processed by the spider.

        Args:
            response (scrapy.http.Response): The response of the request.
            spider (scrapy.Spider): The spider instance that processes the response.

        Returns:
            None: To continue processing, or raise an exception to interrupt processing.
        """
        return None

    def process_spider_output(self, response, result, spider):
        """
        ## process_spider_output()

        Processing of results returned by the spider.

        This method can be used to modify the items or requests before they are sent
        to the item pipeline.

        Args:
            response (scrapy.http.Response): The response processed by the spider.
            result (iterable): The items or requests returned by the spider.
            spider (scrapy.Spider): The spider instance that returns the results.

        Yields:
            scrapy.Request or dict: The items or requests to send to the item pipeline.
        """
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        """
        ## process_spider_exception()

        Handling of exceptions raised by the spider or the `process_spider_input` method.

        This method can be used to handle exceptions and possibly return requests
        to be retried.

        Args:
            response (scrapy.http.Response): The response when an exception is raised.
            exception (Exception): The raised exception.
            spider (scrapy.Spider): The spider instance that raised the exception.

        Returns:
            None: To continue processing the exception or an iterable of requests or items.
        """
        pass

    def process_start_requests(self, start_requests, spider):
        """
        ## process_start_requests()

        Processing of the spider's start requests.

        This method can be used to modify the start requests before they are
        sent to the downloader middleware.

        Args:
            start_requests (iterable): The spider's start requests.
            spider (scrapy.Spider): The spider instance that starts executing the requests.

        Yields:
            scrapy.Request: The processed start requests.
        """
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        """
        ## spider_opened()

        Handling of the `spider_opened` signal.

        This method is called when the spider is opened and can be used to initialize
        resources or perform configuration tasks.

        Args:
            spider (scrapy.Spider): The spider instance that was opened.
        """
        spider.logger.info('Spider opened: %s' % spider.name)


class SimplonscrapyDownloaderMiddleware:
    """
    ## SimplonscrapyDownloaderMiddleware()

    Middleware for processing requests and responses at the downloader level.

    This class allows for handling requests and responses as they pass through the downloader middleware,
    as well as managing exceptions that occur during the download.
    """

    @classmethod
    def from_crawler(cls, crawler):
        """
        ## from_crawler()

        Creates an instance of SimplonscrapyDownloaderMiddleware from the crawler.

        Connects the `spider_opened` signal to the `spider_opened` method.

        Args:
            crawler (scrapy.crawler.Crawler): The Scrapy crawler object.

        Returns:
            SimplonscrapyDownloaderMiddleware: An instance of the middleware.
        """
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        """
        ## process_request()

        Processing of requests before they are sent to the downloader.

        This method can be used to modify the requests before they are sent to the downloader.

        Args:
            request (scrapy.http.Request): The request to process.
            spider (scrapy.Spider): The spider instance that issued the request.

        Returns:
            None: To continue processing the request, or a Response, Request object, or raise IgnoreRequest.
        """
        return None

    def process_response(self, request, response, spider):
        """
        ## process_response()

        Processing of responses returned by the downloader.

        This method can be used to modify the responses before they are sent to the spider.

        Args:
            request (scrapy.http.Request): The request associated with the response.
            response (scrapy.http.Response): The response to process.
            spider (scrapy.Spider): The spider instance that receives the response.

        Returns:
            scrapy.http.Response or scrapy.http.Request: The processed response or a new request.
        """
        return response

    def process_exception(self, request, exception, spider):
        """
        ## process_exception()

        Handling of exceptions raised during the download or processing of requests.

        This method can be used to handle exceptions and possibly return requests
        to be retried.

        Args:
            request (scrapy.http.Request): The request when an exception is raised.
            exception (Exception): The raised exception.
            spider (scrapy.Spider): The spider instance that raised the exception.

        Returns:
            None: To continue processing the exception or an iterable of requests or responses.
        """
        pass

    def spider_opened(self, spider):
        """
        ## spider_opened()

        Handling of the `spider_opened` signal.

        This method is called when the spider is opened and can be used to initialize
        resources or perform configuration tasks.

        Args:
            spider (scrapy.Spider): The spider instance that was opened.
        """
        spider.logger.info('Spider opened: %s' % spider.name)
