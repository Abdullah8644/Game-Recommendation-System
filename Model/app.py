import streamlit as st
import pickle
import requests
from PIL import Image
from io import BytesIO
import numpy as np

def load_split_similarity(file_paths):
    similarity_parts = []
    for file_path in file_paths:
        with open(file_path, 'rb') as file:
            similarity_parts.append(pickle.load(file))
    # Combine all parts into a single array
    return np.concatenate(similarity_parts)


# Load data
data = pickle.load(open(r"Model/moives.pkl", "rb"))
moives_list = data["title"].values
similarity_data=[r"Model\similarty1.pkl",r"Model\similarty2.pkl"]
similarity=load_split_similarity(similarity_data)



def convert_img(url):
    """Convert image URL to bytes."""
    response = requests.get(url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content)).convert("RGB")
        img_bytes = BytesIO()
        img.save(img_bytes, format="JPEG")
        img_bytes.seek(0)
        return img
    else:
        st.error("Failed to download image")
        return None  # Return None to indicate failure

def recommend(movie):
    """Recommend movies based on the selected movie."""
    movie_index = data[data["title"] == movie].index[0]
    distances = similarity[movie_index]
    # Get top 5 similar movies (excluding the selected movie)
    recommended_movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    titles, links, imgs = [], [], []
    for index, _ in recommended_movies:
        titles.append(data.iloc[index].title)
        links.append(data.iloc[index].link)
        imgs.append(data.iloc[index].img)

    return titles, links, imgs

try:
    # Streamlit UI setup
    st.set_page_config(page_title="Game Recommendation System", layout="wide")
    st.title("🎮 Game Recommendation System")

    # Sidebar for movie selection
    st.sidebar.header("Select a Game")
    selected_movie_name = st.sidebar.selectbox("Choose a Movie", moives_list)

    if st.sidebar.button("Recommend"):
        names, links, imgs = recommend(selected_movie_name)

        # Create a grid layout for recommended movies
        st.subheader(f"Recommendations for **{selected_movie_name}**")
        cols = st.columns(5)

        for i, col in enumerate(cols):
            with col:
                # Create a card-like appearance using markdown
                img = convert_img(imgs[i])  # Convert the image file to bytes

                # Display the movie title above the image
                st.markdown(f"<h4>{names[i]}</h4>", unsafe_allow_html=True)

                # Display the image using st.image without a caption
                if img is not None:
                    st.image(img, width=150)  # Display the image directly
                else:
                    st.error(f"Image for {names[i]} could not be loaded.")  # Handle error for each image
                
                # Display the link with reduced spacing
                st.markdown(
                    f"""
                        <a href="{links[i]}" target="_blank" style="text-decoration: none; margin-top: 5px; display: block;">Check it Here</a>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    st.sidebar.markdown("### Contact")
    st.sidebar.info("For any inquiries, reach out at abdullahansir8644@gmail.com")
except Exception as e:
    st.error("An error occurred while loading the recommendations. Please try again.")
    st.write(e)  # Optional: Print the error message for debugging
