import pygame
from pygame.locals import *
from classes import PokemonJoueur
from interface import InterfaceGraphique
import os
import sys


def charger_stats():
    """Charge les statistiques depuis le fichier"""
    stats = {"victoires": 0, "defaites": 0, "niveau": 1}
    if os.path.exists("statistiques.txt"):
        with open("statistiques.txt", "r") as f:
            for ligne in f:
                if ":" in ligne:
                    cle, valeur = ligne.strip().split(": ")
                    stats[cle] = int(valeur)
    return stats


def sauvegarder_stats(stats):
    """Sauvegarde les statistiques dans le fichier"""
    with open("statistiques.txt", "w") as f:
        for cle, valeur in stats.items():
            f.write(f"{cle}: {valeur}\n")


def creer_pokemon_joueur(interface, joueur_num=None):
    """Crée un Pokémon pour le joueur avec interface graphique"""
    titre = "Créez votre Pokémon" if joueur_num is None else f"Création Joueur {joueur_num}"
    interface.boite_dialogue(titre, "Choisissez un nom et un type")

    # Saisie du nom
    nom = ""
    while not nom.strip():
        interface.ecran.fill(interface.couleurs['fond'])
        prompt = "Nom de votre Pokémon:" if joueur_num is None else f"Joueur {joueur_num} - Nom:"
        interface.afficher_texte(prompt,
                                 interface.largeur // 2, 200,
                                 interface.police_moyenne,
                                 interface.couleurs['noir'], True)
        pygame.display.flip()

        nom = ""
        saisie_active = True
        while saisie_active:
            for event in pygame.event.get():
                if event.type == QUIT:
                    interface.fermer()
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        saisie_active = False
                    elif event.key == K_BACKSPACE:
                        nom = nom[:-1]
                    else:
                        nom += event.unicode

            interface.ecran.fill(interface.couleurs['fond'])
            interface.afficher_texte(prompt,
                                     interface.largeur // 2, 200,
                                     interface.police_moyenne,
                                     interface.couleurs['noir'], True)

            pygame.draw.rect(interface.ecran, interface.couleurs['blanc'],
                             (interface.largeur // 2 - 150, 250, 300, 40))
            pygame.draw.rect(interface.ecran, interface.couleurs['noir'],
                             (interface.largeur // 2 - 150, 250, 300, 40), 2)
            interface.afficher_texte(nom, interface.largeur // 2 - 140, 260,
                                     interface.police_moyenne,
                                     interface.couleurs['noir'])

            pygame.display.flip()

    # Sélection du type
    type_pokemon = None
    while type_pokemon not in ["Feu", "Eau", "Plante"]:
        interface.ecran.fill(interface.couleurs['fond'])
        interface.afficher_texte("Choisissez le type:",
                                 interface.largeur // 2, 200,
                                 interface.police_moyenne,
                                 interface.couleurs['noir'], True)

        btn_feu = interface.creer_bouton("FEU", interface.largeur // 2 - 250, 300,
                                         100, 50, interface.couleurs['type_feu'])
        btn_eau = interface.creer_bouton("EAU", interface.largeur // 2 - 50, 300,
                                         100, 50, interface.couleurs['type_eau'])
        btn_plante = interface.creer_bouton("PLANTE", interface.largeur // 2 + 150, 300,
                                            100, 50, interface.couleurs['type_plante'])

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                interface.fermer()
            if event.type == MOUSEBUTTONDOWN:
                if btn_feu.collidepoint(event.pos):
                    type_pokemon = "Feu"
                elif btn_eau.collidepoint(event.pos):
                    type_pokemon = "Eau"
                elif btn_plante.collidepoint(event.pos):
                    type_pokemon = "Plante"

    return PokemonJoueur.creer_pokemon(nom, type_pokemon)


def combat_joueur_vs_sauvage(interface):
    """Gère un combat contre un Pokémon sauvage"""
    stats = charger_stats()
    joueur = creer_pokemon_joueur(interface)
    adversaire = PokemonJoueur.generer_pokemon_sauvage()

    interface.boite_dialogue("Combat", f"Un {adversaire.nom} sauvage apparaît!\nType: {adversaire.type}")

    while joueur.est_vivant() and adversaire.est_vivant():
        # Tour du joueur
        action = interface.afficher_combat(joueur, adversaire, True)

        if action == "attaque":
            message = joueur.attaquer(adversaire)
        elif action == "speciale":
            message = joueur.attaque_speciale(adversaire)
        elif action == "soin":
            message = joueur.soigner()

        interface.boite_dialogue("Résultat", message)

        if not adversaire.est_vivant():
            break

        # Tour de l'adversaire (IA)
        interface.afficher_combat(joueur, adversaire, False)
        message = adversaire.attaquer(joueur)
        interface.boite_dialogue("Action ennemie", message)

        # Réinitialisation des cooldowns
        joueur.nouveau_tour()
        adversaire.nouveau_tour()

    # Résultat du combat
    if joueur.est_vivant():
        stats["victoires"] += 1
        stats["niveau"] += 1
        interface.boite_dialogue("Victoire!",
                                 f"Vous avez vaincu {adversaire.nom}!\nNiveau: {stats['niveau']}")
    else:
        stats["defaites"] += 1
        interface.boite_dialogue("Défaite",
                                 f"{joueur.nom} est K.O.!")

    sauvegarder_stats(stats)


def combat_joueur_vs_joueur(interface):
    """Gère un combat entre deux joueurs"""
    # Création des Pokémon
    joueur1 = creer_pokemon_joueur(interface, 1)
    joueur2 = creer_pokemon_joueur(interface, 2)

    interface.boite_dialogue("Combat", f"Que le combat commence!\n{joueur1.nom} vs {joueur2.nom}")

    tour_joueur1 = True
    while joueur1.est_vivant() and joueur2.est_vivant():
        if tour_joueur1:
            # Tour du Joueur 1
            interface.boite_dialogue("Tour", f"{joueur1.nom}, c'est votre tour!")
            action = interface.afficher_combat(joueur1, joueur2, True, mode_jcj=True)

            if action == "attaque":
                message = joueur1.attaquer(joueur2)
            elif action == "speciale":
                message = joueur1.attaque_speciale(joueur2)
            elif action == "soin":
                message = joueur1.soigner()
        else:
            # Tour du Joueur 2
            interface.boite_dialogue("Tour", f"{joueur2.nom}, c'est votre tour!")
            action = interface.afficher_combat(joueur2, joueur1, True, mode_jcj=True)

            if action == "attaque":
                message = joueur2.attaquer(joueur1)
            elif action == "speciale":
                message = joueur2.attaque_speciale(joueur1)
            elif action == "soin":
                message = joueur2.soigner()

        interface.boite_dialogue("Résultat", message)

        if not (joueur1.est_vivant() and joueur2.est_vivant()):
            break

        # Réinitialisation des cooldowns
        joueur1.nouveau_tour()
        joueur2.nouveau_tour()
        tour_joueur1 = not tour_joueur1

    # Résultat du combat
    if joueur1.est_vivant():
        interface.boite_dialogue("Victoire!", f"{joueur1.nom} a gagné le combat!")
    else:
        interface.boite_dialogue("Victoire!", f"{joueur2.nom} a gagné le combat!")


def afficher_statistiques(interface):
    """Affiche les statistiques du joueur"""
    stats = charger_stats()
    interface.boite_dialogue("Statistiques",
                             f"Victoires: {stats['victoires']}\nDéfaites: {stats['defaites']}\nNiveau: {stats['niveau']}")


def main():
    """Fonction principale du jeu"""
    try:
        interface = InterfaceGraphique()

        while True:
            choix = interface.menu_principal()

            if choix == 1:  # Combat vs sauvage
                combat_joueur_vs_sauvage(interface)
            elif choix == 2:  # Joueur vs Joueur
                combat_joueur_vs_joueur(interface)
            elif choix == 3:  # Stats
                afficher_statistiques(interface)
            elif choix == 4:  # Quitter
                interface.fermer()

    except Exception as e:
        print(f"Erreur: {e}")
        if 'interface' in locals():
            interface.fermer()
        else:
            pygame.quit()
            sys.exit()


if __name__ == "__main__":
    main()