"""Script to generate markdown files and llms.txt from HTML documentation."""

import logging
import os
from pathlib import Path

from .utils import concatenate_markdown_files, convert_html_to_markdown

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_documentation(  # noqa: PLR0913
    docs_dir: str = "site",
    generate_md_files: bool | None = None,
    generate_llms_txt: bool | None = None,
    generate_llms_full_txt: bool | None = None,
    llms_txt_name: str = "llms.txt",
    llms_full_txt_name: str = "llms_full.txt",  # noqa: ARG001
) -> list[str]:
    """Generate markdown and llms.txt files from HTML documentation.

    Args:
    ----
        docs_dir: Directory containing HTML documentation
        generate_md_files: Whether to keep generated markdown files
        generate_llms_txt: Whether to generate llms.txt
        generate_llms_full_txt: Whether to generate full llms.txt
        llms_txt_name: Name of the llms.txt file
        llms_full_txt_name: Name of the full llms.txt file

    Returns:
    -------
        List of generated markdown file paths

    """
    docs_dir = docs_dir.lstrip("/")
    logger.info("Starting Generation....")

    logger.info("Generating MD files....")
    markdown_files = convert_html_to_markdown(docs_dir)

    # Set defaults if None
    generate_md_files = True if generate_md_files is None else generate_md_files
    generate_llms_txt = True if generate_llms_txt is None else generate_llms_txt
    generate_llms_full_txt = True if generate_llms_full_txt is None else generate_llms_full_txt  # noqa: E501

    if generate_llms_txt:
        logger.info("Generating LLMS.txt file....")
        concatenate_markdown_files(
            markdown_files,
            f"{docs_dir}/{llms_txt_name}",
        )
        logger.info("LLMS.txt file generated at %s", f"{docs_dir}/{llms_txt_name}")

    if not generate_md_files:
        logger.info("Deleting MD files....")
        for file in markdown_files:
            Path(file).unlink()
        logger.info("MD files deleted.")

    logger.info("Generation completed.")
    return markdown_files


def main():
    """CLI entry point."""
    docs_dir = os.environ.get("INPUT_DOCS_DIR", "site")
    md_files_env = os.environ.get("INPUT_GENERATE_MD_FILES", "true")
    generate_md_files = md_files_env.lower() == "true"
    generate_llms_txt = (
        os.environ.get("INPUT_GENERATE_LLMS_TXT", "true").lower() == "true"
    )
    generate_llms_full_txt = (
        os.environ.get("INPUT_GENERATE_LLMS_FULL_TXT", "true").lower() == "true"
    )
    llms_txt_name = os.environ.get("INPUT_LLMS_TXT_NAME", "llms.txt")
    llms_full_txt_name = os.environ.get("INPUT_LLMS_FULL_TXT_NAME", "llms_full.txt")

    generate_documentation(
        docs_dir=docs_dir,
        generate_md_files=generate_md_files,
        generate_llms_txt=generate_llms_txt,
        generate_llms_full_txt=generate_llms_full_txt,
        llms_txt_name=llms_txt_name,
        llms_full_txt_name=llms_full_txt_name,
    )


if __name__ == "__main__":
    main()
