import streamlit as st
from data_loader import DataLoader
from data_preprocessor import DataPreprocessor
from difficulty_analyzer import DifficultyAnalyzer
from visualization import DataVisualizer
from pathlib import Path
import pandas as pd
import time

st.set_page_config(page_title="Analyse Super Mario Bros", layout="wide")

def process_data_with_progress(data_path: str):
    """Traite les données avec une barre de progression"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Étape 1: Chargement des données (25%)
    status_text.text("Chargement des données...")
    loader = DataLoader(data_path)
    raw_data = loader.load_data()
    progress_bar.progress(25)
    
    # Étape 2: Prétraitement (50%)
    status_text.text("Prétraitement des données...")
    preprocessor = DataPreprocessor(raw_data)
    cleaned_data = preprocessor.clean_data()
    episode_stats = preprocessor.calculate_episode_stats()
    progress_bar.progress(50)
    
    # Étape 3: Analyse (75%)
    status_text.text("Analyse des données...")
    analyzer = DifficultyAnalyzer(cleaned_data)
    level_metrics = analyzer.calculate_level_metrics()
    action_metrics = analyzer.analyze_player_actions()
    difficulty_data = analyzer.categorize_difficulty(level_metrics)
    progress_bar.progress(75)
    
    # Étape 4: Préparation des visualisations (100%)
    status_text.text("Préparation des visualisations...")
    metrics = {
        'level_metrics': difficulty_data,
        'action_metrics': action_metrics,
        'episode_stats': episode_stats
    }
    visualizer = DataVisualizer(metrics)
    progress_bar.progress(100)
    status_text.text("Analyse terminée!")
    
    return metrics, visualizer

def main():
    st.title("📊 Analyse des données Super Mario Bros")
    
    # Sélection du dossier de données
    data_path = st.text_input(
        "Chemin vers les données",
        value=r"C:\Users\jcpro\OneDrive\Documents\Ma maitrise\analyse\collecte de données\données des performances des joueurs\MarioMetrics\smbdataset\data-smb"
    )

    if st.button("Analyser les données"):
        try:
            # Traitement des données avec barre de progression
            metrics, visualizer = process_data_with_progress(data_path)
            
            # Affichage des résultats
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🎮 Carte de difficulté")
                fig_heatmap = visualizer.get_difficulty_heatmap()
                st.pyplot(fig_heatmap)

            with col2:
                st.subheader("🎯 Distribution des actions")
                fig_actions = visualizer.get_action_distribution()
                st.pyplot(fig_actions)

            # Statistiques générales
            st.subheader("📈 Statistiques générales")
            summary = visualizer.generate_summary_report()
            st.dataframe(summary)

            # Données détaillées
            st.subheader("📋 Données détaillées")
            tabs = st.tabs(["Niveaux", "Actions", "Épisodes"])
            
            with tabs[0]:
                st.dataframe(metrics['level_metrics'])
            with tabs[1]:
                st.dataframe(metrics['action_metrics'])
            with tabs[2]:
                st.dataframe(metrics['episode_stats'])
                
        except Exception as e:
            st.error(f"Une erreur est survenue: {str(e)}")

if __name__ == "__main__":
    main()