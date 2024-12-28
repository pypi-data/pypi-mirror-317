from dahlia import Dahlia

d = Dahlia(depth=24)

for i in ("&#ffaff3;gleaming", "&bdiamond", "&lcool", "&#fbf;gweaming"):
    c = d.convert(i)
    print(i, c, repr(c))
