import re
import os

# Chemin vers ton fichier .md
md_path = r"C:\Users\houes\Documents\GitHub\rai2en.github.io\content\posts\Project-I\PROJET.md"

# Lire le contenu du fichier .md
with open(md_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fonction de remplacement
def replacer(match):
    alt_text = match.group(1)  # Ex: img/ans 01.png
    corrected_path = alt_text.replace(" ", "_")  # Remplace les espaces
    return f"![]({corrected_path})"

# Cherche les balises de la forme ![img/ans 01.png] ou ![img/nom avec espace.png]
pattern = r"!\[([^\]]+\.(?:png|jpg|jpeg|gif|webp|svg))\]"
new_content = re.sub(pattern, replacer, content)

# Sauvegarde du fichier modifié
with open(md_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("[✓] Fichier .md mis à jour.")

# 🖼️ Renommage physique des fichiers d'images
# Récupère le dossier des images
img_dir = os.path.join(os.path.dirname(md_path), "img")

if os.path.isdir(img_dir):
    for filename in os.listdir(img_dir):
        if any(filename.lower().endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"]):
            if " " in filename:
                new_name = filename.replace(" ", "_")
                old_path = os.path.join(img_dir, filename)
                new_path = os.path.join(img_dir, new_name)
                os.rename(old_path, new_path)
                print(f"[→] {filename} → {new_name}")
else:
    print("[!] Dossier 'img' introuvable.")
