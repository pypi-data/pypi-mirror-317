from caasm_post.manage import EnforcementManager, enforcement_registry


def get_enforcement_manager(date=None):
    enforcement_manager = EnforcementManager(date)
    for name, handler in enforcement_registry.get_enforcements():
        enforcement_manager.register_handler(handler)

    return enforcement_manager
