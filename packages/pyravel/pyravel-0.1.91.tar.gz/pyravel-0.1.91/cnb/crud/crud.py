from .create import CoreCreate
from .delete import CoreDelete
from .read import CoreRead
from .update import CoreUpdate


class CoreCRUD(CoreCreate, CoreRead, CoreUpdate, CoreDelete):
    pass
