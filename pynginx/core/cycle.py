#!/usr/bin/env python3

# BoBoBo


class NgxCycle(dict):

    @classmethod
    def instance(cls):
        """Returns a global pngx_cycle instance.

        Every process has only one pngx_cycle.
        """
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance

    def init_cycle(self, conf_file):
        """Call all the core modules`s create_conf
        to create conf_ctx.
        """
        return self
