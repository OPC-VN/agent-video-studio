import builtins
from pathlib import Path

import pytest

from video_studio.contract import ContractError
from video_studio.effect_library import template

HEADINGS = template.CONTRACT_HEADINGS
TABLE = '| chỗ thay | file | số lần xuất hiện | kiểu nội dung | giới hạn |\n| --- | --- | --- | --- | --- |\n| tiêu đề | index.html | 1 | chữ | ngắn |'


def contract():
    return '\n\n'.join(f'## {i}. {h}\n' + (TABLE if i == 3 else 'Nội dung.') for i, h in enumerate(HEADINGS, 1))


def check(text):
    template.check_contract(text.encode('utf-8'), {}, ['index.html', 'assets/style.css'])


def test_exact_six_sections():
    check(contract())
    assert template.contract_headings_of(contract()) == list(HEADINGS)
    assert template.slot_files(contract()) == ['index.html']


@pytest.mark.parametrize('change', ['missing', 'empty', 'duplicate', 'order', 'extra'])
def test_missing_empty_duplicate_out_of_order(change):
    text = contract()
    if change == 'missing':
        text = text.replace('## 2. Bất biến sáng tạo', '### Bất biến sáng tạo')
    elif change == 'empty':
        text = text.replace('## 2. Bất biến sáng tạo\nNội dung.', '## 2. Bất biến sáng tạo')
    elif change == 'duplicate':
        text += '\n## 1. Nguồn gốc và quyền\nNội dung.'
    elif change == 'order':
        text = text.replace('## 2. Bất biến sáng tạo', '## 7. Bất biến sáng tạo')
    else:
        text += '\n## 7. Khác\nNội dung.'
    with pytest.raises(ContractError):
        check(text)


def test_fenced_headings_ignored():
    check(contract() + '\n```markdown\n## 7. Ngoài\n```\n')
    check(contract() + '\n~~~markdown\n## 7. Ngoài\n~~~\n')


def test_fenced_slot_table_is_not_data():
    with pytest.raises(ContractError):
        check(contract().replace(TABLE, '```\n' + TABLE + '\n```'))


def test_table_must_be_in_section_three():
    text = contract().replace(TABLE, 'Nội dung.').replace('## 4. Thời gian và khung hình', '## 4. Thời gian và khung hình\n' + TABLE)
    with pytest.raises(ContractError):
        check(text)


def test_invalid_slot_table_header():
    with pytest.raises(ContractError):
        check(contract().replace('số lần xuất hiện', 'khác'))


def test_slots_separator_not_data():
    with pytest.raises(ContractError):
        check(contract().replace('| tiêu đề | index.html | 1 | chữ | ngắn |', ''))


@pytest.mark.parametrize('count', ['0', '-1', '1.0', 'abc', ''])
def test_slot_count_positive_integer(count):
    with pytest.raises(ContractError):
        check(contract().replace('| 1 | chữ', f'| {count} | chữ'))


def test_slot_file_outside_bundle():
    with pytest.raises(ContractError):
        check(contract().replace('index.html', 'outside.html'))


def test_contract_utf8_bom_and_limit():
    template.check_contract(b'\xef\xbb\xbf' + contract().encode(), {}, ['index.html'])
    with pytest.raises(ContractError):
        template.check_contract(b'\xff', {}, ['index.html'])
    with pytest.raises(ContractError):
        template.check_contract(b'a' * (1024 * 1024 + 1), {}, ['index.html'])


def test_parser_never_opens_files(monkeypatch):
    def fail(*args, **kwargs):
        raise AssertionError('unexpected file access')
    monkeypatch.setattr(builtins, 'open', fail)
    monkeypatch.setattr(Path, 'read_bytes', fail)
    check(contract())


def test_heading_with_long_whitespace_finishes_promptly():
    import subprocess
    import sys

    code = (
        "from video_studio.effect_library.template import _sections; "
        "assert _sections('## x' + ' ' * 64000 + 'x') == "
        "[('x' + ' ' * 64000 + 'x', [])]"
    )
    subprocess.run([sys.executable, '-c', code], check=True, timeout=3)


def test_fenced_json_counts_as_section_content():
    text = contract().replace(
        '## 2. Bất biến sáng tạo\nNội dung.',
        '## 2. Bất biến sáng tạo\n```json\n{"value": 1}\n```',
    )
    check(text)
