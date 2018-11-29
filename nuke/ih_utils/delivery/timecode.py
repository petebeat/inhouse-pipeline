class TimeCode():
    # no drop frame supported yet
    fps = 24.0
    hours = 0
    minutes = 0
    seconds = 0
    frames = 0
    frameno = 0

    def __init__(self, inputvalue, inputfps=None):
        if not inputfps == None:
            self.fps = float(inputfps)
        # looks like we are a frame number
        if isinstance(inputvalue, int) or isinstance(inputvalue, float):
            floatinputvalue = float(inputvalue)
            self.hours = int(floatinputvalue / 3600 / self.fps)
            self.minutes = int((floatinputvalue - (self.hours * 3600 * self.fps)) / 60 / self.fps)
            self.seconds = int(
                (floatinputvalue - (self.hours * 3600 * self.fps) - (self.minutes * 60 * self.fps)) / self.fps)
            self.frames = int(floatinputvalue - (self.hours * 3600 * self.fps) - (self.minutes * 60 * self.fps) - (
            self.seconds * self.fps))
            self.frameno = int(floatinputvalue)
        else:
            if inputvalue == "" or inputvalue == None:
                raise ValueError("TimeCode: Error: Timecode provided to constructor may not be blank or null.")
            input_list = inputvalue.split(':')
            if len(input_list) > 4:
                raise ValueError("TimeCode: Error: Timecode provided to constructor must be of the format HH:MM:SS:FF.")
            elif len(input_list) == 4:
                if int(input_list[3]) >= self.fps or int(input_list[3]) < 0:
                    raise ValueError(
                        "TimeCode: Error: Frames provided must not be greater than FPS rate of %d or less than zero." % self.fps)
                if int(input_list[2]) > 59 or int(input_list[2]) < 0:
                    raise ValueError("TimeCode: Error: Seconds provided must not be greater than 59 or less than zero.")
                if int(input_list[1]) > 59 or int(input_list[1]) < 0:
                    raise ValueError("TimeCode: Error: Minutes provided must not be greater than 59 or less than zero.")
                if int(input_list[0]) > 23 or int(input_list[0]) < 0:
                    raise ValueError("TimeCode: Error: Hours provided must not be greater than 23 or less than zero.")
                self.hours = int(input_list[0])
                self.minutes = int(input_list[1])
                self.seconds = int(input_list[2])
                self.frames = int(input_list[3])
            elif len(input_list) == 3:
                if int(input_list[2]) >= self.fps or int(input_list[2]) < 0:
                    raise ValueError(
                        "TimeCode: Error: Frames provided must not be greater than FPS rate of %d or less than zero." % self.fps)
                if int(input_list[1]) > 59 or int(input_list[1]) < 0:
                    raise ValueError("TimeCode: Error: Seconds provided must not be greater than 59 or less than zero.")
                if int(input_list[0]) > 59 or int(input_list[0]) < 0:
                    raise ValueError("TimeCode: Error: Minutes provided must not be greater than 59 or less than zero.")
                self.minutes = int(input_list[0])
                self.seconds = int(input_list[1])
                self.frames = int(input_list[2])
            elif len(input_list) == 2:
                if int(input_list[1]) >= self.fps or int(input_list[1]) < 0:
                    raise ValueError(
                        "TimeCode: Error: Frames provided must not be greater than FPS rate of %d or less than zero." % self.fps)
                if int(input_list[0]) > 59 or int(input_list[0]) < 0:
                    raise ValueError("TimeCode: Error: Seconds provided must not be greater than 59 or less than zero.")
                self.seconds = int(input_list[0])
                self.frames = int(input_list[1])
            elif len(input_list) == 1:
                if int(input_list[0]) >= self.fps or int(input_list[0]) < 0:
                    raise ValueError(
                        "TimeCode: Error: Frames provided must not be greater than FPS rate of %d or less than zero." % self.fps)
                self.frames = int(input_list[0])
            self.frameno = (self.hours * 3600 * self.fps) + (self.minutes * 60 * self.fps) + (
            self.seconds * self.fps) + self.frames

    def __str__(self):
        return "%02d:%02d:%02d:%02d" % (self.hours, self.minutes, self.seconds, self.frames)

    def __repr__(self):
        return "TimeCode(\"%02d:%02d:%02d:%02d\", inputfps=%d)" % (
        self.hours, self.minutes, self.seconds, self.frames, self.fps)

    def frame_number(self):
        return self.frameno

    def time_code(self):
        return "%02d:%02d:%02d:%02d" % (self.hours, self.minutes, self.seconds, self.frames)

    def __add__(self, inputobject):
        inttco = None
        if isinstance(inputobject, TimeCode):
            inttco = inputobject
        else:
            inttco = TimeCode(inputobject)
        newframeno = self.frameno + inttco.frameno
        numdays = int(newframeno / (24 * 3600 * inttco.fps))
        if numdays > 0:
            newframeno = newframeno - (numdays * 24 * 3600 * inttco.fps)
        rettco = TimeCode(newframeno)
        return rettco

    def __sub__(self, inputobject):
        inttco = None
        if isinstance(inputobject, TimeCode):
            inttco = inputobject
        else:
            inttco = TimeCode(inputobject)
        newframeno = self.frameno - inttco.frameno
        numdays = abs(int(newframeno / (24 * 3600 * inttco.fps)))
        if numdays > 0:
            newframeno = newframeno + (numdays * 24 * 3600 * inttco.fps)
        if newframeno < 0:
            newframeno = newframeno + (24 * 3600 * inttco.fps)
        rettco = TimeCode(newframeno)
        return rettco
