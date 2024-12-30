"""
Command-line interface for the languagetools project.

INSTALLATION AND USAGE NOTES:
-----------------------------
1. This CLI provides access to functionalities of:
   - ai       (upload, cloud, chat, summarize, etc.)
   - audio    (transcription)
   - files    (read, search, edit, map)
   - vision   (OCR, query about images)
   - docs     (search over docstrings)
   - document (convert HTML to PDF)

2. Example usage:
   > lt ai upload my_image.png
   > lt audio transcribe my_audio.mp3
   > lt files read /path/to/file_or_directory --extensions .md,.py
   > lt files search "some_function_name" /path/to/codebase --height 5
   > lt files edit /path/to/file.py "original_text" "replacement_text"
   > lt docs search "search phrase"
   > lt document convert file.html file.pdf
"""

import json
from typer import Argument, echo, Exit, Typer, Option
from pathlib import Path
from typing import Optional, List

from .computer import Computer

computer = Computer()

app = Typer(help="Command-line tool to interact with the languagetools suite.")

# AI Commands (`lt ai [...]`)
ai_app = Typer(help="AI functionalities (upload, cloud, chat, summarize, etc.).")
app.add_typer(ai_app, name="ai")

@ai_app.command("upload", help="Upload a local file to the AI's server.")
def upload(file_path: Path = Argument(..., exists=True)):
    """
    Example usage:
       lt ai upload my_image.png
       lt ai upload stories.pdf
    """
    try:
        url = computer.ai.upload(str(file_path))
        echo(f"File uploaded successfully. URL: {url}")
    except Exception as e:
        echo(f"Error uploading file: {e}")
        raise Exit(code=1)


@ai_app.command("cloud", help="Use a Cloud tool with your input (e.g. replicate).")
def cloud(
    tool: str = Argument(...),
    input_args: List[str] = Argument(None),
):
    """
    Example usage:
      lt ai cloud upscale -- '{ "image": "https://..." }'
      (use '--' to separate your shell arguments from Typer's parsing)
    """
    joined_input = " ".join(input_args) if input_args else ""
    try:
        # Attempt JSON parse; fall back to raw string if that fails
        try:
            parsed = json.loads(joined_input)
        except json.JSONDecodeError:
            parsed = joined_input

        output = computer.ai.cloud(tool, parsed)
        echo(output)
    except Exception as e:
        echo(f"Error running cloud tool: {e}")
        raise Exit(code=1)


@ai_app.command("summarize", help="Summarize a piece of text.")
def summarize(text: str = Argument(str)):
    """
    Example usage:
      lt ai summarize "This is a long text that I want to summarize..."
    """
    if not text:
        echo("Please provide some text to summarize.")
        raise Exit(code=1)
    try:
        summary = computer.ai.summarize(text)
        echo("Summary: " + summary)
    except Exception as e:
        echo(f"Error during summarization: {e}")
        raise Exit(code=1)

# AUDIO Commands (`lt audio [...]`)
audio_app = Typer(help="Audio transcription.")
app.add_typer(audio_app, name="audio")


@audio_app.command("transcribe", help="Transcribe an audio file locally using Whisper.")
def transcribe(audio_path: Path = Argument(..., exists=True)):
    """
    Example usage:
       lt audio transcribe my_audio.mp3
    """
    try:
        output = computer.audio.transcribe(str(audio_path))
        echo("Transcription Output:\n"+output)
    except Exception as e:
        echo(f"Error transcribing audio: {e}")
        raise Exit(code=1)


# Files (`lt files [...]`)
files_app = Typer(help="File operations (read, search, edit, map).")
app.add_typer(files_app, name="files")


@files_app.command("read", help="Read a file or directory of text-based files.")
def read(
    path: Path = Argument(..., exists=True),
    extensions: Optional[str] = Option(None, "--extensions", help="Comma-separated list of file extensions, e.g. '.py,.txt,.md'.")
):
    """
    Reads and prints file content if PATH is a file.
    If PATH is a directory, reads all matching files (e.g. .py or .txt) under it.

    Example usage:
      lt files read /path/to/file_or_directory --extensions .md,.py
    """
    exts = tuple(ext.strip() for ext in extensions.split(",")) if extensions else None
    try:
        output = computer.files.read(str(path), exts)
        if isinstance(output, list):
            for item in output:
                echo(f"\n=== {item['path']} ===")
                echo(item["text"])
        else:
            echo(output)
    except Exception as e:
        echo(f"Error reading file(s): {e}")
        raise Exit(code=1)


@files_app.command("search", help="Search for a query within a file or directory.")
def search(
    query: str = Argument(...),
    path: Path = Argument(".", exists=True),
    height: int = Option(3, "--height", help="Number of lines of context before/after match."),
):
    """
    Search for QUERY in PATH. If PATH is a directory, recursively search all files.

    Example usage:
      lt files search "def my_function" /path/to/codebase --height 5
    """
    try:
        matches = computer.files.search(query, path=str(path), height=height)
        for match in matches:
            echo(f"File: {match['path']} (Line {match['line_number']})")
            echo(match["context"])
            echo("---------------------------")
    except Exception as e:
        echo(f"Error searching: {e}")
        raise Exit(code=1)


