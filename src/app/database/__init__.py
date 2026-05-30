from .tickets_db import (
    init_db, save_ticket, get_ticket, delete_ticket,
    update_ticket_status, get_stats, get_all_tickets
)
from .afk_db import (
    init_afk_db, set_afk, remove_afk, get_afk_user, get_all_afk,
    check_cooldown, set_cooldown, get_user_stats,
    update_stats_on_set, update_stats_on_remove
)