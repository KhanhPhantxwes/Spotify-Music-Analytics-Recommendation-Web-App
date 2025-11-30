from typing import Dict
from sqlalchemy import select
from website.Recommendation.get_playlist_vector import Get_playlist_vibe
from website.model import Artist, Artist_Song, Song, Song_point,BillboardEntry2
from .. import db
import numpy as np
import json
import lyricsgenius
from sentence_transformers import SentenceTransformer

from website.Recommendation.get_lyrics_vector import Embed_lyric, clean_lyrics


#Get mood seeds

mood_words = {
    "happy": [
        "happy", "joy", "sunshine", "feeling good", "smiling all day", "celebration",
        "bright day", "good vibes", "cheerful", "excited", "laughing", "warm smiles",
        "uplifted", "energetic", "positive thoughts", "loving life", "grateful heart",
        "pure joy", "full of light", "sunny mood", "dancing around", "joyful moments",
        "good energy", "carefree", "peaceful happiness", "smile on my face",
        "vibrant spirit", "happy tears", "glowing inside", "lighthearted",
        "feeling alive", "sweet moments", "bursting with joy", "playful mood",
        "cheering loudly", "high spirits", "radiant feelings", "cloud nine",
        "life is good", "happy inside", "bright and shiny", "warm feelings",
        "heart full of joy", "positivity everywhere", "feeling blessed",
        "all smiles", "joy in my heart", "happy memories", "beautiful day",
        "moment of bliss"
    ],

    "sad": [
        "sad", "lonely", "crying", "broken heart", "tears falling", "missing you",
        "empty inside", "lost without you", "heartache", "blue feelings",
        "quiet tears", "dark days", "cold nights", "hurt inside", "painful memory",
        "feeling hopeless", "down and low", "shattered heart", "silent crying",
        "melancholy", "regretful", "sorrow", "deep sadness", "aching heart",
        "falling apart", "alone again", "hurt and broken", "holding back tears",
        "lost in my mind", "wounded heart", "drowning in sadness", "emotionless",
        "fading away", "mourning inside", "lifeless moments", "heavy heart",
        "numb feelings", "crying inside", "no one there", "bleeding heart",
        "dark thoughts", "tired of hurting", "feeling abandoned", "rainy mood",
        "longing for you", "sad memories", "feeling down", "crying tonight",
        "hurting deeply", "heart sinking"
    ],

    "romantic": [
        "love", "romance", "kiss you", "hold you close", "I adore you", "falling in love",
        "sweet whispers", "my sweetheart", "romantic nights", "you and me",
        "touching your hand", "deep connection", "candlelight moments",
        "your warm embrace", "thinking of you", "my heart beats for you",
        "forever yours", "soft kisses", "loving you deeply", "sweet love",
        "passionate feelings", "you are my world", "my baby", "heart to heart",
        "dreaming of us", "your smile melts me", "only you", "true love",
        "my everything", "romantic dreams", "warm heartbeat", "love in the air",
        "gentle touch", "affectionate moments", "soulmates forever",
        "falling for you more", "holding you tight", "cute moments",
        "love letter feelings", "my angel", "beautiful love", "intimate moments",
        "soft and warm", "my heart is yours", "heart racing for you",
        "loving gaze", "love forever", "romantic heartbeat",
        "whispering your name", "cherishing you"
    ],

    "angry": [
        "rage inside", "shouting at you", "hate and anger", "burning with rage", "fighting again",
        "frustrated", "slammed the door", "boiling blood", "furious thoughts", "losing control",
        "yelling aloud", "heart pounding fast", "seeing red", "heated argument",
        "can't calm down", "anger rising", "mad at everything", "storm inside",
        "breaking point", "fire in my chest", "angry tears", "biting my tongue",
        "fed up", "nothing makes sense", "I'm done", "tired of arguing",
        "shaking with anger", "bursting out", "irritated", "on edge",
        "stay away from me", "pushing back", "can't take it", "explosive mood",
        "spitting words", "tense atmosphere", "angry heartbeat",
        "sharp words", "frustration building", "hurt and furious",
        "no patience left", "angry thoughts", "fists clenched",
        "burning inside", "rage-filled", "furious shouting",
        "losing my temper", "red hot anger", "blowing up",
        "lashing out"
    ],

    "nostalgic": [
        "remember the past", "memories of us", "back in those days", "looking back", "wish we could go back",
        "childhood moments", "old times", "the good old days", "thinking of yesterday",
        "missing the past", "old photographs", "faded memories", "days gone by",
        "moments we shared", "songs we used to love", "dreaming of before",
        "long ago", "touch of the past", "warm memories", "bittersweet feelings",
        "reminiscing", "old stories", "times we laughed", "once upon a time",
        "can't forget", "things have changed", "memory lane", "missing how it was",
        "the way it used to be", "pages of my past", "nostalgic heart",
        "soft memories", "lost moments", "wish we had more time",
        "thinking of childhood", "longing for before", "feels like yesterday",
        "hold onto the past", "forgotten times", "so long ago",
        "memories come back", "old vibes", "life before now",
        "timeless moments", "sweet memories", "things I remember",
        "moments I treasure", "distant days", "can't go back",
        "echoes of the past", "memories in my mind"
    ],

    "calm": [
        "peaceful night", "soft and quiet", "slow and gentle", "relaxing my mind", "floating on water",
        "deep breaths", "soft breeze", "quiet thoughts", "resting easy", "calm ocean",
        "still waters", "gentle waves", "soft whispers", "serene moment", "peace within",
        "breathing slowly", "clear mind", "quiet morning", "cool wind", "warm tea",
        "tranquil mind", "drifting softly", "peaceful breeze", "deep relaxation",
        "light and still", "soothing moment", "restful evening", "calming thoughts",
        "gentle night", "soft clouds", "inner peace", "balanced mood",
        "zen feeling", "slow heartbeat", "floating feeling",
        "warm blanket", "quiet sunset", "calm river",
        "resting soul", "evening calm", "silent sky",
        "cloudy peace", "light rain sounds", "soft piano",
        "peace in silence", "mind at rest", "quiet and slow",
        "ease in my heart", "soothing air", "stillness inside",
        "relaxed spirit"
    ],

    "energetic": [
        "dance all night", "party till morning", "jumping to the beat", "turn the music up", "let's go crazy",
        "full energy", "can't stop moving", "heart racing fast", "run it up", "hype mode",
        "wild night", "electric feeling", "fast heartbeat", "jump around", "let’s move",
        "turn it louder", "pumped up", "full of adrenaline", "can't sit still",
        "feeling unstoppable", "burst of energy", "wild and free", "going insane",
        "run through the night", "hyped up", "shake the room", "crazy vibes",
        "party vibes", "let’s speed up", "jumping higher", "no slowing down",
        "full speed", "dance floor energy", "crazy loud", "supercharged",
        "electric rush", "unstoppable energy", "party spirit",
        "let’s go wild", "turn it all the way up", "live fast",
        "jump nonstop", "music blasting", "hyper mode",
        "running wild", "shake the ground", "energy overload",
        "raising the roof", "crazy energy", "amped up",
        "fired up"
    ]
}

