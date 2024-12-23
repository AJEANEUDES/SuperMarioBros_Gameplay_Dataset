import pandas as pd
import numpy as np
from typing import Dict

class DataPreprocessor:
    def __init__(self, dataframes: Dict[str, pd.DataFrame]):
        self.dataframes = dataframes

    def process_button_inputs(self, action: int) -> Dict[str, bool]:
        """Convertit le code d'action en boutons individuels"""
        return {
            'A': bool(action & 128),
            'up': bool(action & 64),
            'left': bool(action & 32),
            'B': bool(action & 16),
            'start': bool(action & 8),
            'right': bool(action & 4),
            'down': bool(action & 2),
            'select': bool(action & 1)
        }

    def clean_data(self) -> Dict[str, pd.DataFrame]:
        """Nettoie et prépare les données"""
        cleaned_dfs = {}
        
        if 'frames' in self.dataframes:
            df_frames = self.dataframes['frames'].copy()
            
            # Vérification de l'existence de la colonne 'action'
            if 'action' in df_frames.columns:
                # Conversion des actions en colonnes de boutons
                button_data = df_frames['action'].apply(self.process_button_inputs)
                button_df = pd.DataFrame(button_data.tolist())
                df_frames = pd.concat([df_frames, button_df], axis=1)
            
            # Conversion des outcomes en format numérique
            if 'outcome' in df_frames.columns:
                df_frames['outcome_numeric'] = df_frames['outcome'].map({'fail': 0, 'win': 1})
            
            cleaned_dfs['frames'] = df_frames

        if 'episodes' in self.dataframes:
            df_episodes = self.dataframes['episodes'].copy()
            if 'outcome' in df_episodes.columns:
                df_episodes['outcome_numeric'] = df_episodes['outcome'].map({'fail': 0, 'win': 1})
            cleaned_dfs['episodes'] = df_episodes
            
        return cleaned_dfs

    def calculate_episode_stats(self) -> pd.DataFrame:
        """Calcule les statistiques par épisode"""
        if 'frames' not in self.dataframes:
            return pd.DataFrame()
            
        df_frames = self.dataframes['frames']
        
        # Vérification des colonnes nécessaires
        required_columns = ['session_id', 'episode', 'frame', 'action', 'outcome_numeric']
        if not all(col in df_frames.columns for col in required_columns):
            print("Colonnes manquantes pour le calcul des statistiques d'épisode")
            return pd.DataFrame()
        
        episode_stats = df_frames.groupby(['session_id', 'episode']).agg({
            'frame': 'count',
            'action': ['nunique', 'mean'],
            'outcome_numeric': 'first'
        }).reset_index()
        
        episode_stats.columns = ['session_id', 'episode', 'frame_count', 
                               'unique_actions', 'avg_action_value', 'outcome']
                               
        return episode_stats