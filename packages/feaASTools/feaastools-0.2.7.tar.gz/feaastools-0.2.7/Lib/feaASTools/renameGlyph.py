"""
renameGlyph
===============================================================================

Rename glyph in feature files.

To make it simple we inject a renameGlyph method in every `ast.Statement` class 
which deserves one.
As a result we can simply call `syntaxTree.renameGlyph(oldName, newName)`.

"""
from __future__ import annotations

import logging
from typing import List, Tuple, Union

from fontTools.feaLib import ast

from . import getFeatureSyntaxTree

log = logging.getLogger(__name__)

noGlyphRenameStatment = (
    ast.Comment,
    ast.LanguageSystemStatement,
    ast.LanguageStatement,
    ast.ScriptStatement,
    ast.LookupFlagStatement,
    ast.FeatureReferenceStatement,
    ast.LookupReferenceStatement,
    ast.SubtableStatement,
    ast.FeatureNameStatement,
)


def _add_method(*classes):
    """
    Returns a decorator function that adds a new method to one or
    more classes.
    """

    def wrapper(method):
        done = []
        for c in classes:
            if c in done:
                continue  # Support multiple names of a class
            done.append(c)
            assert not hasattr(
                c, method.__name__
            ), "Oops, class '%s' has method '%s'." % (c.__name__, method.__name__)
            setattr(c, method.__name__, method)
        return None

    return wrapper


def replaceInSequence(sequence: Union[List, Tuple], old: str, new: str) -> Union[List, Tuple]:
    result = sequence
    if old in sequence:
        newSequece = [new if i == old else i for i in sequence]
        if isinstance(newSequece, type(sequence)):
            result = newSequece
        else:
            result = sequence.__class__(newSequece)
    return result


@_add_method(ast.GlyphClassName, ast.ValueRecord)
def renameGlyph(self, oldName: str, newName: str) -> None:
    pass


@_add_method(ast.GlyphName)
def renameGlyph(self, oldName: str, newName: str) -> None:
    if self.glyph == oldName:
        self.glyph = newName


@_add_method(ast.GlyphClass)
def renameGlyph(self, oldName: str, newName: str) -> None:
    self.glyphs = replaceInSequence(self.glyphs, oldName, newName)


@_add_method(ast.GlyphClassDefinition, ast.MarkClassDefinition)
def renameGlyph(self, oldName: str, newName: str) -> None:
    self.glyphs.renameGlyph(oldName, newName)


# GSUB lookup type 1
@_add_method(ast.SingleSubstStatement)
def renameGlyph(self, oldName: str, newName: str) -> None:
    for glyphSetList in (self.prefix, self.suffix, self.glyphs, self.replacements):
        for glyphSet in glyphSetList:
            if hasattr(glyphSet, "renameGlyph"):
                glyphSet.renameGlyph(oldName, newName)
            else:
                log.error("unhandled glyphSet type: %r", type(glyphSet))


# GSUB lookup type 2 and 3
@_add_method(ast.MultipleSubstStatement, ast.AlternateSubstStatement)
def renameGlyph(self, oldName: str, newName: str) -> None:
    for glyphSetList in (self.prefix, self.suffix):
        for glyphSet in glyphSetList:
            if hasattr(glyphSet, "renameGlyph"):
                glyphSet.renameGlyph(oldName, newName)
            else:
                log.error("unhandled glyphSet type: %r", type(glyphSet))
    if self.glyph == oldName:
        self.glyph = newName
    if isinstance(self.replacement, ast.GlyphClass):
        self.replacement.renameGlyph(oldName, newName)
    elif isinstance(self.replacement, ast.GlyphClassName):
        pass
    else:
        self.replacement = replaceInSequence(self.replacement, oldName, newName)


# GSUB lookup type 4
@_add_method(ast.LigatureSubstStatement)
def renameGlyph(self, oldName: str, newName: str) -> None:
    for glyphSetList in (self.prefix, self.suffix, self.glyphs):
        for glyphSet in glyphSetList:
            if hasattr(glyphSet, "renameGlyph"):
                glyphSet.renameGlyph(oldName, newName)
            else:
                log.error("unhandled glyphSet type: %r", type(glyphSet))
    if self.replacement == oldName:
        self.replacement = newName


# GSUB lookup type 6
@_add_method(ast.ChainContextSubstStatement)
def renameGlyph(self, oldName: str, newName: str) -> None:
    for glyphSetList in (self.prefix, self.suffix, self.glyphs):
        for glyphSet in glyphSetList:
            if hasattr(glyphSet, "renameGlyph"):
                glyphSet.renameGlyph(oldName, newName)
            else:
                log.error("unhandled glyphSet type: %r", type(glyphSet))
    for lookup in self.lookups:
        if hasattr(lookup, "renameGlyph"):
            lookup.renameGlyph(oldName, newName)
        elif isinstance(lookup, (list, tuple)):
            for item in lookup:
                item.renameGlyph(oldName, newName)


