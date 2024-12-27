import hashlib

REPLACEMENTS_CHARS = {
    'Ã‚Â°': '°',
    'Ã©': 'é',
    'Ãƒâ€°': 'É',
    'ÃƒÂ©': 'é',
    'ÃƒÂ¨': 'è',
    'ÃƒÂ ': 'à',
    'ÃƒÂ¢': 'â',
    'ÃƒÂ®': 'î',
    'ÃƒÂ´': 'ô',
    'ÃƒÂ»': 'û',
    'Ã¨': 'è',
    'Ã ': 'à',
    'Ã¢': 'â',
    'Ã®': 'î',
    'Ã´': 'ô',
    'Ã»': 'û'
}

def string2hash(input_string:str, algorithm:str='sha256') -> str:
    # Crée un nouvel objet de hash avec l'algorithme spécifié
    hash_function = hashlib.new(algorithm)
    # Met à jour l'objet de hash avec la chaîne de caractères (en encodage binaire)
    hash_function.update(input_string.encode('utf-8'))
    # Renvoie la chaîne de caractères hachée sous forme hexadécimale
    return hash_function.hexdigest()

def fix_encoding(text:str) -> str:
    """
    Corrige les problèmes d'encodage courants dans le texte.
    
    Args:
        text (str): Le texte mal encodé
        
    Returns:
        str: Le texte avec l'encodage corrigé
    """
    # Méthode 1: Utilisation de encode/decode
    try:
        # Essaie de décoder depuis latin1 puis encoder en utf-8
        return text.encode('latin1').decode('utf-8')
    except:
        pass
    
    # Méthode 2: Remplacement direct des séquences problématiques
    for bad, good in REPLACEMENTS_CHARS.items():
        text = text.replace(bad, good)
    
    return text

def multi_replace(texte:str, *replacements:list[tuple[str]]|list[str]) -> str:
    """
    Remplace plusieurs chaînes dans le texte.

    Args:
        texte: La chaîne de caractères à modifier.
        replacements: Un ou plusieurs tuples sous la forme (ancien, nouveau) ou (ancien, nouveau, occurrences) ou (ancien1, nouveau1, ancien2, nouveau2, ...).

    Returns:
        Une nouvelle chaîne avec les remplacements appliqués.
    """
    result = texte
    if isinstance(replacements[0], (list, tuple)) and len(replacements) == 1:
        for t in range(0, len(replacements[0]), 2):
            old, new = replacements[0][t], replacements[0][t+1]
            result = result.replace(old, new)
    elif isinstance(replacements[0], (list, tuple)):
        for t in replacements:
            old, new, occurrences = t[0], t[1], t[2] if len(t) > 2 else -1
            result = result.replace(old, new, occurrences)
    else:
        assert "type not found"
    return result

def while_replace(texte:str, old:str, new:str) -> str:
    result = texte
    while old in result:
        result = result.replace(old, new)
    return result
