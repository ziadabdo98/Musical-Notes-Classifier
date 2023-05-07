from Note import Note
from Constants import names
import numpy as np
from model import model, independent_dict, independent_list


class Classifier:
    def __init__(self):
        self.model = model

    def classify_staff(self, staff):
        self.data = ""
        self.staff_lines = staff.staff_lines
        notes = staff.get_notes()
        for note in notes:
            self.classify_note(note)
        for i in range(len(notes)):
            sign = notes[i].name
            if sign == "##" or sign == "#" or sign == "&&" or sign == "&":
                if i + 1 != len(notes) - 1:
                    notes[i + 1].name += sign
                    notes[i].name = ""
        for note in notes:
            if note.name != "":
                self.data += " " + note.name
        return self.data

    def classify_note(self, note):
        name = self.__get_least_diff(note.normalized_image)
        if self.__is_position_dependent(name):
            note.name = self.get_note_name(name, note.start_y)
            self.data += " " + note.name
        else:
            note.name = independent_dict[name]
            self.data += " " + note.name

    def __get_least_diff(self, note):
        v, h = calculate_histograms(note)
        diff = []
        for name in names:
            vc, hc = np.array(self.model[name][0]), np.array(self.model[name][1])
            diff.append((name, np.sum(np.abs(vc - v) + np.abs(hc - h))))
        tup = min(diff, key=lambda t: t[1])
        return tup[0]

    def __is_position_dependent(self, name):
        if name in independent_list:
            return False
        else:
            return True

    def get_note_name(self, name, y):
        first_y = self.staff_lines[0].y
        quarter_staff = (self.staff_lines[1].y - self.staff_lines[0].y) / 4
        if name == "normal_note":
            if y > first_y - quarter_staff * 5 and y <= first_y - quarter_staff * 3:
                return "a1/4"
            if y > first_y - quarter_staff * 3 and y <= first_y - quarter_staff * 1:
                return "g1/4"
            if y > first_y - quarter_staff * 1 and y <= first_y + quarter_staff * 1:
                return "f1/4"
            if y > first_y + quarter_staff * 1 and y <= first_y + quarter_staff * 3:
                return "e1/4"
            if y > first_y + quarter_staff * 3 and y <= first_y + quarter_staff * 5:
                return "d1/4"
            return "c1/4"
        if name == "inverted_normal_note":
            if y > first_y - quarter_staff * 9 and y <= first_y - quarter_staff * 7:
                return "b2/4"
            if y > first_y - quarter_staff * 7 and y <= first_y - quarter_staff * 5:
                return "a2/4"
            if y > first_y - quarter_staff * 5 and y <= first_y - quarter_staff * 3:
                return "g2/4"
            if y > first_y - quarter_staff * 3 and y <= first_y - quarter_staff * 1:
                return "f2/4"
            if y > first_y - quarter_staff * 1 and y <= first_y + quarter_staff * 1:
                return "e2/4"
            if y > first_y + quarter_staff * 1 and y <= first_y + quarter_staff * 3:
                return "d2/4"
            if y > first_y + quarter_staff * 3 and y <= first_y + quarter_staff * 5:
                return "c2/4"
            if y > first_y + quarter_staff * 5 and y <= first_y + quarter_staff * 7:
                return "b1/4"
            return "c/4"
        if name == "3_normal_note" or name == "3_normal_note_line":
            if y > first_y - quarter_staff * 5 and y <= first_y - quarter_staff * 3:
                return "{a1/4,d1/4,f1/4}"
            if y > first_y - quarter_staff * 3 and y <= first_y - quarter_staff * 1:
                return "{c1/4,e1/4,g1/4}"
            return "c/4"
        if name == "double_normal_note":
            if y > first_y - quarter_staff * 5 and y <= first_y - quarter_staff * 3:
                return "{a1/4,f1/4}"
            if y > first_y - quarter_staff * 3 and y <= first_y - quarter_staff * 1:
                return "{e1/4,g1/4}"
            if y > first_y - quarter_staff * 1 and y <= first_y + quarter_staff * 1:
                return "{d1/4,f1/4}"
            if y > first_y + quarter_staff * 1 and y <= first_y + quarter_staff * 3:
                return "{c1/4,e1/4}"
            return "c/4"
        if name == "normal_note_1_stripe":
            if y > first_y - quarter_staff * 5 and y <= first_y - quarter_staff * 3:
                return "a1/8"
            if y > first_y - quarter_staff * 3 and y <= first_y - quarter_staff * 1:
                return "g1/8"
            if y > first_y - quarter_staff * 1 and y <= first_y + quarter_staff * 1:
                return "f1/8"
            if y > first_y + quarter_staff * 1 and y <= first_y + quarter_staff * 3:
                return "e1/8"
            if y > first_y + quarter_staff * 3 and y <= first_y + quarter_staff * 5:
                return "d1/8"
            return "c1/8"
        if name == "normal_note_2_stripes":
            if y > first_y - quarter_staff * 5 and y <= first_y - quarter_staff * 3:
                return "a1/16"
            if y > first_y - quarter_staff * 3 and y <= first_y - quarter_staff * 1:
                return "g1/16"
            if y > first_y - quarter_staff * 1 and y <= first_y + quarter_staff * 1:
                return "f1/16"
            if y > first_y + quarter_staff * 1 and y <= first_y + quarter_staff * 3:
                return "e1/16"
            if y > first_y + quarter_staff * 3 and y <= first_y + quarter_staff * 5:
                return "d1/16"
            return "c/8"
        if name == "normal_note_3_stripes":
            if y > first_y - quarter_staff * 7 and y <= first_y - quarter_staff * 5:
                return "a1/32"
            if y > first_y - quarter_staff * 5 and y <= first_y - quarter_staff * 3:
                return "g1/32"
            if y > first_y - quarter_staff * 3 and y <= first_y - quarter_staff * 1:
                return "f1/32"
            if y > first_y - quarter_staff * 1 and y <= first_y + quarter_staff * 1:
                return "e1/32"
            if y > first_y + quarter_staff * 1 and y <= first_y + quarter_staff * 3:
                return "d1/32"
            if y > first_y + quarter_staff * 3 and y <= first_y + quarter_staff * 5:
                return "c1/32"
            return "c1/32"
        if name == "hollow_note":
            if y > first_y - quarter_staff * 5 and y <= first_y - quarter_staff * 3:
                return "a1/2"
            if y > first_y - quarter_staff * 3 and y <= first_y - quarter_staff * 1:
                return "g1/2"
            if y > first_y - quarter_staff * 1 and y <= first_y + quarter_staff * 1:
                return "f1/2"
            if y > first_y + quarter_staff * 1 and y <= first_y + quarter_staff * 3:
                return "e1/2"
            if y > first_y + quarter_staff * 3 and y <= first_y + quarter_staff * 5:
                return "d1/2"
            return "c1/2"
        if name == "hollow_inverted_note":
            if y > first_y - quarter_staff * 9 and y <= first_y - quarter_staff * 7:
                return "b2/2"
            if y > first_y - quarter_staff * 7 and y <= first_y - quarter_staff * 5:
                return "a2/2"
            if y > first_y - quarter_staff * 5 and y <= first_y - quarter_staff * 3:
                return "g2/2"
            if y > first_y - quarter_staff * 3 and y <= first_y - quarter_staff * 1:
                return "f2/2"
            if y > first_y - quarter_staff * 1 and y <= first_y + quarter_staff * 1:
                return "e2/2"
            if y > first_y + quarter_staff * 1 and y <= first_y + quarter_staff * 3:
                return "d2/2"
            if y > first_y + quarter_staff * 3 and y <= first_y + quarter_staff * 5:
                return "c2/2"
            if y > first_y + quarter_staff * 5 and y <= first_y + quarter_staff * 7:
                return "b1/2"
            return "c/2"
        if name == "double_beam_4_equal":
            if y > first_y - quarter_staff * 5 and y <= first_y - quarter_staff * 3:
                return "{a1/16,a1/16,a1/16,a1/16}"
            if y > first_y - quarter_staff * 3 and y <= first_y - quarter_staff * 1:
                return "{g1/16,g1/16,g1/16,g1/16}"
            if y > first_y - quarter_staff * 1 and y <= first_y + quarter_staff * 1:
                return "{f1/16,f1/16,f1/16,f1/16}"
            if y > first_y + quarter_staff * 1 and y <= first_y + quarter_staff * 3:
                return "{e1/16,e1/16,e1/16,e1/16}"
            if y > first_y + quarter_staff * 3 and y <= first_y + quarter_staff * 5:
                return "{d1/16,d1/16,d1/16,d1/16}"
            return "c1/16"
        return ""


def calculate_histograms(image):
    v = []
    image = image.astype(bool)
    for i in range(0, image.shape[1] - 1, 10):
        row = image[i : i + 9, :]
        v.append(np.sum(row, dtype=float))
    h = []
    for i in range(0, image.shape[0] - 1, 10):
        col = image[:, i : i + 9]
        h.append(np.sum(col, dtype=float))
    return np.array(v), np.array(h)
