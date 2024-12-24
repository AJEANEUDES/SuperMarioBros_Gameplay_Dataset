import os
import tempfile
from pathlib import Path
from typing import Union, Optional
import gdown
import streamlit as st

class DataSource:
    @staticmethod
    def is_google_drive_url(path: str) -> bool:
        """Vérifie si le chemin est une URL Google Drive"""
        return path.startswith('https://drive.google.com/')
    
    @staticmethod
    def extract_file_id(url: str) -> Optional[str]:
        """Extrait l'ID du fichier/dossier depuis l'URL Google Drive"""
        if 'folders/' in url:
            folder_id = url.split('folders/')[1].split('?')[0]
            return folder_id
        return None
    
    @staticmethod
    def download_from_drive(url: str) -> str:
        """Télécharge les données depuis Google Drive"""
        folder_id = DataSource.extract_file_id(url)
        if not folder_id:
            raise ValueError("URL Google Drive invalide")
            
        # Créer un dossier temporaire
        temp_dir = tempfile.mkdtemp()
        st.info("Téléchargement des données depuis Google Drive...")
        
        try:
            # Télécharger le dossier
            gdown.download_folder(
                id=folder_id,
                output=temp_dir,
                quiet=False
            )
            return temp_dir
        except Exception as e:
            raise Exception(f"Erreur lors du téléchargement: {str(e)}")
    
    @staticmethod
    def get_data_path(path: str) -> str:
        """Retourne le chemin approprié selon la source"""
        if DataSource.is_google_drive_url(path):
            return DataSource.download_from_drive(path)
        elif os.path.exists(path):
            return path
        else:
            raise FileNotFoundError(f"Le chemin {path} n'existe pas")