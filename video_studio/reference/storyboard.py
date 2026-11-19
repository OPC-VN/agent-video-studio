"""Pure rebuild storyboard checks; callers supply validated authoritative inputs.

This is not the public reference CLI and performs no filesystem I/O.
"""
import math
import re
import unicodedata
from pathlib import PurePosixPath

SCHEMA = 'video_studio.rebuild_storyboard.v1'
INHERIT_ALLOWED = frozenset(('structure', 'rhythm', 'motion_style', 'layout'))
INHERIT_REQUIRED = frozenset(('structure', 'rhythm'))
FEASIBILITY = frozenset(('buildable', 'needs_user_media', 'needs_new_component', 'unsupported'))
_ALLOWED_ORIGINS = frozenset(('user', 'generated', 'template'))
_PATH_COMPONENT = re.compile(r'[^\x00-\x1f\x7f]+\Z')


def _asset_path(value, *, allow_protected=False):
    if not isinstance(value, str) or not value or len(value) > 512 or '\\' in value or value.startswith('/'):
        return None
    parts = value.split('/')
    if any(part in ('', '.', '..') or part.endswith((' ', '.')) or not _PATH_COMPONENT.fullmatch(part) or ':' in part for part in parts):
        return None
    if not allow_protected and parts[0].casefold() in ('source', 'evidence', 'transcripts'):
        return None
    return '/'.join(PurePosixPath(value).parts)


def _text(value):
    return unicodedata.normalize('NFC', re.sub(r'\s+', ' ', value)).casefold()


def _grams(corpus, minimum=40):
    result = set()
    for source in corpus:
        value = _text(source)
        result.update(value[i:i + minimum] for i in range(max(0, len(value) - minimum + 1)))
    return result


def _overlaps(text, grams, minimum=40):
    value = _text(text)
    return any(value[i:i + minimum] in grams for i in range(max(0, len(value) - minimum + 1)))


