import string
import csv

# Grammar definition (same as yours with a small duplicate rule fix)
grammar = {
    "S": [["Det", "NV"], ["Pronoun", "AV"], ["Det", "NA"], ["Noun", "AV"], ["Noun", "AA"], ["Verb", "PP"]],
    "NV": [["Noun", "VV"], ["Noun","VD"], ["Noun", "VP"], ["Noun", "VN"]],
    "VV": [["Verb", "VN"]],
    "VN": [["Verb", "Noun"], ["Verb", "NN"], ["Verb", "NV"]],
    "AV": [["Aux", "VP"], ["Aux", "Verb"], ["Aux", "VN"]],
    "VP": [["Verb", "PV"], ["Verb", "PN"], ["Verb", "PP"]],
    "PN": [["Preposition", "Noun"], ["Pronoun", "Noun"]],
    "VD": [["Verb", "DN"]],
    "DN": [["Det", "Noun"]],
    "NA": [["Noun", "AV"]],
    "PV": [["Preposition", "VN"], ["Pronoun", "VN"]],
    "AA": [["Aux", "AA"], ["Aux", "AV"]],
    "PP": [["Pronoun", "PN"], ["Preposition", "PV"]],
    "NN": [["Noun", "Noun"]],

    "Det": [["the"], ["some"], ["a"], ["this"]],
    "Noun": [["librarian"], ["books"], ["system"], ["location"], ["card"], ["topic"],
             ["library"], ["catalog"], ["authors"], ["online"], ["number"], ["genre"], ["help"]],
    "Verb": [["helps"], ["find"], ["search"], ["shows"], ["needed"], ["borrow"],
             ["arranged"], ["may"], ["available"], ["borrowed"], ["request"], ["has"],
             ["assist"], ["located"], ["updates"], ["is"], ["easy"], ["ask"], ["need"], ["finding"]],
    "Pronoun": [["you"], ["its"]],
    "Aux": [["may"], ["can"], ["is"], ["be"], ["are"], ["not"]],
    "Preposition": [["for"], ["by"], ["with"], ["to"], ["if"]]
}

sentences = [
    "The librarian helps find books.",
    "You can search for books.",
    "The system shows the location.",
    "A card is needed to borrow books.",
    "Books are arranged by topic.",
    "Books may not be available.",
    "Some books are borrowed.",
    "You can request books.",
    "The library has a catalog.",
    "The librarian can assist with books.",
    "The catalog helps you find authors.",
    "You may find books online.",
    "Books are located by number.",
    "The library updates its catalog.",
    "You can search by genre.",
    "The system is easy.",
    "Ask if you need help finding books.",
    "The librarian could not find it",
    "You can look for books on Google.",
    "Book the flight through Houston.",
]

def tokenize(sentence):
    return sentence.lower().translate(str.maketrans('', '', string.punctuation)).split()

def cyk_parse(sentence):
    words = tokenize(sentence)
    n = len(words)
    table = [[set() for _ in range(n)] for _ in range(n)]

    for j in range(n):
        word = words[j]
        for non_terminal, productions in grammar.items():
            if [word] in productions:
                table[j][j].add(non_terminal)

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            for k in range(i, j):
                for non_terminal, productions in grammar.items():
                    for production in productions:
                        if len(production) == 2:
                            left, right = production
                            if left in table[i][k] and right in table[k + 1][j]:
                                table[i][j].add(non_terminal)

    return table, words

def is_sentence_in_language(sentence):
    table, _ = cyk_parse(sentence)
    return "S" in table[0][len(tokenize(sentence)) - 1]

def prepare_cyk_table_for_csv(sentence):
    table, words = cyk_parse(sentence)
    rows = []
    header = words

    for i in range(len(words)):
        row = []
        for j in range(len(words)):
            if i <= j:
                cell_content = '|'.join(sorted(table[i][j]))
                index = f"[{i},{j+1}]"
                row.append(f"{cell_content}\n{index}")
            else:
                row.append("")
        rows.append(row)

    return header, rows

def write_all_cyk_tables_to_csv(all_headers, all_rows):
    try:
        with open("all_cyk_tables.csv", mode="w", newline='') as file:
            writer = csv.writer(file)
            for sentence, (header, rows) in zip(sentences, zip(all_headers, all_rows)):
                writer.writerow([f"Sentence: {sentence}"])
                writer.writerow(header)
                writer.writerows(rows)
                writer.writerow([])

        print("All CYK tables have been written to 'all_cyk_tables.csv'.")

    except PermissionError:
        print("Permission denied: Unable to write to 'all_cyk_tables.csv'.")

def main():
    all_headers = []
    all_rows = []

    for sentence in sentences:
        if is_sentence_in_language(sentence):
            print(f"✓ '{sentence}' Yes, the sentences belongs to the language.")
        else:
            print(f"✗ '{sentence}' No, the sentence does not belong to the language.")
        header, rows = prepare_cyk_table_for_csv(sentence)
        all_headers.append(header)
        all_rows.append(rows)

    write_all_cyk_tables_to_csv(all_headers, all_rows)

if __name__ == "__main__":
    main()
