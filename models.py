from django.db import models
from django.utils import timezone
from django.conf import settings
import os

class Deck(models.Model):
    cards = models.ManyToManyField(
        'Card',
        through='Contains',
    )
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    create_date=models.DateTimeField('date created', db_index=True)
    colors = models.CharField(max_length=5)

CARD_TYPE = {"unit":1, "spell":2, "weapon":3, "curse":4, "relic_weapon":5, "relic":6}
class Card(models.Model):
    name = models.CharField(max_length=100)
    colors = models.CharField(max_length=2)
    cost = models.IntegerField(default=2)
    type = models.IntegerField(default=CARD_TYPE['unit'])

class Contains(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)    

def new_deck(cards, w, l):
    card_objs = []
    deck_color_set = set()
    for card_txt in cards.split(')'):
        card_txt = card_txt.strip()
        if not card_txt: continue  # for the last item
        count = int(card_txt.split(' ')[0])
        name = card_txt[card_txt.index(' ') + 1: card_txt.index(' (')]
        colors = get_colors(name)
        for color in colors: deck_color_set.add(color)
        cost = get_cost(name)
        card, created = Card.objects.get_or_create(name=name, defaults={'colors': colors, 'cost': cost})
        card_objs.append((count, card))
    deck_colors = sort_colors(''.join(deck_color_set))
    deck = Deck.objects.create(wins=w, losses=l, create_date=timezone.now(), colors=deck_colors)
    Contains.objects.bulk_create(
        [Contains(deck=deck, card=card_obj, count=count) for count, card_obj in card_objs])


def get_cost(card_name):
    if card_name in CARD_COSTS:
        return CARD_COSTS[card_name]
    return -1

def get_colors(card_name):
    if card_name in CARD_COLORS:
        return sort_colors(CARD_COLORS[card_name])
    return ''

# list colors in FTJPS order to match the game.
def sort_colors(color_string):
    return ''.join(sorted(color_string, key=lambda x: "FTJPS".index(x)))