def validate_storyboard(board, breakdown, provenance, library, *, known_templates, known_skills, source_texts=None):
    """Return findings; the caller must validate provenance, evidence and reads separately."""
    findings = []
    def fail(path, message):
        findings.append({'path': path, 'problem': message})
    if not all(isinstance(value, dict) for value in (board, breakdown, provenance, library)):
        return {'ok': False, 'findings': [{'path': '$', 'problem': 'đầu vào phải là object'}], 'summary': {}}
    if board.get('schema') != SCHEMA or board.get('mode') != 'rebuild':
        fail('$', 'schema hoặc mode không hợp lệ')
    if board.get('breakdown_ref') != 'breakdown.json':
        fail('breakdown_ref', 'tham chiếu breakdown không hợp lệ')
    inherit = board.get('inherits')
    if (not isinstance(inherit, list) or any(not isinstance(x, str) for x in inherit)
            or len(inherit) != len(set(inherit)) or not INHERIT_REQUIRED.issubset(inherit)
            or not set(inherit).issubset(INHERIT_ALLOWED)):
        fail('inherits', 'chỉ được kế thừa cấu trúc, nhịp, kiểu chuyển động và bố cục')
    refs = breakdown.get('shots')
    if not isinstance(refs, list) or len(refs) > 40 or any(not isinstance(s, dict) or not isinstance(s.get('id'), str) for s in refs):
        return {'ok': False, 'findings': findings + [{'path': 'breakdown', 'problem': 'cảnh nguồn không hợp lệ'}], 'summary': {}}
    valid_shots = {shot['id'] for shot in refs}
    if len(valid_shots) != len(refs):
        fail('breakdown', 'ID cảnh nguồn trùng')
    raw_assets = provenance.get('assets', [])
    assets = {}
    if not isinstance(raw_assets, list) or len(raw_assets) > 1000:
        return {'ok': False, 'findings': findings + [{'path': 'assets', 'problem': 'hồ sơ tài sản không hợp lệ'}], 'summary': {}}
    for item in raw_assets:
        path = _asset_path(item.get('path'), allow_protected=True) if isinstance(item, dict) else None
        if path is None:
            fail('assets', 'đường tài sản trong hồ sơ không hợp lệ')
            continue
        key = path.casefold()
        if key in assets:
            fail('assets', 'đường tài sản trùng hoặc mơ hồ')
        else:
            assets[key] = item
    unchecked = ['source_texts'] if source_texts is None else []
    if source_texts is None:
        fail('source_texts', 'chưa kiểm trùng chữ với nguồn')
    source_texts = () if source_texts is None else source_texts
    if (not isinstance(source_texts, (list, tuple)) or len(source_texts) > 10000 or
            any(not isinstance(text, str) or len(text) > 100000 for text in source_texts) or
            sum(map(len, source_texts)) > 200000):
        return {'ok': False, 'findings': findings + [{'path': 'source_texts', 'problem': 'nguồn chữ không hợp lệ'}], 'summary': {}}
    corpus_grams = _grams(source_texts)
    scenes = board.get('scenes')
    if not isinstance(scenes, list) or not 1 <= len(scenes) <= 40:
        return {'ok': False, 'findings': findings + [{'path': 'scenes', 'problem': 'cần 1 đến 40 cảnh'}], 'summary': {}}
    counts = {name: 0 for name in FEASIBILITY}
    unapproved = 0
    gaps = []
    text_total = 0
    seen_ids = set()
    for index, scene in enumerate(scenes):
        path = f'scenes[{index}]'
        if not isinstance(scene, dict):
            fail(path, 'cảnh phải là object')
            continue
        scene_id = scene.get('id')
        if not isinstance(scene_id, str) or not re.fullmatch(r'SN[0-9]{2,3}', scene_id) or scene_id in seen_ids:
            fail(path, 'ID cảnh không hợp lệ hoặc trùng')
        else:
            seen_ids.add(scene_id)
        from_shots = scene.get('from_shots')
        if not isinstance(from_shots, list) or not from_shots or any(not isinstance(x, str) or x not in valid_shots for x in from_shots):
            fail(path, 'tham chiếu cảnh nguồn không hợp lệ')
        value = scene.get('duration_s')
        try:
            duration_ok = (not isinstance(value, bool) and isinstance(value, (int, float)) and
                           math.isfinite(value) and 0 < value <= 3600)
        except OverflowError:
            duration_ok = False
        if not duration_ok:
            fail(path, 'thời lượng cảnh không hợp lệ')
        feasibility = scene.get('feasibility')
        if not isinstance(feasibility, str) or feasibility not in FEASIBILITY:
            fail(path, 'mức khả thi không hợp lệ')
        else:
            counts[feasibility] += 1
        gap = scene.get('gap')
        if feasibility == 'needs_new_component' and gap is None:
            fail(path, 'cảnh cần component mới phải nêu gap')
        if gap is not None:
            if feasibility in ('buildable', 'needs_user_media'):
                fail(path, 'không được che khoảng trống thư viện')
            if (not isinstance(gap, dict) or any(not isinstance(gap.get(k), str) or not gap[k].strip() or len(gap[k]) > 500 for k in ('need', 'why_no_library_match'))):
                fail(path, 'gap cần need và why_no_library_match')
            elif any(any(ord(c) < 32 or c in '/\\' for c in gap[k]) for k in ('need', 'why_no_library_match')):
                fail(path, 'gap chứa đường dẫn hoặc ký tự điều khiển')
            else:
                safe_scene = scene_id if isinstance(scene_id, str) and re.fullmatch(r'SN[0-9]{2,3}', scene_id) else 'unknown'
                gaps.append({'scene': safe_scene, 'need': gap['need']})
        motion = scene.get('motion_refs')
        if not isinstance(motion, list) or len(motion) > 100:
            fail(path, 'motion_refs không hợp lệ')
            motion = []
        for ref in motion:
            identifier = ref.get('id') if isinstance(ref, dict) else None
            expected = library.get(identifier) if isinstance(identifier, str) else None
            if not isinstance(expected, dict) or type(expected.get('runtime_tested')) is not bool:
                fail(path, 'ID chuyển động không có trong thư viện')
                continue
            if type(ref.get('runtime_tested')) is not bool or ref['runtime_tested'] != expected['runtime_tested']:
                fail(path, 'runtime_tested không khớp thư viện')
            if feasibility == 'buildable' and (not expected['runtime_tested'] or expected.get('reusable') is not True):
                fail(path, 'cảnh buildable có chuyển động chưa chứng minh tái sử dụng')
        route = scene.get('build_route')
        if not isinstance(route, str) or not (route == 'edit' or
                (route.startswith('render:') and route[7:] in known_templates) or
                (route.startswith('hyperframes:') and known_skills is not None and route[12:] in known_skills)):
            fail(path, 'đường dựng không hợp lệ hoặc chưa kiểm được')
        scene_assets = scene.get('assets')
        if not isinstance(scene_assets, list) or len(scene_assets) > 100:
            fail(path, 'assets không hợp lệ')
            scene_assets = []
        for asset in scene_assets:
            asset_id = _asset_path(asset.get('asset_id')) if isinstance(asset, dict) else None
            entry = assets.get(asset_id.casefold()) if asset_id is not None else None
            if not entry or not isinstance(entry.get('origin'), str) or entry.get('origin') not in _ALLOWED_ORIGINS:
                fail(path, 'tài sản không có quyền dựng trong hồ sơ')
        content = scene.get('content')
        if not isinstance(content, dict) or not isinstance(content.get('on_screen_text'), list):
            fail(path, 'content không hợp lệ')
        else:
            texts = [content.get('narration_text'), content.get('message', ''), *content['on_screen_text']]
            if len(texts) > 100 or any(not isinstance(text, str) or len(text) > 20000 for text in texts):
                fail(path, 'chữ nội dung không hợp lệ')
            else:
                text_total += sum(map(len, texts))
                if text_total > 100000:
                    fail(path, 'tổng chữ nội dung vượt trần')
                elif any(_overlaps(text, corpus_grams) for text in texts):
                    fail(path, 'nội dung trùng lời hoặc chữ của mẫu')
        anchor = scene.get('anchor')
        if not isinstance(anchor, dict) or anchor.get('type') not in ('word', 'cue', 'time'):
            fail(path, 'anchor không hợp lệ')
        elif anchor['type'] == 'time':
            value = anchor.get('ref')
            try:
                valid = (not isinstance(value, bool) and isinstance(value, (int, float)) and
                         math.isfinite(value) and value >= 0 and anchor.get('basis') in ('measured', 'decided'))
            except OverflowError:
                valid = False
            if not valid:
                fail(path, 'anchor thời gian cần giá trị và cơ sở hợp lệ')
        elif anchor['type'] in ('word', 'cue'):
            fail(path, 'anchor lời chưa được đối chiếu với transcript')
        def references_protected(value, depth=0):
            if depth > 30:
                return True
            if isinstance(value, str):
                normalized = value.replace('\\', '/').casefold()
                if normalized.startswith('/') or re.match(r'^[a-z]:', normalized):
                    return True
                parts = normalized.split('/')
                if '..' in parts:
                    return True
                return any(part.rstrip(' .') in ('source', 'evidence', 'transcripts') for part in parts[:-1])
            if isinstance(value, list):
                return len(value) > 1000 or any(references_protected(item, depth + 1) for item in value)
            if isinstance(value, dict):
                return len(value) > 1000 or any(references_protected(item, depth + 1) for item in value.values())
            return False
        if any(references_protected(value) for key, value in scene.items() if key not in ('content', 'evidence')):
            fail(path, 'cảnh chứa đường đến tư liệu mẫu')
        if scene.get('status') not in ('draft', 'approved'):
            fail(path, 'status không hợp lệ')
        if scene.get('status') != 'approved':
            unapproved += 1
    return {'ok': not findings, 'findings': findings,
            'summary': {'by_feasibility': counts, 'unapproved': unapproved, 'gaps': gaps, 'unchecked': unchecked}}


