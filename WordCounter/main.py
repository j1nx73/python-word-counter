import re
import os
from collections import Counter, defaultdict
from pathlib import Path
import json


class WordCounter:
    def __init__(self):
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these',
            'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him',
            'her', 'us', 'them', 'my', 'your', 'his', 'its', 'our', 'their'
        }

    def clean_text(self, text):
        """Clean and normalize text for analysis."""
        # Convert to lowercase
        text = text.lower()
        # Remove punctuation and special characters, keep only letters and spaces
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        # Replace multiple spaces with single space
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def extract_words(self, text, include_stop_words=True):
        """Extract words from text."""
        cleaned_text = self.clean_text(text)
        words = cleaned_text.split()

        if not include_stop_words:
            words = [word for word in words if word not in self.stop_words]

        return [word for word in words if word]  # Remove empty strings

    def count_characters(self, text):
        """Count characters in text."""
        return {
            'total_chars': len(text),
            'chars_no_spaces': len(text.replace(' ', '')),
            'alphabetic_chars': len(re.sub(r'[^a-zA-Z]', '', text)),
            'numeric_chars': len(re.sub(r'[^0-9]', '', text)),
            'spaces': text.count(' '),
            'punctuation': len(re.sub(r'[a-zA-Z0-9\s]', '', text))
        }

    def analyze_text(self, text, include_stop_words=True):
        """Perform comprehensive text analysis."""
        words = self.extract_words(text, include_stop_words)
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        paragraphs = text.split('\n\n')
        paragraphs = [p.strip() for p in paragraphs if p.strip()]

        # Word frequency analysis
        word_freq = Counter(words)

        # Character analysis
        char_stats = self.count_characters(text)

        # Calculate averages
        avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
        avg_sentence_length = len(words) / len(sentences) if sentences else 0

        # Reading time estimate (average 200 words per minute)
        reading_time_minutes = len(words) / 200

        return {
            'word_count': len(words),
            'unique_words': len(word_freq),
            'sentence_count': len(sentences),
            'paragraph_count': len(paragraphs),
            'character_stats': char_stats,
            'word_frequency': word_freq,
            'avg_word_length': round(avg_word_length, 2),
            'avg_sentence_length': round(avg_sentence_length, 2),
            'reading_time_minutes': round(reading_time_minutes, 2),
            'most_common_words': word_freq.most_common(10)
        }

    def analyze_file(self, file_path, include_stop_words=True):
        """Analyze text file and return statistics."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            analysis = self.analyze_text(content, include_stop_words)
            analysis['file_path'] = file_path
            analysis['file_size_bytes'] = os.path.getsize(file_path)

            return analysis

        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except UnicodeDecodeError:
            raise UnicodeDecodeError("Unable to read file. Please ensure it's a text file with UTF-8 encoding.")

    def compare_texts(self, text1, text2):
        """Compare two texts and show differences."""
        analysis1 = self.analyze_text(text1, include_stop_words=False)
        analysis2 = self.analyze_text(text2, include_stop_words=False)

        # Find unique words in each text
        words1 = set(analysis1['word_frequency'].keys())
        words2 = set(analysis2['word_frequency'].keys())

        unique_to_text1 = words1 - words2
        unique_to_text2 = words2 - words1
        common_words = words1 & words2

        return {
            'text1_stats': analysis1,
            'text2_stats': analysis2,
            'unique_to_text1': list(unique_to_text1)[:10],  # Show top 10
            'unique_to_text2': list(unique_to_text2)[:10],
            'common_words_count': len(common_words),
            'similarity_ratio': len(common_words) / len(words1 | words2) if (words1 | words2) else 0
        }

    def save_analysis(self, analysis, output_file):
        """Save analysis results to a file."""
        # Convert Counter objects to regular dicts for JSON serialization
        if 'word_frequency' in analysis:
            analysis['word_frequency'] = dict(analysis['word_frequency'])

        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(analysis, file, indent=2, ensure_ascii=False)

    def create_sample_file(self, filename="sample.txt"):
        """Create a sample text file for testing."""
        sample_text = """
The quick brown fox jumps over the lazy dog. This sentence contains every letter of the alphabet at least once.

Python is a powerful programming language that is widely used in various fields such as web development, data science, artificial intelligence, and automation. Its simple syntax makes it an excellent choice for beginners, while its extensive libraries and frameworks make it powerful enough for complex applications.

Data analysis is becoming increasingly important in today's world. With the rise of big data, companies need tools and professionals who can extract meaningful insights from large datasets. Python, with libraries like pandas, numpy, and matplotlib, provides excellent capabilities for data manipulation and visualization.

