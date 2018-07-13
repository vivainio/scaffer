from __future__ import print_function
import subprocess

def run(c):
    cmd = ["python","../scaffer"] + c
    print(">",cmd)
    subprocess.check_call(cmd)

run(["g", "s1", "-v", "bar=aa-bb", "prj=cc-dd", "-f"])
cont=open("cc-dd/aa-bb.txt").read()
assert cont == 'CcDdHello vs AaBbWorld in pascalcase.\nLower kebab cc-dd-hello aa-bb-world\nLower snake cc_dd_hello aa_bb_world\nLower dotted cc.dd.hello aa.bb.world\nLower flat ccdd aabb\nUpper dotted SCF.PRJ.HELLO SCF.BAR.world\nUpper kebab SCF-PRJ-HELLO SCF-BAR-world\nUpper snake SCF_PRJ_HELLO SCF_BAR_world\nUpper flat CCDD AABB\n'
run(["g",  "sinit", "-f"])

assert "@" in open("projectdetails.txt").read()

# these should not ask anything since all scf instances are invalid
run(["g", "-f", "errorcases"])

assert open("error_prone.txt").read() == open("gen2/errorcases/error_prone.txt").read()

run(["g", "doesnotexist"])

