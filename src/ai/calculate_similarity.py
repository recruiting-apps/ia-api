from sklearn.metrics.pairwise import cosine_similarity

# tfidf_skills -> matriz TF-IDF de habilidades requeridas
# tfidf_cvs -> matriz TF-IDF de CVs

def calculate_similarity(tfidf_skills, tfidf_cvs):
    similarities = []

    for tfidf_cv in tfidf_cvs:
        similarity = cosine_similarity(tfidf_skills, tfidf_cv)
        similarity_mean = similarity.mean(axis=0)
        similarities.append(similarity_mean)

    indices_sorted = [idx for idx, _ in sorted(enumerate(similarities), key=lambda x: x[1], reverse=True)]

    for idx in indices_sorted:
        print(f"CV {idx + 1}: Similarity = {similarities[idx]}")

    # return similarities, indices_sorted
    return [], []