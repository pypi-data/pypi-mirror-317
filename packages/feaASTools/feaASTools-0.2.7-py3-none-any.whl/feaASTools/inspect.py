"""
inspect
===============================================================================

Inspect feature files.

"""
from __future__ import annotations

import logging
from typing import Optional, Tuple, Iterable

from fontTools.feaLib import ast

log = logging.getLogger(__name__)


def hasFeature(featureSyntaxTree: ast.FeatureFile, featureTag: str) -> bool:
    """
    :return: True if a feature with the specified featureTag is found, False otherwise.
    """
    for statement in featureSyntaxTree.statements:
        if isinstance(statement, ast.FeatureBlock) and statement.name == featureTag:
            return True
    return False


def getFeature(
    featureSyntaxTree: ast.FeatureFile, featureTag: str
) -> Optional[ast.FeatureBlock]:
    """
    :return: The first feature block with the specified featureTag, if any,
        None otherwise.
    """
    for statement in featureSyntaxTree.statements:
        if isinstance(statement, ast.FeatureBlock) and statement.name == featureTag:
            return statement


def getFeatureTags(featureSyntaxTree: ast.FeatureFile) -> Tuple[str]:
    """
    :return: All feature tags found in the feature syntax tree.
    """
    return tuple(
        s.name for s in featureSyntaxTree.statements if isinstance(s, ast.FeatureBlock)
    )


def renameFeature(featureSyntaxTree: ast.FeatureFile, oldTag: str, newTag: str) -> bool:
    """
    Rename a feature block in a feature syntax tree.

    :return: True if feature was successfully renamed, False otherwise.
    """
    if hasFeature(featureSyntaxTree, newTag):
        log.warning(
            "Can't rename feature from %s to %s. A feature with tag %s already exists.",
            oldTag,
            newTag,
            newTag,
        )
        return False
    feature = getFeature(featureSyntaxTree, oldTag)
    if feature:
        feature.name = newTag
        feature_aalt = getFeature(featureSyntaxTree, "aalt")
        if feature_aalt:
            for statement in feature_aalt.statements:
                if isinstance(statement, ast.FeatureReferenceStatement) and statement.featureName == oldTag:
                    statement.featureName = newTag
        return True
    log.warning("Feature with tag %s not found", oldTag)
    return False


def removeFeatures(
    featureSyntaxTree: ast.FeatureFile, featureTags: Iterable[str]
) -> bool:
    """
    :param featureTags: Tags of features to be removed
    :return: True if at least one feature was removed, False otherwise.
    """
    statements = []
    removed = False
    if isinstance(featureTags, str):
        featureTags = (featureTags,)
    for statement in featureSyntaxTree.statements:
        if isinstance(statement, ast.FeatureBlock) and statement.name in featureTags:
            removed = True
            continue
        statements.append(statement)
    featureSyntaxTree.statements = statements
    return removed


#: Comments which mark a feature as automatically generated.
featureAutomaticStrings = ('# <protection state="no"/>', "# automatic")


def isFeatureAutomatic(feature: ast.FeatureBlock) -> bool:
    """
    :return: True if the specified feature is marked as automatically generated,
        False otherwise.
    """
    assert isinstance(feature, ast.FeatureBlock)
    for statement in feature.statements:
        if (
            isinstance(statement, ast.Comment)
            and statement.text.strip() in featureAutomaticStrings
        ):
            return True
    return False


def setFeatureAutomatic(feature: ast.FeatureBlock, automatic: bool = True) -> None:
    """
    :param automatic: If True the feature is marked as automatically generated,
        otherwise the automatic marker is removed. Defaults to True.
    """
    assert isinstance(feature, ast.FeatureBlock)
    commentAutomatic = ast.Comment("# automatic")
    if isFeatureAutomatic(feature):
        if automatic:
            return
        statements = []
        for statement in feature.statements:
            if (
                isinstance(statement, ast.Comment)
                and statement.text.strip() in featureAutomaticStrings
            ):
                continue
            statements.append(statement)
        feature.statements = statements
    elif automatic:
        feature.statements.insert(0, commentAutomatic)
