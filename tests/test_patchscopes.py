from shattered.interp.patchscopes import detok_layer, identifies


def test_identifies_requires_prefix_and_boundaries():
    assert identifies("cat", " cat, cat, cat")
    # FragMend's rule: string prefix AND a bounded occurrence anywhere, so this counts (replicated as-is)
    assert identifies("cat", " caterpillar, cat")
    assert not identifies("cat", " caterpillar, dog")        # prefix alone is not enough
    assert not identifies("cat", " dog, cat")                # must start with the word
    assert not identifies("cat", "catalog")                  # boundary after the word
    assert identifies("ಕನ್ನಡ", " ಕನ್ನಡ, ಕನ್ನಡ")
    assert not identifies("ಕನ್ನಡ", "ಕನ್ನಡದ, ಕನ್ನಡ")          # Kannada letters/marks count as word characters
    assert identifies("beMgaLUru", "beMgaLUru, beMgaLUru")


def test_detok_layer_first_identifying():
    assert detok_layer("cat", ["dog", " cat,", "cat"]) == 1
    assert detok_layer("cat", ["dog", "dogs"]) is None
