import copy
from dataclasses import dataclass, field
from random import choice, choices, shuffle, uniform
from typing import Literal


# backup names in case we try to generate from an empty list
NAMES = [
    'Andy', 'Becca', 'Chandru', 'Deniz', 'Ewald', 'Frankie',
    'Gisele', 'Humberto', 'Inez', 'Jae', 'Kenny', 'Libby',
    'Montero', 'Nick', 'Opal', 'Pru', 'Quinton', 'Ruby',
    'Sam', 'Tierney', 'Ursula', 'Viktor', 'Wociek', 'Xavier',
    'Yar', 'Zed',
]
ADJECTIVES = [
    'Ancient', 'Anointed', 'Brazen', 'Desperate', 'Frenzied', 'Gilded',
    'Looming', 'Prosperous', 'Apprentice', 'Shining', 'Territorial',
    'Ambush', 'Armored', 'Doomed', 'Elder', 'Feral', 'Grizzled',
    'Makeshift', 'Night', 'Day', 'One-Eyed', 'Selfless', 'Selfish',
    'Tormented', 'Unruly', 'Interloping', 'Village', 'Woodland',
    'Undead', 'Bellowing', 'Brave', 'Frilled', 'Intrepid', 'Rough',
    'Thieving', 'Guarded', 'Assistant', 'Tragic', 'Conscripted',
]
FRAME_CODE = Literal['W', 'U', 'B', 'R', 'G', 'A', 'Z', 'L']
RARITY_CODE = Literal['C', 'U', 'R', 'M']


@dataclass
class Slot:
    rarity: RARITY_CODE
    color: FRAME_CODE
    number: int
    instruction: str
    id: str = field(init=False)
    name: str = ''
    cost: str = ''
    typeline: str = ''
    text: str = ''
    stats: str | None = None

    def __post_init__(self):
        self.id = f"{self.rarity}{self.color}{self.number:02}"


@dataclass
class Card:
    name: str
    cost: str|None = None
    type: str = ""
    subtypes: list[str]|None = None
    text: str|None = None
    stats: tuple[int,int]|None = None


@dataclass(frozen=True)
class TaggedWord:
    word: str
    tag: str


class Bag:
    def __init__(self, *args: TaggedWord):
        self._bag: list[TaggedWord] = list(set(args)) or []

    def add(self, word: TaggedWord):
        if not word in self._bag:
            self._bag.append(word)
    
    def remove(self, word: TaggedWord):
        self._bag.remove(word)

    def words(self):
        yield from self._bag
    
    def words_tagged(self, tag: str):
        for word in self._bag:
            if word.tag == tag:
                yield word
    
    def has(self, word: str, tag: str):
        for x in self._bag:
            if x.word == word and x.tag == tag:
                return True
        return False
    
    def has_any(self, tag: str):
        for x in self._bag:
            if x.tag == tag:
                return True
        return False
    
    def __str__(self):
        return ", ".join([f"<{x.tag}: {x.word}>" for x in self._bag])


def _make_cost(mv: int|tuple[int], frame: FRAME_CODE):
    if frame == 'L':
        return None
    elif frame in 'WUBRGZ':
        if isinstance(mv, int):
            generic = mv-1
        else:
            generic = choice(mv) - 1
        
        color = 'H' if frame == 'Z' else frame
        if generic:
            return f"{{{generic}}}{{{color}}}"
        return f"{{{color}}}"

    else:
        if isinstance(mv, int):
            return f"{{{mv}}}"
        return f"{{{choice(mv)}}}"


def _infinite_shuffle(list_of_items):
    local_copy = list(list_of_items)
    try:
        while True:
            shuffle(local_copy)
            for element in local_copy:
                yield element
    finally:
        return


