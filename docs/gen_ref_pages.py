"""Generate the code reference pages and navigation."""

import logging
from pathlib import Path

import mkdocs_gen_files

from camply.config import FileConfig
from camply.containers.search_model import YamlSearchFile

logger = logging.getLogger(__name__)

project_dir = Path(__file__).resolve().parent.parent
source_code = project_dir.joinpath("camply")
nav = mkdocs_gen_files.Nav()

for path in sorted(source_code.rglob("*.py")):
    module_path = path.relative_to(project_dir).with_suffix("")
    doc_path = path.relative_to(source_code).with_suffix(".md")
    full_doc_path = Path("reference", doc_path)

    parts = tuple(module_path.parts)
    if parts[-1] == "__init__":
        parts = parts[:-1]
        doc_path = doc_path.with_name("index.md")
        full_doc_path = full_doc_path.with_name("index.md")
    elif parts[-1] == "__main__":
        continue

    nav[parts] = doc_path.as_posix()

    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        ident = ".".join(parts)
        fd.write(f"::: {ident}")

    mkdocs_gen_files.set_edit_path(full_doc_path, path)

with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())

schema_file = FileConfig.ROOT_DIRECTORY.joinpath("docs/yaml_search.json")
schema_file.write_text(YamlSearchFile.schema_json(indent=2))