@files_app.command("edit", help="Edit a file by replacing ORIGINAL_TEXT with REPLACEMENT_TEXT.")
def edit(
    path: Path = Argument(..., exists=True),
    original_text: str = Argument(...),
    replacement_text: str = Argument(...),
    force: bool = Option(False, "--force", help="Skip AI-based review and force the replacement."),
):
    """
    Replaces ORIGINAL_TEXT with REPLACEMENT_TEXT within a file.
    By default, attempts an AI-based safety check for syntax/placement issues.

    Example usage:
      lt files edit /path/to/file.py "old_code()" "new_code()"
      lt files edit /path/to/file.py "class A:" "class B:" --force
    """
    try:
        computer.files.edit(str(path), original_text, replacement_text, force)
        echo(f"Successfully edited {path}.")
    except Exception as e:
        echo(f"Error editing file: {e}")
        raise Exit(code=1)


@files_app.command("map", help="Generate a hierarchical map of a directory, optionally listing classes/functions.")
def map_command(
    path: Path = Argument(".", exists=True),
    extensions: Optional[str] = Option(None, "--extensions", help="Comma-separated list of file extensions to include, e.g. '.py'. Defaults to .py if not specified."),
    codebase: bool = Option(False, "--codebase", help="If set, attempts to list classes/functions."),
):
    """
    Generate a 'tree' view of the specified directory. If --codebase is specified,
    attempts to list classes and function definitions in .py files.

    Example usage:
      lt files map /path/to/project --extensions .py,.md --codebase
    """
    exts = tuple(ext.strip() for ext in extensions.split(",")) if extensions else None
    try:
        tree_output = computer.files.map(path=str(path), extensions=exts, codebase=codebase)
        echo(tree_output)
    except Exception as e:
        echo(f"Error generating map: {e}")
        raise Exit(code=1)

# Vision (`lt vision [...]`)
vision_app = Typer(help="Vision tasks (OCR, queries).")
app.add_typer(vision_app, name="vision")

@vision_app.command("ocr", help="Extract text (OCR) from an image.")
def ocr(image_path: Path = Argument(..., exists=True)):
    """
    Extract text from an image using OCR.

    Example usage:
       lt vision ocr my_image.png
    """
    try:
        text = computer.vision.ocr(path=str(image_path))
        echo("Extracted text:\n"+text)
    except Exception as e:
        echo(f"Error performing OCR: {e}")
        raise Exit(code=1)


@vision_app.command("query", help="Ask a question about an image (Moondream local model).")
def query(
    image_path: Path = Argument(..., exists=True),
    question: str = Argument(None),
):
    """
    Example usage:
       lt vision query my_image.png "What is shown in this picture?"
    """
    if not question:
        echo("Please provide a question for the image query.")
        raise Exit(code=1)

    try:
        answer = computer.vision.query(query=question, path=str(image_path))
        echo(f"Answer:\n{answer}")
    except Exception as e:
        echo(f"Error querying image: {e}")
        raise Exit(code=1)

# Docs (`lt docs [...]`)
docs_app = Typer(help="Search docstrings or documentation in your code.")
app.add_typer(docs_app, name="docs")


@docs_app.command("search", help="Search docstrings in the current codebase or paths.")
def docs_search(
    query: str = Argument(...),
    module: Optional[str] = Option(None, "--module", help="Specify a Python module to search within."),
    paths: Optional[str] = Option(None, "--paths", help="Comma-separated list of file paths to search in, e.g. 'file1.py,file2.py'."),
):
    """
    Search docstrings or inline docs for QUERY.
    If --paths is specified, only those files are searched.
    Otherwise, the entire module or folder is searched.

    Example usage:
      lt docs search "Initialize the database"
      lt docs search "API usage" --paths file1.py,file2.py
    """
    parsed_paths = [p.strip() for p in paths.split(",")] if paths else None

    try:
        results = computer.docs.search(query, module=module, paths=parsed_paths)
        echo(results)
    except Exception as e:
        echo(f"Error searching docs: {e}")
        raise Exit(code=1)

# Document (`lt document [...]`)
document_app = Typer(help="Document generation or conversion (e.g., HTML to PDF).")
app.add_typer(document_app, name="document")


@document_app.command("convert", help="Convert an HTML file to a PDF.")
def convert_html_to_pdf(
    input_html_file: Path = Argument(..., exists=True),
    output_pdf_file: str = Argument(...),
):
    """
    Convert an HTML file to a PDF.

    Example usage:
      lt document convert file.html file.pdf
    """
    try:
        computer.document.html_to_pdf(str(input_html_file), str(output_pdf_file))
    except Exception as e:
        echo(f"Error converting HTML to PDF: {e}")
        raise Exit(code=1)

def main():
    app()

if __name__ == "__main__":
    main()