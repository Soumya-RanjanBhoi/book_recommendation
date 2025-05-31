import streamlit as st
import pickle
import numpy as np
import gzip


st.set_page_config(page_title="Book Recommender", layout="wide")


popular_df = pickle.load(open("popular_df.pkl", "rb"))

sim_score = pickle.load(open("sim_score_.pkl", "rb"))
pivot_tb = pickle.load(open("pivot_table.pkl", "rb"))
books = pickle.load(open("books.pkl", "rb"))

if "temp_page" in st.session_state:
    st.session_state.page = st.session_state.temp_page
    del st.session_state.temp_page
    st.rerun()


if "page" not in st.session_state:
    st.session_state.page = "Home"


st.sidebar.radio("Navigation", ["Home", "Popular Books", "Similar Books", "My Recommendations"], key="page")





if st.session_state.page == "Home":
    st.markdown("""
        <h1 style='text-align: center; color: #6EE7B7;'>📚 Your Next Great Read Awaits</h1>
        <p style='text-align: center; color: #C0C0C0; font-size:18px;'>
            Discover books that speak to you. Our AI-powered recommendation system learns your reading preferences and helps you uncover hidden literary gems.
        </p>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.image("https://img.icons8.com/fluency/96/books.png", width=60)
        st.markdown("### 🔥 Trending Now")
        st.write("Browse the most loved and talked-about books by readers across the globe. Updated with the latest top-rated reads.")
        if st.button("📚 Browse Popular Books", key="home_popular"):
            st.session_state.temp_page = "Popular Books"
            st.rerun()


    with col2:
        st.image("https://img.icons8.com/fluency/96/search.png", width=60)
        st.markdown("### 📖 If You Liked That, You'll Love This")
        st.write("Enter a book you enjoyed, and let our algorithm find similar stories with the same vibes and themes.")
        if st.button("🔍 Find Similar Books", key="home_similar"):
            st.session_state.temp_page = "Similar Books"
            st.rerun()

    with col3:
        st.image("https://img.icons8.com/color/96/star--v1.png", width=60)
        st.markdown("### 🌟 Tailored Just for You")
        st.write("Hand-picked books based on multiple titles you love — perfect for discovering your next favorite.")
        if st.button("⭐ Personalized For You", key="home_recommend"):
            st.session_state.temp_page = "My Recommendations"
            st.rerun()




elif st.session_state.page == "Popular Books":
    st.markdown("<h1 style='text-align: center; color: #50C7C7;'>🌍 The World's Favorite Reads</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #C0C0C0;'>Explore the top 150 books adored by millions of readers — curated by ratings and reviews.</p>", unsafe_allow_html=True)

    num_cols = 4
    for i in range(0, len(popular_df), num_cols):
        cols = st.columns(num_cols)
        for j in range(num_cols):
            if i + j < len(popular_df):
                row = popular_df.iloc[i + j]
                with cols[j]:
                    st.image(row['Image-URL-M'], width=120)
                    st.markdown(f"**{row['Book-Title']}**")
                    st.markdown(f"*by {row['Book-Author']}*")
                    st.markdown(f"⭐ {round(row['Avg_rating'], 2)} | 💬 {row['num_rating']} reviews")






elif st.session_state.page == "Similar Books":
    st.title("🔎 Find Books Similar to Your Favorites")
    st.write("Can't get over a great book? Discover titles that match its magic, tone, and storytelling.")

    user_input = st.text_input("Enter Book Title...")
    if st.button("🔍 Find Similar Books", key="find_similar"):
        def recommend(book_name):
            if book_name not in pivot_tb.index:
                st.warning(f"Book '{book_name}' not found in the recommendation list.")
                return

            index = np.where(pivot_tb.index == book_name)[0][0]
            similar_items = sorted(list(enumerate(sim_score[index])), key=lambda x: x[1], reverse=True)[1:10]

            st.subheader("Books You Might Like:")
            for i in similar_items:
                recommended_title = pivot_tb.index[i[0]]
                book_info = books[books['Book-Title'] == recommended_title].drop_duplicates('Book-Title')
                for _, row in book_info.iterrows():
                    st.image(row['Image-URL-M'], width=120)
                    st.markdown(f"**{row['Book-Title']}**")
                    st.markdown(f"*by {row['Book-Author']}*")
                    break

        recommend(user_input)







elif st.session_state.page == "My Recommendations":
    st.title("My Personalized Book Recommendations")
    st.write("🔍 Personalized suggestions based on your interests.")

    recommend_titles = [
        "1984",
        "The Da Vinci Code",
        "Life of Pi",
        "The Notebook",
        "Harry Potter and the Prisoner of Azkaban (Book 3)",
        "The Hobbit : The Enchanting Prelude to The Lord of the Rings",
        "About a Boy",
        "How to Be Good",
        "The Pilot's Wife : A Novel",
        "Timeline"
    ]

    recommended_df = books[books['Book-Title'].isin(recommend_titles)].drop_duplicates('Book-Title')

    if recommended_df.empty:
        st.warning("⚠️ No book details found for your recommended titles.")
    else:
        num_cols = 4
        for i in range(0, len(recommended_df), num_cols):
            cols = st.columns(num_cols)
            for j in range(num_cols):
                if i + j < len(recommended_df):
                    row = recommended_df.iloc[i + j]
                    with cols[j]:
                        st.image(row['Image-URL-M'], width=120)
                        st.markdown(f"**{row['Book-Title']}**")
                        st.markdown(f"*by {row['Book-Author']}*")
