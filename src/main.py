"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs


# Named user preference profiles, covering realistic tastes plus
# adversarial/edge cases meant to stress the scoring logic.
PROFILES = {
    "High-Energy Pop": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.85,
        "likes_acoustic": False,
    },
    "Chill Lofi": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.3,
        "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.9,
        "likes_acoustic": False,
    },
    "Acoustic Jazz Lover": {
        "genre": "jazz",
        "mood": "relaxed",
        "energy": 0.4,
        "likes_acoustic": True,
    },
    # Adversarial: sad mood paired with very high target energy. No song in
    # the dataset combines "sad" with high energy, so mood match and energy
    # similarity pull the score in opposite directions.
    "Conflicting Sad + High Energy": {
        "genre": "blues",
        "mood": "sad",
        "energy": 0.95,
        "likes_acoustic": False,
    },
    # Adversarial: energy target outside the dataset's valid 0-1 range,
    # which can push the (unclamped) energy term negative.
    "Out-of-Range Energy": {
        "genre": "metal",
        "mood": "angry",
        "energy": 1.5,
        "likes_acoustic": False,
    },
}


def print_recommendations(profile_name: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    print(f"=== Profile: {profile_name} ===")
    print(f"Preferences: {user_prefs}")

    recommendations = recommend_songs(user_prefs, songs, k=k)

    print(f"\nTop {k} recommendations:\n")
    for rank, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        print(f"{rank}. {song['title']} — {song['artist']}")
        print(f"   Score: {score:.2f}")
        print(f"   Reasons: {explanation}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")
    print()

    for profile_name, user_prefs in PROFILES.items():
        print_recommendations(profile_name, user_prefs, songs, k=5)


if __name__ == "__main__":
    main()
