import time

class ViolationManager:
    def __init__(self, cooldown_seconds=3, log_once_per_session=True):
        """
        Manages violation logging to prevent duplicates.
        
        Args:
            cooldown_seconds: Minimum seconds between logs for same person/violation
            log_once_per_session: If True, log each person only once per session
        """
        self.cooldown = cooldown_seconds
        self.log_once_per_session = log_once_per_session
        self.last_logged = {}  # key = (person_id, missing_tuple), value = timestamp
        self.session_logged = set()  # person_ids already logged this session

    def should_log(self, person_id, missing_items):
        """
        Returns True only if violation should be logged.
        
        In session mode: logs each person once per session
        In cooldown mode: logs after cooldown period expires
        """
        if not missing_items:
            return False

        # Session-based: log each person only once
        if self.log_once_per_session:
            if person_id in self.session_logged:
                return False
            self.session_logged.add(person_id)
            return True
        
        # Cooldown-based: log after cooldown expires
        key = (person_id, tuple(sorted(missing_items)))
        now = time.time()

        if key not in self.last_logged:
            self.last_logged[key] = now
            return True

        if now - self.last_logged[key] >= self.cooldown:
            self.last_logged[key] = now
            return True

        return False
    
    def reset_session(self):
        """Reset session-logged persons (for new video/session)."""
        self.session_logged.clear()
        self.last_logged.clear()
