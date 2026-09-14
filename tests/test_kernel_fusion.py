from pydantic import ValidationError
import pytest

from sigilflow import (
    FlowLibrary,
    Presheaf,
    RestrictionMap,
    SIGILBOOK_COMMIT,
    TFG_COMMIT,
    build_reference_kernel,
)


def test_reference_kernel_pins_both_sources() -> None:
    kernel = build_reference_kernel(epoch=4)
    assert kernel.sync.tfg_pin.commit == TFG_COMMIT
    assert kernel.sync.sigilbook_pin.commit == SIGILBOOK_COMMIT
    assert kernel.sync.auto_pull is False
    assert kernel.sync.auto_merge is False
    assert kernel.sync.auto_push is False


def test_join_meet_preserve_split() -> None:
    kernel = build_reference_kernel()
    assert kernel.fusion.join_is_flatten is False
    assert kernel.fusion.meet_is_identity_intersection is False
    assert kernel.fusion.fusion_bearer_is_source_bearer is False
    assert "typed_flow_interface" in kernel.fusion.meet
    assert "poetry_kernel_semantics" in kernel.fusion.join


def test_required_admission_spine_is_present() -> None:
    kernel = build_reference_kernel()
    libs = set(kernel.libraries)
    assert {FlowLibrary.PACAPDG, FlowLibrary.UAP, FlowLibrary.SAFE_REPLAY} <= libs
    assert kernel.pacapdg_precedes_uap
    assert kernel.uap_precedes_safe_replay


def test_presheaf_rejects_duplicate_bearers() -> None:
    kernel = build_reference_kernel()
    sections = list(kernel.presheaf.sections)
    sections[1] = sections[1].model_copy(update={"bearer_id": sections[0].bearer_id})
    with pytest.raises(ValidationError):
        Presheaf(presheaf_id="bad", sections=tuple(sections))


def test_restriction_requires_distinct_sections() -> None:
    with pytest.raises(ValidationError):
        RestrictionMap(
            map_id="bad",
            source_section="x",
            target_section="x",
        )