def library_index():
    """Load authoritative bundled or checkout catalogs through anchored bounded reads."""
    from ..effect_library.catalog import validate_entry
    from ..effect_library.resources import resource_root
    from ..contract import ContractError
    from ._scan import read_json_strict

    root = resource_root()
    entries = read_json_strict(root / 'skills/video-theme-library/assets/effect-library/entries.json')
    prompt = read_json_strict(root / 'skills/video-theme-library/assets/prompt-motion/index.json')
    if not isinstance(entries, list) or len(entries) > 10000 or not isinstance(prompt, dict):
        raise ContractError('catalog không hợp lệ')
    prompts = prompt.get('entries')
    if not isinstance(prompts, list) or len(prompts) > 10000:
        raise ContractError('prompt motion index không hợp lệ')
    result = {}
    for item in entries:
        validate_entry(item)
        identifier = item['id']
        if identifier in result:
            raise ContractError('catalog có ID trùng')
        result[identifier] = {'origin': 'VE', 'runtime_tested': item['checks']['render'] == 'pass',
                              'reusable': item['maturity'] == 'verified' and item['checks']['reuse_evidence'] == 'pass'}
    for item in prompts:
        if not isinstance(item, dict) or not isinstance(item.get('id'), str):
            raise ContractError('prompt motion entry không hợp lệ')
        identifier = item['id']
        verified = item.get('verified')
        if (not re.fullmatch(r'PM-[a-z0-9]+(?:-[a-z0-9]+)*', identifier) or identifier in result or
                not isinstance(verified, dict) or type(verified.get('hyperframes_runtime_tested')) is not bool):
            raise ContractError('prompt motion ID hoặc trạng thái không hợp lệ')
        result[identifier] = {'origin': 'PM', 'runtime_tested': verified['hyperframes_runtime_tested'],
                              'reusable': False}
    return result
