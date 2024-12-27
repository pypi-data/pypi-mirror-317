from typing import Optional

from ..config.config import ElroyConfig
from ..config.constants import USER_ALIAS_STRING
from ..db.db_manager import DbManager
from ..tools.user_preferences import get_or_create_user_preference


def get_persona(db: DbManager, config: ElroyConfig, user_id: Optional[int]):
    if not user_id:
        user_noun = "my user"
        raw_persona = config.default_persona
    else:
        user_preference = get_or_create_user_preference(db, user_id)
        if user_preference.system_persona:
            raw_persona = user_preference.system_persona
        else:
            raw_persona = config.default_persona

        if user_preference.preferred_name:
            user_noun = user_preference.preferred_name
        else:
            user_noun = "my user"
    return raw_persona.replace(USER_ALIAS_STRING, user_noun)