@_add_method(ast.IgnoreSubstStatement)
def renameGlyph(self, oldName: str, newName: str) -> None:
    for chainContext in self.chainContexts:
        for glyphSetList in chainContext:
            for glyphSet in glyphSetList:
                if hasattr(glyphSet, "renameGlyph"):
                    glyphSet.renameGlyph(oldName, newName)
                else:
                    log.error("unhandled glyphSet type: %r", type(glyphSet))


# GPOS lookup type 1
@_add_method(ast.SinglePosStatement)
def renameGlyph(self, oldName: str, newName: str) -> None:
    for glyphSetList in (self.prefix, self.suffix):
        for glyphSet in glyphSetList:
            if hasattr(glyphSet, "renameGlyph"):
                glyphSet.renameGlyph(oldName, newName)
            else:
                log.error("unhandled glyphSet type: %r", type(glyphSet))
    for pos in self.pos:
        for item in pos:
            if hasattr(item, "renameGlyph"):
                item.renameGlyph(oldName, newName)
            else:
                log.error("unhandled item type: %r", type(item))


# GPOS lookup type 2
@_add_method(ast.PairPosStatement)
def renameGlyph(self, oldName: str, newName: str) -> None:
    for glyphs in (self.glyphs1, self.glyphs2):
        if hasattr(glyphs, "renameGlyph"):
            glyphs.renameGlyph(oldName, newName)
        else:
            log.error("unhandled glyphs type: %r", type(glyphs))


# GPOS lookup type 3
# todo: implement renameGlyph for Cursive Attachment Positioning


# GPOS lookup type 4
@_add_method(ast.MarkBasePosStatement)
def renameGlyph(self, oldName: str, newName: str) -> None:
    if hasattr(self.base, "renameGlyph"):
        self.base.renameGlyph(oldName, newName)
    else:
        log.error("unhandled base type: %r", type(self.base))
    for anchor, markClass in self.marks:
        for definition in markClass.definitions:
            definition.renameGlyph(oldName, newName)
        names = [n for n in markClass.glyphs.keys() if n == oldName]
        for name in names:
            value = markClass.glyphs.pop(name)
            markClass.glyphs[newName] = value.renameGlyph(oldName, newName)


# GPOS lookup type 5
@_add_method(ast.MarkLigPosStatement)
def renameGlyph(self, oldName: str, newName: str) -> None:
    if hasattr(self.ligatures, "renameGlyph"):
        self.ligatures.renameGlyph(oldName, newName)
    else:
        log.error("unhandled ligatures type: %r", type(self.ligatures))
    for component in self.marks:
        for anchor, markClass in component:
            for definition in markClass.definitions:
                definition.renameGlyph(oldName, newName)
            names = [n for n in markClass.glyphs.keys() if n == oldName]
            for name in names:
                value = markClass.glyphs.pop(name)
                markClass.glyphs[newName] = value.renameGlyph(oldName, newName)


# GPOS lookup type 6
@_add_method(ast.MarkMarkPosStatement)
def renameGlyph(self, oldName: str, newName: str) -> None:
    if hasattr(self.baseMarks, "renameGlyph"):
        self.baseMarks.renameGlyph(oldName, newName)
    else:
        log.error("unhandled baseMarks type: %r", type(self.baseMarks))
    for anchor, markClass in self.marks:
        for definition in markClass.definitions:
            definition.renameGlyph(oldName, newName)
        names = [n for n in markClass.glyphs.keys() if n == oldName]
        for name in names:
            value = markClass.glyphs.pop(name)
            markClass.glyphs[newName] = value.renameGlyph(oldName, newName)


@_add_method(ast.GlyphClassDefStatement)
def renameGlyph(self, oldName: str, newName: str) -> None:
    for glyphs in (
        self.baseGlyphs,
        self.markGlyphs,
        self.ligatureGlyphs,
        self.componentGlyphs,
    ):
        if glyphs:
            glyphs.renameGlyph(oldName, newName)


@_add_method(ast.Block)
def renameGlyph(self, oldName: str, newName: str) -> None:
    for statement in self.statements:
        if hasattr(statement, "renameGlyph"):
            statement.renameGlyph(oldName, newName)
        elif isinstance(statement, noGlyphRenameStatment):
            pass
        else:
            log.error(
                "unhandled statement type: %r on line %r",
                statement.__class__.__name__,
                statement.location[1],
            )


def renameGlyphInFeatureText(featureText: str, oldName: str, newName: str):
    """
    :param featureText: The feature text to inspect
    :param oldName: Glyph name to find
    :param newName: Glyph name to replace with
    """
    syntaxTree = getFeatureSyntaxTree(featureText)
    syntaxTree.renameGlyph(oldName, newName)
    return syntaxTree.asFea()
