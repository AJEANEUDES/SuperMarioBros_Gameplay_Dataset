import pandas as pd
import os
from pathlib import Path
import re
from PIL import Image
from typing import Dict, Tuple, List
from tqdm import tqdm
import gdown
import zipfile
class DataLoader:
    def __init__(self, data_path: str):
        self.data_path = Path(data_path)
        if not self.data_path.exists():
            raise FileNotFoundError(f"Le chemin {data_path} n'existe pas")
        
    def parse_folder_name(self, folder_name: str) -> Dict:
        """Parse les informations du nom du dossier"""
        pattern = r"(.+)_(.+)_e(\d+)_(\d+)-(\d+)_(\w+)"
        match = re.match(pattern, folder_name)
        if match:
            return {
                "user": match.group(1),
                "session_id": match.group(2),
                "episode": int(match.group(3)),
                "world": int(match.group(4)),
                "level": int(match.group(5)),
                "outcome": match.group(6)
            }
        return None

    def parse_frame_name(self, frame_name: str) -> Dict:
        """Parse les informations du nom de frame"""
        pattern = r"(.+)_(.+)_e(\d+)_(\d+)-(\d+)_f(\d+)_a(\d+)_(.+)\.(\w+)\.png"
        match = re.match(pattern, frame_name)
        if match:
            return {
                "user": match.group(1),
                "session_id": match.group(2),
                "episode": int(match.group(3)),
                "world": int(match.group(4)),
                "level": int(match.group(5)),
                "frame": int(match.group(6)),
                "action": int(match.group(7)),
                "datetime": match.group(8),
                "outcome": match.group(9)
            }
        return None

    def extract_png_metadata(self, image_path: str) -> Dict:
        """Extrait les métadonnées des chunks PNG personnalisés"""
        try:
            with Image.open(image_path) as img:
                metadata = img.info
                return {
                    "ram_data": metadata.get("RAM", b""),
                    "player_input": int(metadata.get("BP1", 0)),
                    "outcome_code": int(metadata.get("OUTCOME", 0))
                }
        except Exception as e:
            print(f"Erreur lors de l'extraction des métadonnées de {image_path}: {e}")
            return {"ram_data": b"", "player_input": 0, "outcome_code": 0}

    def count_total_files(self) -> int:
        """Compte le nombre total de fichiers PNG à traiter"""
        return sum(1 for _ in self.data_path.glob("**/*.png"))

    def load_data(self) -> Dict[str, pd.DataFrame]:
        """Charge et organise les données du dataset"""
        episodes_data = []
        frames_data = []
        
        # Compte le nombre total de fichiers
        total_files = self.count_total_files()
        print(f"\nNombre total de fichiers PNG trouvés: {total_files}")
        
        # Initialise la barre de progression principale
        with tqdm(total=total_files, desc="Chargement des données", unit="fichiers") as pbar:
            # Parcours des dossiers d'épisodes
            for folder in self.data_path.iterdir():
                if folder.is_dir():
                    folder_info = self.parse_folder_name(folder.name)
                    if folder_info:
                        episodes_data.append(folder_info)
                        
                        # Parcours des frames dans le dossier
                        for frame_file in folder.glob("*.png"):
                            frame_info = self.parse_frame_name(frame_file.name)
                            if frame_info:
                                try:
                                    metadata = self.extract_png_metadata(str(frame_file))
                                    frame_data = {**frame_info, **metadata}
                                    frames_data.append(frame_data)
                                except Exception as e:
                                    print(f"\nErreur lors du traitement de {frame_file}: {e}")
                                    continue
                            pbar.update(1)

        # Création des DataFrames
        print("\nCréation des DataFrames...")
        df_episodes = pd.DataFrame(episodes_data) if episodes_data else pd.DataFrame()
        df_frames = pd.DataFrame(frames_data) if frames_data else pd.DataFrame()
        
        # Affichage des statistiques de chargement
        print(f"\nEpisodes chargés: {len(df_episodes)}")
        print(f"Frames chargées: {len(df_frames)}")
        
        if df_episodes.empty:
            print("Attention: Aucun épisode n'a été chargé!")
        if df_frames.empty:
            print("Attention: Aucune frame n'a été chargée!")
            
        return {
            "episodes": df_episodes,
            "frames": df_frames
        }

    def get_file_info(self) -> List[Dict]:
        
        def __init__(self, data_path):
         self.data_path = data_path


    def load_data(self):
        # Vérifiez si c'est une URL Google Drive
        if self.data_path.startswith("https://drive.google.com"):
            # Téléchargez le fichier dans un dossier temporaire
            file_id = self.data_path.split('/')[-2]  # Extrait l'ID du fichier
            output = "data-smb.zip"
            gdown.download(f"https://drive.google.com/uc?id={file_id}", output, quiet=False)
            # Décompressez le fichier ZIP si nécessaire
            os.makedirs("temp_data", exist_ok=True)
            with zipfile.ZipFile(output, 'r') as zip_ref:
                zip_ref.extractall("temp_data")
            return "temp_data"
        else:
            # Charger les données locales
            return self.data_path
        """Retourne les informations sur les fichiers disponibles"""
        return [
            {
                "name": file.name,
                "size": file.stat().st_size,
                "modified": file.stat().st_mtime
            }
            for file in self.data_path.glob("**/*.png")
        ]