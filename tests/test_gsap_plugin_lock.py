"""Regression checks for the six plugin files in the pinned GSAP package."""
from video_studio import runtime_libs


def test_gsap_plugins_share_pinned_package_and_core_dependency():
    lock = runtime_libs.load_lock()
    names = {"gsap-drawsvg", "gsap-morphsvg", "gsap-motionpath", "gsap-splittext", "gsap-flip", "gsap-customease"}
    destinations = {lock["libs"]["gsap"]["members"][0]["dest"]}
    for name in names:
        lib = lock["libs"][name]
        assert lib["package"] == "gsap"
        assert lib["requires"] == ["gsap"]
        assert len(lib["members"]) == 1
        member = lib["members"][0]
        assert len(member["file_sha256"]) == 64
        assert int(member["file_sha256"], 16) >= 0
        assert "/" not in member["dest"] and "\\" not in member["dest"]
        assert member["dest"] not in destinations
        destinations.add(member["dest"])
    assert runtime_libs.resolve(["gsap-drawsvg"]) == ["gsap", "gsap-drawsvg"]
