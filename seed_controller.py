from .anyType import anyType
import random

class SeedControl_invAIder:
    def __init__(self):
        self.last_seed = None
        self.saved_seeds_indx = 0
        self.saved_seeds = []

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mode": (["1:fixed", "2:increment", "3:decrement", "4:randomize", "5:saved", "use mode_sel"],),
                "start_seed": ("INT", {"default": -1, "min": -1, "max": 0xffffffffffffffff, "step": 1}),
            },
            "optional": {
                "restart": (anyType,),
                "hold": (anyType,),
                "save": (anyType,),
                "mode_sel": (anyType,),
            },
        }

    OUTPUT_NODE = True

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

    RETURN_TYPES = ("INT", "STRING",)
    RETURN_NAMES = ("SEED", "info",)

    FUNCTION = "node"
    CATEGORY = "👾 invAIder"

    def node(self, mode, start_seed, restart=0, hold=0, save=0, mode_sel=1):
        # Convert the anyType inputs to their correct modes
        restart = bool(restart)
        hold = bool(hold)
        save = bool(save)
        mode_sel = int(mode_sel)

        # Initialize the 'seed' variable if self.last_seed is None
        if self.last_seed is None:
            self.last_seed = start_seed

        seed = self.last_seed

        # Variable to track the true final mode (for info printout)
        true_mode = ""

        # If restart is set or changed...
        if restart:
            self.saved_seeds_indx = 0
            self.saved_seeds = []

        # Fixed
        if mode == "1:fixed" or (mode == "use mode_sel" and mode_sel == 1):
            true_mode = "Fixed"
            seed = self.last_seed
        # Increment
        elif mode == "2:increment" or (mode == "use mode_sel" and mode_sel == 2):
            true_mode = "Increment"
            seed = min(self.last_seed + 1, 0xffffffffffffffff)
        # Decrement
        elif mode == "3:decrement" or (mode == "use mode_sel" and mode_sel == 3):
            true_mode = "Decrement"
            seed = max(self.last_seed - 1, 0)
        # Randomize
        elif mode == "4:randomize" or (mode == "use mode_sel" and mode_sel == 4):
            true_mode = "Randomize"
            seed = -1
        # Saved
        elif mode == "5:saved" or (mode == "use mode_sel" and mode_sel == 5):
            true_mode = "Saved"
            if len(self.saved_seeds) == 0:
                seed = -1
            else:
                seed = self.saved_seeds[self.saved_seeds_indx]
                if not hold:
                    self.saved_seeds_indx = (self.saved_seeds_indx + 1) % len(self.saved_seeds)

        # If restart, set seed to start_seed
        if restart:
            seed = start_seed
        # ElseIf held, set seed to last seed
        elif hold:
            seed = self.last_seed 

        # Convert special "-1" seed syntax to a random number
        if seed == -1:
            seed = random.randrange(0, 0xffffffffffffffff + 1)

        # If saving a seed, append a new entry in the 'saved_seeds' array
        if save == 1 and true_mode != "Saved" and not hold:
            self.saved_seeds.append(seed)

        # Update this instance's last seed and previous restart value
        self.last_seed = seed
        self.previous_restart = restart

        # Info printout
        info = "Mode: " + true_mode + "\n"
        info += "Seed: " + str(seed) + "\n"
        info += "Restart: " + str(restart) + "\n"
        info += "Hold: " + str(hold == 1) + "\n"

        # Append saved seeds info if any are saved
        if self.saved_seeds:
            saved_seeds_info = "\n".join(f"{i+1}) {seed}" for i, seed in enumerate(self.saved_seeds))
            info += "Saved Seeds (indx=" + str(self.saved_seeds_indx+1) + "):\n" + saved_seeds_info + "\n"

        return (seed, info,)