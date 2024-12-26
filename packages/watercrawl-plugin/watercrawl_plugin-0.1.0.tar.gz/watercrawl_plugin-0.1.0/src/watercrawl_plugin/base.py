from abc import abstractmethod, ABC
from typing import Type

from .utils import validate_json


class AbstractInputValidator(ABC):

    def __init__(self, data, context):
        self.data = data
        self.context = context
        self.errors = {}

    @classmethod
    def get_json_schema(cls) -> dict or None:
        """
        Returns the json schema of the input validator
        """
        return None

    @property
    def plugin(self):
        return self.context.get('plugin')

    @property
    def initial_data(self):
        return self.context.get('initial_data')

    def add_error(self, field, message):
        if field not in self.errors:
            self.errors[field] = []
        self.errors[field].append(message)

    def is_valid(self):
        try:
            self.validate()
        except Exception as e:
            self.add_error('non_field_errors', str(e))
            return False
        return True

    def validate(self):
        self.validate_with_json_schema()

    def validate_with_json_schema(self):
        schema = self.get_json_schema()
        if not schema:
            return
        errors = validate_json(schema, self.data)
        for field, messages in errors.items():
            for message in messages:
                self.add_error(field, message)


class AbstractPlugin(ABC):

    @classmethod
    def from_crawler(cls, spider):
        spider.logger.info("Bootstrapping plugin: %s" % cls.get_name())

    @classmethod
    @abstractmethod
    def get_pipeline_classes(cls) -> dict:
        """Returns the class of a pipeline plugin to be used by the plugin or None

        If a subclass of AbstractPlugin overrides this method, it should return a
        class that is a subclass of AbstractPipelinePlugin. That class will be used
        by the plugin to process the scraped items.

        If this method is not overridden, it will return None, which means that
        the plugin will not use a pipeline plugin to process the scraped items.

        It is follow the scrapy pipeline format, for example:
        example: {
            'watercrawl_plugin.pipeline.BasePipelinePlugin': 543,
        }
        """
        return {}

    @classmethod
    @abstractmethod
    def get_spider_middleware_classes(cls) -> dict:
        """
        Returns the class of a spider middleware plugin to be used by the plugin or None

        If a subclass of AbstractPlugin overrides this method, it should return a
        class that is a subclass of BaseSpiderMiddleware. That class will be used
        by the plugin to process the scraped items.

        If this method is not overridden, it will return None, which means that
        the plugin will not use a spider middleware plugin to process the scraped items.

        It is follow the scrapy pipeline format, for example:
        example: {
            'watercrawl_plugin.middlewares.BaseSpiderMiddleware': 999,
        }
        """
        return {}

    @classmethod
    @abstractmethod
    def get_downloader_middleware_classes(cls) -> dict:
        """
        Returns the class of a downloader middleware plugin to be used by the plugin or None

        If a subclass of AbstractPlugin overrides this method, it should return a
        class that is a subclass of BaseDownloaderMiddleware. That class will be used
        by the plugin to process the scraped items.

        If this method is not overridden, it will return None, which means that
        the plugin will not use a downloader middleware plugin to process the scraped items.

        It is follow the scrapy pipeline format, for example:
        example: {
            'watercrawl_plugin.middlewares.BaseDownloaderMiddleware': 543,
        }
        """
        return {}

    @classmethod
    @abstractmethod
    def get_input_validator(cls) -> Type[AbstractInputValidator]:
        """
        Returns the class of an input validator to be used by the plugin.

        If a subclass of AbstractPlugin overrides this method, it should return a
        class that is a subclass of AbstractInputValidator. That class will be used
        by the plugin to validate input data.

        Returns:
        Type[AbstractInputValidator]: The class of the input validator.
        """
        return AbstractInputValidator

    @classmethod
    @abstractmethod
    def extended_fields(cls):
        # If you want to add additional fields to scrap response, you can override this method
        # and return a list of strings representing the names of the fields you want to add
        # for example ['title', 'description']
        # you have to fill this information in the pipelines
        return []

    @classmethod
    @abstractmethod
    def get_author(cls) -> str:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_version(cls) -> str:
        raise NotImplementedError

    @classmethod
    def get_name(cls) -> str:
        return cls.__name__

    @classmethod
    def get_description(cls) -> str:
        return cls.__doc__

    @classmethod
    @abstractmethod
    def plugin_key(cls) -> str:
        raise NotImplementedError

    @classmethod
    def context(cls):
        return {
            'plugin': cls,
        }

    @classmethod
    def make_input_validator(cls, data):
        input_validator_class = cls.get_input_validator()
        plugin_data = data['plugin_options'].get(cls.plugin_key(), {})
        return input_validator_class(
            data=plugin_data,
            context={
                **cls.context(),
                'initial_data': data
            })


class PluginHelperMixin:
    @classmethod
    def get_plugin_validator(cls, spider, plugin_key):
        return spider.crawl_sevice.crawl_request.options.get('plugin_options', {}).get(plugin_key, {})




class BasePipeline:
    def process_item(self, item, spider):
        return item


class BaseSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.
    # For more information, see https://docs.scrapy.org/en/latest/topics/spider-middleware.html

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class BaseDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    # for more info: https://docs.scrapy.org/en/latest/topics/downloader-middleware.html

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass
