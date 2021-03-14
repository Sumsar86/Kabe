from copy import deepcopy
from nupp import Mehike, Kuningas
import math


class Kabe(object):
    def __init__(self, laud=None):
        if laud != None:
            self.laud = laud
        else:
            self.laud = [
                Mehike(1, "m", (0, 1)),
                Mehike(2, "m", (0, 3)),
                Mehike(3, "m", (0, 5)),
                Mehike(4, "m", (0, 7)),
                Mehike(5, "m", (1, 0)),
                Mehike(6, "m", (1, 2)),
                Mehike(7, "m", (1, 4)),
                Mehike(8, "m", (1, 6)),
                Mehike(9, "m", (2, 1)),
                Mehike(10, "m", (2, 3)),
                Mehike(11, "m", (2, 5)),
                Mehike(12, "m", (2, 7)),
                Mehike(1, "v", (5, 0)),
                Mehike(2, "v", (5, 2)),
                Kuningas(3, "v", (5, 4)),
                Mehike(4, "v", (5, 6)),
                Mehike(5, "v", (6, 1)),
                Mehike(6, "v", (6, 3)),
                Mehike(7, "v", (6, 5)),
                Mehike(8, "v", (6, 7)),
                Mehike(9, "v", (7, 0)),
                Mehike(10, "v", (7, 2)),
                Mehike(11, "v", (7, 4)),
                Mehike(12, "v", (7, 6)),
            ]
        self.mangKaib = True
        self.saabVeel = False
        self.veel = False
        self.max_sugavus = 2

    def __repr__(self):
        return "Kabe(laud=laud, mangKaib='{}', saabVeel={}, veel={}, max_sugavus={})".format(
            self.mang_kaib(), self.saabVeel, self.veel, self.max_sugavus
        )

    def getLaud(self):
        for nupp in self.laud:
            print(nupp)

    def leiaNupp(self, x=None, y=None, nimi=None, laud=None):
        if laud == None:
            laud = self.laud
        if nimi != None:
            for nupp in laud:
                if nupp.getNimi() == nimi:
                    return nupp
        for nupp in laud:
            if nupp.asukoht == (x, y):
                return nupp
        return None

    def leiaAsukoht(self, nimi):
        for nupp in self.laud:
            if nupp.getNimi() == nimi:
                return nupp.asukoht

    def teisendaKoord(self, x, y, aj_seis):
        nupp = self.leiaNupp(x, y).getNimi()
        nupp = aj_seis.leiaNupp(nimi=nupp)
        if nupp == None:
            print("Sellist nuppu ei ole!")
            return
        return nupp.asukoht

    def kustuta(self, x=None, y=None, nupp=None, laud=None):
        if nupp == None:
            nupp = self.leiaNupp(x, y)
        if laud == None:
            laud = self.laud
        if nupp in laud:
            laud.remove(nupp)
        else:
            print("\n\n\nVäga tõsine viga!!! Nupp ei kustunud.\n\n\n")

    def asenda(self, nupp):
        uus_nupp = Kuningas()
        uus_nupp.kopeeri(nupp)
        self.kustuta(nupp=nupp)
        self.laud.append(uus_nupp)

    def loo_n(self, laud=None):
        n = {}
        if laud == None:
            laud = self.laud
        for nupp in laud:
            n[nupp.asukoht] = nupp.varv
        return n

    def loo_maatriks(self):
        n = self.loo_n()
        m = [["", "", "", "", "", "", "", ""] for i in range(8)]

        for i in range(8):
            for j in range(8):
                if (i, j) in n:
                    m[i][j] = self.leiaNupp(i, j)
        return m

    def keera_paripaeva(self):
        jar = [[] for i in range(8)]
        m = self.loo_maatriks()

        for j in reversed(range(8)):
            for i in range(8 - 1, -1, -1):
                jar[i].append(m[j][i])
        return jar

    def keera_vastupaeva(self):
        jar = [[] for i in range(8)]
        m = self.loo_maatriks()

        for j in range(8):
            for i in reversed(range(8 - 1, -1, -1)):
                jar[i].append(m[j][7 - i])
        return jar

    @staticmethod
    def muuda_asukohad(fun):
        m = fun()

        for x in range(len(m)):
            for y in range(len(m[x])):
                if m[x][y] != "":
                    m[x][y].asukoht = (x, y)
        return m

    def mang_kaib(self):
        varvid = set()
        for nupp in self.laud:
            varvid.add(nupp.varv)
        if len(varvid) < 2:
            return False
        return True

    def print(self, debug=False):
        d = int(debug)

        print(f"   {1-d}   {2-d}   {3-d}   {4-d}   {5-d}   {6-d}   {7-d}   {8-d}")
        print(f" ┌───┬───┬───┬───┬───┬───┬───┬───┐\n{1-d}", end="")
        for x in range(8):
            for y in range(8):
                n = self.loo_n()
                if (x, y) in n:
                    try:
                        nupp = self.leiaNupp(x, y)
                    except AttributeError:
                        print("│ h ", end="")
                    else:
                        if isinstance(nupp, Kuningas):
                            print("│{:3s}".format(nupp.getNimi()), end="")
                        else:
                            print("│{:3s}".format(nupp.getNimi().lower()), end="")
                else:
                    print("│   ", end="")
            print("│")
            if x < 7:
                print(f" ├───┼───┼───┼───┼───┼───┼───┼───┤\n{x+2-d}", end="")
            else:
                print(" └───┴───┴───┴───┴───┴───┴───┴───┘")

    def alusta(self):

        varvid = {"m": ["must", "musta"], "v": ["valge", "valge"]}
        i = 0

        while self.mangKaib:
            for nupp in self.laud:
                self.muundaNupp(nupp)

            if not self.mang_kaib():
                break

            if i == 0:
                self.print()

                if self.saabVeel:
                    print("Kas soovite veel ühe hüppe teha?")
                    sis = input("Jah / Ei: ").strip(" ").lower()
                    if sis == "jah":
                        i += 1
                        self.veel = True

                    else:
                        self.saabVeel = False

                mangija_varv = list(varvid.keys())[i][0]

                if not self.veel:
                    print(f"\n{varvid[mangija_varv][1].capitalize()} nupu kord.")

                    x_algus, y_algus = self.valesti4(
                        "Sisestage soovitud nupu koordinaadid", mangija_varv, varvid
                    )
                    if x_algus == None:
                        break

                    nupp = self.leiaNupp(x_algus - 1, y_algus - 1)

                x_lopp, y_lopp = self.valesti1("Sisestage uue koha koordinaadid")
                if x_lopp == None:
                    break

                nupp.liigu(x_lopp, y_lopp, self)

            else:
                self = self.Minimax2(1, True)[1]

            i += 1
            i %= 2

        self.print()
        print("MÄNG LÄBI!")

    def valesti1(self, son):
        print(son)
        algus = input("rida verg: ")
        try:
            x, y = tuple(map(int, algus.split()))
        except ValueError:
            print("Kas te soovite mängu lõpetada?")
            sis = input("Jah / Ei: ").strip(" ").lower()
            if sis == "jah" or sis == "stopp" or sis == "stop":
                self.mangKaib = False
                return None, None
            elif sis == "debug":
                print(self)
                self.getLaud()
                return self.valesti1(son)
            else:
                return self.valesti1(son)
        return x, y

    def valesti2(self):
        print("Sisestage oma nupu värv.")
        vastus = input("M / V: ").strip(" ").lower()
        if vastus == "m" or vastus == "must":
            pass
        elif vastus == "v" or vastus == "valge":
            pass
        else:
            print("Sellist värvi pole. Kas soovite mängu lõpetada?")
            sis = input("Jah / Ei: ").lower()
            if sis == "jah" or sis == "stopp" or sis == "stop":
                self.mangKaib = False
                return None, None
            else:
                return self.valesti2()
        return vastus

    def valesti3(self, son):
        print(son)
        try:
            x, y = tuple(map(int, input("rida verg: ").split()))
            return x, y
        except ValueError:
            print("Kas te soovite mängu lõpetada?")
            sis = input("Jah / Ei: ").strip(" ").lower()
            if sis == "jah" or sis == "stopp" or sis == "stop":
                self.mangKaib = False
                return None, None
            else:
                return self.valesti3(son)

    def valesti4(self, son, varv, varvid, x=None, y=None):
        x, y = self.valesti1(son)
        if x == None:
            return None, None

        nupp = self.leiaNupp(x - 1, y - 1)
        if nupp == None:
            return self.valesti4("Ei saa. Proovige uuesti.", varv, varvid, x, y)
        else:
            if nupp.varv != varv:
                return self.valesti4(
                    f"Ei saa. Praegu saab liikuda vaid {varvid[varv][0]} nupp. Proovige uuesti.",
                    varv,
                    varvid,
                    x,
                    y,
                )
            else:
                return x, y

    def muundaNupp(self, nupp, aj=False):
        if nupp.varv == "m" and nupp.asukoht[0] == 7 and isinstance(nupp, Mehike):
            if aj:
                uus_nupp = Kuningas()
                uus_nupp.kopeeri(nupp)
                return uus_nupp
            self.asenda(nupp)
        elif nupp.varv == "v" and nupp.asukoht[0] == 0 and isinstance(nupp, Mehike):
            if aj:
                uus_nupp = Kuningas()
                uus_nupp.kopeeri(nupp)
                return uus_nupp
            self.asenda(nupp)
        else:
            return nupp

    @staticmethod
    def onLaual(kabe1, jar):
        for kabe2 in jar:
            if len(kabe1.laud) == len(kabe2.laud):
                i = 0
                for nupp1, nupp2 in zip(kabe1.laud, kabe2.laud):
                    if nupp1.onVordsed(nupp2):
                        i += 1
                if i == len(kabe2.laud):
                    return True
        return False

    def arvutaSkoor(self, w1, w2):
        kokku = 0
        for nupp in self.laud:
            if isinstance(nupp, Kuningas):
                if nupp.varv == "v":
                    kokku += 1 * w1
                else:
                    kokku -= 1 * w1
            else:
                if nupp.varv == "v":
                    kokku += 1 * w2
                else:
                    kokku -= 1 * w2
        return kokku

    def voimalikud_sammud(self, nupp):
        x, y = nupp.asukoht[0], nupp.asukoht[1]
        n = self.loo_n()
        sammud = set()

        if isinstance(nupp, Mehike) and nupp.varv == "v":
            for i in range(-1, 2, 2):
                if (x - 1, y + i) not in n and nupp.onLaual(x - 1, y + i):
                    sammud.add((x - 1, y + i))
                h_lopp = (
                    (x - 1) + ((x - 1) - nupp.asukoht[0]),
                    (y + i) + ((y + i) - nupp.asukoht[1]),
                )
                if (
                    (x - 1, y + i) in n
                    and h_lopp not in n
                    and nupp.onLaual(h_lopp[0], h_lopp[1])
                    and nupp.onLaual(x - 1, y + i)
                    and n[(x - 1, y + i)] != nupp.varv
                ):
                    sammud.add((x - 1, y + i))
        elif isinstance(nupp, Mehike) and nupp.varv == "m":
            for i in range(-1, 2, 2):
                if (x + 1, y + i) not in n and nupp.onLaual(x + 1, y + i):
                    sammud.add((x + 1, y + i))
                h_lopp = (
                    (x + 1) + ((x + 1) - nupp.asukoht[0]),
                    (y + i) + ((y + i) - nupp.asukoht[1]),
                )
                if (
                    (x + 1, y + i) in n
                    and h_lopp not in n
                    and nupp.onLaual(h_lopp[0], h_lopp[1])
                    and nupp.onLaual(x + 1, y + i)
                    and n[(x + 1, y + i)] != nupp.varv
                ):
                    sammud.add((x + 1, y + i))
        elif isinstance(nupp, Kuningas):
            for i in range(-1, 2, 2):
                for j in range(-1, 2, 2):
                    if (x + i, y + j) not in n and nupp.onLaual(x + i, y + j):
                        sammud.add((x + i, y + j))
                    h_lopp = (
                        (x + i) + ((x + i) - nupp.asukoht[0]),
                        (y + j) + ((y + j) - nupp.asukoht[1]),
                    )
                    if (
                        (x + i, y + j) in n
                        and h_lopp not in n
                        and nupp.onLaual(h_lopp[0], h_lopp[1])
                        and nupp.onLaual(x + i, y + j)
                        and n[(x + i, y + j)] != nupp.varv
                    ):
                        sammud.add((x + i, y + j))
        return sammud

    def koik_voimalikud_sammud(self, varv, kabe):
        lauad = []

        for nupp in self.laud:
            if nupp.varv == varv:
                sammud = self.voimalikud_sammud(nupp)
                for samm in sammud:
                    aj_kabe = deepcopy(kabe)
                    aj_nupp = aj_kabe.leiaNupp(nupp.asukoht[0], nupp.asukoht[1])
                    aj_kabe.liiguta_nuppu(
                        aj_nupp, samm, (nupp.asukoht[0], nupp.asukoht[1])
                    )
                    if not self.onLaual(aj_kabe, lauad):
                        lauad.append(aj_kabe)

        return lauad

    def liiguta_nuppu(self, nupp, samm, e_asukoht):
        ex, ey = e_asukoht[0], e_asukoht[1]
        x, y = samm[0], samm[1]
        n = self.loo_n()

        if samm in n:
            h_lopp = (
                x + (x - ex),
                y + (y - ey),
            )
            if h_lopp not in n:
                self.kustuta(x, y)
                nupp.asukoht = h_lopp
        elif samm not in n:
            nupp.asukoht = (x, y)

    def hinda(self):
        return self.arvutaSkoor(1.2, 1)

    def Minimax2(
        self, sugavus, max_player=True, kabe=None, alfa=float("-inf"), beta=float("inf")
    ):
        if kabe == None:
            kabe = self

        if sugavus >= self.max_sugavus or not kabe.mang_kaib():
            return kabe.hinda(), kabe

        if max_player:
            maxSkoor = float("-inf")
            parim = None
            for kabe in kabe.koik_voimalikud_sammud("v", kabe):
                vaartus = self.Minimax2(sugavus + 1, False, kabe)[0]
                maxSkoor = max(maxSkoor, vaartus)
                alfa = max(alfa, maxSkoor)
                if alfa >= beta:
                    break
                if maxSkoor == vaartus:
                    parim = kabe
            return maxSkoor, parim

        else:
            minSkoor = float("inf")
            parim = None
            for kabe in kabe.koik_voimalikud_sammud("m", kabe):
                vaartus = self.Minimax2(sugavus + 1, False, kabe)[0]
                minSkoor = min(minSkoor, vaartus)
                beta = min(beta, minSkoor)
                if beta >= alfa:
                    break
                if minSkoor == vaartus:
                    parim = kabe
            return minSkoor, parim
