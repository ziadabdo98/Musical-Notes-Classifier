import numpy as np
from Note import Note
import Constants


class Staff:
    def __init__(self, sy, ey, sx, ex, image, staff_lines):
        self.start_y = sy
        self.end_y = ey
        self.start_x = sx
        self.end_x = ex
        self.image = image
        self.staff_lines = staff_lines

    def get_notes(self):
        notes = []
        i = 0
        start = end = None
        while i < self.image.shape[1]:
            column = self.image[:, i]
            if np.any(column):
                if start is None:
                    start = i
            else:
                if start is not None:
                    end = i
                    image = np.copy(self.image[:, start:end])
                    if image.shape[1] > Constants.MINIMUM_NOTE_WIDTH:
                        notes.append(
                            Note(
                                self.start_y,
                                self.end_y,
                                start + self.start_x,
                                end + self.start_x,
                                image,
                            )
                        )
                    start = None
            i += 1

        notes = self.__remove_one_color_notes(notes)
        imgs = []
        for note in notes:
            imgs.append(note.normalized_image)
        return notes

    # Remove fully black or white notes
    def __remove_one_color_notes(self, notes):
        for note in notes:
            img = note.image
            if np.all(img == 0) or np.all(img == 1):
                notes.remove(note)

        return notes
