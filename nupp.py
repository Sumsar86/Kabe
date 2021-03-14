from copy import deepcopy


class Nupp(object):
    def __init__(self, num=None, varv=None, asukoht=None):
        self.num = str(num)
        self.varv = varv
        self.asukoht = asukoht

    def __repr__(self):
        return "Nupp(num={}, varv='{}', asukoht={})".format(
            self.num, self.varv, self.asukoht
        )

    def getInfo(self):
        return self.varv, self.asukoht

    def getNimi(self):
        return self.num + self.varv

    def onVordsed(self, nupp):
        return (
            self.num == nupp.num
            and self.varv == nupp.varv
            and self.asukoht == nupp.asukoht
        )

    def hindamine(self, y1, y2):
        if self.varv == "v":
            return y1 - 1 == y2
        else:
            return y1 + 1 == y2

    def kMiinus(self, x, y):
        if self.varv == "v":
            return (x - 1, y - 1)
        else:
            return (x + 1, y - 1)

    def kPluss(self, x, y):
        if self.varv == "v":
            return (x - 1, y + 1)
        else:
            return (x + 1, y + 1)

    def kopeeri(self, teine_nupp):
        self.num = teine_nupp.num
        self.varv = teine_nupp.varv
        self.asukoht = teine_nupp.asukoht

    def uusSisend(self, kabe, son="Ei saa. Proovige uuesti."):
        x, y = kabe.valesti1(son)
        if x == None:
            kabe.mangKaib = False
            return None

        self.liigu(x, y, kabe)

    def liigu(self, x, y, kabe):

        x -= 1
        y -= 1

        if self.kontrolli_liikumist(x, y, kabe):
            saab, vaenlased, sobrad, h_lopp = self.kontrolli_rundamist(x, y, kabe)

            if saab:
                self.runda(x, y, h_lopp, kabe)
            elif len(vaenlased) > 0:
                n = kabe.loo_n(kabe.laud)
                for v in vaenlased:
                    h_lopp = (
                        v[0] + (v[0] - self.asukoht[0]),
                        v[1] + (v[1] - self.asukoht[1]),
                    )
                    if h_lopp not in n and self.onLaual(h_lopp):
                        return self.uusSisend(kabe, "Ei saa. Peate ründama.")
                self.asukoht = (x, y)
            else:
                if len(sobrad) > 0:
                    if (x, y) in sobrad:
                        return self.uusSisend(kabe)
                    else:
                        self.asukoht = (x, y)
                else:
                    self.asukoht = (x, y)
        else:
            return self.uusSisend(kabe)

    def runda(self, x, y, huppe_lopp, kabe):
        kabe.kustuta(x, y)
        self.asukoht = huppe_lopp

    @staticmethod
    def onLaual(*args):
        for i in args:
            try:
                if i < 0 or i > 7:
                    return False
            except TypeError:
                for j in i:
                    if j < 0 or j > 7:
                        return False
        return True


class Mehike(Nupp):
    def __init__(self, num=None, varv=None, asukoht=None):
        super().__init__(num, varv, asukoht)

    def __repr__(self):
        return "Mehike(num={}, varv={}, asukoht={})".format(
            self.num, self.varv, self.asukoht
        )

    def kontrolli_liikumist(self, x_lopp, y_lopp, kabe):
        x, y = self.asukoht[0], self.asukoht[1]
        n = kabe.loo_n()

        if (
            (y - 1 == y_lopp or y + 1 == y_lopp)
            and self.hindamine(x, x_lopp)
            and self.onLaual(x, y, x_lopp, y_lopp)
        ):
            if (x_lopp, y_lopp) in n:
                if self.varv != n[(x_lopp, y_lopp)]:
                    return True
                return False
            return True
        else:
            return False

    def kontrolli_rundamist(self, x_lopp, y_lopp, kabe, laud=None):
        lopp = (x_lopp, y_lopp)
        x, y = self.asukoht[0], self.asukoht[1]

        huppe_lopp = (x_lopp + (x_lopp - x), y_lopp + (y_lopp - y))
        n = kabe.loo_n(laud)

        vaenlased = self.kontrolli_vastaseid(n, "m", "v")
        sobrad = self.kontrolli_vastaseid(n, "v", "m")

        if huppe_lopp not in n and self.onLaual(huppe_lopp):
            if (
                len(vaenlased) > 0
                and lopp in vaenlased
                and self.varv != kabe.leiaNupp(x_lopp, y_lopp).varv
            ):
                return True, vaenlased, sobrad, huppe_lopp
            else:
                return False, vaenlased, sobrad, huppe_lopp
        else:
            return False, vaenlased, sobrad, huppe_lopp

    def kontrolli_vastaseid(self, n, var1, var2):
        jar = []
        x, y = self.asukoht[0], self.asukoht[1]

        ajutineM = self.kMiinus(x, y)
        ajutineP = self.kPluss(x, y)

        if ajutineM in n:
            if self.varv == "m" and n[ajutineM] != var1:
                jar.append(ajutineM)
            elif self.varv == "v" and n[ajutineM] != var2:
                jar.append(ajutineM)

        if ajutineP in n:
            if self.varv == "m" and n[ajutineP] != var1:
                jar.append(ajutineP)
            elif self.varv == "v" and n[ajutineP] != var2:
                jar.append(ajutineP)

        if len(jar) > 0:
            return jar
        else:
            return []


class Kuningas(Nupp):
    def __init__(self, num=None, varv=None, asukoht=None):
        super().__init__(num, varv, asukoht)

    def __repr__(self):
        return "Kuningas(num={}, varv={}, asukoht={})".format(
            self.num, self.varv, self.asukoht
        )

    def getNimi(self):
        return self.num + self.varv.upper()

    def kontrolli_liikumist(self, x_lopp, y_lopp, kabe):
        x, y = self.asukoht[0], self.asukoht[1]
        n = kabe.loo_n()

        if (
            (y - 1 == y_lopp or y + 1 == y_lopp)
            and (x - 1 == x_lopp or x + 1 == x_lopp)
            and self.onLaual(x, y, x_lopp, y_lopp)
        ):
            if (x_lopp, y_lopp) in n:
                if self.varv != n[(x_lopp, y_lopp)]:
                    return True
                return False
            return True
        else:
            return False

    def kontrolli_rundamist(self, x_lopp, y_lopp, kabe):
        lopp = (x_lopp, y_lopp)
        x, y = self.asukoht[0], self.asukoht[1]

        huppe_lopp = (x_lopp + (x_lopp - x), y_lopp + (y_lopp - y))
        n = kabe.loo_n()

        vaenlased = self.kontrolli_vastaseid(n)
        sobrad = self.kontrolli_vastaseid(n)

        if huppe_lopp not in n and self.onLaual(huppe_lopp):
            if (
                len(vaenlased) > 0
                and lopp in vaenlased
                and self.varv != kabe.leiaNupp(x_lopp, y_lopp).varv
            ):
                return True, vaenlased, sobrad, huppe_lopp
            else:
                return False, vaenlased, sobrad, huppe_lopp
        else:
            return False, vaenlased, sobrad, huppe_lopp

    def kontrolli_vastaseid(self, n):
        x, y = self.asukoht[0], self.asukoht[1]
        jar = []

        naabrid = [(x - 1, y - 1), (x - 1, y + 1), (x + 1, y - 1), (x + 1, y + 1)]

        for naaber in naabrid:
            if naaber in n and self.varv != n[naaber]:
                jar.append(naaber)

        if len(jar) > 0:
            return jar
        else:
            return []