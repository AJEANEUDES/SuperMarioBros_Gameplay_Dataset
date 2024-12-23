import streamlit as st
from data_loader import DataLoader
from data_preprocessor import DataPreprocessor
from difficulty_analyzer import DifficultyAnalyzer
from visualization import DataVisualizer
from pathlib import Path
import pandas as pd

st.set_page_config(page_title="Analyse Super Mario Bros", layout="wide")

def main():
    st.title("📊 Analyse des données Super Mario Bros")
    
    # Sélection du dossier de données
    data_path = st.text_input(
        "Chemin vers les données",
        value=r"C:\Users\jcpro\OneDrive\Documents\Ma maitrise\analyse\smbdataset\data-smb"
    )

    if st.button("Analyser les données"):
        with st.spinner("Chargement des données..."):
            # Chargement des données
            loader = DataLoader(data_path)
            raw_data = loader.load_data()

            # Prétraitement
            preprocessor = DataPreprocessor(raw_data)
            cleaned_data = preprocessor.clean_data()
            episode_stats = preprocessor.calculate_episode_stats()

            # Analyse
            analyzer = DifficultyAnalyzer(cleaned_data)
            level_metrics = analyzer.calculate_level_metrics()
            action_metrics = analyzer.analyze_player_actions()
            difficulty_data = analyzer.categorize_difficulty(level_metrics)

            # Visualisation
            metrics = {
                'level_metrics': difficulty_data,
                'action_metrics': action_metrics,
                'episode_stats': episode_stats
            }
            visualizer = DataVisualizer(metrics)

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
                st.dataframe(difficulty_data)
            with tabs[1]:
                st.dataframe(action_metrics)
            with tabs[2]:
                st.dataframe(episode_stats)

if __name__ == "__main__":
    main()