class _SkeletonIterator:
    def __init__(self, rarity, frame, creatures, spells):
        self._rarity = copy.copy(rarity)
        self._frame = copy.copy(frame)
        self._creatures = copy.deepcopy(creatures)
        self._spells = copy.deepcopy(spells)
        self._index = -1

    def __iter__(self):
        self._index += 1
        for bag in self._creatures:
            yield Slot(
                self._rarity, self._frame, self._index + 1,
                **self._get_bag_parts(bag),
            )
            self._index += 1
        for bag in self._spells:
            yield Slot(
                self._rarity, self._frame, self._index + 1,
                **self._get_bag_parts(bag),
            )
            self._index += 1
    
    def _get_bag_parts(self, bag: Bag):
        result = {}

        name_tags = list(bag.words_tagged('name'))
        if name_tags:
            result['name'] = name_tags[0].word
        elif bag.has_any('power'):
            result['name'] = self._generate_name(bag)

        keyword_tags = bag.words_tagged("keyword")
        # convert to a set to dedupe keywords
        keyword_text = ", ".join(set([w.word for w in keyword_tags]))
        text_tags = bag.words_tagged("text")
        text = " // ".join([t.word for t in text_tags])
        result['text'] = keyword_text
        if keyword_text and text:
            result['text'] += " // "
        if text:
            result['text'] += text

        mv_tags = list(bag.words_tagged("manavalue"))
        instruction_tags = list(bag.words_tagged("instruction"))
        if mv_tags:
            result['instruction'] = f"{mv_tags[0].word} MV"
        elif instruction_tags:
            result['instruction'] = f"{instruction_tags[0].word}"
        else:
            result['instruction'] = ""
        
        cost_tags = list(bag.words_tagged("cost"))
        if cost_tags:
            result['cost'] = cost_tags[0].word
        
        pow_tags = list(bag.words_tagged("power"))
        tou_tags = list(bag.words_tagged("toughness"))
        if pow_tags and tou_tags:
            result['stats'] = f"{pow_tags[0].word}/{tou_tags[0].word}"
        
        type_tags = list(bag.words_tagged("type"))
        type_ = " ".join([t.word for t in type_tags])
        subtypes = (
            list([s.word for s in bag.words_tagged('subtype')]) +
            list([r.word for r in bag.words_tagged('race')]) +
            list([c.word for c in bag.words_tagged('class')])
        )
        if subtypes:
            result['typeline'] = f"{type_.title()} — {" ".join([s.title() for s in subtypes])}"
        else:
            result['typeline'] = type_.title()

        return result

    def _generate_name(self, bag: Bag):
        race_class = list(bag.words_tagged('race')) + \
                     list(bag.words_tagged('class'))
        if len(race_class) > 0:
            name = choice(race_class).word
        else:
            name = choice(NAMES)
        adjective = choice(ADJECTIVES)
        return f'{adjective} {name.title()}'


