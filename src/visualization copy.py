import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict

class DataVisualizer:
    
    #initiation des paramètres et des métriques
    def __init__(self, metrics: Dict[str, pd.DataFrame]):
        self.metrics = metrics
        plt.style.use('classic')
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['axes.grid'] = True
        plt.rcParams['font.size'] = 10

    def plot_level_difficulty_heatmap(self, save_path: str = None):
        """Crée une heatmap de la difficulté par niveau et monde"""
        if 'level_metrics' not in self.metrics:
            return
            
        df = self.metrics['level_metrics'].pivot(
            index='world', 
            columns='level', 
            values='difficulty_score'
        )
        
        plt.figure(figsize=(12, 8))
        sns.heatmap(df, annot=True, cmap='YlOrRd', fmt='.2f')
        plt.title('Carte de Difficulté par Niveau', pad=20)
        plt.xlabel('Niveau')
        plt.ylabel('Monde')
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight', dpi=300)
        plt.close()

    def plot_action_distribution(self, save_path: str = None):
        """Visualise la distribution des actions par niveau de difficulté"""
        if 'action_metrics' not in self.metrics:
            return
            
        df = self.metrics['action_metrics']
        
        plt.figure(figsize=(12, 6))
        actions = ['jump_freq', 'run_freq', 'right_freq', 'left_freq']
        df[actions].boxplot()
        plt.title('Distribution des Actions par Type', pad=20)
        plt.ylabel('Fréquence')
        plt.xticks(rotation=45)
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight', dpi=300)
        plt.close()

    def generate_summary_report(self) -> pd.DataFrame:
        """Génère un rapport récapitulatif des métriques"""
        summary_data = {}
        
        if 'level_metrics' in self.metrics:
            lm = self.metrics['level_metrics']
            difficulty_stats = lm['difficulty_score'].describe()
            success_stats = lm['success_rate'].describe()
            
            # Formatage des statistiques de difficulté
            summary_data.update({
                'difficulty_mean': difficulty_stats['mean'],
                'difficulty_std': difficulty_stats['std'],
                'difficulty_min': difficulty_stats['min'],
                'difficulty_max': difficulty_stats['max'],
                'success_rate_mean': success_stats['mean'],
                'success_rate_std': success_stats['std'],
                'success_rate_min': success_stats['min'],
                'success_rate_max': success_stats['max']
            })
            
        if 'action_metrics' in self.metrics:
            am = self.metrics['action_metrics']
            for action in ['jump_freq', 'run_freq']:
                stats = am[action].describe()
                summary_data.update({
                    f'{action}_mean': stats['mean'],
                    f'{action}_std': stats['std'],
                    f'{action}_min': stats['min'],
                    f'{action}_max': stats['max']
                })
        
        # Création d'un DataFrame avec une seule ligne
        return pd.DataFrame([summary_data])