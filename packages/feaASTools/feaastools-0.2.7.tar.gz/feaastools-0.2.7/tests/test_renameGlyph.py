from feaASTools.renameGlyph import renameGlyphInFeatureText

featureText_in = (
"feature ss01 {\n"
"    @input = [a b c];\n"
"    sub a by a.ss01;\n"
"} ss01;\n"
)

featureText_out = (
"feature ss01 {\n"
"    @input = [b b c];\n"
"    sub b by a.ss01;\n"
"} ss01;\n"
)

def test_renameGlyphInFeatureText():
    assert renameGlyphInFeatureText(featureText_in, "a", "b") == featureText_out
