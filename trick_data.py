from item_data import Items
from trick import Trick


class Tricks:
    sbj_underwater_no_hjb = Trick(Items.Morph, Items.Speedball)
    """ underwater springball jump - no hi jump boots """

    sbj_underwater_w_hjb = Trick(Items.Morph, Items.Speedball, Items.HiJump)
    """ underwater springball jump with hi jump boots """

    sbj_wall = Trick(Items.Morph, Items.Speedball)
    """ springball jump off of a wall jump - not underwater """

    uwu_2_tile = Trick()
    """ underwater wall jumps between left and right in a 2-tile wide space """

    gravity_jump = Trick(Items.GravitySuit)
    """ remove aqua suit right after jumping for extra jump height in water """

    hell_run_hard = Trick()
    """ heated or cold without varia hell runs requiring the minimum amount of energy """

    hell_run_medium = Trick()
    """ heated or cold without varia hell runs requiring 1.5x energy """

    hell_run_easy = Trick()
    """ heated or cold without varia hell runs requiring 2x energy """

    movement_moderate = Trick()
    """ moderately fast/precise movement """

    movement_zoast = Trick()
    """ difficult fast/precise movement """

    wall_jump_delayed = Trick()
    """
    need to jump as far from the wall as possible
    (like top of hive crossways left side, or vanilla getting up to gauntlet)
    """

    wall_jump_precise = Trick()
    """ around wide ledges (2 tiles without hjb, 3 tiles with hjb) """

    mockball_hard = Trick(Items.Morph)
    """ short hop or short run (warrior shrine) """

    morph_jump_3_tile = Trick(Items.Morph)
    """ mid-air morph in a 3-tile-high space (no water) """

    morph_jump_4_tile = Trick(Items.Morph)
    """ mid-air morph in a 4-tile-high space (no water) """

    morph_jump_3_tile_water = Trick(Items.Morph)
    """ mid-air morph in a 3-tile-high space in water """

    crouch_or_downgrab = Trick()
    """ use crouch jump and/or down-grab to jump to higher ledge """

    crouch_precise = Trick()
    """ crouch jump along with some precision movement (not just straight up and over at the top) """

    dark_easy = Trick()
    """ without dark visor, move through darker rooms where walls are light-colored (Spore Field) """

    dark_medium = Trick()
    """ without dark visor, move through darker rooms where walls are NOT light-colored (Meandering Passage) """

    dark_hard = Trick()
    """ without dark visor, move through very dark rooms (Dark Crevice) """

    freeze_hard = Trick(Items.Ice)
    """
    freeze an enemy that's difficult to freeze in the right place, because of erratic/fast/dangerous movement

    an example of an enemy that's NOT hard to freeze in the right place is Choot (pancake)
    """

    wave_gate_glitch = Trick()
    """ shoot a normal beam through a wave gate """

    clip_crouch = Trick()
    """ jump into a 2-tile high space crouched to clip through the ceiling """

    short_charge_2 = Trick(Items.SpeedBooster)
    """ charge shinespark in smaller running space - 2 tap """

    short_charge_3 = Trick(Items.SpeedBooster)
    """ charge shinespark in smaller running space - 3 tap """

    short_charge_4 = Trick(Items.SpeedBooster)
    """ charge shinespark in smaller running space - 4 tap """

    searing_gate_tricks = Trick(Items.Morph)
    """ "It's a secret to everybody." """
