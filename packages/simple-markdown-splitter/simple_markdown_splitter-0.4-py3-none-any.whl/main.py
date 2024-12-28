from os import linesep

from simplemarkdownsplitter.split import split


def main() -> None:
    max_length = 2000
    markdown = read_file()
    chunks = split(markdown, max_length=max_length)
    chunk_lengths = [len(chunk) for chunk in chunks]
    print(linesep.join(chunks).strip())
    print(chunk_lengths)


def read_file() -> str:
    with open("other_example.md", "r") as file:
        return file.read()


if __name__ == "__main__":
    main()
