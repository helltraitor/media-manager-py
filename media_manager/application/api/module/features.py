import logging

from dataclasses import dataclass, field


@dataclass(slots=True, eq=True, unsafe_hash=True)
class Feature:
    name: str
    component: str | None = field(default=None, kw_only=True)
    provides: frozenset["Feature"] = field(default=frozenset(), kw_only=True)
    requires: frozenset["Feature"] = field(default=frozenset(), kw_only=True)

    def __post_init__(self):
        intersected = set.intersection(self.all_requires(), self.all_provides())
        if intersected:
            logging.error("%s: Attempting to create %s with intersected required and provided features: %s",
                          type(self).__name__, self, intersected)
            raise RuntimeError(f"Invalid {self} has intersected required and provided features: {intersected}")

    def all_provides(self, *, including: bool = False) -> set["Feature"]:
        provides: set["Feature"] = {self} if including else set()
        features: set["Feature"] = set(self.provides)
        while features:
            feature = features.pop()
            if feature.provides:
                features.update(feature.provides)
            provides.add(feature)
        return provides

    def all_requires(self, *, including: bool = False) -> set["Feature"]:
        requires: set["Feature"] = {self} if including else set()
        features: set["Feature"] = set(self.requires)
        while features:
            feature = features.pop()
            if feature.requires:
                features.update(feature.requires)
            requires.add(feature)
        return requires

    def requirements(self, *features: "Feature") -> set["Feature"]:
        provides: set["Feature"] = set()
        for feature in features:
            provides.update(feature.all_provides())
        return self.all_requires() - provides


FDeferred = Feature("Deferred", component="DeferredPoolChannel")
FMessages = Feature("Messages", component="MessageClient")

FMetaInformation = Feature("MetaInformation", component="MetaInformation")

FWidget = Feature("Widget", component="Widget")
FDefaultWidget = Feature("DefaultWidget", component="Widget", provides=frozenset((FWidget, )))

FWindow = Feature("Window", component="Window", requires=frozenset((FWidget, )))

SUPPORTED_FEATURES = frozenset((
    FDefaultWidget,
    FDeferred,
    FMessages,
    FMetaInformation,
    FWidget,
    FWindow
))
