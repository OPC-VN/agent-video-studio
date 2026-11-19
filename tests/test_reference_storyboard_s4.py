"""Pure rebuild rules; file reads and CLI exposure are deliberately separate."""
import copy
import pytest
from video_studio.reference.storyboard import validate_storyboard


def setup():
    breakdown={'shots':[{'id':'SH001','text_layers':[]}]}
    provenance={'assets':[{'path':'assets/photo.png','origin':'user','owner':'author'}]}
    library={'VE-test': {'runtime_tested':True,'reusable':True,'origin':'VE'}}
    board={'schema':'video_studio.rebuild_storyboard.v1','mode':'rebuild','breakdown_ref':'breakdown.json','inherits':['structure','rhythm'],
           'scenes':[{'id':'SN01','from_shots':['SH001'],'motion_refs':[{'id':'VE-test','runtime_tested':True}],
                      'build_route':'edit','duration_s':2.0,'assets':[{'slot':'hero','asset_id':'assets/photo.png'}],
                      'content':{'narration_text':'original narration','on_screen_text':[]},
                      'anchor':{'type':'time','ref':0,'basis':'decided'},
                      'feasibility':'buildable','gap':None,'status':'draft'}]}
    return board, breakdown, provenance, library


def check(board, breakdown, provenance, library, corpus=()):
    return validate_storyboard(board, breakdown, provenance, library, known_templates=set(), known_skills=set(), source_texts=corpus)


def test_owned_asset_and_runtime_evidence_are_accepted_but_draft_not_approved():
    args=setup(); result=check(*args)
    assert result['ok'] and result['summary']['unapproved'] == 1


def test_reference_asset_and_unknown_asset_are_rejected():
    args=setup();args[2]['assets'][0]['origin']='reference'
    assert not check(*args)['ok']
    args=setup();args[0]['scenes'][0]['assets'][0]['asset_id']='assets/missing.png'
    assert not check(*args)['ok']


def test_ambiguous_provenance_duplicate_path_is_rejected():
    args=setup();args[2]['assets'].append(dict(args[2]['assets'][0], origin='reference'))
    assert not check(*args)['ok']


def test_runtime_cannot_be_self_upgraded_or_gap_hidden():
    args=setup();args[3]['VE-test']['runtime_tested']=False
    assert not check(*args)['ok']
    args=setup();args[0]['scenes'][0]['gap']={'need':'new effect'}
    assert not check(*args)['ok']


def test_no_verbatim_transcript_and_no_reference_source_in_asset():
    args=setup();phrase='a long reference phrase should never be copied into a final video'
    args[0]['scenes'][0]['content']['narration_text']=phrase
    assert not check(*args,corpus=[phrase])['ok']
    args=setup();args[0]['scenes'][0]['assets'][0]['asset_id']='source/original.mp4'
    assert not check(*args)['ok']


def test_storyboard_malformed_types_fail_without_exception():
    args=setup();args[0]['scenes'][0]['feasibility']=[]
    assert not check(*args)['ok']
    args=setup();args[0]['scenes'][0]['anchor']['ref']=10**1000
    assert not check(*args)['ok']


def test_gap_assets_and_nested_reference_path_are_not_accepted():
    args=setup();args[0]['scenes'][0]['motion_refs'][0]['adaptation']='source/private.mp4'
    assert not check(*args)['ok']


def test_windows_alias_source_cannot_be_asset():
    args=setup();args[0]['scenes'][0]['assets'][0]['asset_id']='source./private.mp4'
    args[2]['assets'][0]['path']='source./private.mp4'
    assert not check(*args)['ok']


def test_missing_breakdown_duration_anchor_and_message_overlap_fail():
    args=setup();args[0]['breakdown_ref']='missing.json';assert not check(*args)['ok']
    args=setup();args[0]['scenes'][0]['duration_s']=None;assert not check(*args)['ok']
    args=setup();args[0]['scenes'][0]['anchor']={'type':'cue','ref':'unknown#3'};assert not check(*args)['ok']
    args=setup();phrase='reference text longer than forty characters cannot be copied'
    args[0]['scenes'][0]['content']['message']=phrase
    assert not check(*args,corpus=[phrase])['ok']


def test_bad_provenance_origin_type_is_a_finding():
    args=setup();args[2]['assets'][0]['origin']=[]
    assert not check(*args)['ok']


def test_unused_reference_asset_does_not_invalidate_own_assets():
    args=setup(); args[2]['assets'].append({'path':'source/reference.mp4','origin':'reference','owner':'author'})
    assert check(*args)['ok']


def test_gap_details_are_reported_and_missing_fields_rejected():
    args=setup(); scene=args[0]['scenes'][0];scene['feasibility']='needs_new_component'
    scene['gap']={'need':'new transition','why_no_library_match':'not available'}
    result=check(*args)
    assert result['ok'] and result['summary']['gaps'] == [{'scene':'SN01','need':'new transition'}]
    scene['gap']={'need':'new transition'}
    assert not check(*args)['ok']


def test_missing_source_text_corpus_is_explicitly_unchecked():
    board, breakdown, provenance, library=setup()
    result=validate_storyboard(board, breakdown, provenance, library, known_templates=set(), known_skills=set())
    assert 'source_texts' in result['summary']['unchecked']


@pytest.mark.parametrize('anchor', [None, [], 'bad'])
def test_invalid_anchor_is_finding_not_exception(anchor):
    args=setup();args[0]['scenes'][0]['anchor']=anchor
    assert not check(*args)['ok']


@pytest.mark.parametrize('path', ['./source/ref.mp4','other/../source/ref.mp4','C:/private/file','/home/private'])
def test_hidden_source_paths_are_rejected(path):
    args=setup();args[0]['scenes'][0]['motion_refs'][0]['adaptation']=path
    assert not check(*args)['ok']


def test_component_gap_requires_details():
    args=setup();args[0]['scenes'][0]['feasibility']='needs_new_component';args[0]['scenes'][0]['gap']=None
    assert not check(*args)['ok']


def test_unicode_normalization_detects_verbatim():
    import unicodedata
    phrase='Một nội dung tiếng Việt rất dài không được sao chép nguyên văn từ video mẫu'
    args=setup();args[0]['scenes'][0]['content']['narration_text']=unicodedata.normalize('NFD', phrase)
    assert not check(*args,corpus=[unicodedata.normalize('NFC', phrase)])['ok']


def test_missing_source_corpus_cannot_report_fully_valid():
    board, breakdown, provenance, library=setup()
    result=validate_storyboard(board, breakdown, provenance, library, known_templates=set(), known_skills=set())
    assert not result['ok'] and 'source_texts' in result['summary']['unchecked']


def test_gap_text_can_contain_ratio():
    args=setup();scene=args[0]['scenes'][0];scene['feasibility']='needs_new_component'
    scene['gap']={'need':'Hiệu ứng 16:9','why_no_library_match':'Chưa có trong thư viện'}
    assert check(*args)['ok']


def test_rendered_candidate_not_automatically_buildable():
    args=setup();args[3]['VE-test']['reusable']=False
    assert not check(*args)['ok']


def test_library_index_uses_render_and_reuse_evidence_independently():
    from video_studio.reference.storyboard import library_index
    index = library_index()
    candidate = index['VE-gsap-core-draw']
    assert candidate['runtime_tested'] is True and candidate['reusable'] is False
    assert all(not value['reusable'] for key, value in index.items() if key.startswith('PM-'))
