from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        """Initialise the recommender with a list of Song objects."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k songs ranked by compatibility with the given user profile."""
        prefs = self._profile_to_prefs(user)
        scored = sorted(
            self.songs,
            key=lambda s: score_song(prefs, self._song_to_dict(s))[0],
            reverse=True,
        )
        return scored[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation of why a song was recommended to the user."""
        prefs = self._profile_to_prefs(user)
        _, reasons = score_song(prefs, self._song_to_dict(song))
        if not reasons:
            return f"{song.title} loosely matches your preferences."
        return f"{song.title} was recommended because: {'; '.join(reasons)}."

    # ------------------------------------------------------------------ helpers
    @staticmethod
    def _profile_to_prefs(user: UserProfile) -> Dict:
        """Convert a UserProfile dataclass to a score_song-compatible prefs dict."""
        return {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "acousticness": 1.0 if user.likes_acoustic else 0.0,
        }

    @staticmethod
    def _song_to_dict(song: Song) -> Dict:
        """Convert a Song dataclass to a score_song-compatible dict."""
        return {
            "id": song.id,
            "title": song.title,
            "artist": song.artist,
            "genre": song.genre,
            "mood": song.mood,
            "energy": song.energy,
            "tempo_bpm": song.tempo_bpm,
            "valence": song.valence,
            "danceability": song.danceability,
            "acousticness": song.acousticness,
        }

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    import csv
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for line_num, row in enumerate(reader, start=2):  # start=2: row 1 is the header
            try:
                songs.append({
                    "id":           int(row["id"]),
                    "title":        row["title"],
                    "artist":       row["artist"],
                    "genre":        row["genre"],
                    "mood":         row["mood"],
                    "energy":       float(row["energy"]),
                    "tempo_bpm":    float(row["tempo_bpm"]),
                    "valence":      float(row["valence"]),
                    "danceability": float(row["danceability"]),
                    "acousticness": float(row["acousticness"]),
                })
            except (ValueError, KeyError) as e:
                print(f"Warning: skipping row {line_num} in {csv_path!r} — {e}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    score = 0.0
    reasons = []

    # Categorical features — case-insensitive exact match
    if song["mood"].lower() == str(user_prefs.get("mood", "")).lower():
        score += 3.0
        reasons.append(f"matches mood: {song['mood']}")

    if song["genre"].lower() == str(user_prefs.get("genre", "")).lower():
        score += 1.0
        reasons.append(f"matches genre: {song['genre']}")

    # Numerical features — proximity scoring (closer to target = higher score)
    # Scores are clamped to 0 so a bad match never penalises the total.
    # Reasons are only appended when the match is meaningful (>= 0.5).
    if "energy" in user_prefs:
        energy_score = max(0.0, 1 - abs(song["energy"] - user_prefs["energy"]))
        score += energy_score * 5.0
        if energy_score >= 0.5:
            reasons.append(f"energy match: {energy_score:.2f}")

    if "acousticness" in user_prefs:
        acoustic_score = max(0.0, 1 - abs(song["acousticness"] - user_prefs["acousticness"]))
        score += acoustic_score * 2.0
        if acoustic_score >= 0.5:
            reasons.append(f"acousticness match: {acoustic_score:.2f}")

    if "tempo_bpm" in user_prefs:
        tempo_score = max(0.0, 1 - abs(song["tempo_bpm"] - user_prefs["tempo_bpm"]) / 200)
        score += tempo_score * 1.5
        if tempo_score >= 0.5:
            reasons.append(f"tempo match: {tempo_score:.2f}")

    if "danceability" in user_prefs:
        dance_score = max(0.0, 1 - abs(song["danceability"] - user_prefs["danceability"]))
        score += dance_score * 1.0
        if dance_score >= 0.5:
            reasons.append(f"danceability match: {dance_score:.2f}")

    if "valence" in user_prefs:
        valence_score = max(0.0, 1 - abs(song["valence"] - user_prefs["valence"]))
        score += valence_score * 0.5
        if valence_score >= 0.5:
            reasons.append(f"valence match: {valence_score:.2f}")

    return (score, reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, List[str]]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    if k <= 0:
        raise ValueError(f"k must be a positive integer, got {k}")
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    ranked = sorted(scored, key=lambda x: x[1], reverse=True)
    # Drop songs that scored nothing before slicing to k
    ranked = [entry for entry in ranked if entry[1] > 0]
    return ranked[:k]
