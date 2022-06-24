import logging

from dataclasses import dataclass, field
from typing import Type

from media_manager.application.api.context import Context

from .abc import (
    ComponentStorage,
    Module,
    PrimitiveModule,
    DeferrableModule,
    SociableModule,
    ViewableModule
)
from .components import (
    Component,
    CDeferredChannel
)
from .features import (
    Feature,
    FDeferred,
    FMessages,
    FMetaInformation,
    FWidget, FWindow,
    SUPPORTED_FEATURES,
)

BASES_BY_FEATURE: list[tuple[frozenset[Feature], Type[Module]]] = [
    (frozenset((FMetaInformation, )), PrimitiveModule),
    (frozenset((FDeferred, )), DeferrableModule),
    (frozenset((FMessages, )), SociableModule),
    (frozenset((FWidget, FWindow)), ViewableModule)
]

COMPONENTS_BY_FEATURE: dict[Feature, Type[Component]] = {
    FDeferred: CDeferredChannel
}


@dataclass(slots=True, eq=True, unsafe_hash=True)
class FTComponent:
    feature: Feature
    component: Type[Component] = field(compare=False, hash=False)
    context: Context = field(compare=False, hash=False)


class ModuleBuilder:
    def __init__(self, bases: tuple[Type[Module], ...], components: frozenset[FTComponent]):
        self.__bases = bases
        self.__components = components

    def build(self, *, context: Context) -> PrimitiveModule:
        # CREATING A NEW ASSEMBLED SUBCLASS
        AssembledModule: Type[PrimitiveModule] = type("AssembledModule", self.__bases, {})  # type: ignore
        if not issubclass(AssembledModule, PrimitiveModule):
            logging.error("%s: Assembled class must be subclass of %s",
                          type(self).__name__, PrimitiveModule.__name__)
            raise RuntimeError(f"Assembled class must be subclass of {PrimitiveModule.__name__}")

        # INITIALIZING ALL COMPONENTS
        features: set[Feature] = set()
        components: dict[Feature, Component] = {}
        for ftc in self.__components:
            if intersected := set.intersection(features, ftc.feature.all_provides(), {ftc.feature}):
                logging.error("%s: Attempting to use same features for different components: %s",
                              type(self).__name__, intersected)
                raise RuntimeError(f"Some features already have components: {intersected}")

            component = ftc.component(context.union(ftc.context))
            for feature in ftc.feature.all_provides(including=True):
                # We must have different ways to get component by feature
                # Example:
                #     FDefaultWidget implements FWidget, so we must have an ability to use FWidget for access
                #     But also, some others components or application may have special actions for default widget
                #     So we must have an ability to use FDefaultWidget too and, moreover, we need that FDefaultWidget
                #     and FWidget point to ONE component
                components[feature] = component

        # LINKING ALL COMPONENTS
        module: PrimitiveModule = AssembledModule(ComponentStorage(components))
        for component in components.values():
            component.link(module)

        # RETURNING AT LEAST PrimitiveModule INSTANCE
        return module


class ModuleFactory:
    def __init__(self):
        # Provided by user
        self.__installed: dict[Feature, FTComponent] = {}
        self.__overrided: dict[Feature, FTComponent] = {}
        # All
        self.__features: set[Feature] = set()

    def assemble(self) -> ModuleBuilder:
        # All modules must provide their information
        if FMetaInformation not in self.__features:
            logging.error("%s: %s is required for creating a module but not provided",
                          type(self).__name__, FMetaInformation)
            raise RuntimeError(f"{FMetaInformation} is not provided")

        # Module must be at least PrimitiveModule to be used by application
        #   That is checked by code above
        bases: set[Type[Module]] = {PrimitiveModule}
        for group, base in BASES_BY_FEATURE:
            if group.issubset(self.__features):
                bases.add(base)

        # All modules are subclasses of BasicModule, so we don't want to have one more basic module class in mro
        return ModuleBuilder(tuple(bases), frozenset((self.__installed | self.__overrided).values()))

    def install_component(self,
                          feature: Feature,
                          component: Type[Component],
                          *,
                          context: Context | None = None,
                          critical: bool = True) -> "ModuleFactory":
        if feature not in SUPPORTED_FEATURES:
            logging.warning("%s: %s is not supported", type(self).__name__, feature)
            if critical:
                raise RuntimeError(f"Critical {feature} is not supported")
            return self

        if feature in self.__overrided:
            logging.warning("%s: Attempting to install component with same feature %s",
                            type(self).__name__, feature)
            if critical:
                raise RuntimeError(f"Unable to install critical component. {feature} was overrided")
            return self

        if feature in self.__installed:
            logging.warning("%s: Attempting to install component with same feature %s",
                            type(self).__name__, feature)
            if critical:
                raise RuntimeError(f"Unable to install critical component. {feature} was overrided")
            return self

        if requirements := feature.requirements(*self.__features):
            for requirement in requirements:
                logging.error("%s: Feature %s requirement %s is not satisfied",
                              type(self).__name__, feature.name, requirement.name)
            raise RuntimeError(f"Some requirements of {feature} are not satisfied: {requirements}")

        self.__installed[feature] = FTComponent(feature, component, context or Context())
        self.__features.add(feature)
        self.__features.update(feature.all_provides())
        return self

    def override_component(self,
                           feature: Feature,
                           component: Type[Component],
                           *,
                           context: Context | None = None) -> "ModuleFactory":
        if feature in SUPPORTED_FEATURES:
            logging.warning("%s: System component with %s was overrided",
                            type(self).__name__, feature)

        if requirements := feature.requirements(*self.__features):
            for requirement in requirements:
                logging.error("%s: Feature %s requirement %s is not satisfied",
                              type(self).__name__, feature.name, requirement.name)
            raise RuntimeError(f"Some requirements of {feature} are not satisfied: {requirements}")

        self.__overrided[feature] = FTComponent(feature, component, context or Context())
        self.__features.add(feature)
        self.__features.update(feature.all_provides())
        return self

    def request_feature(self, feature: Feature, *, critical: bool = False) -> "ModuleFactory":
        if feature not in SUPPORTED_FEATURES:
            if critical:
                logging.error("%s: Critical feature %s is not supported",
                              type(self).__name__, feature)
                raise RuntimeError(f"Cannot create module without {feature}")
            return self

        if requirements := feature.requirements(*self.__features):
            for requirement in requirements:
                logging.error("%s: Feature %s requirement %s is not satisfied",
                              type(self).__name__, feature.name, requirement.name)
            raise RuntimeError(f"Some requirements of {feature} are not satisfied: {requirements}")

        # TODO: Track unsupported features (for debugging or dynamic modules)
        if feature not in COMPONENTS_BY_FEATURE:
            if critical:
                logging.error("%s: Critical feature %s has no component",
                              type(self).__name__, feature)
                raise RuntimeError(f"Cannot create module without {feature}")
            return self
        self.install_component(feature, COMPONENTS_BY_FEATURE[feature])
        return self
