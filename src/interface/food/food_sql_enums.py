from enum import Enum


class AmountType(Enum):
    error = 0
    g = 1
    number = 2
    a_little = 3
    ml = 4


class Ingradient(Enum):
    chleb_zytni = 1
    twarog_bialy = 2
    warzywka = 3
    ryz_brazowy = 4
    kasza_gryczana = 5
    makaron_pelnoziarnisty = 6
    owoce = 7
    serek_wiejski = 8
    jogurt_natralny = 9
    platki_owsiane_gorskie = 10
    orzechy = 11
    piers_z_kurczaka = 12
    przyprawy_sol_pieprz = 13
    cebula = 14
    maka = 15
    buraki = 16
    chrzan = 17


class MealType(Enum):
    breakfast = 1
    second_breakfast = 2
    dinner = 3
    tea = 4
    supper = 5