# determined by dumping a decklist of every card and splitting by alphabetical decreases
CARD_COSTS = {
  "Charchain Flail": 0,
  "Flame Blast": 0,
  "Sand Warrior": 0,
  "Trail Stories": 0,
  "Copper Conduit": 0,
  "Spiked Helm": 0,
  "Detain": 1,
  "District Infantry": 1,
  "Elder's Feather": 1,
  "Excavate": 1,
  "Finest Hour": 1,
  "Forge Wolf": 1,
  "Frontier Jito": 1,
  "Grenadin Drone": 1,
  "Heavy Axe": 1,
  "Humbug": 1,
  "Infinite Hourglass": 1,
  "Initiate of the Sands": 1,
  "Inspire": 1,
  "Light the Fuse": 1,
  "Oni Ronin": 1,
  "Ornamental Daggers": 1,
  "Predator's Instinct": 1,
  "Protect": 1,
  "Pyroknight": 1,
  "Ruin": 1,
  "Ruthless Stranger": 1,
  "Sanctuary Priest": 1,
  "Seek Power": 1,
  "Silence": 1,
  "Slow": 1,
  "Steadfast Deputy": 1,
  "Temper": 1,
  "Ticking Grenadin": 1,
  "Tinker Apprentice": 1,
  "Torch": 1,
  "Valkyrie Aspirant": 1,
  "Warhelm": 1,
  "Water of Life": 1,
  "Blind Storyteller": 1,
  "Blood Beetle": 1,
  "Cloudsnake Hatchling": 1,
  "Dark Return": 1,
  "Direfang Spider": 1,
  "Ghostform": 1,
  "Knifejack": 1,
  "Levitate": 1,
  "Permafrost": 1,
  "Pilfer": 1,
  "Rapid Shot": 1,
  "Sabotage": 1,
  "Slumbering Stone": 1,
  "Suffocate": 1,
  "Unstable Form": 1,
  "Yeti Spy": 1,
  "Call the Ancients": 1,
  "Combust": 1,
  "Fearless Nomad": 1,
  "Safe Return": 1,
  "Twilight Raptor": 1,
  "Worn Shield": 1,
  "Accelerate": 2,
  "Argenport Soldier": 2,
  "Bladekin Apprentice": 2,
  "Bold Adventurer": 2,
  "Brazen Daredevil": 2,
  "Crownwatch Longsword": 2,
  "Crownwatch Paladin": 2,
  "Eager Owlet": 2,
  "Ephemeral Wisp": 2,
  "Find the Way": 2,
  "Friendly Wisp": 2,
  "Kaleb's Favor": 2,
  "Oni Striker": 2,
  "Ornate Katana": 2,
  "Piercing Shot": 2,
  "Pyre Adept": 2,
  "Rakano Outlaw": 2,
  "Rampage": 2,
  "Refresh": 2,
  "Sauropod Wrangler": 2,
  "Song of War": 2,
  "Synchronized Strike": 2,
  "Talir's Favored": 2,
  "Teleport": 2,
  "Temple Scribe": 2,
  "Voice of the Speaker": 2,
  "Annihilate": 2,
  "Argenport Instigator": 2,
  "Backlash": 2,
  "Borderlands Waykeeper": 2,
  "Cabal Cutthroat": 2,
  "Cloudsnake Saddle": 2,
  "Dark Wisp": 2,
  "Devour": 2,
  "East-Wind Herald": 2,
  "Eilyn's Favor": 2,
  "Herald's Song": 2,
  "Lethrai Ranger": 2,
  "Lightning Storm": 2,
  "Lightning Strike": 2,
  "Minotaur Grunt": 2,
  "Paladin Oathbook": 2,
  "Rebuke": 2,
  "Reinforce": 2,
  "Rolant's Favor": 2,
  "Scavenging Vulture": 2,
  "Second Sight": 2,
  "Sporefolk": 2,
  "Static Bolt": 2,
  "Tinker Overseer": 2,
  "Tundra Explorer": 2,
  "Vampire Bat": 2,
  "Vanquish": 2,
  "Vara's Favor": 2,
  "Venomfang Dagger": 2,
  "Violent Gust": 2,
  "Whispering Wind": 2,
  "Wild Cloudsnake": 2,
  "Yeti Snowslinger": 2,
  "Accelerated Evolution": 2,
  "Awakened Student": 2,
  "Champion of Glory": 2,
  "Combrei Stranger": 2,
  "Daze": 2,
  "Desert Marshal": 2,
  "Elysian Stranger": 2,
  "Feln Stranger": 2,
  "Gorgon Swiftblade": 2,
  "Grim Stranger": 2,
  "Hair-Trigger Stranger": 2,
  "Haunting Scream": 2,
  "Obsidian Golem": 2,
  "Rakano Artisan": 2,
  "Rakano Stranger": 2,
  "Stonescar Stranger": 2,
  "Storm Lynx": 2,
  "Treachery": 2,
  "Twinning Ritual": 2,
  "Ageless Mentor": 3,
  "Amber Acolyte": 3,
  "Assembly Line": 3,
  "Censari Brigand": 3,
  "Clockroach": 3,
  "Dawnwalker": 3,
  "Decay": 3,
  "Determined Stranger": 3,
  "Dispel": 3,
  "Dune Phantom": 3,
  "Fevered Scout": 3,
  "Granite Acolyte": 3,
  "Oasis Sanctuary": 3,
  "Oni Quartermaster": 3,
  "Rakano Flagbearer": 3,
  "Rally": 3,
  "Rebel Sharpshooter": 3,
  "Scorpion Wasp": 3,
  "Secret Pages": 3,
  "Shogun's Scepter": 3,
  "Unlock Potential": 3,
  "Amethyst Acolyte": 3,
  "Auric Sentry": 3,
  "Beastcaller's Amulet": 3,
  "Blackguard Sidearm": 3,
  "Brightmace Paladin": 3,
  "Cabal Countess": 3,
  "Cobalt Acolyte": 3,
  "Desperado": 3,
  "Devouring Shadow": 3,
  "Direwood Beastcaller": 3,
  "Emerald Acolyte": 3,
  "Execute": 3,
  "Eye of Winter": 3,
  "Flash Freeze": 3,
  "Gilded Glaive": 3,
  "Hero of the People": 3,
  "Hooru Envoy": 3,
  "Ice Sprite": 3,
  "Icebreaker": 3,
  "Lethrai Nightblade": 3,
  "Loyal Watchwing": 3,
  "Mark of Shame": 3,
  "Mirror Image": 3,
  "Order of the Spire": 3,
  "Polymorph": 3,
  "Privilege of Rank": 3,
  "Scaly Gruan": 3,
  "Silverwing Familiar": 3,
  "Skysnapper": 3,
  "Spire Chaplain": 3,
  "Thunderbird": 3,
  "Treasury Guard": 3,
  "Valkyrie Enforcer": 3,
  "Valorous Stranger": 3,
  "Wisdom of the Elders": 3,
  "Wump, Party Starter": 3,
  "Alchemical Blast": 3,
  "Amaran Camel": 3,
  "Bloodrite Kalis": 3,
  "Brimstone Altar": 3,
  "Champion of Chaos": 3,
  "Combrei Healer": 3,
  "Crown of Possibilities": 3,
  "Crownwatch Deserter": 3,
  "False Prince": 3,
  "Feln Bloodcaster": 3,
  "Feln Cauldron": 3,
  "Forsworn Stranger": 3,
  "Gorgon Fanatic": 3,
  "Ijin, Imperial Armorer": 3,
  "Knight-Chancellor Siraf": 3,
  "Lifedrinker": 3,
  "Madness": 3,
  "Midnight Gale": 3,
  "Plague": 3,
  "Pteriax Hatchling": 3,
  "Ravenous Thornbeast": 3,
  "Recurring Nightmare": 3,
  "Scheme": 3,
  "Shadowlands Guide": 3,
  "Stand Together": 3,
  "Sword of Icaria": 3,
  "Torrent of Spiders": 3,
  "Trickster's Cloak": 3,
  "Vodakhan's Staff": 3,
  "Xenan Cultist": 3,
  "Xenan Destroyer": 3,
  "Ancient Lore": 4,
  "Burn Out": 4,
  "Centaur Outrider": 4,
  "Cloud of Ash": 4,
  "Furnace Mage": 4,
  "Guerrilla Fighter": 4,
  "Healer's Cloak": 4,
  "Horned Vorlunk": 4,
  "Magma Javelin": 4,
  "Marisen's Disciple": 4,
  "Morningstar": 4,
  "Outlands Sniper": 4,
  "Praxis Displacer": 4,
  "Rebel Illuminator": 4,
  "Recogulator": 4,
  "Sandstorm Titan": 4,
  "Steelfang Chakram": 4,
  "Steward of Prophecy": 4,
  "Timekeeper": 4,
  "Towertop Patrol": 4,
  "Vault of the Praxis": 4,
  "Xenan Guardian": 4,
  "Xenan Obelisk": 4,
  "Armorsmith": 4,
  "Auric Runehammer": 4,
  "Bronze Cuirass": 4,
  "Copperhall Blessing": 4,
  "Copperhall Recruit": 4,
  "Crownwatch Cavalry": 4,
  "Deranged Dinomancer": 4,
  "Hammer of Might": 4,
  "Jarrall's Frostkin": 4,
  "Mantle of Justice": 4,
  "Rain of Frogs": 4,
  "Serpent Trainer": 4,
  "Silverwing Avenger": 4,
  "Soaring Stranger": 4,
  "Stalwart Shield": 4,
  "Stormcaller": 4,
  "Treasury Gate": 4,
  "Yeti Troublemaker": 4,
  "Back-Alley Bouncer": 4,
  "Bandit Queen": 4,
  "Battleblur Centaur": 4,
  "Black Iron Manacles": 4,
  "Cabal Recruiter": 4,
  "Champion of Wisdom": 4,
  "Copperhall Elite": 4,
  "Crystalline Chalice": 4,
  "Deathstrike": 4,
  "Enlightened Stranger": 4,
  "Feeding Time": 4,
  "Impending Doom": 4,
  "Karmic Guardian": 4,
  "Lethrai Falchion": 4,
  "Longhorn Sergeant": 4,
  "Navani, Warsinger": 4,
  "Nesting Avisaur": 4,
  "Renegade Valkyrie": 4,
  "Righteous Fury": 4,
  "Rise to the Challenge": 4,
  "Soul Collector": 4,
  "Statuary Maiden": 4,
  "Steward of the Past": 4,
  "Stonescar Magus": 4,
  "Subvert": 4,
  "The Great Parliament": 4,
  "Blazing Renegade": 5,
  "Calderan Gunsmith": 5,
  "Centaur Raidleader": 5,
  "Dusthoof Brawler": 5,
  "Elysian Pathfinder": 5,
  "Flash Fire": 5,
  "Idol of Destran": 5,
  "Infernus": 5,
  "Lumen Defender": 5,
  "Obliterate": 5,
  "Reliquary Raider": 5,
  "Shogun of the Wastes": 5,
  "Soulfire Drake": 5,
  "Striking Snake Formation": 5,
  "Towering Terrazon": 5,
  "Twinbrood Sauropod": 5,
  "Aerial Ace": 5,
  "Combrei Magister": 5,
  "Crystallize": 5,
  "Elysian Trailblazer": 5,
  "Harsh Rule": 5,
  "Hooru Fledgling": 5,
  "Jotun Hurler": 5,
  "Jotun Warrior": 5,
  "Magus of the Mist": 5,
  "Marshal Ironthorn": 5,
  "Mithril Mace": 5,
  "Primal Incarnation": 5,
  "Psionic Savant": 5,
  "Silverwing Commander": 5,
  "Skycrag Wyvarch": 5,
  "Staff of Stories": 5,
  "Throne Warden": 5,
  "West-Wind Herald": 5,
  "Windshaper": 5,
  "Ashara, the Deadshot": 5,
  "Champion of Cunning": 5,
  "Cirso, the Great Glutton": 5,
  "Deepforged Plate": 5,
  "Explorer Emeritus": 5,
  "Field Captain": 5,
  "Grasping at Shadows": 5,
  "Hunting Pteriax": 5,
  "Lurking Sanguar": 5,
  "Merciless Stranger": 5,
  "Oblivion Spike": 5,
  "Reality Warden": 5,
  "Runic Revolver": 5,
  "Scraptank": 5,
  "Smuggler's Stash": 5,
  "Spell Swipe": 5,
  "Stronghold's Visage": 5,
  "Umbren Reaper": 5,
  "Warband Chieftain": 5,
  "Withering Witch": 5,
  "Crowd Favorite": 6,
  "Divining Rod": 6,
  "Frontline Cyclops": 6,
  "General Izalio": 6,
  "Hellfire Rifle": 6,
  "Lumen Shepherd": 6,
  "Mystic Ascendant": 6,
  "Predatory Carnosaur": 6,
  "Stonescar Maul": 6,
  "Worldpyre Phoenix": 6,
  "Augmented Form": 6,
  "Celestial Omen": 6,
  "Ceremonial Mask": 6,
  "Civic Peacekeeper": 6,
  "Fourth-Tree Elder": 6,
  "Hatchery Hunter": 6,
  "Jarrall Iceheart": 6,
  "North-Wind Herald": 6,
  "Plated Demolisher": 6,
  "Sapphire Dragon": 6,
  "Scouting Party": 6,
  "Thunderstrike Dragon": 6,
  "Valkyrie Wings": 6,
  "Argenport Ringmaster": 6,
  "Black-Sky Harbinger": 6,
  "Champion of Progress": 6,
  "Direwood Rampager": 6,
  "Ferocious Stranger": 6,
  "Fortunate Stranger": 6,
  "Horsesnatcher Bat": 6,
  "Infernal Tyrant": 6,
  "Minotaur Ambassador": 6,
  "Spirit Drain": 6,
  "Starsteel Daisho": 6,
  "Whispers in the Void": 6,
  "Ancient Terrazon": 7,
  "Claw of the First Dragon": 7,
  "Dormant Sentinel": 7,
  "Hall of Lost Kings": 7,
  "Pillar of Amar": 7,
  "Steelbound Dragon": 7,
  "Araktodon": 7,
  "Flight Lieutenant": 7,
  "Mistveil Drake": 7,
  "Rimescale Draconus": 7,
  "Rolant's Honor Guard": 7,
  "Strength of the Pack": 7,
  "Azindel's Gift": 7,
  "Curiox, the Collector": 7,
  "Icaria, the Liberator": 7,
  "Nightmaw, Sight Unseen": 7,
  "Stonescar Leviathan": 7,
  "Venomspine Hydra": 7,
  "Vodakhan, Temple Speaker": 7,
  "Voprex, the Great Ruin": 7,
  "Kaleb, Uncrowned Prince": 8,
  "Marisen, the Eldest": 8,
  "Talir, Who Sees Beyond": 8,
  "Channel the Tempest": 8,
  "Eilyn, Queen of the Wilds": 8,
  "Rolant, the Iron Fist": 8,
  "Sword of the Sky King": 8,
  "Shimmerpack": 8,
  "Snowcrush Animist": 8,
  "Touch of the Umbren": 8,
  "Vara, Fate-Touched": 8,
  "Lavablood Goliath": 9,
  "Scourge of Frosthome": 10,
  "The Last Word": 9,
  "Fire Sigil": 0,
  "Justice Sigil": 0,
  "Time Sigil": 0,
  "Primal Sigil": 0,
  "Shadow Sigil": 0,
  "A New Tomorrow": 10,
  "The Witching Hour": 24,
  "Amber Monument": 0,
  "Emerald Monument": 0,
  "Granite Monument": 0,
  "Amethyst Monument": 0,
  "Cobalt Monument": 0,
  "Argenport Banner": 0,
  "Combrei Banner": 0,
  "Diplomatic Seal": 0,
  "Elysian Banner": 0,
  "Feln Banner": 0,
  "Hooru Banner": 0,
  "Praxis Banner": 0,
  "Rakano Banner": 0,
  "Seat of Chaos": 0,
  "Seat of Cunning": 0,
  "Seat of Fury": 0,
  "Seat of Glory": 0,
  "Seat of Impulse": 0,
  "Seat of Mystery": 0,
  "Seat of Order": 0,
  "Seat of Progress": 0,
  "Seat of Vengeance": 0,
  "Seat of Wisdom": 0,
  "Skycrag Banner": 0,
  "Stonescar Banner": 0,
  "Xenan Banner": 0,
}


