from abc import ABC, abstractmethod
import random


class Pokemon(ABC):
    def __init__(self, nom, type_pokemon, pv, force):
        self.nom = nom
        self.type = type_pokemon
        self.pv = pv
        self.pv_max = pv
        self.force = force
        self.cooldown_special = 0

    def attaquer(self, cible):
        degats = self.force
        if (self.type == "Feu" and cible.type == "Plante") or \
                (self.type == "Eau" and cible.type == "Feu") or \
                (self.type == "Plante" and cible.type == "Eau"):
            degats = int(degats * 1.5)
        cible.pv -= degats
        return f"{self.nom} attaque {cible.nom} ({degats} dégâts)"

    def soigner(self):
        soin = min(20, self.pv_max - self.pv)
        self.pv += soin
        return f"{self.nom} se soigne (+{soin} PV)"

    def attaque_speciale(self, cible):
        if self.cooldown_special > 0:
            return f"Attaque spéciale en recharge ({self.cooldown_special} tours)"

        degats = self.force * 2
        cible.pv -= degats
        self.cooldown_special = 3
        return f"{self.nom} utilise une attaque spéciale! ({degats} dégâts)"

    def est_vivant(self):
        return self.pv > 0

    def nouveau_tour(self):
        if self.cooldown_special > 0:
            self.cooldown_special -= 1

    def __str__(self):
        return f"{self.nom} ({self.type}) PV: {self.pv}/{self.pv_max}"


class PokemonFeu(Pokemon):
    def attaque_speciale(self, cible):
        if self.cooldown_special > 0:
            return f"Flammèche en recharge ({self.cooldown_special} tours)"

        degats = int(self.force * 2.2)
        cible.pv -= degats
        self.cooldown_special = 3
        return f"{self.nom} lance Flammèche! ({degats} dégâts)"


class PokemonEau(Pokemon):
    def attaque_speciale(self, cible):
        if self.cooldown_special > 0:
            return f"Hydrocanon en recharge ({self.cooldown_special} tours)"

        degats = int(self.force * 2)
        cible.pv -= degats
        self.cooldown_special = 3
        return f"{self.nom} lance Hydrocanon! ({degats} dégâts)"


class PokemonPlante(Pokemon):
    def attaque_speciale(self, cible):
        if self.cooldown_special > 0:
            return f"Fouet Lianes en recharge ({self.cooldown_special} tours)"

        degats = int(self.force * 1.8)
        cible.pv = max(1, cible.pv - degats)
        self.cooldown_special = 3
        return f"{self.nom} lance Fouet Lianes! ({degats} dégâts, PV restants: {cible.pv})"


class PokemonJoueur:
    @staticmethod
    def creer_pokemon(nom, type_pokemon):
        pv = 100
        force = 15
        if type_pokemon == "Feu":
            return PokemonFeu(nom, type_pokemon, pv, force)
        elif type_pokemon == "Eau":
            return PokemonEau(nom, type_pokemon, pv, force)
        elif type_pokemon == "Plante":
            return PokemonPlante(nom, type_pokemon, pv, force)
        raise ValueError("Type invalide")

    @staticmethod
    def generer_pokemon_sauvage():
        types = ["Feu", "Eau", "Plante"]
        noms = ["Salamèche", "Carapuce", "Bulbizarre", "Roucool", "Ratata", "Mystherbe"]
        nom = random.choice(noms)
        type_pokemon = random.choice(types)
        pv = random.randint(80, 120)
        force = random.randint(12, 18)
        return PokemonJoueur.creer_pokemon(nom, type_pokemon)