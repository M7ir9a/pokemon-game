import pygame
import sys
from pygame.locals import *


class InterfaceGraphique:
    def __init__(self):
        pygame.init()
        self.largeur, self.hauteur = 1024, 768
        self.ecran = pygame.display.set_mode((self.largeur, self.hauteur))
        pygame.display.set_caption("Pokémon Combat")

        # Couleurs
        self.couleurs = {
            'blanc': (255, 255, 255),
            'noir': (0, 0, 0),
            'fond': (240, 240, 240),
            'bouton': (70, 130, 180),
            'texte_btn': (255, 255, 255),
            'rouge': (255, 99, 71),
            'vert': (60, 179, 113),
            'bleu': (100, 149, 237),
            'gris': (200, 200, 200),
            'jaune': (255, 255, 0),
            'type_feu': (238, 129, 48),
            'type_eau': (99, 144, 240),
            'type_plante': (122, 199, 76)
        }

        # Polices
        self.police_grande = pygame.font.SysFont('Arial', 32, bold=True)
        self.police_moyenne = pygame.font.SysFont('Arial', 24)
        self.police_petite = pygame.font.SysFont('Arial', 18)

    def afficher_texte(self, texte, x, y, police, couleur, centrer_x=False, centrer_y=False):
        surface = police.render(texte, True, couleur)
        rect = surface.get_rect()
        if centrer_x:
            x -= rect.width // 2
        if centrer_y:
            y -= rect.height // 2
        self.ecran.blit(surface, (x, y))
        return rect

    def creer_bouton(self, texte, x, y, largeur=300, hauteur=50, couleur=None, centrer_x=False):
        couleur = couleur or self.couleurs['bouton']
        if centrer_x:
            x -= largeur // 2
        rect = pygame.Rect(x, y, largeur, hauteur)
        pygame.draw.rect(self.ecran, couleur, rect, border_radius=10)
        pygame.draw.rect(self.ecran, self.couleurs['noir'], rect, 2, border_radius=10)
        self.afficher_texte(texte, x + largeur // 2, y + hauteur // 2,
                            self.police_moyenne, self.couleurs['texte_btn'], True, True)
        return rect

    def afficher_combat(self, joueur, adversaire, tour_joueur=True, mode_jcj=False):
        self.ecran.fill(self.couleurs['fond'])

        # Dimensions et positions
        largeur_pokemon = 300
        espace_horizontal = (self.largeur - 2 * largeur_pokemon) // 3

        if mode_jcj:
            # Mode Joueur vs Joueur - Les deux Pokémon en haut
            y_joueur = 150
            y_adversaire = 150
            titre_joueur = joueur.nom
            titre_adversaire = adversaire.nom
        else:
            # Mode Joueur vs Sauvage - Positions verticales différentes
            y_joueur = 400  # Votre Pokémon en bas
            y_adversaire = 150  # Adversaire en haut
            titre_joueur = joueur.nom  # Affiche directement le nom
            titre_adversaire = adversaire.nom

        # Positionnement horizontal centré
        x_joueur = espace_horizontal
        x_adversaire = 2 * espace_horizontal + largeur_pokemon

        # Affichage des Pokémon
        self.afficher_pokemon(joueur, x_joueur, y_joueur, titre_joueur)
        self.afficher_pokemon(adversaire, x_adversaire, y_adversaire, titre_adversaire)

        # Affichage du tour actuel
        if mode_jcj:
            titre_tour = f"Tour de {joueur.nom}" if tour_joueur else f"Tour de {adversaire.nom}"
        else:
            titre_tour = "Votre tour" if tour_joueur else "Tour de l'adversaire"

        self.afficher_texte(titre_tour, self.largeur // 2, 50,
                            self.police_grande, self.couleurs['noir'], True)

        # Zone d'actions
        if tour_joueur:
            # Cadre actions
            cadre_width = 700
            cadre_x = (self.largeur - cadre_width) // 2
            pygame.draw.rect(self.ecran, self.couleurs['blanc'], (cadre_x, 550, cadre_width, 150), border_radius=15)
            pygame.draw.rect(self.ecran, self.couleurs['noir'], (cadre_x, 550, cadre_width, 150), 2, border_radius=15)

            # Boutons d'action
            btn_width = 200
            espacement = 50
            start_x = cadre_x + (cadre_width - (2 * btn_width + espacement)) // 2

            btn_attaque = self.creer_bouton("Attaque Normale", start_x, 570, btn_width)
            btn_speciale = self.creer_bouton("Attaque Spéciale", start_x + btn_width + espacement, 570, btn_width)
            btn_soin = self.creer_bouton("Soin", (self.largeur - 300) // 2, 630, 300, 40, centrer_x=True)

            pygame.display.flip()

            # Gestion des événements
            while True:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        self.fermer()
                    if event.type == MOUSEBUTTONDOWN:
                        if btn_attaque.collidepoint(event.pos):
                            return "attaque"
                        elif btn_speciale.collidepoint(event.pos):
                            return "speciale"
                        elif btn_soin.collidepoint(event.pos):
                            return "soin"
        else:
            # Tour de l'adversaire
            if mode_jcj:
                message = f"{adversaire.nom} prépare son attaque..."
            else:
                message = "L'adversaire réfléchit..."

            self.afficher_texte(message, self.largeur // 2, 600,
                                self.police_moyenne, self.couleurs['noir'], True)
            pygame.display.flip()
            pygame.time.delay(1500)
            return "attaque"

    def afficher_pokemon(self, pokemon, x, y, titre):
        # Cadre
        largeur_cadre = 300
        pygame.draw.rect(self.ecran, self.couleurs['blanc'], (x, y, largeur_cadre, 200), border_radius=15)
        pygame.draw.rect(self.ecran, self.couleurs['noir'], (x, y, largeur_cadre, 200), 2, border_radius=15)

        # Titre
        self.afficher_texte(titre, x + largeur_cadre // 2, y + 20,
                            self.police_moyenne, self.couleurs['noir'], True)

        # Nom
        self.afficher_texte(pokemon.nom, x + largeur_cadre // 2, y + 50,
                            self.police_grande, self.couleurs['noir'], True)

        # Barre de PV
        barre_width = 250
        pv_width = int(barre_width * (pokemon.pv / pokemon.pv_max))
        barre_x = x + (largeur_cadre - barre_width) // 2
        pygame.draw.rect(self.ecran, self.couleurs['gris'], (barre_x, y + 90, barre_width, 20))
        pygame.draw.rect(self.ecran, self.couleurs['vert'], (barre_x, y + 90, pv_width, 20))

        # Texte PV
        self.afficher_texte(f"{pokemon.pv}/{pokemon.pv_max}",
                            x + largeur_cadre // 2, y + 90,
                            self.police_petite, self.couleurs['noir'], True, True)

        # Type
        type_color = {
            'Feu': self.couleurs['type_feu'],
            'Eau': self.couleurs['type_eau'],
            'Plante': self.couleurs['type_plante']
        }.get(pokemon.type, self.couleurs['noir'])

        type_width = 100
        type_x = x + (largeur_cadre - type_width) // 2
        pygame.draw.rect(self.ecran, type_color, (type_x, y + 130, type_width, 30), border_radius=15)
        self.afficher_texte(pokemon.type,
                            x + largeur_cadre // 2, y + 145,
                            self.police_petite, self.couleurs['blanc'], True, True)

    def afficher_actions_combat(self):
        # Cadre actions
        cadre_width = 700
        cadre_x = (self.largeur - cadre_width) // 2
        pygame.draw.rect(self.ecran, self.couleurs['blanc'], (cadre_x, 550, cadre_width, 150), border_radius=15)
        pygame.draw.rect(self.ecran, self.couleurs['noir'], (cadre_x, 550, cadre_width, 150), 2, border_radius=15)

        # Boutons
        btn_width = 200
        espacement = 50
        start_x = cadre_x + (cadre_width - (2 * btn_width + espacement)) // 2

        btn_attaque = self.creer_bouton("Attaque Normale", start_x, 570, btn_width)
        btn_speciale = self.creer_bouton("Attaque Spéciale", start_x + btn_width + espacement, 570, btn_width)
        btn_soin = self.creer_bouton("Soin", (self.largeur - 300) // 2, 630, 300, 40, centrer_x=True)

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.fermer()
                if event.type == MOUSEBUTTONDOWN:
                    if btn_attaque.collidepoint(event.pos):
                        return "attaque"
                    elif btn_speciale.collidepoint(event.pos):
                        return "speciale"
                    elif btn_soin.collidepoint(event.pos):
                        return "soin"

    def menu_principal(self):
        while True:
            self.ecran.fill(self.couleurs['fond'])

            # Titre
            self.afficher_texte("POKÉMON COMBAT",
                                self.largeur // 2, 100,
                                self.police_grande, self.couleurs['noir'], True)

            # Boutons
            btn_width = 300
            btn_x = (self.largeur - btn_width) // 2
            espacement = 70
            start_y = 200

            btn_combat = self.creer_bouton("COMBAT vs SAUVAGE", btn_x, start_y, btn_width)
            btn_joueur = self.creer_bouton("JOUEUR vs JOUEUR", btn_x, start_y + espacement, btn_width)
            btn_stats = self.creer_bouton("STATISTIQUES", btn_x, start_y + 2 * espacement, btn_width)
            btn_quitter = self.creer_bouton("QUITTER", btn_x, start_y + 3 * espacement, btn_width,
                                            couleur=self.couleurs['rouge'])

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.fermer()
                if event.type == MOUSEBUTTONDOWN:
                    if btn_combat.collidepoint(event.pos):
                        return 1
                    elif btn_joueur.collidepoint(event.pos):
                        return 2
                    elif btn_stats.collidepoint(event.pos):
                        return 3
                    elif btn_quitter.collidepoint(event.pos):
                        return 4

    def boite_dialogue(self, titre, message):
        # Cadre
        cadre_width, cadre_height = 600, 300
        cadre_x = (self.largeur - cadre_width) // 2
        cadre_y = (self.hauteur - cadre_height) // 2

        fond = pygame.Surface((cadre_width, cadre_height))
        fond.fill(self.couleurs['fond'])
        self.ecran.blit(fond, (cadre_x, cadre_y))

        pygame.draw.rect(self.ecran, self.couleurs['noir'],
                         (cadre_x, cadre_y, cadre_width, cadre_height), 2)

        # Titre
        self.afficher_texte(titre,
                            self.largeur // 2, cadre_y + 30,
                            self.police_grande, self.couleurs['noir'], True)

        # Message
        lignes = message.split('\n')
        for i, ligne in enumerate(lignes):
            self.afficher_texte(ligne,
                                self.largeur // 2, cadre_y + 90 + i * 30,
                                self.police_moyenne, self.couleurs['noir'], True)

        # Bouton OK
        btn_ok = self.creer_bouton("OK",
                                   (self.largeur - 100) // 2, cadre_y + cadre_height - 70,
                                   100, 40, centrer_x=True)
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.fermer()
                if event.type == MOUSEBUTTONDOWN and btn_ok.collidepoint(event.pos):
                    return

    def saisie_texte(self, prompt, x, y):
        input_rect = pygame.Rect(x, y, 300, 40)
        texte = ''
        actif = True

        while actif:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.fermer()
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        actif = False
                    elif event.key == K_BACKSPACE:
                        texte = texte[:-1]
                    else:
                        texte += event.unicode

            self.ecran.fill(self.couleurs['fond'])
            self.afficher_texte(prompt, x, y - 40, self.police_moyenne, self.couleurs['noir'])
            pygame.draw.rect(self.ecran, self.couleurs['blanc'], input_rect, 2)
            self.afficher_texte(texte, x + 10, y + 10, self.police_moyenne, self.couleurs['noir'])
            pygame.display.flip()

        return texte

    @staticmethod
    def fermer():
        pygame.quit()
        sys.exit()