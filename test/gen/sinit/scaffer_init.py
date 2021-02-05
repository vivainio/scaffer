import os


print(scaffer_in)
print(scaffer_out)

def git_data():
    return {
        b"gitusername": os.popen("git config user.name").read().strip().encode(),
        b"gitemail": os.popen("git config user.email").read().strip().encode()
    }

d = git_data()
d[b"targetdir"] = os.getcwd().encode()
scaffer_out.update(d)



