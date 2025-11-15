from Bots.marks_coding_corner.VoltaicSpearTeamFarm import open_final_chest
from Py4GWCoreLib import Botting, Routines, GLOBAL_CACHE, ModelID, Range, Utils, ConsoleLog
import Py4GW
import os
# ALLOWED_MAPS = [638, 558]  # Gadds Encampment, Sparkfly Swamp

BOT_NAME = "BOOG"
TEXTURE = os.path.join(Py4GW.Console.get_projects_path(), "Bots", "Vanquish", "VQ_Helmet.png")
OUTPOST_TO_TRAVEL = 638  # Gadds encampment


Too_Boog_Path: list[tuple[float, float]] = [
    (-9706.96, -18226.23),  # First waypoint - get blessing here
    (-4487.20, -11839.81),  # Continue path
    (-4184.71, -6247.72),
    (-3828.28, -2655.30),
    (-846.20, 1021.55),
    (4141.44, 7805.86),
    (6063.04, 16119.25),
    (10083.08, 21992.15), # Final waypoint
]

Boog_lvl1: list[tuple[float, float]] = [
    (17192.66, 2597.08),
    (17895.35, 4717.28),
    (17992.93, 4804.98),
    (18277.31, 7647.05),
    (15546.85, 10094.44),
    (10962.63, 11092.09),
    (9433.01, 9707.25),
    (6031.89, 7901.37),
    (4935.79, 1886.17),
    (256.57, -1792.90),
    (-888.11, -4078.04),
    (-1096.31, -6477.00),
    (642.94, -9310.18),
    (1460.26, -12544.18),
    (2861.14, -15491.92),
    (6507.46, -16994.93),
    (7387.50, -18442.89),
    (7541.45, -18826.75),
]

Boog_lvl2_to_first_boss: list[tuple[float, float]] = [
    (-10574.06, -4620.96),
    (-7652.74, -2095.13),
    (-9326.92, -1771.17),
    (-8482.91, 679.28),
    (-4325.99, 4211.24),
    (-2803.12, 6936.79),
    (-582.90, 8734.06),
    (-280.81, 10950.48),
    (3677.35, 13785.09),
    (5506.90, 13586.20), #kanske missade ett snepp här
    (6602.60, 10130.08),
    (7876.17, 7353.99),
    (8421.37, 2800.72), #to first boss-room
]

Boog_lvl2_kill_first_boss: list[tuple[float, float]] = [
    (8735.67, 1536.08),
    (9431.43, -867.45),
    (11105.88, -5283.65),
    (13319.63, -6206.42),
    (15940.67, -6119.35),
]

Boog_lvl2_run_to_Final_boss: list[tuple[float, float]] = [
    (17925.77, -8922.50),
    (17198.06, -11824.11),
    (19229.74, -11825.55),
]

Boog_lvl2_kill_Final_boss: list[tuple[float, float]] = [
    (17528.61, -14078.98),
    (15201.93, -15034.60),
    (13545.31, -17510.12),
    (15186.46, -18893.94),
]



bot = Botting(BOT_NAME,
              upkeep_honeycomb_active=True)


