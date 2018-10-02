'''
Module containing archery objects.
'''

import random

class Arrow:
    '''
    Arrow class for shooting targets.
    '''
    def __init__(self, f_colour, n_fletch, s_length, s_material):
        '''
        :param f_colour: String; fletch colour
        :param n_fletches: Int; number of fletches on the arrow
        :param s_length: Int; length of shaft in inches
        :param s_material: String; shaft material
        '''
        self.f_colour = f_colour
        self.n_fletch = n_fletch
        self.s_length = s_length
        self.s_material = s_material
        self.nocked = False
        self.nocked_on = None

    def nock(self, bow):
        '''
        :param bow: Bow; bow to which the arrow is nocked
        '''
        self.nocked = True
        self.nocked_on = bow.name


class Bow:
    '''
    '''
    def __init__(self, brand, limb_colour, limb_len, limb_mat, limb_weight,
        name, riser_colour, riser_len, riser_mat):
        '''
        :param brand: String; maker of the bow
        :param limb_colour: String; colour of the limbs
        :param limb_len: Int; length of the limbs in inches
        :param limb_mat: String; material of the limbs
        :param limb_weight: Int; weight of the limbs in pounds
        :param name: String; name of the bow
        :param riser_colour: String; colour of the riser
        :param riser_len: Int; length of the riser in inches
        :param riser_mat: String; material of the riser
        '''
        self.brand = brand
        self.limb_colour = limb_colour
        self.limb_len = limb_len
        self.limb_mat = limb_mat
        self.limb_weight = limb_weight
        self.name = name
        self.riser_colour = riser_colour
        self.riser_len = riser_len
        self.riser_mat = riser_mat
        self.assembled = False
        self.tuned = False
        self.shots = 0

    def assemble(self):
        '''
        '''
        self.assembled = True

    def get_full_length(self):
        '''
        '''
        length = self.riser_len + self.limb_len * 2
        return length

    def tune(self):
        '''
        '''
        self.tuned = True



class Archer:
    '''
    '''
    def __init__(self, name, skill, wingspan):
        '''
        '''
        self.name = name
        self.skill = skill
        self.wingspan = wingspan
        self.drawn = False

        if self.skill < 0:
            raise ValueError("Invalid skill; nobody is that bad!")
        elif self.skill > 10: 
            raise ValueError("Invalid skill; nobody is that good!")

    def get_draw_length(self):
        '''
        :return draw_length: Int the draw length of self
        '''
        draw_length = int(self.wingspan/2.5)
        return draw_length

    def get_prob_on_bow_length(self, bow):
        '''
        '''
        chance = 1
        bow_length = bow.get_full_length()
        draw_length = self.get_draw_length()
        if bow_length < draw_length - 5 or bow_length > draw_length + 5:
            chance -= 0.10
        elif bow_length < draw_length - 2 or bow_length > draw_length + 2:
            chance -= 0.20
        return chance

    def get_prob_on_limb_weight(self, bow):
        '''
        '''
        chance = 1
        if bow.limb_weight < 20:
            if self.skill < 2:
                chance -= 0.05
        if bow.limb_weight < 24:
            if self.skill < 2:
                chance -= 0.20
            elif self.skill < 5:
                chance -= 0.10
        if bow.limb_weight < 30:
            if self.skill < 2:
                chance -= 0.50
            elif self.skill < 5:
                chance -= 0.30
            elif self.skill < 7:
                chance -= 0.15
        if bow.limb_weight >= 30:
            if self.skill < 2:
                chance -= 0.90
            elif self.skill < 5:
                chance -= 0.70
            elif self.skill < 7:
                chance -= 0.35
        return chance


    def draw(self, bow, arrow):
        '''
        :param bow: Bow; the bow self is shooting with
        :param arrow: Arrow; the arrow being shot
        :return prob_success: float;
             the probability of a successful shot after the draw
        '''
        if not arrow.nocked or arrow.nocked_on != bow.name:
            raise ValueError("The arrow isn't nocked on {}".format(bow.name))

        length_prob = self.get_prob_on_bow_length(bow)
        weight_prob = self.get_prob_on_limb_weight(bow)

        prob_success = length_prob * weight_prob
        self.drawn = True
        return prob_success

    def shoot(self, bow, arrow):
        '''
        '''
        if not self.drawn:
            raise ValueError("You can't shoot if you don't draw.")
        prob_success = self.draw(bow, arrow)
        shot_success = random.random() < prob_success
        return shot_success

def main():
    # Choose a bow
    vincent = Bow(
        brand='WNS', limb_colour='white', limb_len=12, 
        limb_mat='wood-fibreglass', limb_weight=24,
        name='Vincent', riser_colour='blue',
        riser_len=25, riser_mat='aluminium')
    evalyn = Bow(
        brand='Galaxy', limb_colour='black', limb_len=8, 
        limb_mat='wood-fibreglass', limb_weight=20,
        name='Evalyn', riser_colour='blue',
        riser_len=23, riser_mat='aluminium')
    beryl = Bow(
        brand='Hoyt', limb_colour='white', limb_len=9, 
        limb_mat='carbon-foam', limb_weight=26,
        name='Beryl', riser_colour='grey',
        riser_len=26, riser_mat='aluminium')
    edward = Bow(
        brand='Galaxy', limb_colour='white', limb_len=9, 
        limb_mat='wood', limb_weight=18,
        name='Edward', riser_colour='brown',
        riser_len=23, riser_mat='wood')
    
    # Choose an arrow
    red = Arrow(f_colour='red', n_fletch=3, s_length=25, s_material='carbon')
    blue = Arrow(f_colour='blue', n_fletch=3, s_length=26, s_material='carbon')
    pink = Arrow(f_colour='pink', n_fletch=3, s_length=27, s_material='aluminium')
    green = Arrow(f_colour='green', n_fletch=4, s_length=28, s_material='aluminium')
    purple = Arrow(f_colour='purple', n_fletch=4, s_length=29, s_material='carbon')
    
    # Create an Archer instance for yourself!
    shooters = []
    Lindsay = Archer(name='Lindsay', skill=6, wingspan=68)
    blue.nock(vincent)
    Lindsay.draw(bow=vincent, arrow=blue)
    Lindsay_result = Lindsay.shoot(bow=vincent, arrow=blue)
    shooters.append((Lindsay, vincent, blue))

    for shooter in shooters:
        archer = shooter[0]
        bow = shooter[1]
        arrow = shooter[2]
        archer.draw(bow=bow, arrow=arrow)
        shot_success = archer.shoot(bow=vincent, arrow=blue)
        if shot_success:
            print("{}'s shot was successful!".format(archer.name))
        else:
            print("{}'s shot missed.".format(archer.name))

if __name__ == '__main__':
    main()
