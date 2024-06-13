from .anyType import anyType

class Number_Counter_invAIder:
    def __init__(self):
        self.counter_x = 0
        self.restartMySelf = False
        self.mode_1 = None
        self.mode_2 = None
        self.started = False
        self.previous_output = None

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mode": (["Loop", "Stop_at_stop", "No_Stop"],),
                "start": ("FLOAT", {"default": 0, "min": 0, "max": 100000, "step": 1}),
                "stop": ("FLOAT", {"default": 1, "min": 0, "max": 100000, "step": 1}),
                "step": ("FLOAT", {"default": 0.1, "min": 0.01, "max": 100000, "step": 1}),
            },
            "optional": {
                "restart": (anyType,),
                "hold": (anyType,),
            },
        }

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

    RETURN_TYPES = (anyType, "INT", "STRING")
    RETURN_NAMES = ("ANY", "COUNT", "info")

    FUNCTION = "node"
    CATEGORY = "👾 invAIder"

    def node(self, mode, start, stop, step, restart=0, hold=0):

        # Treat the restart and hold inputs as truthies
        restart = bool(restart)
        hold = bool(hold)

        # Define my mode
        mode_1 = mode
        mode_2 = 'increment' if start < stop else 'decrement'

        # Hold last values if hold is true, no restart, and if node was ran atleast once
        # Note that 'hold' prioritizes over self_restarts but not restarts
        if hold and not restart and self.previous_output is not None:
            counter = self.counter_x
            count = self.previous_output[1] if self.previous_output is not None else 0
        else:
            if self.restartMySelf or restart:
                self.started = False
                self.restartMySelf = False
                self.previous_output = None #Set to 0 to distinguish
                self.counter_x = start
        
            if self.mode_1 == mode_1 and self.mode_2 == mode_2:
                if self.started:
                    if not stop == start:
                        counter = self.counter_x
                        counter = counter + step if mode_2 == 'increment' else counter - step
                        counter = round(counter, 3)
                        FloatBugFix = 0.005
                        if mode_1 != "No_Stop":
                            if mode_2 == 'increment' and counter >= stop - FloatBugFix:
                                counter = stop
                                if mode_1 == "Loop":
                                    self.restartMySelf = True
                            elif mode_2 == 'decrement' and counter <= stop + FloatBugFix:
                                counter = stop
                                if mode_1 == "Loop":
                                    self.restartMySelf = True
                        counter = counter if counter >= 0 else 0
                    else:
                        counter = start
                else:
                    self.started = True
                    counter = start
            else:
                self.started = True
                counter = start

            if step != 0:
                count = int(abs((stop - start) / step)) + 1  # Calculate the total number of steps
            else:
                count = 0  # If step is 0, there are no steps

            self.mode_1 = mode_1
            self.mode_2 = mode_2
            self.counter_x = counter

        # Info output
        info = f"Mode: {mode}"
        info += f"\nOutput: {counter}"

        if mode_1 != "No_Stop":
            if mode_1 == "Loop":
                info += "\nLoop in: "
            elif mode_1 == "Stop_at_stop":
                info += "\nEnd in: "
            info += str(int(abs((stop - self.counter_x) / step))) if step != 0 else "∞"
            info += "\nCount: " + str(count)

        info += "\nRestart: " + str(restart)
        info += "\nHold: " + str(hold)

        output = (counter, count, info,)

        self.previous_output = output

        return output