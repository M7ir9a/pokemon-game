def cooldown(methode):
    def wrapper(self, *args, **kwargs):
        if not hasattr(self, '_cooldown'):
            self._cooldown = 0
        if self._cooldown <= 0:
            result = methode(self, *args, **kwargs)
            self._cooldown = 3  # 3 tours de cooldown
            return result
        else:
            return f"Action en cooldown ({self._cooldown} tours restants)"
    return wrapper