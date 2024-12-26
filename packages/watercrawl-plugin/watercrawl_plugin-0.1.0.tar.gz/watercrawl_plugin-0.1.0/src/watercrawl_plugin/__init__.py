from .base import AbstractPlugin, AbstractInputValidator, BaseSpiderMiddleware, BaseDownloaderMiddleware, BasePipeline
from .utils import get_settings

version = '0.0.2'

__all__ = [
    'AbstractInputValidator',
    'AbstractPlugin',
    'get_settings',
    'BasePipeline',
    'BaseSpiderMiddleware',
    'BaseDownloaderMiddleware'
]

__version__ = version

__title__ = "watercrawl_plugin"
__description__ = "Base plugin for WaterCrawl"
__url__ = "https://github.com/watercrawl/watercrawl-plugin"
