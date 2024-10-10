import os
import pandas as pd
import chardet

def read_csv_with_encoding(file_path):
    """Essaye de lire un fichier CSV avec plusieurs encodages possibles."""
    encodings_to_try = ['utf-8', 'ISO-8859-1', 'Windows-1252', 'utf-16']
    
    for encoding in encodings_to_try:
        try:
            return pd.read_csv(file_path, encoding=encoding)
        except (UnicodeDecodeError, pd.errors.ParserError) as e:
            print(f"Erreur avec l'encodage {encoding}: {e}")
    
    raise ValueError(f"Impossible de lire le fichier {file_path} avec les encodages tentés.")

def read_file(file_path, input_format):
    """Lit un fichier en fonction de son format."""
    if input_format == 'csv':
        return read_csv_with_encoding(file_path)
    elif input_format == 'json':
        return pd.read_json(file_path)
    elif input_format == 'xlsx':
        return pd.read_excel(file_path)
    else:
        raise ValueError("Format d'entrée non supporté.")

def convert_file(file_path, output_format, output_dir):
    """Convertit un fichier dans le format spécifié et l'enregistre dans le répertoire de sortie."""
    input_format = file_path.split('.')[-1].lower()
    
    # Lire le fichier
    df = read_file(file_path, input_format)

    # Créer le nom du fichier converti
    output_file_name = os.path.basename(file_path).replace(input_format, output_format)
    output_file_path = os.path.join(output_dir, output_file_name)

    # Sauvegarder le fichier dans le format de sortie
    if output_format == 'csv':
        df.to_csv(output_file_path, index=False)
    elif output_format == 'json':
        df.to_json(output_file_path, orient='records', lines=True)
    elif output_format == 'xlsx':
        df.to_excel(output_file_path, index=False)
    
    return output_file_path

def main():
    while True:
        input_dir = input("Entrez le chemin du dossier contenant les fichiers: ").strip()
        
        # Vérification si le répertoire existe
        if os.path.isdir(input_dir):
            break
        else:
            print("Le chemin spécifié n'est pas un répertoire valide (Attention avec les guillemets). Veuillez essayer à nouveau.")

    input_format = input("Entrez le format des fichiers à convertir (csv, json, xlsx): ").strip().lower()

    # Vérification du format d'entrée
    if input_format not in ['csv', 'json', 'xlsx']:
        print("Format non reconnu. Veuillez spécifier 'csv', 'json' ou 'xlsx'.")
        return

    # Récupérer les fichiers du répertoire
    files_to_convert = [f for f in os.listdir(input_dir) if f.endswith(f'.{input_format}')]
    
    # Si aucun fichier à convertir
    if not files_to_convert:
        print(f"Aucun fichier avec le format {input_format} trouvé dans le répertoire spécifié.")
        return

    output_format = input("Dans quel format voulez-vous convertir les fichiers ? (csv, json, xlsx): ").strip().lower()

    # Vérification du format de sortie
    if output_format not in ['csv', 'json', 'xlsx']:
        print("Format non reconnu. Veuillez spécifier 'csv', 'json' ou 'xlsx'.")
        return

    # Créer un répertoire pour les fichiers convertis
    converted_dir = os.path.join(input_dir, "converted_files")
    os.makedirs(converted_dir, exist_ok=True)

    converted_files = []
    for file in files_to_convert:
        file_path = os.path.join(input_dir, file)
        converted_file = convert_file(file_path, output_format, converted_dir)
        converted_files.append(converted_file)
        print(f"Fichier converti: {converted_file}")

    # Demander à l'utilisateur s'il souhaite concaténer les fichiers
    if len(converted_files) > 1:
        concat = input("Voulez-vous concaténer les fichiers convertis ? (oui/non): ").strip().lower()
        
        if concat == 'oui':
            if output_format == 'csv':
                all_data = pd.concat([pd.read_csv(f) for f in converted_files], ignore_index=True)
            elif output_format == 'json':
                all_data = pd.concat([pd.read_json(f, lines=True) for f in converted_files], ignore_index=True)
            elif output_format == 'xlsx':
                all_data = pd.concat([pd.read_excel(f) for f in converted_files], ignore_index=True)
            else:
                print("Format de sortie non supporté pour la concaténation.")
                return
            
            # Enregistrer le fichier concaténé
            concat_file_path = os.path.join(converted_dir, f"concatenated.{output_format}")
            if output_format == 'csv':
                all_data.to_csv(concat_file_path, index=False)
            elif output_format == 'json':
                all_data.to_json(concat_file_path, orient='records', lines=True)
            elif output_format == 'xlsx':
                all_data.to_excel(concat_file_path, index=False)

            print(f"Fichiers concaténés enregistrés dans: {concat_file_path}")

if __name__ == "__main__":
    main()
