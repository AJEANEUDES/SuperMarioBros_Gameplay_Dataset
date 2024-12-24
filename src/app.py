import streamlit as st
from data_loader import DataLoader
from data_preprocessor import DataPreprocessor
from difficulty_analyzer import DifficultyAnalyzer
from visualization import DataVisualizer
from utils.data_source import DataSource
import pandas as pd
import time

st.set_page_config(page_title="Analyse Super Mario Bros", layout="wide")

def process_data_with_progress(data_path: str):
    """Traite les données avec une barre de progression"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Étape 0: Préparation des données (10%)
        status_text.text("Préparation de la source de données...")
        actual_path = DataSource.get_data_path(data_path)
        progress_bar.progress(10)
        
        # Étape 1: Chargement des données (35%)
        status_text.text("Chargement des données...")
        loader = DataLoader(actual_path)
        raw_data = loader.load_data()
        progress_bar.progress(35)
        
        # Étape 2: Prétraitement (60%)
        status_text.text("Prétraitement des données...")
        preprocessor = DataPreprocessor(raw_data)
        cleaned_data = preprocessor.clean_data()
        episode_stats = preprocessor.calculate_episode_stats()
        progress_bar.progress(60)
        
        # Étape 3: Analyse (85%)
        status_text.text("Analyse des données...")
        analyzer = DifficultyAnalyzer(cleaned_data)
        level_metrics = analyzer.calculate_level_metrics()
        action_metrics = analyzer.analyze_player_actions()
        difficulty_data = analyzer.categorize_difficulty(level_metrics)
        progress_bar.progress(85)
        
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
        
    except Exception as e:
        status_text.text("Une erreur est survenue!")
        raise e

def main():
    st.title("📊 Analyse des données Super Mario Bros")
    
    # Sélection de la source des données
    source_type = st.radio(
        "Source des données",
        ["Chemin local", "Google Drive"],
        horizontal=True
    )
    
    if source_type == "Chemin local":
        data_path = st.text_input(
            "Chemin vers les données",
            value=r"C:\Users\Yao ADJANOHOUN\Documents\Ma maitrise\analyse\smbdataset\data-smb"
        )
    else:
        data_path = st.text_input(
            "URL Google Drive",
            value="https://drive.google.com/drive/folders/1--4DCtgVaE5KzMUElhHDK3YNSq1M9NeL?usp=sharing",
            help="Assurez-vous que le dossier est partagé et accessible"
        )

    if st.button("Analyser les données"):
        try:
            with st.spinner("Traitement en cours..."):
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