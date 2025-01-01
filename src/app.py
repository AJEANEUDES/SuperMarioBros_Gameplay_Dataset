import streamlit as st
from io import StringIO
import pandas as pd
import requests
from PIL import Image
import matplotlib.pyplot as plt

st.set_page_config(page_title="Visualisation des Données Super Mario Bros", layout="wide")

def download_csv_from_drive(link):
    """Télécharge un fichier CSV depuis un lien Google Drive et le retourne comme DataFrame."""
    try:
        file_id = link.split("/d/")[1].split("/view")[0]
        direct_url = f"https://drive.google.com/uc?id={file_id}"
        response = requests.get(direct_url)
        response.raise_for_status()  # Vérifie que la requête a réussi
        csv_data = StringIO(response.text)
        return pd.read_csv(csv_data)
    except Exception as e:
        st.error(f"Erreur lors du chargement de {link}: {str(e)}")
        return None

def download_image_from_drive(link):
    """Télécharge une image depuis un lien Google Drive et la retourne comme objet PIL."""
    try:
        file_id = link.split("/d/")[1].split("/view")[0]
        direct_url = f"https://drive.google.com/uc?id={file_id}"
        response = requests.get(direct_url, stream=True)
        response.raise_for_status()  # Vérifie que la requête a réussi
        return Image.open(response.raw)
    except Exception as e:
        st.error(f"Erreur lors du chargement de l'image: {str(e)}")
        return None

def main():
    st.title("📊 Visualisation des Données Super Mario Bros")
    
    # Liens des fichiers CSV
    csv_links = {
        "Level Metrics": "https://drive.google.com/file/d/17wMGdk6VoyIdEUOi325qeb4kBxHqHLlG/view?usp=sharing",
        "Episode Stats": "https://drive.google.com/file/d/1JSXIxmqDsr8LChyNlonNCIF-NYkG69NR/view?usp=sharing",
        "Difficulty Data": "https://drive.google.com/file/d/1NhQ7U4Yxa7k9v6y5IfQ9U9X4Ffl3qEor/view?usp=sharing"
    }
    
    # Liens des fichiers PNG
    image_links = {
        "Action Distribution": "https://drive.google.com/file/d/1A82VUq26WioJgDD9LqnhbIvhdeFs3SRi/view?usp=sharing",
        "Difficulty Heatmap": "https://drive.google.com/file/d/1Vbcwfl3xlw1UYfbwScMY97k58jqvs80b/view?usp=sharing"
    }

    # Charger et afficher les CSV
    st.subheader("📋 Données CSV")
    tabs = st.tabs(list(csv_links.keys()))
    for i, (name, link) in enumerate(csv_links.items()):
        with tabs[i]:
            st.text(f"Chargement de {name}...")
            df = download_csv_from_drive(link)
            if df is not None:
                st.write(f"**{name}**")
                st.dataframe(df)

    # Charger et afficher les images
    st.subheader("🖼️ Visualisations des Images")
    for name, link in image_links.items():
        st.text(f"Chargement de {name}...")
        img = download_image_from_drive(link)
        if img is not None:
            st.image(img, caption=name, use_column_width=True)

if __name__ == "__main__":
    main()
