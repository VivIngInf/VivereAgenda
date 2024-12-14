from hashlib import sha256
from base64 import urlsafe_b64encode


def safe_hash_name(string1: str, string2: str) -> str:
    return urlsafe_b64encode(sha256(str(string1 + "_" + string2).encode()).digest()).decode('utf-8')[:16]


CONVERSATION_CLASSES = ["ConversationManager", "Registration", ]

ACQUIRE_USERNAME_REGISTRATION = "SRwRn962weWpk_8A"
ACQUIRE_EMAIL_REGISTRATION = "Zzi3aVHP0fvcI5Sp"



GENDER_DICT = {"donna": "a", "uomo": "o", "altro": "ə"}
DB_GENDER_DICT = {"D": "a", "U": "o", "A": "ə", "M": "o", "F": "a"}