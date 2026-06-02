from __future__ import annotations

import re
import zipfile
from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree

from media_downloader.models import ParsedInput


URL_PATTERN = re.compile(r"https?://[^\s\"'<>]+", re.IGNORECASE)
DOCX_NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}
REL_NS = {"rel": "http://schemas.openxmlformats.org/package/2006/relationships"}


def extract_urls_from_text(text: str) -> list[str]:
    seen: set[str] = set()
    urls: list[str] = []
    for match in URL_PATTERN.findall(text):
        url = match.strip().rstrip(").,;]")
        if url and url not in seen:
            seen.add(url)
            urls.append(url)
    return urls


def parse_text_input(text: str) -> ParsedInput:
    return ParsedInput(urls=extract_urls_from_text(text), source_label="Texto pegado")


def parse_txt_file(file_path: Path) -> ParsedInput:
    text = file_path.read_text(encoding="utf-8", errors="ignore")
    return ParsedInput(urls=extract_urls_from_text(text), source_label=file_path.name)


def parse_docx_file(file_path: Path) -> ParsedInput:
    with zipfile.ZipFile(file_path) as archive:
        document_xml = archive.read("word/document.xml")
        document_rels_xml = archive.read("word/_rels/document.xml.rels") if "word/_rels/document.xml.rels" in archive.namelist() else None

    root = ElementTree.fromstring(document_xml)
    text_fragments = [node.text or "" for node in root.findall(".//w:t", DOCX_NS)]
    combined_text = "\n".join(text_fragments)

    urls = extract_urls_from_text(combined_text)
    if document_rels_xml:
        rel_root = ElementTree.fromstring(document_rels_xml)
        for relation in rel_root.findall(".//rel:Relationship", REL_NS):
            target = relation.attrib.get("Target", "")
            target_mode = relation.attrib.get("TargetMode", "")
            if target_mode.lower() == "external" and target.startswith(("http://", "https://")):
                if target not in urls:
                    urls.append(target)

    return ParsedInput(urls=urls, source_label=file_path.name)


def parse_uploaded_file(file_name: str, file_bytes: bytes, temp_path: Path) -> ParsedInput:
    temp_path.write_bytes(file_bytes)
    suffix = file_name.lower().rsplit(".", 1)[-1] if "." in file_name else ""
    if suffix == "txt":
        return parse_txt_file(temp_path)
    if suffix == "docx":
        return parse_docx_file(temp_path)
    return ParsedInput(urls=[], source_label=file_name)
