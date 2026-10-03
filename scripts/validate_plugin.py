"""Validate the public connector package, not the private service or user data."""
import json
import pathlib
import re
import urllib.request
import xml.etree.ElementTree as ET

import yaml
from jsonschema import Draft202012Validator

ROOT = pathlib.Path(__file__).resolve().parents[1]


def document(name):
    return json.loads((ROOT / name).read_text())


def validate_standard(name, schema_url):
    with urllib.request.urlopen(schema_url, timeout=20) as response:
        schema = json.load(response)
    Draft202012Validator.check_schema(schema)
    value = document(name)
    Draft202012Validator(schema).validate(value)
    return value


plugin = validate_standard('plugin.json', 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json')
mcp = validate_standard('mcp.json', 'https://agent-plugins.org/schemas/1.0.0/mcp.schema.json')
cursor = document('.cursor-plugin/plugin.json')
assert {key: value for key, value in cursor.items() if key != 'logo'} == {
    key: value for key, value in plugin.items() if key != '$schema'
}, 'Portable and Cursor manifests must describe the same release'
assert plugin['name'] == 'blindless'
assert re.fullmatch(r'\d+\.\d+\.\d+', plugin['version']), 'Use a release version'
assert plugin['repository'] == 'https://github.com/FastFix-SF/blindless-plugin'
assert plugin['license'] == 'MIT' and (ROOT / 'LICENSE').is_file()
assert mcp['mcpServers'] == {
    'blindless': {'type': 'streamable-http', 'url': 'https://blindless.ai/api/mcp'}
}, 'The connector uses owner authorization, with no bundled credential or command'

logo = (ROOT / cursor['logo']).resolve()
assert logo.is_relative_to(ROOT) and logo.is_file(), 'Logo must stay inside the public package'
svg = ET.parse(logo).getroot()
box = [float(number) for number in svg.attrib['viewBox'].split()]
assert box[2] == box[3] and box[2] > 0, 'Marketplace logo must be square'
assert any(element.tag.endswith('rect') and element.attrib.get('fill') for element in svg), 'Logo needs a background plate'

skills = list((ROOT / 'skills').glob('*/SKILL.md'))
assert skills, 'The reporting skill must be included'
for skill in skills:
    text = skill.read_text()
    sections = text.split('---', 2)
    assert len(sections) == 3 and not sections[0].strip(), 'Skill needs YAML frontmatter'
    frontmatter = yaml.safe_load(sections[1])
    assert frontmatter['name'] == skill.parent.name
    assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', frontmatter['name'])
    assert isinstance(frontmatter['description'], str) and 0 < len(frontmatter['description']) <= 1024
    assert sections[2].strip(), 'Skill must include its operating instructions'
assert (ROOT / 'README.md').is_file()
print(f"Blindless {plugin['version']}: official manifest/MCP schemas, release consistency, logo, and skills verified")