class SkeletonGenerator:
    def __init__(
            self,
            rarity: RARITY_CODE,
            frame: FRAME_CODE,
            creatures: int,
            spells: int,
    ):
        """
        Generate a skeleton for a given rarity and frame code with the
        given number of creature and spell slots.
        
        Valid rarities are: C,U,R,M
        Valid frame codes are: W,U,B,R,G,A,Z,L
        """
        self._rarity = rarity
        self._frame = frame
        if frame == 'A':
            self._creatures = [Bag(TaggedWord('Artifact', 'type'), TaggedWord('Creature', 'type')) for _ in range(creatures)]
            self._spells = [Bag(TaggedWord('Artifact', 'type')) for _ in range(spells)]
        elif frame == 'L':
            self._creatures = [Bag(TaggedWord('Land', 'type'), TaggedWord('Creature', 'type')) for _ in range(creatures)]
            self._spells = [Bag(TaggedWord('Land', 'type')) for _ in range(spells)]
        else:
            self._creatures = [Bag(TaggedWord('Creature', 'type')) for _ in range(creatures)]
            self._spells = [Bag() for _ in range(spells)]
        # internal bookkeeping
        self._index = -1
        self._next_spell = 0

    def __iter__(self):
        self._check_and_normalize()

        yield from _SkeletonIterator(
            self._rarity,
            self._frame,
            self._creatures,
            self._spells,
        )

    def keywords(self, **kwargs: float):
        """
        Keywords and the approximate number of times they should appear.

        For example:
          generator.keywords(flying=2, vigilance=1.5, haste=0.5)
        
        This example will attempt to put flying on two creatures and
        vigilance on one. Then, about half the time, it will put
        vigilance on another. Finally, also about half the time, it will
        put haste on one creature.
        """
        creatures = _infinite_shuffle(self._creatures)
        for keyword, count in kwargs.items():
            keyword = keyword.replace('_', ' ')
            while count > 1:
                tag = TaggedWord(keyword, "keyword")
                bag = next(creatures)
                bag.add(tag)
                count -= 1
            if uniform(0.0, 1.0) < count:
                tag = TaggedWord(keyword, "keyword")
                bag = next(creatures)
                bag.add(tag)
        creatures.close()

    def mana_values(self, *args: int|tuple[int]):
        """
        The exact mana value or range of mana values to use for each creature slot.
        
        Example:
          generator.mana_values((1, 2), 2, (2, 3))

        This example will generate a creature with MV 1 or 2, another with
        MV 2, and then a third with MV either 2 or 3.
        """
        if len(args) != len(self._creatures):
            raise ValueError("incorrect number of mana values passed: "
                             f"expected {len(self._creatures)} "
                             f"but got {len(args)}")
        for mv, bag in zip(args, self._creatures):
            cost = _make_cost(mv, self._frame)
            if isinstance(mv, int):
                mv = str(mv)
            else:
                mv = "/".join([str(x) for x in mv])
            bag.add(TaggedWord(mv, "manavalue"))
            bag.add(TaggedWord(cost, "cost"))

    def powers(self, *args: int|tuple[int]):
        """
        The exact power or range of powers to use for each creature slot.
        
        Example:
          generator.powers(1, 2, (2, 3))

        This example will generate a creature with power 1, another with
        power 2, and then a third creature with power either 2 or 3.
        """
        self._pt_tag('power', *args)

    def toughnesses(self, *args: int|tuple[int]):
        """
        The exact toughness or range of toughnesses to use for each creature slot.
        
        Example:
          generator.toughnesses(1, 1, (1, 2, 3))

        This example will generate two creatures with toughness 1 and
         a third creature with toughness somewhere between 1 and 3.
        """
        self._pt_tag('toughness', *args)

    def _pt_tag(self, _tag_word: str, *args: int|tuple[int]):
        if len(args) != len(self._creatures):
            raise ValueError(f"incorrect number of {_tag_word} passed: "
                             f"expected {len(self._creatures)} "
                             f"but got {len(args)}")
        for pt, bag in zip(args, self._creatures):
            if isinstance(pt, int):
                pt = str(pt)
            else:
                pt = str(choice(pt))
            tag = TaggedWord(pt, _tag_word)
            bag.add(tag)

    def races(self, **kwargs: float):
        """
        Races and the relative frequency with which they should appear.

        For example:
          generator.races(bear=2, mouse=1)
        
        This example will generate approximately 2 Bears for every
        1 Mouse. As a special case, "nothing" can be used to stand for
        a creature with no race.
        """
        self._choose_and_tag('race', **kwargs)

    def classes(self, **kwargs: float):
        """
        Classes and the relative frequency with which they should appear.

        For example:
          generator.classes(soldier=5, cleric=2)
        
        This example will generate approximately 5 Soldiers for every
        2 Clerics. As a special case, "nothing" can be used to occasionally
        (or always!) make creatures classless.
        """
        self._choose_and_tag('class', **kwargs)

    def _choose_and_tag(self, _tag_word: str, **kwargs: float):
        if len(kwargs) == 0:
            raise ValueError(f"need at least one {_tag_word} passed in")

        distribution = choices(
            list(kwargs.keys()),
            weights=list(kwargs.values()),
            k=len(self._creatures)
        )
        for ch, bag in zip(distribution, self._creatures):
            if ch != "nothing":
                tag = TaggedWord(ch, _tag_word)
                bag.add(tag)

    def add_spell(self, instruction: str, *possibilities: Card):
        """
        Given an (optional) list of roughly equivalent reprints, choose
        one for the next spell slot.
        """
        try:
            bag = self._spells[self._next_spell]
        except IndexError:
            raise IndexError("too many spells; increase the number of spell slots")
        self._next_spell += 1

        bag.add(TaggedWord(instruction, 'instruction'))
        if len(possibilities) > 0:
            spell = choice(possibilities)
            bag.add(TaggedWord(spell.name, 'name'))
            bag.add(TaggedWord(spell.cost, 'cost'))
            bag.add(TaggedWord(spell.type, 'type'))
            for subtype in spell.subtypes or []:
                bag.add(TaggedWord(subtype, 'subtype'))
            bag.add(TaggedWord(spell.text, 'text'))
            if spell.stats:
                bag.add(TaggedWord(spell.stats[0], 'power'))
                bag.add(TaggedWord(spell.stats[1], 'toughness'))

    def _check_and_normalize(self):
        non_obligate_flyers: list[Bag] = []

        for bag in self._creatures:
            if bag.has('flying', 'keyword') and not bag.has('bird', 'race') and not bag.has('bat', 'race'):
                non_obligate_flyers.append(bag)

            if (bag.has('bird', 'race') or bag.has('bat', 'race')) and not bag.has('flying', 'keyword'):
                flying = TaggedWord('flying', 'keyword')
                bag.add(flying)
                # try to remove a non-bird/bat flyer to keep flying counts stable
                # if we haven't yet encountered one, the list will be empty
                # so we might make too many flyers. as a design skeleton, this
                # is probably fine.
                if non_obligate_flyers:
                    non_obligate_flyers.pop().remove(flying)
