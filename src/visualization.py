import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict

class DataVisualizer:
    def __init__(self, metrics: Dict[str, pd.DataFrame]):
        self.metrics = metrics
        plt.style.use('classic')
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['axes.grid'] = True
        plt.rcParams['font.size'] = 10

    def get_difficulty_heatmap(self):
        """Crée une heatmap de la difficulté par niveau et monde"""
        if 'level_metrics' not in self.metrics:
            return None
            
        df = self.metrics['level_metrics'].pivot(
            index='world', 
            columns='level', 
            values='difficulty_score'
        )
        
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.heatmap(df, annot=True, cmap='YlOrRd', fmt='.2f', ax=ax)
        plt.title('Carte de Difficulté par Niveau', pad=20)
        plt.xlabel('Niveau')
        plt.ylabel('Monde')
        
        return fig

    def get_action_distribution(self):
        """Visualise la distribution des actions par niveau de difficulté"""
        if 'action_metrics' not in self.metrics:
            return None
            
        df = self.metrics['action_metrics']
        
        fig, ax = plt.subplots(figsize=(12, 6))
        actions = ['jump_freq', 'run_freq', 'right_freq', 'left_freq']
        df[actions].boxplot(ax=ax)
        plt.title('Distribution des Actions par Type', pad=20)
        plt.ylabel('Fréquence')
        plt.xticks(rotation=45)
        
        return fig

    def generate_summary_report(self) -> pd.DataFrame:
        """Génère un rapport récapitulatif des métriques"""
        summary_data = {}
        
        if 'level_metrics' in self.metrics:
            lm = self.metrics['level_metrics']
            difficulty_stats = lm['difficulty_score'].describe()
            success_stats = lm['success_rate'].describe()
            
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
        
        return pd.DataFrame([summary_data])