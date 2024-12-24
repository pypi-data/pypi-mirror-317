from typing import Dict


class FuzzyProvider:
    def __init__(self, category):
        self.category = category

    def provide(self, aql, additions) -> Dict:
        raise NotImplementedError()


class FuzzyProviderManager:
    def __init__(self):
        self._providers = dict()

    def register(self, provider: FuzzyProvider):
        self._providers[provider.category] = provider

    def get(self, category):
        return self._providers.get(category)
