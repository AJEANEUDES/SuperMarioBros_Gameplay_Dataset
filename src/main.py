from data_loader import DataLoader
from data_preprocessor import DataPreprocessor
from difficulty_analyzer import DifficultyAnalyzer
from visualization import DataVisualizer
import os
import time
from tqdm import tqdm
from pathlib import Path

def print_separator(char="-", length=50):
    """Affiche une ligne de séparation"""
    print("\n" + char * length + "\n")

def format_time(seconds):
    """Formate le temps en format lisible"""
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    if hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"

def setup_paths():
    """Configure les chemins du projet"""
    # Chemin vers les données
    
    # data_path = Path(r"C:\Users\jcpro\OneDrive\Documents\Ma maitrise\analyse\collecte de données\données des performances des joueurs\MarioMetrics\smbdataset\data-smb")
    data_path = Path(r"https://drive.google.com/drive/folders/1--4DCtgVaE5KzMUElhHDK3YNSq1M9NeL?usp=sharing")

    # Chemin pour les résultats (dans le même dossier que le script)
    script_dir = Path(__file__).parent
    results_path = script_dir / "results"
    
    # Création du dossier results s'il n'existe pas
    results_path.mkdir(exist_ok=True)
    
    return data_path, results_path

def count_files(path):
    """Compte le nombre total de fichiers PNG"""
    return sum(1 for _ in Path(path).rglob("*.png"))

def main():
    try:
        total_start_time = time.time()
        
        # Configuration des chemins
        data_path, results_path = setup_paths()
        
        print_separator("=")
        print("DEMARRAGE DE L'ANALYSE DU DATASET SUPER MARIO BROS")
        print(f"Chemin des donnees: {data_path}")
        print(f"Dossier des resultats: {results_path}")
        
        # Phase 1: Chargement des données
        print_separator()
        print("PHASE 1/4: CHARGEMENT DES DONNEES")
        phase_start = time.time()
        
        total_files = count_files(data_path)
        print(f"\nNombre total de fichiers a traiter: {total_files}")
        
        loader = DataLoader(str(data_path))
        raw_data = loader.load_data()
        
        phase_time = time.time() - phase_start
        print(f"\nChargement termine en {format_time(phase_time)}")
        
        if raw_data:
            print("\nStatistiques du chargement:")
            for key, df in raw_data.items():
                print(f"- {key.capitalize()}: {len(df)} entrees")
                if not df.empty:
                    print(f"  Colonnes: {', '.join(df.columns)}")

        # Phase 2: Prétraitement
        print_separator()
        print("PHASE 2/4: PRETRAITEMENT DES DONNEES")
        phase_start = time.time()
        
        preprocessor = DataPreprocessor(raw_data)
        print("\nNettoyage des donnees...")
        cleaned_data = preprocessor.clean_data()
        
        print("\nResultats du nettoyage:")
        for key, df in cleaned_data.items():
            print(f"- {key.capitalize()}: {len(df)} entrees valides")
        
        print("\nCalcul des statistiques par episode...")
        episode_stats = preprocessor.calculate_episode_stats()
        if not episode_stats.empty:
            print(f"Statistiques calculees pour {len(episode_stats)} episodes")
        
        phase_time = time.time() - phase_start
        print(f"\nPretraitement termine en {format_time(phase_time)}")

        # Phase 3: Analyse de la difficulté
        print_separator()
        print("PHASE 3/4: ANALYSE DE LA DIFFICULTE")
        phase_start = time.time()
        
        analyzer = DifficultyAnalyzer(cleaned_data)
        
        print("\nCalcul des metriques de niveau...")
        level_metrics = analyzer.calculate_level_metrics()
        print(f"Metriques calculees pour {len(level_metrics)} niveaux")
        
        print("\nAnalyse des actions des joueurs...")
        action_metrics = analyzer.analyze_player_actions()
        print(f"Actions analysees pour {len(action_metrics)} niveaux")
        
        difficulty_data = analyzer.categorize_difficulty(level_metrics)
        print("\nDistribution des niveaux de difficulte:")
        diff_dist = difficulty_data['difficulty_category'].value_counts()
        for category, count in diff_dist.items():
            percentage = (count / len(difficulty_data)) * 100
            print(f"- {category}: {count} niveaux ({percentage:.1f}%)")
        
        phase_time = time.time() - phase_start
        print(f"\nAnalyse terminee en {format_time(phase_time)}")

        # Phase 4: Visualisation et export
        print_separator()
        print("PHASE 4/4: GENERATION DES VISUALISATIONS ET RAPPORTS")
        phase_start = time.time()
        
        metrics = {
            'level_metrics': difficulty_data,
            'action_metrics': action_metrics,
            'episode_stats': episode_stats
        }
        
        visualizer = DataVisualizer(metrics)
        
        print("\nCreation des visualisations...")
        
        # Génération des visualisations
        viz_files = {
            "difficulty_heatmap.png": visualizer.plot_level_difficulty_heatmap,
            "action_distribution.png": visualizer.plot_action_distribution
        }
        
        for filename, viz_func in viz_files.items():
            filepath = results_path / filename
            print(f"- Generation de {filename}")
            viz_func(str(filepath))
        
        print("\nGeneration des rapports CSV...")
        summary_report = visualizer.generate_summary_report()
        
        # Sauvegarde des résultats
        csv_files = {
            "level_difficulty.csv": difficulty_data,
            "player_actions.csv": action_metrics,
            "episode_statistics.csv": episode_stats,
            "summary_report.csv": summary_report
        }
        
        for filename, data in csv_files.items():
            filepath = results_path / filename
            data.to_csv(filepath, index=False, encoding='utf-8')
            print(f"- {filename} sauvegarde")
        
        phase_time = time.time() - phase_start
        total_time = time.time() - total_start_time
        
        print_separator("=")
        print("ANALYSE TERMINEE AVEC SUCCES!")
        print(f"Temps total d'execution: {format_time(total_time)}")
        print(f"\nResultats disponibles dans '{results_path}':")
        print("  - Visualisations:")
        print("    * difficulty_heatmap.png")
        print("    * action_distribution.png")
        print("  - Rapports:")
        print("    * level_difficulty.csv")
        print("    * player_actions.csv")
        print("    * episode_statistics.csv")
        print("    * summary_report.csv")
        print_separator("=")

    except Exception as e:
        print_separator("!")
        print("ERREUR LORS DE L'EXECUTION")
        print(f"Type: {type(e).__name__}")
        print(f"Message: {str(e)}")
        print_separator("!")
        raise

if __name__ == "__main__":
    main()