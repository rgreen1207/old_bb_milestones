# from alembic import context
# from app.models.base_class import Base
# from app.configs.database_configs import db_config

from app.models.clients import (
    ClientModelDB, # noqa: F401
    ClientAwardModelDB, # noqa: F401
    ClientBudgetModelDB, # noqa: F401
    ClientUserModelDB, # noqa: F401
)
from app.models.messages import MessageModelDB # noqa: F401
from app.models.programs import (
    ProgramModelDB, # noqa: F401
    AdminModelDB, # noqa: F401
    ProgramAwardModelDB, # noqa: F401
    ProgramEventModelDB, # noqa: F401
    ProgramRuleModelDB, # noqa: F401
)
from app.models.segments import (
    SegmentModelDB, # noqa: F401
    SegmentAwardModelDB, # noqa: F401
    SegmentDesignModelDB, # noqa: F401
    SegmentRuleModelDB, # noqa: F401
)
from app.models.users import (
    UserModelDB, # noqa: F401
    UserServiceModelDB # noqa: F401
)
from app.models.base_class import Base # noqa: F401

# # this is the Alembic Config object, which provides
# # access to the values within the .ini file in use.
# config = context.config

# config.set_main_option("sqlalchemy.url",db_config.DATABASE_URL)

# target_metadata = Base.metadata  #find and replace target_metadata with Base.metadata
