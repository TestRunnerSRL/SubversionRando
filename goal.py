import random
import struct

events = [
	[(0x40, "KR", "KRAID")],
	[(0x49, "SS", "SPORE SPAWN")],
	[(0x4A, "BT", "BOMB TORIZO")],
	[(0x50, "DR", "DRAYGON")],
	[(0x51, "DT", "DUST TORIZO")],
	[(0x52, "GT", "GOLD TORIZO")],
	[(0x58, "CR", "CROCOMIRE")],
	[(0x60, "RI", "RIDLEY"), (0x61, "PH", "PHANTOON")],
	[(0x6A, "HT", "HYPER TORIZO")],
	[(0x1D, "SP", "CRASH SPACE PORT"), (0x79, "BO", "BOTWOON")],
	[(0x1F, "PO", "POWER OFF")],
]

hints = [
	0x2ffaf4, # GFS DAPHNE MAP STATION
	0x2ffb02, # ORBITAL MAP STATION
	0x2ffb82, # REEF MAP STATION
	0x2ffb46, # SUZI RUINS MAP STATION
	0x2ffbe2, # VULNAR PEAK MAP STATION
	0x2ffbc2, # HYDRAULIC WORKS MAP STATION
	0x2ffcfa, # JUNGLE RUINS MAP STATION
	0x2ffc82, # LABORATORY MAP STATION
	0x2ffe2a, # MINES MAP STATION
	0x2ffd72, # HIVE MAP STATION
	0x2ffe38, # VULNAR CAVES MAP STATION
	0x2fff50, # OCEANIA MAP STATION
	0x2ffc8a, # WRECKED MAP STATION
]

text_free = 0x2fd600

#spoiler = 0x2ffc8a # WRECKED MAP STATION
event_address = 0x780d3 + 2

def GenerateGoals(romWriter, count):
	goals = [random.sample(subgoals, 1)[0] for subgoals in random.sample(events, count)]

	data = bytes([goal[0] for goal in goals])
	romWriter.writeBytes(event_address, data)

	remaining_hints = list(hints)
	random.shuffle(remaining_hints)

	new_text_free = text_free

	for i,hint in enumerate(remaining_hints):
		i = i % len(goals)
		goal = goals[i]
		message = f'GOAL {chr(ord("A") + i)} {goal[2]}'.encode('ASCII')

		romWriter.writeBytes(hint, struct.pack('<H', new_text_free & 0xFFFF))
		romWriter.writeBytes(new_text_free, bytes([len(message)]))
		romWriter.writeBytes(new_text_free+1, message)
		new_text_free += len(message) + 1

	#message = 'GOALS ' + ' '.join(goal[1] for goal in goals)
	#message = message.encode('ASCII')
	#romWriter.writeBytes(spoiler, struct.pack('<H', new_text_free & 0xFFFF))
	#romWriter.writeBytes(new_text_free, bytes([len(message)]))
	#romWriter.writeBytes(new_text_free+1, message)

