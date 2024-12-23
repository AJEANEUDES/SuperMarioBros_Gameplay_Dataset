import pandas as pd
import numpy as np
from typing import Dict, Tuple

class DifficultyAnalyzer:
    def __init__(self, dataframes: Dict[str, pd.DataFrame]):
        self.dataframes = dataframes

    def calculate_level_metrics(self) -> pd.DataFrame:
        """Calcule les métriques de difficulté par niveau"""
        if 'episodes' not in self.dataframes:
            raise KeyError("Données d'épisodes non trouvées")

        df = self.dataframes['episodes']
        
        level_metrics = df.groupby(['world', 'level']).agg({
            'episode': 'count',
            'outcome_numeric': ['mean', 'count'],
        }).reset_index()
        
        level_metrics.columns = ['world', 'level', 'total_attempts', 
                               'success_rate', 'total_plays']
        
        # Calcul du score de difficulté
        level_metrics['difficulty_score'] = 1 - level_metrics['success_rate']
        
        return level_metrics

    def analyze_player_actions(self) -> pd.DataFrame:
        """Analyse les actions du joueur par niveau"""
        if 'frames' not in self.dataframes:
            return pd.DataFrame()
            
        df = self.dataframes['frames']
        
        action_metrics = df.groupby(['world', 'level']).agg({
            'A': 'mean',  # Fréquence des sauts
            'B': 'mean',  # Fréquence des courses
            'right': 'mean',
            'left': 'mean',
            'frame': 'count'
        }).reset_index()
        
        action_metrics.columns = ['world', 'level', 'jump_freq', 
                                'run_freq', 'right_freq', 'left_freq', 
                                'total_frames']
                                
        return action_metrics

    def categorize_difficulty(self, metrics: pd.DataFrame) -> pd.DataFrame:
        """Catégorise les niveaux par difficulté"""
        df = metrics.copy()
        
        # Gestion des valeurs dupliquées dans les bins
        try:
            df['difficulty_category'] = pd.qcut(
                df['difficulty_score'],
                q=5,
                labels=['Très Facile', 'Facile', 'Moyen', 'Difficile', 'Très Difficile'],
                duplicates='drop'
            )
        except ValueError:
            # Si pas assez de valeurs uniques pour 5 catégories, utiliser moins de catégories
            unique_values = len(df['difficulty_score'].unique())
            if unique_values < 5:
                n_categories = max(2, unique_values)
                labels = ['Facile', 'Difficile'] if n_categories == 2 else \
                        ['Facile', 'Moyen', 'Difficile'] if n_categories == 3 else \
                        ['Très Facile', 'Facile', 'Difficile', 'Très Difficile']
                
                df['difficulty_category'] = pd.qcut(
                    df['difficulty_score'],
                    q=n_categories,
                    labels=labels,
                    duplicates='drop'
                )
            else:
                # Utiliser une méthode alternative de catégorisation
                df['difficulty_category'] = pd.cut(
                    df['difficulty_score'],
                    bins=[0, 0.2, 0.4, 0.6, 0.8, 1.0],
                    labels=['Très Facile', 'Facile', 'Moyen', 'Difficile', 'Très Difficile'],
                    include_lowest=True
                )
        
        return df