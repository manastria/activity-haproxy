# Fichier : correcteur_typo.py
import re
import sys
import uuid
# argparse est plus robuste pour gérer les arguments de ligne de commande
import argparse

# --- Constantes typographiques ---
NBSP = '\u00A0'          # Espace insécable
NNBSP = '\u202F'         # Espace fine insécable
TYPO_APOSTROPHE = '\u2019'  # Apostrophe typographique

def correcteur_typographique_md(contenu_md):
    """
    Applique des corrections typographiques à une chaîne Markdown en protégeant les blocs de code.
    """
    protections = {}

    # --- PASSE 1 : PROTECTION ---

    def proteger_bloc(match):
        # Génère un identifiant unique pour le bloc de code
        key = f"__PROTECTED_BLOCK_{uuid.uuid4().hex}__"
        protections[key] = match.group(0)
        return key

    # Protéger le frontmatter YAML au tout début du fichier
    # On utilise re.DOTALL pour que '.' puisse correspondre aux sauts de ligne
    contenu_md = re.sub(r"^\s*---\s*\n(.*?)\n---\s*\n", proteger_bloc, contenu_md, count=1, flags=re.DOTALL)

    # Protéger les blocs de code clôturés (```...```)
    contenu_md = re.sub(r"^\s*(```.*?```)", proteger_bloc, contenu_md, flags=re.MULTILINE | re.DOTALL)
    
    # Protéger le code en ligne (`...`)
    contenu_md = re.sub(r"`(.+?)`", proteger_bloc, contenu_md)

    # Protéger les URLs pour éviter la modification du ':' dans http:// etc. # <--- AJOUT
    contenu_md = re.sub(r"[a-zA-Z][a-zA-Z0-9+.-]*://\S*", proteger_bloc, contenu_md)

    # Protéger les lignes de délimitation de tableau Markdown # <--- AJOUT
    # Cible les lignes comme "| :--- | ---: | :-: |"
    contenu_md = re.sub(r"^\s*\|[: \t|-]+\|\s*$", proteger_bloc, contenu_md, flags=re.MULTILINE)

    # Protéger les lignes de callouts ':::' (ou '::: note', '::: info {..}', etc.)
    # Empêche les règles de ponctuation d'ajouter des espaces avant les ':' et de casser les fences.
    contenu_md = re.sub(r'^[ \t]*:::[^\n]*$', proteger_bloc, contenu_md, flags=re.MULTILINE)

    # --- PASSE 2 : CORRECTION TYPOGRAPHIQUE ---

    texte_a_corriger = contenu_md
    
    # Règle 1 : Espace avant les ponctuations doubles (:;?! et guillemets)
    texte_a_corriger = re.sub(r'[ \t\u00A0]*([:;?!»])', NBSP + r'\1', texte_a_corriger)
    
    # Règle 2 : Espace après le guillemet ouvrant
    texte_a_corriger = re.sub(r'([«])[ \t\u00A0]*', r'\1' + NNBSP, texte_a_corriger)
    
    # Règle 3 : Guillemets droits (") -> français (« »)
    texte_a_corriger = re.sub(r'"(.*?)"', r'«' + NNBSP + r'\1' + NNBSP + r'»', texte_a_corriger)

    # Règle 4 : Guillemets typographiques anglais (“ ”) -> français (« »)
    texte_a_corriger = re.sub(r'“(.+?)”', r'«' + NNBSP + r'\1' + NNBSP + r'»', texte_a_corriger)

    # Règle 5 : Apostrophe droite (') -> typographique (’)
    texte_a_corriger = re.sub(r"'", TYPO_APOSTROPHE, texte_a_corriger)
    
    # Règle 6 : Supprimer le gras des titres Markdown # <--- NOUVEL AJOUT
    # Cible les lignes comme "# **Titre**" et les transforme en "# Titre"
    # L'option MULTILINE est cruciale pour que `^` corresponde au début de chaque ligne.
    texte_a_corriger = re.sub(r'^(#+[ \t]*)\*\*(.*?)\*\*', r'\1\2', texte_a_corriger, flags=re.MULTILINE)
    
    texte_corrige = texte_a_corriger

    # --- PASSE 3 : RESTITUTION ---
    
    # On restitue les blocs protégés en bouclant tant qu'il reste des clés à remplacer
    while True:
        texte_avant_remplacement = texte_corrige
        for key, value in protections.items():
            texte_corrige = texte_corrige.replace(key, value)
        # Si plus aucune clé n'est remplacée, on sort de la boucle
        if texte_avant_remplacement == texte_corrige:
            break
            
    return texte_corrige

# --- AMÉLIORATION DE L'EXÉCUTION ---
# On modifie la partie principale pour la rendre plus pratique

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Applique des corrections typographiques à des fichiers Markdown.",
        epilog="Par défaut, le script modifie les fichiers directement. Utilisez --stdout pour imprimer le résultat."
    )
    parser.add_argument(
        'fichiers', 
        nargs='*', 
        help="Chemin vers un ou plusieurs fichiers Markdown à corriger."
    )
    parser.add_argument(
        '--stdout', 
        action='store_true', 
        help="Affiche le résultat dans la sortie standard au lieu de modifier le fichier."
    )

    args = parser.parse_args()

    if not args.fichiers:
        print("Erreur : Vous devez spécifier au moins un fichier à traiter.")
        parser.print_help()
        sys.exit(1)

    for fichier_path in args.fichiers:
        try:
            with open(fichier_path, 'r', encoding='utf-8') as f:
                contenu = f.read()
            
            contenu_corrige = correcteur_typographique_md(contenu)
            
            if args.stdout:
                print(contenu_corrige)
            else:
                with open(fichier_path, 'w', encoding='utf-8') as f:
                    f.write(contenu_corrige)
                print(f"s Correction appliquée à : {fichier_path}")

        except FileNotFoundError:
            print(f"Erreur : Le fichier '{fichier_path}' n'a pas été trouvé.")
        except Exception as e:
            print(f"Une erreur est survenue lors du traitement de {fichier_path} : {e}")