def bot_routine(bot: Botting) -> None:
    global Vanquish_Path
    # events
    condition = lambda: OnPartyWipe(bot)
    bot.Events.OnPartyWipeCallback(condition)
    # end events

    #Travel to outpost and exit
    bot.States.AddHeader(BOT_NAME)  #1?
    bot.Templates.Multibox_Aggressive()
    bot.Templates.Routines.PrepareForFarm(map_id_to_travel=OUTPOST_TO_TRAVEL)
    bot.Party.SetHardMode(False)
    bot.Move.XYAndExitMap(-9554.00, -20148.00, 558)    # Enter Sparkfly Swamp
    bot.Wait.ForTime(4000)  # Do I really need this?


    bot.States.AddHeader("Run to Dungeon")  # 2
    #bot.Move.XYAndInteractNPC(-9002.13, -19823.62)  Saving time, not using this
    #bot.Multibox.SendDialogToTarget(0x84)  # Get blessing  Saving time, not using this
    bot.Move.FollowPath(Too_Boog_Path)

    bot.States.AddHeader("Take Quest and enter dungeon") #3
    bot.Templates.Multibox_Aggressive()
    bot.Move.XYAndInteractNPC(12503.00, 22721.00)  # Drop quest in town and re-take always?
    bot.Multibox.SendDialogToTarget(0x833901)
    bot.Wait.ForTime(2000)
    bot.Move.XYAndInteractNPC(12490.09, 22550.11)
    bot.Multibox.SendDialogToTarget(0x833905)
    bot.Move.XYAndExitMap(13034.00, 26391.00, 615)

    bot.States.AddHeader("Level1 - start") #4
    bot.Templates.Multibox_Aggressive()  # Bara tillfälligt för att attackera, körs i början annars.
    bot.Multibox.UseAllConsumables()
    bot.States.AddManagedCoroutine("Upkeep Multibox Consumables", lambda: _upkeep_multibox_consumables(bot))
    bot.Move.FollowAutoPath(Boog_lvl1, "Level 1")
    bot.Move.XYAndExitMap(7801.38, -19287.83, 616)

    bot.States.AddHeader("Level2 - start") #5
    bot.Templates.Multibox_Aggressive()
    bot.Move.XYAndInteractNPC(-11055.00, -5533.00, "Get blessing")
    bot.Multibox.SendDialogToTarget(0x84)
    bot.Move.FollowAutoPath(Boog_lvl2_to_first_boss, "Level 2_to_first_boss")
    bot.States.AddHeader("Level2 - First boss")  #6
    bot.Move.FollowAutoPath(Boog_lvl2_kill_first_boss, "Level 2_kill_first_boss")
    bot.Move.XYAndInteractGadget(17901.49, -6258.27, "Try to interact gadget")
    bot.States.AddHeader("Level2 - Run to last boss")  #7
    bot.Move.FollowAutoPath(Boog_lvl2_run_to_Final_boss)


    bot.States.AddHeader("Level2 - Final boss")
    bot.Templates.Multibox_Aggressive()
    bot.Move.FollowAutoPath(Boog_lvl2_kill_Final_boss)


    bot.States.AddHeader("Take quest reward & Loot chest")
    bot.Move.ToModel(6744, "testa nå tekks")
    bot.Interact.WithModel(6744)
    bot.Multibox.SendDialogToTarget(0x833907)

    bot.States.AddHeader("Loot chest")
    bot.Move.XYAndInteractGadget(15130.66, -19158.59)
    bot.Move.XYAndInteractGadget(14985.91, -19117.45, "Loot chest")
    bot.Interact.WithGadgetAtXY(15030.00, -19168.00)


    bot.Wait.ForMapToChange(558)
   

# take quest Giriff 0x832201
# update quest Giriff 0x832205



    #bot.Wait.UntilOutOfCombat()
    #bot.States.AddCustomState(lambda: _reverse_path(), "Reverse Path") #if not VQ we reverse path
    #bot.Move.FollowAutoPath(Vanquish_Path, "Return Route")
    #bot.Wait.UntilOutOfCombat()

    #bot.Multibox.ResignParty()
    ConsoleLog("TEST, finished script", "TEST, finished script")

    try:
        # Hämta alla state-namn direkt från FSM
        all_states = [s.name for s in bot.config.FSM.states]
        target_state = None
        for name in all_states:
            if "Take Quest and enter dungeon" in name:
                target_state = name
                bot.Templates.Multibox_Aggressive()
                break

        if target_state:
            ConsoleLog(f"Jumping to state: {target_state}", BOT_NAME)
            bot.Templates.Multibox_Aggressive()
            bot.States.JumpToStepName(target_state)
        else:
            ConsoleLog("Header not found — restarting FSM", BOT_NAME)
            bot.config.FSM.jump_to_state_by_index(0)

    except Exception as e:
        ConsoleLog(f"Jump failed ({e}) — restarting FSM", BOT_NAME)
        bot.config.FSM.jump_to_state_by_index(0)


