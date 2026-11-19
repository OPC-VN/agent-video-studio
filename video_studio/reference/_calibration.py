"""One-to-one scene-cut evaluation, independent of media and reference text."""
import math

from ..contract import ContractError


def _times(values):
    try:
        values = list(values)
        if any(isinstance(value, bool) for value in values):
            raise ValueError('boolean timestamp')
        result = [float(value) for value in values]
    except (TypeError, ValueError, OverflowError):
        raise ContractError('mốc phải là số hữu hạn không âm') from None
    if any(not math.isfinite(value) or value < 0 for value in result):
        raise ContractError('mốc phải là số hữu hạn không âm')
    return sorted(result)


def score_cuts(truth, detected, tolerance=.25):
    """Greedy sorted matching gives maximum cardinality for equal tolerance."""
    if isinstance(tolerance, bool):
        raise ContractError('tolerance phải hữu hạn không âm')
    try:
        tolerance = float(tolerance)
    except (TypeError, ValueError, OverflowError):
        raise ContractError('tolerance phải hữu hạn không âm') from None
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ContractError('tolerance phải hữu hạn không âm')
    expected, actual = _times(truth), _times(detected)
    i = j = matched = 0
    while i < len(expected) and j < len(actual):
        difference = abs(actual[j] - expected[i])
        if difference <= tolerance or math.isclose(difference, tolerance, rel_tol=1e-12, abs_tol=1e-12):
            i += 1
            j += 1
            matched += 1
        elif actual[j] < expected[i]:
            j += 1
        else:
            i += 1
    return {'matched': matched, 'missed': len(expected) - matched,
            'extra': len(actual) - matched,
            'precision': matched / len(actual) if actual else None,
            'recall': matched / len(expected) if expected else None}
