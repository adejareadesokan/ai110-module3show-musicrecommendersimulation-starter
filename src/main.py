"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from pathlib import Path
from recommender import load_songs, recommend_songs


PROFILES = {
    "High-Energy Pop": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.90,
        "danceability": 0.85,
        "tempo_bpm": 128,
    },
    "Chill Lofi": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.35,
        "acousticness": 0.80,
        "tempo_bpm": 75,
    },
    "Deep Intense Rock": {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.92,
        "danceability": 0.55,
        "tempo_bpm": 150,
    },
}


def print_recommendations(label: str, recommendations: list) -> None:
    """Print a labelled recommendation block to stdout."""
    print(f"\n{'=' * 40}")
    print(f"Profile: {label}")
    print(f"{'=' * 40}")
    for i, (song, score, reasons) in enumerate(recommendations, start=1):
        print(f"\n#{i}  {song['title']} — {song['artist']}")
        print(f"    Score  : {score:.2f}")
        print(f"    Genre  : {song['genre']}  |  Mood: {song['mood']}")
        if reasons:
            print("    Reasons:")
            for reason in reasons:
                print(f"      • {reason}")
        print("-" * 40)


# Adversarial / edge-case profiles — designed to expose unexpected scoring behaviour.
ADVERSARIAL_PROFILES = {
    # Conflicting mood vs energy: mood weight (3.0) may force a low-energy sad
    # song to the top even though energy: 0.9 points the opposite direction.
    "Sad but Hype": {
        "mood": "sad",
        "energy": 0.90,
        "tempo_bpm": 140,
        "danceability": 0.85,
    },
    # Phantom labels: neither "k-pop" nor "melancholy" exist in the catalog.
    # Categorical scores are always 0, so results depend entirely on numerics.
    "Phantom Genre & Mood": {
        "genre": "k-pop",
        "mood": "melancholy",
        "energy": 0.70,
        "tempo_bpm": 120,
    },
    # Empty profile: every song scores 0.0, triggering the >0 filter and
    # returning an empty recommendation list — silent failure.
    "Empty Preferences": {},
    # Physically impossible combination: high-energy acoustic songs don't
    # exist in the catalog, forcing the scorer to pick the least-bad compromise.
    "High Energy + Fully Acoustic": {
        "energy": 0.95,
        "acousticness": 0.95,
        "tempo_bpm": 140,
    },
    # Extreme BPM (300) exceeds the 200-BPM normalisation divisor in score_song.
    # Raw tempo scores go negative for every song and are clamped to 0,
    # so tempo contributes nothing — other features dominate unexpectedly.
    "Impossible Tempo": {
        "genre": "edm",
        "mood": "euphoric",
        "tempo_bpm": 300,
        "energy": 0.95,
    },
    # Valence-only: the lowest-weighted feature (cap 0.5).  No categorical
    # anchors means all songs cluster in a very tight score band, making the
    # ranking nearly arbitrary and easy to flip by rounding differences.
    "Valence Only": {
        "valence": 0.50,
    },
}


def main() -> None:
    csv_path = Path(__file__).parent.parent / "data" / "songs.csv"
    songs = load_songs(str(csv_path))
    print(f"Loaded {len(songs)} songs.\n")

    for label, user_prefs in PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(label, recommendations)

    print("\n\n*** ADVERSARIAL PROFILES ***")
    for label, user_prefs in ADVERSARIAL_PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)
        if not recommendations:
            print(f"\n{'=' * 40}")
            print(f"Profile: {label}")
            print(f"{'=' * 40}")
            print("  (no songs scored above 0 — empty result)")
        else:
            print_recommendations(label, recommendations)


if __name__ == "__main__":
    main()
