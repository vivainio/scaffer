import os

def run(s):
    cmd = "python ../scaffer "+s
    print ">",cmd
    os.system(cmd)

run("g s1 -v bar=aa-bb prj=cc-dd -f")
cont=open("cc-dd/aa-bb.txt").read()
assert cont == 'CcDdHello vs AaBbWorld in pascalcase.\nKebab case cc-dd-hello aa-bb-world\nsnake case cc_dd_hello aa_bb_world\nDotted cc.dd.hello aa.bb.world'

run("g sinit")