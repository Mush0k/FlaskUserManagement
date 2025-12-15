def slugify(text):
    import re
    # замена кириллицы на латиницу (очень упрощенная)
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text) 
    text = re.sub(r'[\s_]+', '-', text)  
    return text.strip('-')