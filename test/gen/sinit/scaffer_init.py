import os

print("hello from scaffer init")
print(scaffer_in)

print(scaffer_out)

def git_data():
    return {
        "gitusername": os.popen("git config user.name").read().strip(),
        "gitemail": os.popen("git config user.email").read().strip()
    }

d = git_data()
scaffer_out.update(d)

scaffer_out["targetdir"] = scaffer_in["target_dir"]