def _upkeep_multibox_consumables(bot: "Botting"):
    while True:
        yield from bot.helpers.Wait._for_time(15000)
        if not Routines.Checks.Map.MapValid():
            continue

        if Routines.Checks.Map.IsOutpost():
            continue

        yield from bot.helpers.Multibox._use_consumable_message((ModelID.Essence_Of_Celerity.value,
                                                                 GLOBAL_CACHE.Skill.GetID(
                                                                     "Essence_of_Celerity_item_effect"), 0, 0))
        yield from bot.helpers.Multibox._use_consumable_message((ModelID.Grail_Of_Might.value,
                                                                 GLOBAL_CACHE.Skill.GetID("Grail_of_Might_item_effect"),
                                                                 0, 0))
        yield from bot.helpers.Multibox._use_consumable_message((ModelID.Armor_Of_Salvation.value,
                                                                 GLOBAL_CACHE.Skill.GetID(
                                                                     "Armor_of_Salvation_item_effect"), 0, 0))
        yield from bot.helpers.Multibox._use_consumable_message((ModelID.Birthday_Cupcake.value,
                                                                 GLOBAL_CACHE.Skill.GetID("Birthday_Cupcake_skill"), 0,
                                                                 0))
        yield from bot.helpers.Multibox._use_consumable_message((ModelID.Golden_Egg.value,
                                                                 GLOBAL_CACHE.Skill.GetID("Golden_Egg_skill"), 0, 0))
        yield from bot.helpers.Multibox._use_consumable_message((ModelID.Candy_Corn.value,
                                                                 GLOBAL_CACHE.Skill.GetID("Candy_Corn_skill"), 0, 0))
        yield from bot.helpers.Multibox._use_consumable_message((ModelID.Candy_Apple.value,
                                                                 GLOBAL_CACHE.Skill.GetID("Candy_Apple_skill"), 0, 0))
        yield from bot.helpers.Multibox._use_consumable_message((ModelID.Slice_Of_Pumpkin_Pie.value,
                                                                 GLOBAL_CACHE.Skill.GetID("Pie_Induced_Ecstasy"), 0, 0))
        yield from bot.helpers.Multibox._use_consumable_message((ModelID.Drake_Kabob.value,
                                                                 GLOBAL_CACHE.Skill.GetID("Drake_Skin"), 0, 0))
        yield from bot.helpers.Multibox._use_consumable_message((ModelID.Bowl_Of_Skalefin_Soup.value,
                                                                 GLOBAL_CACHE.Skill.GetID("Skale_Vigor"), 0, 0))
        yield from bot.helpers.Multibox._use_consumable_message((ModelID.Pahnai_Salad.value,
                                                                 GLOBAL_CACHE.Skill.GetID("Pahnai_Salad_item_effect"),
                                                                 0, 0))
        yield from bot.helpers.Multibox._use_consumable_message((ModelID.War_Supplies.value,
                                                                 GLOBAL_CACHE.Skill.GetID("Well_Supplied"), 0, 0))
        for i in range(1, 5):
            GLOBAL_CACHE.Inventory.UseItem(ModelID.Honeycomb.value)
            yield from bot.helpers.Wait._for_time(250)


def _reverse_path():
    global Vanquish_Path
    if GLOBAL_CACHE.Map.GetIsVanquishComplete():
        Vanquish_Path = []
        yield
        return

    Vanquish_Path = list(reversed(Vanquish_Path))
    yield


def _on_party_wipe(bot: "Botting"):
    while GLOBAL_CACHE.Agent.IsDead(GLOBAL_CACHE.Player.GetAgentID()):
        yield from bot.Wait._for_time(1000)  # ✅ Rätt namespace
        if not Routines.Checks.Map.MapValid():
            # Map invalid → release FSM and exit
            bot.config.FSM.resume()
            return

    ConsoleLog("Party revived — restoring aggressive combat template", BOT_NAME)
    bot.Templates.Multibox_Aggressive()

        # Player revived on same map → jump to recovery step
    try:
        bot.States.JumpToHeader("Level1 - start")
    except AttributeError:
        for state in bot.config.FSM.states:
            if "Level1 - start" in state.name:
                bot.States.JumpToStepName(state.name)
                break
    bot.config.FSM.resume()


def OnPartyWipe(bot: "Botting"):
    ConsoleLog("on_party_wipe", "event triggered")
    fsm = bot.config.FSM
    fsm.pause()
    fsm.AddManagedCoroutine("OnWipe_OPD", lambda: _on_party_wipe(bot))


bot.SetMainRoutine(bot_routine)


def main():
    bot.Update()
    bot.UI.draw_window(icon_path=TEXTURE)


if __name__ == "__main__":
    main()