# determined by running a script on my past draft decks to identify each card as the color of the decks that contained it.
CARD_COLORS = {
    "Accelerated Evolution": "PT",
    "Aerial Ace": "P",
    "Ageless Mentor": "TP",
    "Alchemical Blast": "",
    "Amber Acolyte": "T",
    "Amber Monument": "T",
    "Amethyst Acolyte": "S",
    "Amethyst Monument": "SF",
    "Ancient Lore": "T",
    "Annihilate": "S",
    "Argenport Instigator": "S",
    "Argenport Ringmaster": "S",
    "Argenport Soldier": "J",
    "Armorsmith": "JF",
    "Ashara, the Deadshot": "S",
    "Assembly Line": "F",
    "Augmented Form": "J",
    "Auric Bailiff": "J",
    "Auric Runehammer": "J",
    "Auric Sentry": "J",
    "Avalanche Stalker": "P",
    "Awakened Student": "TJ",
    "Back-Alley Bouncer": "S",
    "Backlash": "P",
    "Battleblur Centaur": "FJ",
    "Beastcaller's Amulet": "S",
    "Black-Sky Harbinger": "PS",
    "Blackguard Sidearm": "S",
    "Bladekin Apprentice": "F",
    "Blind Storyteller": "P",
    "Blood Beetle": "S",
    "Bold Adventurer": "T",
    "Brightmace Paladin": "J",
    "Brimstone Altar": "SF",
    "Burn Out": "F",
    "Cabal Countess": "S",
    "Cabal Cutthroat": "S",
    "Cabal Recruiter": "S",
    "Centaur Raidleader": "F",
    "Champion of Chaos": "SF",
    "Champion of Cunning": "PS",
    "Champion of Glory": "FJ",
    "Champion of Progress": "TJ",
    "Channel the Tempest": "P",
    "Charchain Flail": "F",
    "Civic Peacekeeper": "J",
    "Clever Stranger": "F",
    "Cloud of Ash": "F",
    "Cloudsnake Harrier": "P",
    "Cloudsnake Saddle": "P",
    "Cobalt Acolyte": "P",
    "Cobalt Monument": "P",
    "Combrei Banner": "TJ",
    "Combrei Healer": "TJ",
    "Combrei Magister": "FJ",
    "Combrei Stranger": "",
    "Combust": "SF",
    "Copper Conduit": "T",
    "Copperhall Elite": "TJ",
    "Copperhall Recruit": "J",
    "Crown of Possibilities": "TP",
    "Crownwatch Cavalry": "J",
    "Crownwatch Deserter": "FJ",
    "Crownwatch Longsword": "J",
    "Crownwatch Paladin": "J",
    "Crystalline Chalice": "TP",
    "Crystallize": "P",
    "Curiox, the Collector": "TP",
    "Dark Return": "S",
    "Dark Wisp": "S",
    "Dawnwalker": "T",
    "Deathstrike": "S",
    "Deranged Dinomancer": "P",
    "Desert Marshal": "TJ",
    "Desperado": "S",
    "Determined Stranger": "T",
    "Devour": "S",
    "Diplomatic Seal": "",
    "Direfang Spider": "S",
    "Direwood Beastcaller": "S",
    "Dispel": "T",
    "District Infantry": "J",
    "Dormant Sentinel": "T",
    "Dune Phantom": "T",
    "Dusthoof Brawler": "S",
    "East-Wind Herald": "P",
    "Elder's Feather": "J",
    "Elysian Banner": "TP",
    "Elysian Pathfinder": "T",
    "Elysian Stranger": "",
    "Elysian Trailblazer": "P",
    "Emerald Acolyte": "J",
    "Emerald Monument": "J",
    "Enlightened Stranger": "TJ",
    "Execute": "S",
    "Eye of Winter": "P",
    "False Prince": "TP",
    "Fearless Nomad": "FJ",
    "Feeding Time": "PS",
    "Feln Banner": "SP",
    "Feln Bloodcaster": "PS",
    "Feln Stranger": "",
    "Ferocious Stranger": "FJ",
    "Field Captain": "JF",
    "Finest Hour": "J",
    "Fire Sigil": "F",
    "Flame Blast": "F",
    "Flash Freeze": "P",
    "Flight Lieutenant": "J",
    "Forsworn Stranger": "",
    "Fortunate Stranger": "TP",
    "Fourth-Tree Elder": "J",
    "Frontline Cyclops": "F",
    "Furnace Mage": "F",
    "General Izalio": "F",
    "Gilded Glaive": "J",
    "Gorgon Fanatic": "PS",
    "Gorgon Swiftblade": "PS",
    "Granite Acolyte": "F",
    "Granite Monument": "F",
    "Grenadin Drone": "F",
    "Guerrilla Fighter": "F",
    "Hair-Trigger Stranger": "SF",
    "Hammer of Might": "J",
    "Harbinger's Bite": "PS",
    "Harsh Rule": "J",
    "Hatchery Hunter": "P",
    "Haunting Scream": "PS",
    "Hooru Fledgling": "J",
    "Horned Vorlunk": "T",
    "Horsesnatcher Bat": "S",
    "Hunting Pteriax": "PT",
    "Ice Sprite": "P",
    "Icebreaker": "P",
    "Impending Doom": "S",
    "Infernal Tyrant": "SF",
    "Initiate of the Sands": "T",
    "Inspire": "J",
    "Jarrall's Frostkin": "P",
    "Jotun Hurler": "P",
    "Jotun Warrior": "P",
    "Justice Sigil": "J",
    "Karmic Guardian": "TJ",
    "Knifejack": "S",
    "Knight-Chancellor Siraf": "TJ",
    "Lethrai Falchion": "S",
    "Lethrai Nightblade": "S",
    "Lethrai Ranger": "S",
    "Levitate": "P",
    "Lifedrinker": "S",
    "Lightning Storm": "P",
    "Lightning Strike": "P",
    "Longhorn Sergeant": "FJ",
    "Loyal Watchwing": "J",
    "Lumen Defender": "T",
    "Lurking Sanguar": "S",
    "Madness": "S",
    "Magma Javelin": "F",
    "Magus of the Mist": "P",
    "Mark of Shame": "J",
    "Merciless Stranger": "S",
    "Midnight Gale": "PS",
    "Minotaur Grunt": "J",
    "Mirror Image": "P",
    "Mistveil Drake": "P",
    "Mithril Mace": "J",
    "Morningstar": "F",
    "Nesting Avisaur": "TP",
    "New Stranger": "P",
    "Nightmaw, Sight Unseen": "PS",
    "North-Wind Herald": "P",
    "Obliterate": "F",
    "Oblivion Spike": "S",
    "Obsidian Golem": "SF",
    "Old Skycrag Wyvarch": "P",
    "Oni Quartermaster": "F",
    "Oni Ronin": "F",
    "Order of the Spire": "J",
    "Ornamental Daggers": "T",
    "Ornate Katana": "F",
    "Outlands Sniper": "F",
    "Paladin Oathbook": "J",
    "Permafrost": "P",
    "Piercing Shot": "F",
    "Pilfer": "PSF",
    "Pillar of Amar": "T",
    "Pit Fighter": "SF",
    "Plague": "S",
    "Polymorph": "P",
    "Praxis Displacer": "T",
    "Predator's Instinct": "T",
    "Predatory Carnosaur": "T",
    "Primal Sigil": "P",
    "Privilege of Rank": "J",
    "Prosecutor-at-Arms": "J",
    "Protect": "J",
    "Psionic Savant": "P",
    "Pteriax Hatchling": "TP",
    "Pyre Adept": "F",
    "Pyroknight": "F",
    "Rakano Artisan": "JF",
    "Rakano Banner": "FJ",
    "Rakano Outlaw": "F",
    "Rakano Stranger": "",
    "Rally": "F",
    "Rampage": "F",
    "Rapid Shot": "S",
    "Ravenous Thornbeast": "S",
    "Reality Warden": "TJ",
    "Rebel Illuminator": "F",
    "Rebel Sharpshooter": "F",
    "Rebuke": "J",
    "Recogulator": "F",
    "Reinforce": "J",
    "Reliquary Raider": "T",
    "Renegade Valkyrie": "FJ",
    "Rolant's Honor Guard": "J",
    "Ruthless Stranger": "F",
    "Sandstorm Titan": "T",
    "Sapphire Dragon": "P",
    "Sauropod Wrangler": "T",
    "Scaly Gruan": "P",
    "Scavenging Vulture": "S",
    "Scheme": "S",
    "Scorpion Wasp": "T",
    "Scraptank": "SF",
    "Second Sight": "P",
    "Seek Power": "",
    "Serpent Trainer": "P",
    "Shadow Sigil": "S",
    "Shadowlands Guide": "SF",
    "Shogun of the Wastes": "F",
    "Shogun's Scepter": "F",
    "Silverwing Avenger": "J",
    "Silverwing Commander": "J",
    "Silverwing Familiar": "J",
    "Skycrag Wyvarch": "P",
    "Skysnapper": "P",
    "Slagmite Swarm": "SF",
    "Slumbering Stone": "S",
    "Smuggler's Stash": "SF",
    "Soaring Stranger": "P",
    "Soul Collector": "S",
    "Spell Swipe": "PS",
    "Spirit Drain": "S",
    "Squad Strategist": "TJ",
    "Staff of Stories": "P",
    "Stalwart Shield": "J",
    "Static Bolt": "P",
    "Statuary Maiden": "SF",
    "Steelbound Dragon": "F",
    "Steelfang Chakram": "F",
    "Steward of the Past": "S",
    "Stonescar Banner": "SF",
    "Stonescar Magus": "S",
    "Stonescar Maul": "F",
    "Stonescar Stranger": "",
    "Storm Lynx": "PT",
    "Stormcaller": "P",
    "Striking Snake Formation": "T",
    "Suffocate": "S",
    "Swift Stranger": "SF",
    "Sword of Icaria": "FJ",
    "Talir, Who Sees Beyond": "T",
    "Teleport": "T",
    "Temper": "F",
    "Thunderstrike Dragon": "P",
    "Ticking Grenadin": "F",
    "Time Sigil": "T",
    "Tinker Apprentice": "J",
    "Tinker Overseer": "J",
    "Tireless Stranger": "J",
    "Torch": "F",
    "Touch of the Umbren": "S",
    "Towering Terrazon": "T",
    "Towertop Patrol": "T",
    "Treachery": "SF",
    "Treasury Gate": "J",
    "Treasury Guard": "J",
    "Trickster's Cloak": "PS",
    "Tundra Explorer": "P",
    "Twilight Raptor": "PS",
    "Twinbrood Sauropod": "T",
    "Twinning Ritual": "TP",
    "Umbren Reaper": "S",
    "Unlock Potential": "PT",
    "Valkyrie Aspirant": "J",
    "Valkyrie Enforcer": "J",
    "Valkyrie Wings": "J",
    "Valorous Stranger": "J",
    "Vanquish": "J",
    "Vara, Fate-Touched": "S",
    "Venomspine Hydra": "S",
    "Veteran Mercenary": "",
    "Violent Gust": "P",
    "Vodakhan's Staff": "TJ",
    "Voice of the Speaker": "T",
    "Warband Chieftain": "S",
    "Warhelm": "F",
    "West-Wind Herald": "P",
    "Whip Chain": "S",
    "Wild Cloudsnake": "P",
    "Windshaper": "P",
    "Wisdom of the Elders": "P",
    "Withering Witch": "PS",
    "Worldpyre Phoenix": "F",
    "Xenan Destroyer": "S",
    "Xenan Guardian": "T",
    "Xenan Obelisk": "T",
    "Yeti Snowslinger": "P",
    "Yeti Troublemaker": "P",
}