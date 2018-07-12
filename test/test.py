import os

def run(s):
    cmd = "python ../scaffer "+s
    print ">",cmd
    os.system(cmd)

run("g s1 -v bar=aa-bb prj=cc-dd -f")
cont=open("cc-dd/aa-bb.txt").read()
print "got", `cont`
assert cont == 'CcDdHello vs AaBbWorld in pascalcase.\nLower kebab cc-dd-hello aa-bb-world\nLower snake cc_dd_hello aa_bb_world\nLower dotted cc.dd.hello aa.bb.world\nLower flat ccdd aabb\nUpper dotted SCF.PRJ.HELLO SCF.BAR.world\nUpper kebab SCF-PRJ-HELLO SCF-BAR-world\nUpper snake SCF_PRJ_HELLO SCF_BAR_world\nUpper flat CCDD AABB\n'
run("g sinit")