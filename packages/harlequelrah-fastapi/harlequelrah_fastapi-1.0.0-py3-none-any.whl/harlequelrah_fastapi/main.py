import os
import shutil
import sys


def startproject(project_name):
    # Étape 1 : Créer un dossier avec le nom du projet
    project_path = os.path.join(os.getcwd(), project_name)
    os.makedirs(project_path, exist_ok=True)

    # Étape 2 : Créer un sous-dossier avec le nom du projet
    sub_project_path = os.path.join(project_path, project_name)
    os.makedirs(sub_project_path, exist_ok=True)

    # Étape 3 : Créer un dossier settings dans le sous-dossier
    settings_path = os.path.join(sub_project_path, "settings")
    os.makedirs(settings_path, exist_ok=True)

    print(
        f"Le projet {project_name} a été créé avec succès à l'emplacement {project_path}."
    )


def startapp(app_name):
    # Étape 1 : Créer un dossier avec le nom de l'application
    app_path = os.path.join(os.getcwd(), app_name)
    os.makedirs(app_path, exist_ok=True)

    # Étape 2 : Copier le contenu du dossier 'sqlapp' vers le dossier de l'application
    # Assure-toi que 'sqlapp' se trouve dans le même répertoire que le script main.py
    script_dir = os.path.dirname(os.path.realpath(__file__))
    sqlapp_path = os.path.join(script_dir, "sqlapp")

    if os.path.exists(sqlapp_path):
        shutil.copytree(sqlapp_path, app_path, dirs_exist_ok=True)
        print(
            f"L'application {app_name} a été créée avec succès avec le contenu de 'sqlapp'."
        )
    else:
        print(f"Le dossier 'sqlapp' est introuvable à l'emplacement : {sqlapp_path}")


def main():
    if len(sys.argv) < 3:
        print("Usage: harlequelrah_fastapi <commande> <nom>")
        sys.exit(1)

    command = sys.argv[1]
    name = sys.argv[2]

    if command == "startproject":
        startproject(name)
    elif command == "startapp":
        startapp(name)
    else:
        print(f"Commande inconnue: {command}")


if __name__ == "__main__":
    main()
