"""
This module exposes the core concrete classes of the framework, which are intended to be 
instantiated and used by application developers. 

The core package consists of two types of classes:

1. **Abstract Base Classes (ABCs)**: These define the interfaces that framework implementors should 
    follow when creating subclasses. They provide method contracts that must be implemented by concrete 
    subclasses. These classes are **not intended to be instantiated** directly.

2. **Concrete Classes**: These are the classes that **can be instantiated** and used directly by application 
    developers. They represent fully implemented functionality and are ready for use in applications.

### Convention:
- The **abstract base classes** serve as blueprints for framework developers to implement and extend. 
    They should not be directly instantiated by application developers.
- The **concrete classes** are the ones exposed in this module and listed in `__all__`. These are the 
    classes that application developers will typically interact with, as they provide fully implemented,
    ready-to-use features.

### `__all__` Declaration:
- The `__all__` list includes only the concrete classes, making it clear which classes are meant to be 
    instantiated and used by application developers.
- Abstract base classes are excluded from `__all__` to ensure they are not instantiated directly, 
    which maintains clarity and proper separation of concerns.

### Usage:
- **Framework Implementors**: Should inherit from the abstract base classes and implement the necessary methods.
- **Application Developers**: Should use the concrete classes listed in `__all__` for their applications.

This structure ensures clear separation between the framework's core functionality and the classes that can be
used to build applications on top of the framework.

"""

from .masterpiece import MasterPiece, classproperty
from .composite import Composite
from .application import Application
from .log import Log
from .plugin import Plugin
from .plugmaster import PlugMaster
from .treevisualizer import TreeVisualizer
from .url import URL
from .format import Format
from .jsonformat import JsonFormat
from .masterpiecethread import MasterPieceThread

__all__ = [
    "MasterPiece",
    "Composite",
    "Application",
    "Log",
    "Plugin",
    "PlugMaster",
    "ArgsMaestro",
    "TreeVisualizer",
    "classproperty",
    "URL",
    "Format",
    "JsonFormat",
    "MasterPieceThread"
]