Machine learning and artificial intelligence are revolutionizing how we interact with technology. From recommendation systems to autonomous vehicles, AI is transforming industries and creating new possibilities for innovation.
        """.strip()

        with open(filename, 'w', encoding='utf-8') as file:
            file.write(sample_text)

        return filename


def print_analysis_report(analysis):
    """Print a formatted analysis report."""
    print("\n" + "=" * 50)
    print("📊 TEXT ANALYSIS REPORT")
    print("=" * 50)

    if 'file_path' in analysis:
        print(f"📁 File: {analysis['file_path']}")
        print(f"💾 File Size: {analysis['file_size_bytes']} bytes")

    print(f"\n📈 BASIC STATISTICS")
    print(f"   Words: {analysis['word_count']:,}")
    print(f"   Unique Words: {analysis['unique_words']:,}")
    print(f"   Sentences: {analysis['sentence_count']:,}")
    print(f"   Paragraphs: {analysis['paragraph_count']:,}")

    char_stats = analysis['character_stats']
    print(f"\n🔤 CHARACTER ANALYSIS")
    print(f"   Total Characters: {char_stats['total_chars']:,}")
    print(f"   Characters (no spaces): {char_stats['chars_no_spaces']:,}")
    print(f"   Alphabetic: {char_stats['alphabetic_chars']:,}")
    print(f"   Numeric: {char_stats['numeric_chars']:,}")
    print(f"   Spaces: {char_stats['spaces']:,}")
    print(f"   Punctuation: {char_stats['punctuation']:,}")

    print(f"\n📏 AVERAGES")
    print(f"   Average Word Length: {analysis['avg_word_length']} characters")
    print(f"   Average Sentence Length: {analysis['avg_sentence_length']} words")
    print(f"   Estimated Reading Time: {analysis['reading_time_minutes']} minutes")

    print(f"\n🏆 TOP 10 MOST COMMON WORDS")
    for i, (word, count) in enumerate(analysis['most_common_words'], 1):
        print(f"   {i:2}. {word:<15} ({count:,} times)")


def main():
    counter = WordCounter()

    print("📝 Word Counter & Text Analyzer")
    print("=" * 40)

    while True:
        print("\nOptions:")
        print("1. Analyze text input")
        print("2. Analyze text file")
        print("3. Compare two texts")
        print("4. Create sample file")
        print("5. Exit")

        choice = input("\nSelect an option (1-5): ").strip()

        if choice == "1":
            # Analyze direct text input
            print("\nEnter your text (press Enter twice to finish):")
            lines = []
            while True:
                line = input()
                if line == "" and lines and lines[-1] == "":
                    break
                lines.append(line)

            text = "\n".join(lines[:-1])  # Remove the last empty line

            if text.strip():
                include_stop = input("\nInclude stop words in analysis? (y/N): ").lower() == 'y'
                analysis = counter.analyze_text(text, include_stop_words=include_stop)
                print_analysis_report(analysis)

                save_option = input("\nSave analysis to file? (y/N): ").lower() == 'y'
                if save_option:
                    filename = input("Enter filename (default: analysis.json): ").strip() or "analysis.json"
                    counter.save_analysis(analysis, filename)
                    print(f"✅ Analysis saved to {filename}")
            else:
                print("❌ No text entered.")

        elif choice == "2":
            # Analyze file
            file_path = input("Enter file path: ").strip()
            if file_path:
                try:
                    include_stop = input("Include stop words in analysis? (y/N): ").lower() == 'y'
                    analysis = counter.analyze_file(file_path, include_stop_words=include_stop)
                    print_analysis_report(analysis)

                    save_option = input("\nSave analysis to file? (y/N): ").lower() == 'y'
                    if save_option:
                        filename = input("Enter filename (default: analysis.json): ").strip() or "analysis.json"
                        counter.save_analysis(analysis, filename)
                        print(f"✅ Analysis saved to {filename}")

                except (FileNotFoundError, UnicodeDecodeError) as e:
                    print(f"❌ Error: {e}")

        elif choice == "3":
            # Compare two texts
            print("\nEnter first text (press Enter twice to finish):")
            lines1 = []
            while True:
                line = input()
                if line == "" and lines1 and lines1[-1] == "":
                    break
                lines1.append(line)
            text1 = "\n".join(lines1[:-1])

            print("\nEnter second text (press Enter twice to finish):")
            lines2 = []
            while True:
                line = input()
                if line == "" and lines2 and lines2[-1] == "":
                    break
                lines2.append(line)
            text2 = "\n".join(lines2[:-1])

            if text1.strip() and text2.strip():
                comparison = counter.compare_texts(text1, text2)

                print("\n" + "=" * 50)
                print("🔍 TEXT COMPARISON REPORT")
                print("=" * 50)

                print(f"\n📊 TEXT 1 STATISTICS")
                stats1 = comparison['text1_stats']
                print(f"   Words: {stats1['word_count']:,}")
                print(f"   Unique Words: {stats1['unique_words']:,}")

                print(f"\n📊 TEXT 2 STATISTICS")
                stats2 = comparison['text2_stats']
                print(f"   Words: {stats2['word_count']:,}")
                print(f"   Unique Words: {stats2['unique_words']:,}")

                print(f"\n🔗 COMPARISON")
                print(f"   Common Words: {comparison['common_words_count']:,}")
                print(f"   Similarity Ratio: {comparison['similarity_ratio']:.2%}")

                if comparison['unique_to_text1']:
                    print(f"\n📝 Words Unique to Text 1:")
                    print(f"   {', '.join(comparison['unique_to_text1'][:10])}")

                if comparison['unique_to_text2']:
                    print(f"\n📝 Words Unique to Text 2:")
                    print(f"   {', '.join(comparison['unique_to_text2'][:10])}")
            else:
                print("❌ Please enter both texts.")

        elif choice == "4":
            # Create sample file
            filename = input("Enter filename for sample (default: sample.txt): ").strip() or "sample.txt"
            created_file = counter.create_sample_file(filename)
            print(f"✅ Sample file created: {created_file}")

        elif choice == "5":
            print("👋 Goodbye!")
            break

        else:
            print("❌ Invalid option. Please try again.")


if __name__ == "__main__":
    main()