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


def main() -> None:
    csv_path = Path(__file__).parent.parent / "data" / "songs.csv"
    songs = load_songs(str(csv_path))
    print(f"Loaded songs: {len(songs)}\n")

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print(f"\nTop {len(recommendations)} Recommendations")
    print("=" * 40)

    for i, (song, score, reasons) in enumerate(recommendations, start=1):
        print(f"\n#{i}  {song['title']} — {song['artist']}")
        print(f"    Score  : {score:.2f}")
        print(f"    Genre  : {song['genre']}  |  Mood: {song['mood']}")
        if reasons:
            print(f"    Reasons:")
            for reason in reasons:
                print(f"      • {reason}")
        print("-" * 40)


if __name__ == "__main__":
    main()
