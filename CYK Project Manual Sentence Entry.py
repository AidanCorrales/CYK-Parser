#FileName:CYK Project - Repeat
#Author: Aidan Corrales
#Version 3
#Creation 4/4/2025
#Last modified 4/26/2025

import string
import csv

# Grammar definition
grammar = {
    "S": [["Det", "NV"], ["Pronoun", "AV"], ["Det", "NA"], ["Noun", "AV"], ["Noun", "AA"], ["Verb", "PP"]],
    "NV": [["Noun", "VV"], ["Noun","VD"], ["Noun", "VP"], ["Noun", "VN"]],
    "VV": [["Verb", "VN"]],
    "VN": [["Verb", "Noun"], ["Verb", "NN"], ["Verb", "NV"]],
    "AV": [["Aux", "VP"], ["Aux", "Verb"],["Aux", "VN"]],
    "VP": [["Verb", "PV"], ["Verb", "PN"], ["Verb", "PP"]],
    "PN": [["Preposition", "Noun"],["Pronoun", "Noun"]],
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


# Function to tokenize the input sentence
def tokenize(sentence):
    return sentence.lower().translate(str.maketrans('', '', string.punctuation)).split()

# Function to create the CYK table
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

# Function to check if the sentence belongs to the language
def is_sentence_in_language(sentence):
    table, _ = cyk_parse(sentence)
    return "S" in table[0][len(sentence.split()) - 1]

# Function to prepare the CYK table for CSV
def prepare_cyk_table_for_csv(sentence):
    table, words = cyk_parse(sentence)

    # Prepare data for CSV
    rows = []
    
    # First row (header): The sentence words, columns start at 1
    header = words  # Columns are indexed starting at 1
    
    #Formatting
    for i in range(len(words)):
        row = []
        for j in range(len(words)):

            if i <= j:
                cell_content = '|'.join(sorted(table[i][j]))
                index = f"[{i},{j+1}]"  # [x,y] index
                row.append(f"{cell_content}\n{index}")
            else:
                row.append("")
        rows.append(row)

    return header, rows

# Function to write all collected CYK tables to a CSV file
def write_all_cyk_tables_to_csv(all_headers, all_rows):
    try:
        with open("all_cyk_tables.csv", mode="w", newline='') as file:
            writer = csv.writer(file)
            
            for header, rows in zip(all_headers, all_rows):
                writer.writerow(header)
                writer.writerows(rows)
                writer.writerow([])
        
        print("All CYK tables have been written to 'all_cyk_tables.csv'.")
    
    except PermissionError:
        print("Permission denied: Unable to write to 'all_cyk_tables.csv'. Please close any open instances of the file or run the script with elevated privileges.")

# Main driver function
def main():
    all_headers = []
    all_rows = []
    
    while True:
        sentence = input("Enter a sentence: ")
        
        if is_sentence_in_language(sentence):
            print("Yes, the sentence belongs to the language.")
        else:
            print("No, the sentence does not belong to the language.")
        
        header, rows = prepare_cyk_table_for_csv(sentence)
        all_headers.append(header)
        all_rows.append(rows)
        
        # Ask if the user wants to enter another sentence
        repeat = input("Would you like to enter another sentence? (1 for yes, 0 for no): ")
        if repeat == '0':
            print("Exiting the program and saving all CYK tables.")
            break

    # After the loop ends, save all the CYK tables to a CSV
    write_all_cyk_tables_to_csv(all_headers, all_rows)

if __name__ == "__main__":
    main()
