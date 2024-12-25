def number_to_words(num):
    if not isinstance(num, int):
        raise ValueError("The input must be an integer.")

    # Define the number components
    units = ["", "אחד", "שניים", "שלושה", "ארבעה", "חמישה", "שישה", "שבעה", "שמונה", "תשעה"]
    # feminine_units = ["", "אחת", "שתיים", "שלוש", "ארבע", "חמש", "שש", "שבע", "שמונה", "תשע"]
    teens = ["עשרה", "אחד עשר", "שניים עשר", "שלושה עשר", "ארבעה עשר", "חמישה עשר", "שישה עשר", "שבעה עשר", "שמונה עשר", "תשעה עשר"]
    tens = ["", "", "עשרים", "שלושים", "ארבעים", "חמישים", "שישים", "שבעים", "שמונים", "תשעים"]
    hundreds = ["", "מאה", "מאתיים", "שלוש מאות", "ארבע מאות", "חמש מאות", "שש מאות", "שבע מאות", "שמונה מאות", "תשע מאות"]
    big_numbers = ["", "אלף", "מיליון", "מיליארד", "טריליון", "קוואדריליון", "קוונטיליון", "סקסטיליון", "ספטיליון", "אוקטיליון", "נוניליון"]

    # Handle zero
    if num == 0:
        return "אפס"

    # Break the number into chunks of 3 digits each
    def chunk_number(n):
        parts = []
        while n > 0:
            parts.append(n % 1000)
            n //= 1000
        return parts[::-1]

    def chunk_to_words(chunk):
        words = []
        if chunk >= 100:
            words.append(hundreds[chunk // 100])
            chunk %= 100
        if 10 <= chunk < 20:
            t = teens[chunk - 10]
            words.append(t)
        else:
            if chunk >= 20:
                t=tens[chunk // 10]
                words.append(t)
                chunk %= 10
            if chunk > 0:
                if len(words) > 0:
                    words.append(f"ו{units[chunk]}")
                else:
                    words.append(units[chunk])

        return " ".join(words)

    # Handle "and" for special cases
    def handle_special_cases(parts):
        result = []
        for i, part in enumerate(parts):
            text = ''
            if part == 0:
                continue
            scale = len(parts) - i - 1
            if scale == 1 and part == 1:
                text = big_numbers[scale]  # "מיליון" and "אלף"
            else:
                text = chunk_to_words(part)
            if scale > 0 and part > 0:
                text = text + " " + big_numbers[scale]
            if i + 1 == len(parts) and len(parts) > 1:
                text = "ו" + text
            result.append(text)
        return result

    # Split number into chunks
    parts = chunk_number(num)
    words = handle_special_cases(parts)
    
    special_cases = {
        "אחד מיליון": "מיליון",
        "אחד אלף": "אלף",
        "שניים אלף": "אלפיים",
        "שלושה אלף": "שלושת אלפים",
        "ארבעה אלף": "ארבעת אלפים",
        "חמישה אלף": "חמשת אלפים",
        "שישה אלף": "שישת אלפים",
        "שבעה אלף": "שבעת אלפים",
        "שמונה אלף": "שמונת אלפים",
        "תשעה אלף": "תשעת אלפים"
    }
    
    for i, word in enumerate(words):
        if word in special_cases:
            words[i] = special_cases[word]

    # Join words with correct punctuation
    result = " ".join(words).strip()
    return result

number_to_words(1955500)