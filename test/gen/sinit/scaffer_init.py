import os


print(scaffer_in)
print(scaffer_out)

def git_data():
    return {
        "gitusername": os.popen("git config user.name").read().strip(),
        "gitemail": os.popen("git config user.email").read().strip()
    }

d = git_data()
d["targetdir"] = os.getcwd()
scaffer_out.update(d)



