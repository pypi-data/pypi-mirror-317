from feaASTools import getFeatureSyntaxTree
from feaASTools.inspect import hasFeature
featureText = """
feature ss01 {
    sub a by a.ss01;
} ss01;
"""

def test_hasFeature():
    features = getFeatureSyntaxTree(featureText)
    assert hasFeature(features, "ss01") == True    
    assert hasFeature(features, "ss02") == False