from __future__ import annotations

import io
from typing import Sequence

import fontTools.feaLib.ast as ast
from fontTools.feaLib.parser import Parser

__version__ = "0.2.7"


def getFeatureSyntaxTree(
    featureText: str, glyphNames: Sequence[str] = (), includeDir=None
) -> ast.FeatureFile:
    """
    Return features from featureText as Abstract Syntax Tree
    """
    featureFile = io.StringIO(featureText)
    parser = Parser(featureFile, glyphNames, includeDir=includeDir)
    syntaxTree = parser.parse()
    return syntaxTree
