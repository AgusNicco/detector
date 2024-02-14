from multiprocessing import Pool, cpu_count
import pandas as pd
from sklearn.model_selection import train_test_split
from collections import Counter
import re

def clean_text(text):
    """Clean and tokenize text."""
    text = text.lower()  # Lowercase the text
    text = re.sub(r'[^a-z0-9\s]', '', text)  # Remove punctuation
    return text.split()

def get_fivegrams(words):
    """Generate fivegrams from a list of words."""
    return zip(words, words[1:], words[2:], words[3:], words[4:])

def calculate_fivegram_frequencies(args):
    """Calculate fivegram frequencies in a single essay."""
    index, essay = args  # Unpack the arguments
    words = clean_text(essay)
    fivegrams = list(get_fivegrams(words))
    # Print progress for each essay processed
    print(f"Processing essay {index + 1}")
    return Counter(fivegrams)

def calculate_total_frequencies(essays):
    """Calculate total fivegram frequencies for a list of essays."""
    num_essays = len(essays)
    print(f"Total essays to process: {num_essays}")
    with Pool(processes=cpu_count()) as pool:
        # Use imap_unordered for potentially faster execution and progress tracking
        result_iter = pool.imap_unordered(calculate_fivegram_frequencies, enumerate(essays))
        
        total_freq = Counter()
        for i, freq in enumerate(result_iter, 1):
            total_freq += freq
            if i % 10 == 0:  # Update progress every 10 essays
                print(f"Processed {i}/{num_essays} essays")
    return total_freq

def main():
    # Load dataset
    path = 'megaset4.csv'  # Update with your actual path
    data = pd.read_csv(path)

    # Split the data into training and testing sets
    train_data, _ = train_test_split(data, test_size=0.00001, random_state=42)

    # Ensure essays are strings and not empty or NaN
    train_data.dropna(subset=['text'], inplace=True)
    train_data['text'] = train_data['text'].astype(str)

    # Calculate fivegram frequencies for AI and Human Essays in parallel
    ai_fivegram_freq = calculate_total_frequencies(train_data[train_data['generated'] == 1]['text'].tolist())
    human_fivegram_freq = calculate_total_frequencies(train_data[train_data['generated'] == 0]['text'].tolist())

    # Normalize the frequencies by total counts
    total_ai_fivegrams = sum(ai_fivegram_freq.values())
    total_human_fivegrams = sum(human_fivegram_freq.values())
    ai_fivegram_freq = {gram: freq / total_ai_fivegrams for gram, freq in ai_fivegram_freq.items()}
    human_fivegram_freq = {gram: freq / total_human_fivegrams for gram, freq in human_fivegram_freq.items()}

    # Prepare the combined DataFrame
    fivegram_frequencies_data = []
    for fivegram in set(ai_fivegram_freq).union(human_fivegram_freq):
        ai_freq = ai_fivegram_freq.get(fivegram, 0)
        human_freq = human_fivegram_freq.get(fivegram, 0)
        prevalence_factor = 0
        if human_freq > 0 and ai_freq > 0:
            prevalence_factor = ai_freq / human_freq if ai_freq >= human_freq else -human_freq / ai_freq
        fivegram_frequencies_data.append({
            'Fivegram': ' '.join(fivegram),
            'Prevalence_Factor': prevalence_factor
        })

    # Create DataFrame
    fivegram_frequencies_df = pd.DataFrame(fivegram_frequencies_data)

    # Sort by 'Prevalence_Factor'
    fivegram_frequencies_df.sort_values(by='Prevalence_Factor', ascending=False, inplace=True)

    # Write to CSV
    fivegram_frequencies_df.to_csv('five_word_prevalence_table.csv', index=False)

if __name__ == '__main__':
    main()



    