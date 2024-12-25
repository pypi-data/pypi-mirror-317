import logging
import time
import traceback
from typing import Dict

from caasm_config.config import caasm_config
from caasm_post.handlers.base import EnforcementBaseHandler
from caasm_post.model import HandlerRequest

log = logging.getLogger()


class EnforcementRegistry:
    def __init__(self):
        self._enforcements = {}

    def register_enforcement(self, handler: type(EnforcementBaseHandler)):
        self._enforcements[handler.get_name()] = handler

    def get_enforcements(self):
        return self._enforcements


enforcement_registry = EnforcementRegistry()


class EnforcementManager(object):
    def __init__(self, date):
        self._handler_mapper = {}
        self._date = date

    def register_handler(self, handler_class):
        self._handler_mapper[handler_class.get_name()] = handler_class

    def execute(self, category, param_mapper: Dict = None):
        if not param_mapper:
            param_mapper = caasm_config.ENFORCEMENT

        if not param_mapper:
            log.warning("Enforcement not found any param info")
            return

        params = param_mapper.get(category)
        if not params:
            log.warning(f"Enforcement {category} not found any param info")
            return
        for param in params:
            try:
                self.execute_common(category, param)
            except Exception as e:
                log.warning(f"Enforcement params({param}) handle error({e})")

    def execute_common(self, category, param):
        handler_request = HandlerRequest(**param)
        handler_instance = self._get_handler(category, handler_request)
        if not handler_instance:
            log.warning(f"Not found enforcement {handler_request.name} handler")
            return
        handler_display_name = handler_instance.get_display_name()
        _start_time = time.time()
        log.debug(f"handler {handler_display_name} start executing.........")
        try:
            handler_instance.execute()
        except Exception as e:
            log.warning(f"handler {handler_display_name} execute failed. title is {e}. {traceback.format_exc()}")
        else:
            _cost_time = time.time() - _start_time
            log.debug(f"handler {handler_display_name} finish executing.......... cost ({_cost_time})s")

    def _get_handler(self, category, handler_request):
        handler_name = handler_request.name

        handler_class = self._handler_mapper.get(handler_name)
        if not handler_class:
            return None
        handler_instance = handler_class(category, self._date)
        handler_instance.initialize(handler_request.params)

        return handler_instance
