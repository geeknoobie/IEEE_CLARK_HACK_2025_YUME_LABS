def split_text_file(input_file, output_prefix="output_part", chunk_size=200000):
    """
    Splits a text file into multiple files, each containing a specified number of characters.

    Args:
        input_file (str): The path to the input text file.
        output_prefix (str): The prefix for the output file names.
        chunk_size (int): The number of characters to include in each output file.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            text = infile.read()

        num_chunks = (len(text) + chunk_size - 1) // chunk_size  # Calculate number of output files

        for i in range(num_chunks):
            start = i * chunk_size
            end = min((i + 1) * chunk_size, len(text))  # Ensure not to exceed the text length
            chunk = text[start:end]

            output_file = f"{output_prefix}_{i + 1}.txt"  # Create output file name

            with open(output_file, 'w', encoding='utf-8') as outfile:
                outfile.write(chunk)

        print(f"File '{input_file}' split into {num_chunks} parts.")

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
input_file_path = "/Users/debabratapanda/PycharmProjects/IEEE_CLARK_HACK_2025_YUME_LABS/output.txt" # replace with your input file path.
split_text_file(input_file_path)