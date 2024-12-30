"""
This file exercises most of the SkeletonGenerator API. However, this isn't
the implementation used to generate a real skeleton. See data/pb2024.toml
and the contents of demilich.reader for that.
"""
from demilich.skeleton import SkeletonGenerator, Card


def pb2024():
    common_white = SkeletonGenerator('C', 'W', 11, 4)
    common_white.keywords(
        flying=3, vigilance=2, lifelink=1,
        first_strike=.25, double_strike=.2,
    )
    common_white.mana_values(
        1, 2, 2, 2, 3, 3,
        3, 4, 4, (5, 6), (6, 7)
    )
    common_white.powers(
        (1, 2), 2, (1, 2, 3), 2, (2, 3), (2, 3),
        3, (3, 4), 4, (4, 5), (4, 5, 6)
    )
    common_white.toughnesses(
        1, 1, (1, 2), (2, 3), 3, 3,
        3, (3, 4), 4, (4, 5), (4, 5)
    )
    common_white.races(
        human=20, bird=5, spirit=5, cat=5, kithkin=2, unicorn=1,
        dog=1, dinosaur=1, avatar=1, loxodon=1, giant=1, nothing=1,
    )
    common_white.classes(
        nothing=2, scout=4, knight=4, soldier=4, monk=2, cleric=2,
        nomad=1, mystic=1, samurai=1,
    )
    common_white.add_spell("Combat-related removal")
    common_white.add_spell(
        "Banishing Light",
        Card("Banishing Light", "{2}{W}", "Enchantment", None, "When this enchantment enters, exile target nonland permanent an opponent controls until this enchantment leaves the battlefield."),
        Card("Journey to Nowhere", "{1}{W}", "Enchantment", None, "When Journey to Nowhere enters, exile target creature. // When Journey to Nowhere leaves the battlefield, return the exiled card to the battlefield under its owner's control."),
        Card("Oblivion Ring", "{2}{W}", "Enchantment", None, "When Oblivion Ring enters, exile another target nonland permanent. //  When Oblivion Ring leaves the battlefield, return the exiled card to the battlefield under its owner's control."),
        Card("Chains of Custody", "{2}{W}", "Enchantment", ["Aura"], "Enchant creature you control // When Chains of Custody enters, exile target nonland permanent an opponent controls until Chains of Custody leaves the battlefield. // Enchanted creature has ward {2}."),
    )
    common_white.add_spell("Combat trick")
    common_white.add_spell(
        "Disenchant/removal",
        Card("Disenchant", "{1}{W}", "Instant", None, "Destroy target artifact or enchantment."),
        Card("Invoke the Divide", "{2}{W}", "Instant", None, "Destroy targert artifact or enchantment. You gain 4 life."),
        Card("Make Your Move", "{2}{W}", "Instant", None, "Destroy target artifact, enchantment, or creature with power 4 or greater."),
        Card("Destroy Evil", "{1}{W}", "Instant", None, "Choose one — // • Destroy target creature with toughness 4 or greater. // • Destroy target enchantment."),
    )
    yield from common_white

    common_blue = SkeletonGenerator('C', 'U', 8, 7)
    common_blue.keywords(
        flying=3, vigilance=1.5,
        ward_N=.5, defender=.5, flash=.5,
    )
    common_blue.mana_values(
        2, 2, 3, 3,
        3, 4, (5, 6), (6, 7)
    )
    common_blue.powers(
        1, (1, 2), (2, 3), 3,
        (3, 4), 4, (4, 5), (4, 5, 6)
    )
    common_blue.toughnesses(
        (1, 2), 2, 3, 3,
        (3, 4), 4, (5, 6), (5, 6)
    )
    common_blue.races(
        human=2, merfolk=4, otter=1, bird=3, spirit=2, dog=1,
        faerie=1, homarid=2, zombie=1, crab=2, turtle=1, nothing=1,
    )
    common_blue.classes(
        nothing=2, scout=4, rogue=4, pirate=1, ninja=2, wizard=2,
        nomad=1, mystic=1, advisor=1, artificer=1,
    )
    common_blue.add_spell("Protective instant")
    common_blue.add_spell("Counterspell")
    common_blue.add_spell("Cantrip")
    common_blue.add_spell("Draw 2-3")
    common_blue.add_spell(
        "Witness Protection aura",
        Card("Witness Protection", "{U}", "Enchantment", ["Aura"], "Enchant creature // Enchanted creature loses all abilities and is a green and white Citizen creature with base power and toughness 1/1 named Legitimate Businessperson."),
        Card("Stop Cold", "{3}{U}", "Enchantment", ["Aura"], "Flash // Enchant artifact or creature // When Stop Cold enter, tap enchanted permanent. // Enchanted permanent loses all abilities and doesn't untap during its controller's untap step."),
        Card("Frogify", "{1}{U}", "Enchantment", ["Aura"], "Enchant creature // Enchanted creature loses all abilities and is a blue Frog creature with base power and toughness 1/1."),
    )
    common_blue.add_spell("Top or bottom")
    common_blue.add_spell("Modal spell")
    yield from common_blue

    common_black = SkeletonGenerator('C', 'B', 9, 6)
    common_black.keywords(
        flying=2, lifelink=1, menace=1.5, deathtouch=1.25,
    )
    common_black.mana_values(
        (1, 2), 2, 2, 3, 3,
        4, (4,5), (5,5), (6,7)
    )
    common_black.powers(
        (1, 2), (1, 2), 2, (2, 3), (2, 3),
        (3, 4), (4, 5), (4, 5), (4, 5)
    )
    common_black.toughnesses(
        1, (1, 2), (1, 2), (2, 3), 3,
        4, 4, (3, 4), (4, 5)
    )
    common_black.races(
        human=1, vampire=4, imp=1, horror=2, bat=1, skeleton=2,
        faerie=1, zombie=1, rat=2, nightmare=1, nothing=1,
    )
    common_black.classes(
        nothing=4, assassin=3, rogue=3, cleric=1, ninja=2, warlock=2,
        nomad=1, knight=3, samurai=1, minion=1,
    )
    common_black.add_spell("Small conditional removal")
    common_black.add_spell("Combat trick")
    common_black.add_spell("Card draw with a cost")
    common_black.add_spell(
        "Coercion+",
        Card("Coercion", "{2}{B}", "Sorcery", None, "Target opponent reveals their hand. You choose a card from it. That player discards that card."),
        Card("Duress", "{B}", "Sorcery", None, "Target opponent reveals their hand. You choose a noncreature, nonland card from it. That player discards that card."),
        Card("Pilfer", "{1}{B}", "Sorcery", None, "Target opponent reveals their hand. You choose a nonland card from it. That player discards that card."),
    )
    common_black.add_spell("Unconditional removal")
    common_black.add_spell("Slightly overcosted removal")
    yield from common_black

    common_red = SkeletonGenerator('C', 'R', 9, 6)
    common_red.keywords(
        first_strike=.25, double_strike=.2, menace=1.5,
        trample=1.5, haste=1.5, reach=1,
    )
    common_red.mana_values(
        (1, 2), 2, 2, 3, 3,
        (3,4), (4,5), 5, 6
    )
    common_red.powers(
        (1, 2), 2, (2, 3), (3, 4), (3, 4),
        3, 4, (4, 5), (4, 5)
    )
    common_red.toughnesses(
        1, (1, 2), (1, 2), (3, 4), 3,
        (3, 4), 4, (3, 4), (3, 4)
    )
    common_red.races(
        goblin=3, devil=1, dwarf=2, giant=1, minotaur=1,
        orc=2, ogre=1, gremlin=1,
    )
    common_red.classes(
        nothing=5, knight=2, pirate=2, samurai=1, shaman=4,
        barbarian=1, warrior=4, artificer=1, berserker=1,
    )
    common_red.add_spell("Direct damage for 2")
    common_red.add_spell("Combat trick")
    common_red.add_spell("Rummage/impulse draw")
    common_red.add_spell(
        "Modal Shatter",
        Card("Shatter", "{1}{R}", "Instant", None, "Destroy target artifact."),
        Card("Abrade", "{1}{R}", "Instant", None, "Choose one — // • Abrade deals 3 damage to target creature. // • Destroy target artifact."),
        Card("Shredded Sails", "{1}{R}", "Instant", None, "Choose one — // • Destroy target artifact. // • Shredded Sails deals 4 damage to target creature with flying. // Cycling {2}"),
    )
    common_red.add_spell("Efficient direct damage for 4")
    common_red.add_spell("Direct damage for 6 (5 mana)")
    yield from common_red

    common_green = SkeletonGenerator('C', 'G', 10, 5)
    common_green.keywords(
        vigilance=1.5, ward_N=.5, deathtouch=1, trample=1.5,
        haste=.2, reach=1.5,
    )
    common_green.mana_values(
        (1, 2), 2, 2, 3, 3,
        (3, 4), (4, 5), 5, 6, (6, 7))
    common_green.powers(
        1, 2, 2, (3, 4), (3, 4),
        (3, 4), (4, 5), 5, 6, (6, 7)
    )
    common_green.toughnesses(
        1, 2, 3, 3, (3, 4),
        (3, 4, 5), (4, 5), (5, 6), 6, 6
    )
    common_green.races(
        elf=4, cat=1, human=2, faerie=1, merfolk=1,
        rhox=1, treefolk=1, troll=1, loxodon=1,
        centaur=1, ape=1, bear=1, dinosaur=3, spider=1,
    )
    common_green.classes(
        nothing=4, archer=1, scout=1, druid=3, warrior=3,
        shaman=1, nomad=1, monk=1, ranger=2,
    )
    common_green.add_spell("Fight spell")
    common_green.add_spell("Bite spell")
    common_green.add_spell(
        "Combat trick (power pump)",
        Card("Giant Growth", "{G}", "Instant", None, "Target creature gets +3/+3 until end of turn."),
        Card("Fanatical Strength", "{1}{G}", "Instant", None, "Target creature gets +3/+3 and gains trample until end of turn."),
        Card("For the Family", "{G}", "Instant", None, "Target creature gets +2/+2 until end of turn. If you control four or more creatures, that creature gets +4/+4 until end of turn instead."),
    )
    common_green.add_spell("Mana acceleration")
    common_green.add_spell("Dig for lands and/or creatures")
    yield from common_green

    common_artifact = SkeletonGenerator('C', 'A', 3, 3)
    common_artifact.mana_values(2, 3, 4)
    common_artifact.powers(1, 2, 3)
    common_artifact.toughnesses(1, 2, 3)
    common_artifact.races(
        construct=3, myr=3, golem=3,
        thopter=1, toy=1, scarecrow=1, gargoyle=1,
    )
    common_artifact.classes(
        nothing=22, drone=1, soldier=1, warrior=1,
    )
    common_artifact.add_spell("Removal")
    common_artifact.add_spell(
        "Manalith+ ability",
        Card("Manalith", "{3}", "Artifact", None, "{T}: Add one mana of any color."),
        Card("Letter of Acceptance", "{3}", "Artifact", None, "{T}: Add one mana of any color. // {2}, {T}, Sacrifice Letter of Acceptance: Draw a card."),
        Card("Network Terminal", "{3}", "Artifact", None, "{T}: Add one mana of any color. // {1}, {T}, Tap another untapped artifact you control: Draw a card, then discard a card."),
    )
    common_artifact.add_spell("Land fixing")
    yield from common_artifact
