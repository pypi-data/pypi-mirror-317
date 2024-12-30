import logging
import warnings
from typing import Literal, Optional

import os
from selenium import webdriver
from selenium.webdriver.common.options import ArgOptions

__all__ = [
    "get_webdriver",
    "DriverType",
]

logger = logging.getLogger(__name__)

DriverType = Literal["chrome", "edge", "firefox", "ie", "android", "ios"]

OPTIONS_CLASS_MAP = {
    "chrome": (webdriver.ChromeOptions, webdriver.ChromeService, webdriver.Chrome),
    "edge": (webdriver.EdgeOptions, webdriver.EdgeService, webdriver.Edge),
    "firefox": (webdriver.FirefoxOptions, webdriver.FirefoxService, webdriver.Firefox),
    "ie": (webdriver.IeOptions, webdriver.IeService, webdriver.Ie),
    # "android": UiAutomator2Options,
    # "ios": XCUITestOptions,
}


def get_options(
    driver_type: DriverType,
    options: Optional[ArgOptions] = None,
    capabilities: Optional[dict] = None,
) -> ArgOptions:
    """
    根据参数生成options，因为desired_capabilities将被启用
    :param driver_type:
    :param options:
    :param capabilities:
    :return:
    """
    capabilities = capabilities or {}

    class_list = OPTIONS_CLASS_MAP.get(driver_type, None)
    if class_list is None:
        raise ValueError("未知的浏览器类型")

    if options is None:
        options = class_list[0]()

    if isinstance(options, webdriver.ChromeOptions):
        options.add_experimental_option(
            "excludeSwitches",
            ["enable-logging"],
        )

    elif isinstance(options, webdriver.IeOptions):
        options.ignore_zoom_level = True

    return options


def get_webdriver(
    driver_type: DriverType = "chrome",
    *,
    hub="",
    version=None,
    options: Optional[ArgOptions] = None,
    service_args: Optional[dict] = None,
    capabilities: Optional[dict] = None,
) -> webdriver.Remote:
    """
    自动就绪selenium，目前只支持Chrome 和 FireFox
    1. 下载浏览器驱动
    2. 实例化Service
    3. 实例化WebDriver
    :param driver_type: 浏览器类型
    :param hub: selenium grid hub地址
    :param version: 浏览器版本
    :param options: 浏览器选项
    :param service_args: service 实例化的参数
    :param capabilities: grid 的启动参数
    :return:
    """

    mirror =  os.environ.get('SE_DRIVER_MIRROR_URL')
    #if not mirror:
    #    warnings.warn("未配置Selenium加速地址, 本次启动没有加速.  ", UserWarning)

    logger.debug(f"启动新的设备: {locals()}")
    if driver_type not in OPTIONS_CLASS_MAP:
        raise ValueError(
            f"未知的浏览器类型: {driver_type} not in {list(OPTIONS_CLASS_MAP.keys())}"
        )


    options_class, service_class, driver_class = OPTIONS_CLASS_MAP.get(
        driver_type, None
    )
    service_args = service_args or {}
    options = get_options(driver_type, options, capabilities)
    service = service_class(**service_args)
    driver = driver_class(service=service, options=options)

    return driver




debugger = upload_by_drop = print