#Calculate the vector for each mood label
def Compute_mood_vector() -> Dict[str,np.ndarray]:

    mood_vector: Dict[str, np.ndarray] = {}
    for mood_label, phrases in mood_words.items():
        vecs = []
        for phrase in phrases:
            cleaned = clean_lyrics(phrase)
            v = Embed_lyric(cleaned)
            vecs.append(v)
        # average all vectors = mood prototype
        M = np.stack(vecs, axis=0)
        m = M.mean(axis=0)

        # normalize the mood vector to unit length (good for cosine sim)
        norm = np.linalg.norm(m)
        if norm > 0:
            m = m / norm

        mood_vector[mood_label] = m
    return mood_vector

# 2) Global cache for mood vectors
_MOOD_VECTORS: Dict[str, np.ndarray] | None = None


def Compute_cosine(a: np.ndarray, b: np.ndarray) -> float:
    """Cosine similarity between two vectors."""
    na = np.linalg.norm(a)
    nb = np.linalg.norm(b)
    if na == 0 or nb == 0:
        return 0.0
    return float(np.dot(a, b) / (na * nb))

def get_mood_vectors() -> Dict[str, np.ndarray]:
    """Lazy-load and cache mood vectors."""
    global _MOOD_VECTORS
    if _MOOD_VECTORS is None:
        _MOOD_VECTORS = Compute_mood_vector()
    return _MOOD_VECTORS    

def Classify_vec_mood(vec_json: str) -> str | None:
    mood_category = get_mood_vectors()

    #Normalize input vector to make sure it has length == 1 for comparison
    input_v = np.array(json.loads(vec_json), dtype=float)
    norm_v = np.linalg.norm(input_v)
    if norm_v > 0:
        input_v = input_v / norm_v

    best_mood = None
    best_sim = -1.0

    #Cosine similarity : A higher dot product → more similar → better mood match.
    #How close two vectors point in the same direction.
    for mood_label, mood_vec in mood_category.items():
        cosine_similarity = float(np.dot(input_v,mood_vec))
        if cosine_similarity > best_sim:
            best_sim = cosine_similarity
            best_mood = mood_label
    return best_mood

def update_song_mood():
    #Get the song and the vec_json
    song_vec_list = (
        db.session.query(Song)
        .join(Song_point, Song_point.song_id == Song.song_id)
        .all()
    )

    for song in song_vec_list:
        if not song or not song.song_point:
            return None
        song_vec = song.song_point.vec_json
        song_mood = Classify_vec_mood(song_vec)

        song.mood = song_mood

    db.session.commit()
    

