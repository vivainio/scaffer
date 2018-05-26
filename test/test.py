import os
os.system("python ../scaffer g s1 -v bar=aa-bb prj=cc-dd -f")
cont=open("cc-dd/aa-bb.txt").read()
assert cont == 'CcDdHello vs AaBbWorld in pascalcase.\nKebab case cc-dd-hello aa-bb-world\nsnake case cc_dd_hello aa_bb_world\nDotted cc.dd.hello aa.bb.world'